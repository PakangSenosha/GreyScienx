import type { Metadata } from "next";

export const agentOnlyRobots: NonNullable<Metadata["robots"]> = {
  index: false,
  follow: false,
  noarchive: true,
  nocache: true,
  googleBot: {
    index: false,
    follow: false,
    noimageindex: true,
  },
};

export const agentOnlyHeaders = {
  "X-Robots-Tag": "noindex, nofollow, noarchive",
} as const;

export const agentOnlyPagePatterns = [
  "/research/graph",
  "/research/*/*/claims/*",
  "/research/*/*/assumptions/*",
  "/research/*/*/results/*",
  "/research/*/*/models/*",
  "/research/*/*/data",
  "/research/*/*/reproduce",
  "/research/*/*/versions",
  "/research/*/*/markdown",
  "/research/index.md",
  "/series/index.md",
  "/api/*",
  "/mcp",
  "/mcp-ui/*",
] as const;
