"use client";

import Link from "next/link";
import { useMemo, useSyncExternalStore } from "react";
import { ResearchSite } from "./ResearchSite";
import { SiteHeader } from "./SiteHeader";
import { SiteFooter } from "./SiteFooter";
import type { ResearchPaper, Researcher } from "@/lib/types";

type PreviewPayload = {
  researcher: Researcher;
  paper: ResearchPaper;
  source?: string;
  warning?: string;
};

const previewKey = "greyscienx-preview";
const subscribe = () => () => undefined;
const getServerPreview = () => null;
const getBrowserPreview = () => sessionStorage.getItem(previewKey);
const getServerHydrated = () => false;
const getBrowserHydrated = () => true;

export function PreviewSite() {
  const raw = useSyncExternalStore(
    subscribe,
    getBrowserPreview,
    getServerPreview,
  );
  const hydrated = useSyncExternalStore(
    subscribe,
    getBrowserHydrated,
    getServerHydrated,
  );
  const payload = useMemo(() => {
    if (!raw) return null;
    try {
      return JSON.parse(raw) as PreviewPayload;
    } catch {
      return null;
    }
  }, [raw]);

  if (hydrated && !payload) {
    return (
      <>
        <SiteHeader />
        <main className="page-shell">
          <p className="eyebrow">Preview</p>
          <h1 className="hub-copy" style={{ fontSize: "3rem", fontWeight: 1000 }}>
            No distillation is waiting.
          </h1>
          <p>
            Submit a manuscript first. GreyScienx will write the research site into this preview.
          </p>
          <p style={{ marginTop: 28 }}>
            <Link className="button button-primary" href="/submit">
              Submit research
            </Link>
          </p>
        </main>
        <SiteFooter />
      </>
    );
  }

  if (!hydrated || !payload) {
    return (
      <>
        <SiteHeader />
        <main className="page-shell">
          <p>Loading distillation…</p>
        </main>
      </>
    );
  }

  return (
    <ResearchSite
      paper={payload.paper}
      researcher={payload.researcher}
      preview
      previewSource={payload.source}
      previewWarning={payload.warning}
    />
  );
}
