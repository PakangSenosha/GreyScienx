import Link from "next/link";
import { packageFor } from "@/lib/research/packages";
import type { ResearchObject } from "@/lib/research/schema";

export function StudyDossier({ study }: { study: ResearchObject }) {
  const pack = packageFor(study.id);
  const lead = study.claims[0];
  const limitations = [...new Set(study.claims.map((claim) => claim.main_limitation))];
  const sensitivity = countSensitivity(study);

  return (
    <>
      {lead ? (
        <section className="article-share-panel" aria-label="Conditional answer">
          <div>
            <p className="kicker">Conditional answer · {lead.id}</p>
            <h2 className="study-question">{lead.claim}</h2>
            <p>
              Evidence status: Modelled. Sensitivity: {lead.sensitivity}. Depends on{" "}
              {lead.depends_on.join(", ")}. {lead.main_limitation}
            </p>
          </div>
          <div className="machine-links">
            <Link href={`/research/${study.series_slug}/${study.slug}/claims/${lead.local_id}`}>
              {lead.local_id}
            </Link>
          </div>
        </section>
      ) : null}

      {study.related_questions.length > 0 ? (
        <section className="page-shell">
          <p className="kicker">Related questions</p>
          <ul className="dossier-questions">
            {study.related_questions.map((question) => (
              <li key={question}>{question}</li>
            ))}
          </ul>
        </section>
      ) : null}

      <RecordBlock
        label="Assumptions"
        count={study.assumptions.length}
        intro="These are the registered model assumptions. A result stays conditional on the ones a claim names."
        rows={study.assumptions.map((item) => ({
          id: item.local_id,
          title: item.name,
          text: item.statement,
          meta: item.value ? `${item.value} ${item.unit ?? ""}`.trim() : item.sensitivity,
          href: `/research/${study.series_slug}/${study.slug}/assumptions/${item.local_id}`,
        }))}
      />
      <RecordBlock
        label="Model"
        count={study.models.length}
        intro="The registered model statement. It is a scenario model, and the manuscript remains the full specification."
        rows={study.models.map((item) => ({
          id: item.local_id,
          title: item.name,
          text: item.statement,
          meta: item.id,
          href: `/research/${study.series_slug}/${study.slug}/models/${item.local_id}`,
        }))}
      />
      <RecordBlock
        label="Results"
        count={study.results.length}
        intro="Modelled scenario results. They are not forecasts."
        rows={study.results.map((item) => ({
          id: item.local_id,
          title: item.value ? `${item.value} ${item.unit}`.trim() : item.local_id,
          text: item.statement,
          meta: item.scenario,
          href: `/research/${study.series_slug}/${study.slug}/results/${item.local_id}`,
        }))}
      />

      {study.claims.length > 0 ? (
        <section className="page-shell">
          <p className="kicker">Sensitivity</p>
          <ul className="topic-links">
            <li><span>High · {sensitivity.high}</span></li>
            <li><span>Moderate · {sensitivity.moderate}</span></li>
            <li><span>Low · {sensitivity.low}</span></li>
          </ul>
        </section>
      ) : null}

      {limitations.length > 0 ? (
        <section className="page-shell">
          <p className="kicker">Limitations</p>
          {limitations.map((limitation) => (
            <p key={limitation}>{limitation}</p>
          ))}
        </section>
      ) : null}

      <RecordBlock
        label="Claims"
        count={study.claims.length}
        intro="Each claim names the assumptions it uses and the limitation that travels with it."
        rows={study.claims.map((claim) => ({
          id: claim.local_id,
          title: claim.id,
          text: claim.claim,
          meta: `Modelled · ${claim.sensitivity} sensitivity`,
          href: `/research/${study.series_slug}/${study.slug}/claims/${claim.local_id}`,
        }))}
      />

      <section className="article-share-panel" aria-label="Sources and reproducibility">
        <div>
          <p className="kicker">Sources and reproducibility</p>
          <h2 className="study-question">The PDF and complete Markdown source are both published.</h2>
          <p>
            Full manuscript: {study.manuscript.word_count.toLocaleString("en-ZA")} words across{" "}
            {study.manuscript.headings.length} indexed headings. Source checksum:{" "}
            {study.manuscript.source_sha256.slice(0, 12)}….{" "}
            Code recorded: {yesNo(pack?.reproducibility.code_available)}. Data recorded:{" "}
            {yesNo(pack?.reproducibility.data_available)}. Environment recorded:{" "}
            {yesNo(pack?.reproducibility.environment_available)}. Published files:{" "}
            {pack?.files.length ?? 0}.{" "}
            {pack?.reproducibility.random_seed || "No random seed is recorded."}{" "}
            {pack?.reproducibility.repository_url
              ? "A repository URL is recorded."
              : "A public code repository is not published."}
          </p>
        </div>
        <div className="machine-links">
          <a href={study.links.pdf}>Manuscript PDF</a>
          <Link href={`/research/${study.series_slug}/${study.slug}/markdown`}>Full Markdown twin</Link>
          <a href={study.links.manuscript}>Manuscript API</a>
          <Link href={`/research/${study.series_slug}/${study.slug}/data`}>Datasets</Link>
          <Link href={`/research/${study.series_slug}/${study.slug}/reproduce`}>Reproducibility</Link>
          <a href={`/api/v1/research/${study.slug}/datasets`}>Datasets JSON</a>
        </div>
      </section>
    </>
  );
}

function RecordBlock({
  label,
  count,
  intro,
  rows,
}: {
  label: string;
  count: number;
  intro: string;
  rows: Array<{ id: string; title: string; text: string; meta: string; href?: string }>;
}) {
  if (count === 0) return null;
  return (
    <section className="series-stack article-related" aria-label={label}>
      <section className="series-block">
        <header className="series-heading">
          <div>
            <span>{count}</span>
            <p>{label}</p>
          </div>
          <div>
            <h2>{label}</h2>
            <p>{intro}</p>
          </div>
        </header>
        <div className="paper-list">
          {rows.map((row) => (
            <article className="paper-row" key={row.id}>
              {row.href ? (
                <Link className="paper-row-link" href={row.href}>
                  <RowBody row={row} />
                </Link>
              ) : (
                <div className="paper-row-link">
                  <RowBody row={row} />
                </div>
              )}
            </article>
          ))}
        </div>
      </section>
    </section>
  );
}

function RowBody({ row }: { row: { id: string; title: string; text: string; meta: string } }) {
  return (
    <>
      <span className="paper-number">{row.id}</span>
      <span className="paper-copy">
        <strong>{row.title}</strong>
        <span>{row.text}</span>
      </span>
      <span className="paper-meta">{row.meta}</span>
    </>
  );
}

function countSensitivity(study: ResearchObject) {
  const counts = { high: 0, moderate: 0, low: 0 };
  for (const claim of study.claims) counts[claim.sensitivity] += 1;
  return counts;
}

function yesNo(value: boolean | undefined) {
  return value ? "yes" : "no";
}
