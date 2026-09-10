"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

export function SubmitForm() {
  const router = useRouter();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function onSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setBusy(true);
    setError("");

    const form = new FormData(event.currentTarget);
    const payload = {
      researcherName: String(form.get("researcherName") ?? ""),
      affiliation: String(form.get("affiliation") ?? ""),
      role: String(form.get("role") ?? ""),
      email: String(form.get("email") ?? ""),
      title: String(form.get("title") ?? ""),
      field: String(form.get("field") ?? ""),
      manuscript: String(form.get("manuscript") ?? ""),
    };

    try {
      const response = await fetch("/api/distill", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || "Could not distill this manuscript.");
      }
      sessionStorage.setItem("greyscienx-preview", JSON.stringify(data));
      router.push("/preview");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not distill this manuscript.");
      setBusy(false);
    }
  }

  return (
    <form className="form-grid" onSubmit={onSubmit}>
      {error ? <p className="form-error">{error}</p> : null}
      <div className="form-row">
        <label>
          Researcher
          <input name="researcherName" required placeholder="Pakang Senosha" />
        </label>
        <label>
          Affiliation
          <input name="affiliation" required placeholder="University of Pretoria" />
        </label>
      </div>
      <div className="form-row">
        <label>
          Role
          <input name="role" placeholder="MSc Epidemiology and Biostatistics" />
        </label>
        <label>
          Email
          <input name="email" type="email" placeholder="you@university.ac.za" />
        </label>
      </div>
      <div className="form-row">
        <label>
          Working title
          <input name="title" placeholder="Academic provenance in South African higher education" />
        </label>
        <label>
          Field
          <input name="field" placeholder="Epidemiology · biostatistics" />
        </label>
      </div>
      <label>
        Manuscript, abstract, or results
        <textarea
          name="manuscript"
          required
          minLength={80}
          placeholder="Paste the armchair paper, or a long abstract plus results and methods. GreyScienx will distill it into the research-site template."
        />
        <span className="form-note">
          The original text remains the source of record. The site is a public distillation: finding, quantities, evidence, methods, and a download slot for the paper.
        </span>
      </label>
      <div>
        <button className="button button-primary" type="submit" disabled={busy}>
          {busy ? "Distilling…" : "Distill into a research site"}
        </button>
      </div>
    </form>
  );
}
