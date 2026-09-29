import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import yaml from "js-yaml";

const here = path.dirname(fileURLToPath(import.meta.url));
const profileDir = path.join(here, "profiles");
const outputFile = path.resolve(here, "../../../lib/research/extractions/from-profiles.ts");

const forms = {};
for (const name of fs.readdirSync(profileDir).sort()) {
  if (!name.endsWith(".yaml")) continue;
  const form = yaml.load(fs.readFileSync(path.join(profileDir, name), "utf8"));
  const slug = form?.identity?.slug;
  if (typeof slug !== "string" || !slug) throw new Error(`Profile ${name} has no identity.slug`);
  if (form?.identity?.id !== `GSX:PROFILE:${slug}`) {
    throw new Error(`Profile ${name} id must be GSX:PROFILE:${slug}`);
  }
  forms[slug] = form;
}

const banner = `// Generated from research/templates/semantic-twin/profiles by compile-profiles.mjs.
// Edit the YAML, then run: node research/templates/semantic-twin/compile-profiles.mjs
`;

fs.writeFileSync(
  outputFile,
  `${banner}export const profileForms = ${JSON.stringify(forms, null, 2)};\n`,
  "utf8",
);

console.log(`Compiled ${Object.keys(forms).length} profile twins into ${outputFile}`);
