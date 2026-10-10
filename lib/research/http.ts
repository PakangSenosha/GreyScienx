const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Accept",
  "X-Robots-Tag": "noindex, nofollow, noarchive",
};

export function json(data: unknown, status = 200, cache = "public, max-age=3600") {
  return Response.json(data, {
    status,
    headers: {
      ...CORS,
      "Cache-Control": cache,
    },
  });
}

export function jsonError(status: number, error: string) {
  return json({ error }, status, "no-store");
}

const WRITE_CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Accept",
  "X-Robots-Tag": "noindex, nofollow, noarchive",
};

export function options() {
  return new Response(null, { status: 204, headers: CORS });
}

export function writeOptions() {
  return new Response(null, { status: 204, headers: WRITE_CORS });
}

export function writeJson(data: unknown, status = 200) {
  return Response.json(data, {
    status,
    headers: {
      ...WRITE_CORS,
      "Cache-Control": "no-store",
    },
  });
}

export async function readJson(request: Request) {
  try {
    return { ok: true as const, value: (await request.json()) as unknown };
  } catch {
    return { ok: false as const, value: undefined };
  }
}

export async function readParam(
  context: { params: Promise<Record<string, string>> },
  name: string,
) {
  const params = await context.params;
  return decodeURIComponent(params[name] ?? "");
}
