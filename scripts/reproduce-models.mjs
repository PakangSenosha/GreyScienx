import { execFileSync } from "node:child_process";
import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const sourceRoot = path.join(root, "research", "source");
const manifest = JSON.parse(fs.readFileSync(
  path.join(root, "research", "templates", "semantic-twin", "model-reproduction-manifest.json"),
  "utf8",
));
const workRoot = fs.mkdtempSync(path.join(os.tmpdir(), "gsx-reproduce-"));
const isolatedRoot = path.join(workRoot, "repo");
const reports = [];

try {
  fs.mkdirSync(path.join(isolatedRoot, "app"), { recursive: true });
  fs.copyFileSync(path.join(root, "app", "globals.css"), path.join(isolatedRoot, "app", "globals.css"));
  fs.mkdirSync(path.join(isolatedRoot, ".agents", "skills", "greyscienx-editorial-pdf"), { recursive: true });
  fs.cpSync(
    path.join(root, ".agents", "skills", "greyscienx-editorial-pdf", "scripts"),
    path.join(isolatedRoot, ".agents", "skills", "greyscienx-editorial-pdf", "scripts"),
    { recursive: true },
  );
  for (const directory of fs.readdirSync(sourceRoot, { withFileTypes: true }).filter((entry) => entry.isDirectory())) {
    const sourceDir = path.join(sourceRoot, directory.name);
    const model = path.join(sourceDir, "model.py");
    if (!fs.existsSync(model)) continue;
    const expected = outputFile(sourceDir);
    if (!expected) {
      reports.push({ package: directory.name, passed: false, error: "No baseline JSON output is registered." });
      continue;
    }
    const workDir = path.join(isolatedRoot, "research", "source", directory.name);
    fs.mkdirSync(path.dirname(workDir), { recursive: true });
    fs.cpSync(sourceDir, workDir, { recursive: true });
    const generated = path.join(workDir, path.relative(sourceDir, expected));
    try {
      execFileSync("python", [path.join(workDir, "model.py")], {
        cwd: workDir,
        env: { ...process.env, MPLBACKEND: "Agg", PYTHONDONTWRITEBYTECODE: "1" },
        encoding: "utf8",
        stdio: "pipe",
        timeout: 180_000,
      });
      const expectedValue = JSON.parse(fs.readFileSync(expected, "utf8"));
      const actualValue = JSON.parse(fs.readFileSync(generated, "utf8"));
      const passed = stable(expectedValue) === stable(actualValue);
      reports.push({
        package: directory.name,
        output: path.relative(sourceDir, expected).replaceAll("\\", "/"),
        model_path: path.relative(root, model).replaceAll("\\", "/"),
        baseline_path: path.relative(root, expected).replaceAll("\\", "/"),
        model_sha256: sha256(fs.readFileSync(model)),
        baseline_sha256: sha256(fs.readFileSync(expected)),
        passed,
        error: passed ? null : `Generated JSON differs from the published baseline at ${firstDifference(expectedValue, actualValue)}.`,
      });
    } catch (error) {
      const detail = error && typeof error === "object" && "stderr" in error
        ? String(error.stderr).trim().split("\n").slice(-2).join(" ")
        : "";
      reports.push({
        package: directory.name,
        output: path.relative(sourceDir, expected).replaceAll("\\", "/"),
        model_path: path.relative(root, model).replaceAll("\\", "/"),
        baseline_path: path.relative(root, expected).replaceAll("\\", "/"),
        model_sha256: sha256(fs.readFileSync(model)),
        baseline_sha256: sha256(fs.readFileSync(expected)),
        passed: false,
        error: `${error instanceof Error ? error.message.split("\n")[0] : "Model execution failed."}${detail ? ` ${detail}` : ""}`,
      });
    }
  }

  const executedLegacy = new Map();
  for (const item of manifest.models) {
    if (reports.some((report) => report.package === item.package)) {
      reports.push({ package: item.package, passed: false, error: "Package is registered twice." });
      continue;
    }
    const model = path.join(root, ...item.script.split("/"));
    const expected = path.join(root, ...item.baseline.split("/"));
    const isolatedModel = path.join(isolatedRoot, ...item.script.split("/"));
    const generated = path.join(isolatedRoot, ...item.generated.split("/"));
    fs.mkdirSync(path.dirname(isolatedModel), { recursive: true });
    fs.copyFileSync(model, isolatedModel);
    try {
      if (!executedLegacy.has(item.script)) {
        execFileSync("python", [isolatedModel], {
          cwd: path.dirname(isolatedModel),
          env: { ...process.env, MPLBACKEND: "Agg", PYTHONDONTWRITEBYTECODE: "1" },
          encoding: "utf8",
          stdio: "pipe",
          timeout: 180_000,
        });
        executedLegacy.set(item.script, true);
      }
      const expectedValue = JSON.parse(fs.readFileSync(expected, "utf8"));
      const actualValue = JSON.parse(fs.readFileSync(generated, "utf8"));
      const passed = stable(expectedValue) === stable(actualValue);
      reports.push({
        package: item.package,
        study_slug: item.study_slug ?? null,
        output: item.generated,
        model_path: item.script,
        baseline_path: item.baseline,
        model_sha256: sha256(fs.readFileSync(model)),
        baseline_sha256: sha256(fs.readFileSync(expected)),
        passed,
        error: passed ? null : `Generated JSON differs from the published baseline at ${firstDifference(expectedValue, actualValue)}.`,
      });
    } catch (error) {
      const detail = error && typeof error === "object" && "stderr" in error
        ? String(error.stderr).trim().split("\n").slice(-2).join(" ")
        : "";
      reports.push({
        package: item.package,
        study_slug: item.study_slug ?? null,
        output: item.generated,
        model_path: item.script,
        baseline_path: item.baseline,
        model_sha256: fs.existsSync(model) ? sha256(fs.readFileSync(model)) : null,
        baseline_sha256: fs.existsSync(expected) ? sha256(fs.readFileSync(expected)) : null,
        passed: false,
        error: `${error instanceof Error ? error.message.split("\n")[0] : "Model execution failed."}${detail ? ` ${detail}` : ""}`,
      });
    }
  }
} finally {
  fs.rmSync(workRoot, { recursive: true, force: true });
}

const failures = reports.filter((report) => !report.passed);
const report = {
  schema_version: "GreyScienxModelReproduction 1.0",
  generated_at: new Date().toISOString(),
  isolation: "Each model ran in a temporary copy of its source package with MPLBACKEND=Agg.",
  compared_output: "Generated primary JSON was structurally compared with the published source-package baseline.",
  passed: failures.length === 0,
  model_count: reports.length,
  passed_models: reports.length - failures.length,
  failed_models: failures.length,
  models: reports,
};
const reportFile = path.join(root, "research", "templates", "semantic-twin", "model-reproduction-report.json");
fs.writeFileSync(reportFile, `${JSON.stringify(report, null, 2)}\n`, "utf8");
console.log(JSON.stringify(report, null, 2));
if (failures.length) process.exitCode = 1;

function outputFile(directory) {
  for (const relative of ["model_results.json", "results/summary.json"]) {
    const candidate = path.join(directory, relative);
    if (fs.existsSync(candidate)) return candidate;
  }
  return null;
}

function stable(value) {
  if (Array.isArray(value)) return `[${value.map(stable).join(",")}]`;
  if (value && typeof value === "object") {
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${stable(value[key])}`).join(",")}}`;
  }
  if (typeof value === "string" && path.isAbsolute(value) && /\.(?:png|svg|pdf)$/i.test(value)) {
    return JSON.stringify(path.basename(value));
  }
  return JSON.stringify(value);
}

function firstDifference(expected, actual, pointer = "$") {
  if (Object.is(expected, actual)) return null;
  if (Array.isArray(expected) && Array.isArray(actual)) {
    if (expected.length !== actual.length) return `${pointer}.length (expected ${expected.length}, actual ${actual.length})`;
    for (let index = 0; index < expected.length; index += 1) {
      const difference = firstDifference(expected[index], actual[index], `${pointer}[${index}]`);
      if (difference) return difference;
    }
    return null;
  } else if (expected && actual && typeof expected === "object" && typeof actual === "object") {
    const keys = [...new Set([...Object.keys(expected), ...Object.keys(actual)])].sort();
    for (const key of keys) {
      if (!(key in expected)) return `${pointer}.${key} (missing from expected)`;
      if (!(key in actual)) return `${pointer}.${key} (missing from actual)`;
      const difference = firstDifference(expected[key], actual[key], `${pointer}.${key}`);
      if (difference) return difference;
    }
    return null;
  }
  return `${pointer} (expected ${JSON.stringify(expected)}, actual ${JSON.stringify(actual)})`;
}

function sha256(value) {
  return crypto.createHash("sha256").update(value).digest("hex");
}
