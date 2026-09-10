import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { researcherHosts } from "./lib/hosts";

const reserved = new Set([
  "www",
  "greyscienx",
  "app",
  "api",
  "preview",
  "localhost",
]);

function subdomainFromHost(host: string) {
  const hostname = host.split(":")[0]?.toLowerCase() ?? "";
  if (hostname.endsWith(".greyscienx.com")) {
    const label = hostname.slice(0, -".greyscienx.com".length);
    if (label && !label.includes(".")) return label;
  }
  if (hostname.endsWith(".localhost")) {
    const label = hostname.slice(0, -".localhost".length);
    if (label && !label.includes(".")) return label;
  }
  return null;
}

export function proxy(request: NextRequest) {
  const host = request.headers.get("host") || "";
  const subdomain = subdomainFromHost(host);
  if (!subdomain || reserved.has(subdomain)) {
    return NextResponse.next();
  }

  const researcherSlug = researcherHosts[subdomain];
  if (!researcherSlug) return NextResponse.next();

  const url = request.nextUrl.clone();
  const prefix = `/r/${researcherSlug}`;
  if (url.pathname === "/" || url.pathname === "") {
    url.pathname = prefix;
    return NextResponse.rewrite(url);
  }
  if (!url.pathname.startsWith(prefix) && !url.pathname.startsWith("/api")) {
    url.pathname = `${prefix}${url.pathname}`;
    return NextResponse.rewrite(url);
  }
  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.svg|papers/|.*\\..*).*)"],
};
