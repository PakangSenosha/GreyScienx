"use client";

import { useEffect, useState } from "react";
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

export function PreviewSite() {
  const [payload, setPayload] = useState<PreviewPayload | null>(null);
  const [missing, setMissing] = useState(false);

  useEffect(() => {
    const raw = sessionStorage.getItem("greyscienx-preview");
    if (!raw) {
      setMissing(true);
      return;
    }
    try {
      setPayload(JSON.parse(raw) as PreviewPayload);
    } catch {
      setMissing(true);
    }
  }, []);

  if (missing) {
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
            <a className="button button-primary" href="/submit">
              Submit research
            </a>
          </p>
        </main>
        <SiteFooter />
      </>
    );
  }

  if (!payload) {
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
    />
  );
}
