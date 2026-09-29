import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { validateCritique, validateFork, validateRevision } from "../lib/research/community.ts";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const args = Object.fromEntries(process.argv.slice(2).flatMap((value, index, all) => value.startsWith("--") ? [[value.slice(2), all[index + 1]]] : []));
const reviewId = args.id;
const reviewer = args.reviewer;
if (!reviewId || !reviewer) {
  console.error("Usage: npm run research:publish-review -- --id GSX:REVIEW:xxxxxxxx --reviewer \"Name\"");
  process.exit(1);
}

const inbox = process.env.GREYSCIENX_REVIEW_INBOX ?? path.join(root, "research", "review", "inbox.jsonl");
if (!fs.existsSync(inbox)) throw new Error(`Review inbox does not exist: ${inbox}`);
const entry = fs.readFileSync(inbox, "utf8")
  .split("\n")
  .filter(Boolean)
  .map((line) => JSON.parse(line))
  .find((row) => row.id === reviewId);
if (!entry) throw new Error(`No queued review has id ${reviewId}.`);
if (entry.object_type === "submission") {
  throw new Error("Research submissions must first receive a catalog id and semantic-twin form; this command only publishes critiques, forks, and revisions.");
}

const validators = { critique: validateCritique, fork: validateFork, revision: validateRevision };
const validator = validators[entry.object_type];
if (!validator) throw new Error(`Unsupported review type ${entry.object_type}.`);
const packet = validator(entry.object);
if (!packet.valid) throw new Error(`Queued object no longer validates: ${packet.errors.join(" ")}`);

const file = path.join(root, "research", "community", "published.json");
const registry = JSON.parse(fs.readFileSync(file, "utf8"));
const collection = `${entry.object_type}s`;
if (registry[collection].some((item) => item.review_id === reviewId)) throw new Error(`${reviewId} is already published.`);
const prefix = { critique: "CRITIQUE", fork: "FORK", revision: "REVISION" }[entry.object_type];
const record = {
  schema_version: "GreyCommunityObject 1.0",
  id: `GSX:${prefix}:${reviewId.split(":").at(-1)}`,
  review_id: reviewId,
  object_type: entry.object_type,
  status: "published",
  published_at: new Date().toISOString(),
  reviewed_by: reviewer,
  ...entry.object,
};
registry[collection].push(record);
fs.writeFileSync(file, `${JSON.stringify(registry, null, 2)}\n`, "utf8");
console.log(JSON.stringify(record, null, 2));
