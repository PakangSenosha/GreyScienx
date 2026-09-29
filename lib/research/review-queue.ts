import { randomUUID } from "node:crypto";
import { appendFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import path from "node:path";
import type { CommunityObjectType, ReviewPacket } from "./community";

export type ReviewEntry = {
  id: string;
  received_at: string;
  object_type: CommunityObjectType;
  status: "queued";
  accepted: false;
  review: "human_review_required";
  summary: string;
};

type StoredReview = ReviewEntry & { object: unknown };

const MAX_ITEMS = 200;
const MAX_BYTES = 80_000;
const memory = new Map<string, StoredReview>();

export function reviewInboxPath() {
  return process.env.GREYSCIENX_REVIEW_INBOX ?? path.join(process.cwd(), "research", "review", "inbox.jsonl");
}

const KV_KEY = "items";

export async function listReviewQueue(): Promise<ReviewEntry[]> {
  return (await readStored()).map(toPublic);
}

export async function holdForReview(packet: ReviewPacket, body: unknown): Promise<ReviewPacket> {
  if (!packet.valid) return packet;
  const encoded = JSON.stringify(body);
  if (encoded.length > MAX_BYTES) {
    return { ...packet, warnings: [...packet.warnings, "The object is too large to keep for review."] };
  }
  const current = await readStored();
  if (current.length >= MAX_ITEMS) {
    return { ...packet, warnings: [...packet.warnings, "The review queue is full."] };
  }
  const entry: StoredReview = {
    id: `GSX:REVIEW:${randomUUID().slice(0, 8)}`,
    received_at: new Date().toISOString(),
    object_type: packet.object_type,
    status: "queued",
    accepted: false,
    review: "human_review_required",
    summary: summaryFor(packet.object_type, body),
    object: body,
  };
  const kv = await reviewKv();
  if (kv) {
    await kv.put(KV_KEY, JSON.stringify([...current, entry]));
    return { ...packet, status: "queued", id: entry.id, received_at: entry.received_at };
  }
  memory.set(entry.id, entry);
  let fileWarning: string | null = null;
  try {
    const file = reviewInboxPath();
    mkdirSync(/* turbopackIgnore: true */ path.dirname(file), { recursive: true });
    appendFileSync(/* turbopackIgnore: true */ file, `${JSON.stringify(entry)}\n`, "utf8");
  } catch {
    fileWarning = "Kept for this server run. The review file could not be written.";
  }
  return {
    ...packet,
    status: "queued",
    id: entry.id,
    received_at: entry.received_at,
    warnings: fileWarning ? [...packet.warnings, fileWarning] : packet.warnings,
  };
}

async function readStored() {
  const kv = await reviewKv();
  if (kv) {
    try {
      const raw = await kv.get(KV_KEY);
      if (!raw) return [];
      const parsed = JSON.parse(raw) as unknown;
      return Array.isArray(parsed) ? parsed.filter(isStored) : [];
    } catch {
      return [];
    }
  }
  const rows = new Map<string, StoredReview>();
  for (const row of readFileQueue()) rows.set(row.id, row);
  for (const row of memory.values()) rows.set(row.id, row);
  return [...rows.values()];
}

async function reviewKv() {
  try {
    const { env } = await import("cloudflare:workers");
    const kv = env.REVIEW_QUEUE;
    if (!kv) return null;
    return kv;
  } catch {
    return null;
  }
}

function isStored(value: unknown): value is StoredReview {
  if (typeof value !== "object" || value === null) return false;
  const row = value as StoredReview;
  return row.status === "queued" && row.accepted === false && typeof row.id === "string";
}

function readFileQueue() {
  const file = reviewInboxPath();
  if (!existsSync(/* turbopackIgnore: true */ file)) return [];
  try {
    return readFileSync(/* turbopackIgnore: true */ file, "utf8")
      .split("\n")
      .map((line) => line.trim())
      .filter(Boolean)
      .flatMap((line) => {
        try {
          const row = JSON.parse(line) as StoredReview;
          if (row.status !== "queued" || row.accepted !== false || typeof row.id !== "string") return [];
          return [row];
        } catch {
          return [];
        }
      });
  } catch {
    return [];
  }
}

function toPublic(row: StoredReview): ReviewEntry {
  return {
    id: row.id,
    received_at: row.received_at,
    object_type: row.object_type,
    status: "queued",
    accepted: false,
    review: "human_review_required",
    summary: typeof row.summary === "string" ? row.summary : row.object_type,
  };
}

function summaryFor(objectType: CommunityObjectType, body: unknown) {
  if (!isRecord(body)) return objectType;
  if (objectType === "submission") return clip(text(body, "title"), "Submission");
  if (objectType === "critique") return clip(text(body, "argument"), "Critique");
  if (objectType === "fork") return clip(text(body, "new_conclusion"), "Fork");
  return clip(text(body, "change"), "Revision");
}

function clip(value: string, fallback: string) {
  const textValue = value.trim();
  if (!textValue) return fallback;
  return textValue.length > 180 ? `${textValue.slice(0, 177)}...` : textValue;
}

function text(record: Record<string, unknown>, key: string) {
  const value = record[key];
  return typeof value === "string" ? value.trim() : "";
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}
