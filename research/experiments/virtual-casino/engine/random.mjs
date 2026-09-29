import { createHash } from "node:crypto";

export function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

export function canonical(value) {
  if (Array.isArray(value)) return `[${value.map(canonical).join(",")}]`;
  if (value && typeof value === "object") {
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonical(value[key])}`).join(",")}}`;
  }
  return JSON.stringify(value);
}

export function hashObject(value) {
  return sha256(canonical(value));
}

// cyrb128 is a deterministic 128-bit string mixer used only to initialise
// independent PRNG state. Cryptographic commitments and ledger hashes use SHA-256.
function cyrb128(value) {
  let h1 = 1779033703;
  let h2 = 3144134277;
  let h3 = 1013904242;
  let h4 = 2773480762;
  for (let index = 0; index < value.length; index += 1) {
    const code = value.charCodeAt(index);
    h1 = h2 ^ Math.imul(h1 ^ code, 597399067);
    h2 = h3 ^ Math.imul(h2 ^ code, 2869860233);
    h3 = h4 ^ Math.imul(h3 ^ code, 951274213);
    h4 = h1 ^ Math.imul(h4 ^ code, 2716044179);
  }
  h1 = Math.imul(h3 ^ (h1 >>> 18), 597399067);
  h2 = Math.imul(h4 ^ (h2 >>> 22), 2869860233);
  h3 = Math.imul(h1 ^ (h3 >>> 17), 951274213);
  h4 = Math.imul(h2 ^ (h4 >>> 19), 2716044179);
  return [(h1 ^ h2 ^ h3 ^ h4) >>> 0, (h2 ^ h1) >>> 0, (h3 ^ h1) >>> 0, (h4 ^ h1) >>> 0];
}

export class DeterministicStream {
  constructor(seed, streamId) {
    this.seed = seed;
    this.streamId = streamId;
    this.counter = 0;
    this.state = cyrb128(`${seed}|${streamId}`);
    if (this.state.every((value) => value === 0)) this.state[0] = 0x9e3779b9;
  }

  nextUint() {
    // xoshiro128** advances locally so output is independent of worker scheduling.
    const [s0, s1, s2, s3] = this.state;
    const result = Math.imul(((Math.imul(s1, 5) << 7) | (Math.imul(s1, 5) >>> 25)) >>> 0, 9) >>> 0;
    const t = (s1 << 9) >>> 0;
    let n2 = (s2 ^ s0) >>> 0;
    let n3 = (s3 ^ s1) >>> 0;
    const n1 = (s1 ^ n2) >>> 0;
    const n0 = (s0 ^ n3) >>> 0;
    n2 = (n2 ^ t) >>> 0;
    n3 = ((n3 << 11) | (n3 >>> 21)) >>> 0;
    this.state = [n0, n1, n2, n3];
    this.counter += 1;
    return result;
  }

  uniform() {
    return this.nextUint() / 0x100000000;
  }

  integer(maxExclusive) {
    if (!Number.isSafeInteger(maxExclusive) || maxExclusive <= 0) throw new Error("maxExclusive must be a positive safe integer");
    return Math.floor(this.uniform() * maxExclusive);
  }

  between(min, max) {
    return min + (max - min) * this.uniform();
  }

  pick(items) {
    if (!items.length) throw new Error("Cannot pick from an empty array");
    return items[this.integer(items.length)];
  }

  weighted(items, weights) {
    const total = weights.reduce((sum, weight) => sum + weight, 0);
    let cursor = this.uniform() * total;
    for (let index = 0; index < items.length; index += 1) {
      cursor -= weights[index];
      if (cursor < 0) return items[index];
    }
    return items.at(-1);
  }
}

export function stream(seed, ...parts) {
  return new DeterministicStream(seed, parts.join(":"));
}
