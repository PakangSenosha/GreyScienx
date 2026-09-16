"use client";

import { useEffect, useRef, useState } from "react";
import { publicUrl } from "@/lib/urls";

type ShareResearchProps = {
  href: string;
  title: string;
  showUrl?: boolean;
};

export function ShareResearch({ href, title, showUrl = false }: ShareResearchProps) {
  const [status, setStatus] = useState<"idle" | "copied">("idle");
  const resetTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    return () => {
      if (resetTimer.current) clearTimeout(resetTimer.current);
    };
  }, []);

  async function copyLink(url: string) {
    try {
      await navigator.clipboard.writeText(url);
    } catch {
      const field = document.createElement("textarea");
      field.value = url;
      field.setAttribute("readonly", "");
      field.style.position = "fixed";
      field.style.opacity = "0";
      document.body.appendChild(field);
      field.select();
      document.execCommand("copy");
      field.remove();
    }

    setStatus("copied");
    if (resetTimer.current) clearTimeout(resetTimer.current);
    resetTimer.current = setTimeout(() => setStatus("idle"), 2000);
  }

  async function share() {
    const url = href.startsWith("http") ? href : publicUrl(href);

    if (navigator.share) {
      try {
        await navigator.share({ title, text: `${title} — GreyScienx`, url });
        return;
      } catch (error) {
        if (error instanceof DOMException && error.name === "AbortError") return;
      }
    }

    await copyLink(url);
  }

  const displayUrl = (href.startsWith("http") ? href : publicUrl(href)).replace(/^https?:\/\//, "");

  const button = (
    <button
      className="share-research"
      type="button"
      onClick={share}
      aria-label={`Copy shareable link for ${title}`}
    >
      <svg aria-hidden="true" viewBox="0 0 24 24" width="16" height="16">
        <path d="M12 16V3m0 0L7 8m5-5 5 5M5 13v7h14v-7" />
      </svg>
      <span aria-live="polite">{status === "copied" ? "Link copied" : "Copy link"}</span>
    </button>
  );

  if (!showUrl) return button;

  return (
    <div className="share-block">
      <p className="article-url">{displayUrl}</p>
      {button}
    </div>
  );
}
