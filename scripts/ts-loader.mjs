import { existsSync, statSync } from "node:fs";
import { readFile } from "node:fs/promises";
import { dirname, join, resolve as resolvePath } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { ModuleKind, ScriptTarget, transpileModule } from "typescript";

const root = fileURLToPath(new URL("..", import.meta.url));

export async function resolve(specifier, context, nextResolve) {
  if (!specifier.startsWith(".") && !specifier.startsWith("@/") && !specifier.startsWith("file:")) {
    return nextResolve(specifier, context);
  }

  let target = specifier;
  if (specifier.startsWith("@/")) {
    target = resolvePath(root, specifier.slice(2));
  } else if (specifier.startsWith(".")) {
    const parent = context.parentURL ? fileURLToPath(context.parentURL) : root;
    target = resolvePath(dirname(parent), specifier);
  } else {
    target = fileURLToPath(specifier);
  }

  const candidates = [
    target,
    `${target}.ts`,
    `${target}.tsx`,
    `${target}.mjs`,
    `${target}.js`,
    join(target, "index.ts"),
  ];
  for (const candidate of candidates) {
    if (existsSync(candidate) && statSync(candidate).isFile()) {
      return { url: pathToFileURL(candidate).href, shortCircuit: true };
    }
  }
  return nextResolve(specifier, context);
}

export async function load(url, context, nextLoad) {
  if (!url.endsWith(".ts") && !url.endsWith(".tsx")) return nextLoad(url, context);
  const source = await readFile(fileURLToPath(url), "utf8");
  const { outputText } = transpileModule(source, {
    compilerOptions: {
      module: ModuleKind.ESNext,
      target: ScriptTarget.ES2022,
    },
    fileName: url,
  });
  return { format: "module", source: outputText, shortCircuit: true };
}
