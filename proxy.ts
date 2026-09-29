import { NextResponse, type NextRequest } from "next/server";

export function proxy(request: NextRequest) {
  if (request.nextUrl.hostname.toLowerCase() === "www.greyscienx.com") {
    const target = request.nextUrl.clone();
    target.protocol = "https:";
    target.hostname = "greyscienx.com";
    target.port = "";
    return NextResponse.redirect(target, 308);
  }
  if (request.method !== "GET" && request.method !== "HEAD") return NextResponse.next();
  const accept = request.headers.get("accept")?.toLowerCase() ?? "";
  const wantsAlternate = ["application/json", "text/markdown", "application/pdf"].some((type) =>
    accept.includes(type),
  );
  if (!wantsAlternate || accept.includes("text/html")) {
    const response = NextResponse.next();
    response.headers.set("Vary", "Accept");
    return response;
  }
  const parts = request.nextUrl.pathname.split("/").filter(Boolean);
  if (parts.length !== 3) return NextResponse.next();
  const [, series, paper] = parts;
  const target = request.nextUrl.clone();
  target.pathname = `/api/v1/negotiate/${series}/${paper}`;
  const response = NextResponse.rewrite(target);
  response.headers.set("Vary", "Accept");
  return response;
}

export const config = {
  matcher: "/((?!_next/static|_next/image|favicon.ico).*)",
};
