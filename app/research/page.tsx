import type { Metadata } from "next";
import Link from "next/link";
import { PaperRow } from "@/components/PaperRow";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { papers, researchSeries } from "@/lib/catalog";
import { discoveryMethods, matchesDiscovery } from "@/lib/research/packages";
import { listTopicRecords, researchObjects, researchTypeLabel, searchResearch } from "@/lib/research/registry";
import { articlePath } from "@/lib/urls";

type ResearchPageProps = {
  searchParams: Promise<{
    q?: string | string[];
    series?: string | string[];
    topic?: string | string[];
    geography?: string | string[];
    type?: string | string[];
    method?: string | string[];
    code?: string | string[];
  }>;
};

function queryFrom(value: string | string[] | undefined) {
  const query = Array.isArray(value) ? value[0] : value;
  return (query ?? "").trim();
}

export async function generateMetadata({ searchParams }: ResearchPageProps): Promise<Metadata> {
  const query = queryFrom((await searchParams).q);
  if (!query) {
    return {
      title: "Research archive",
      description: "The GreyScienx archive: complete research papers arranged by series.",
    };
  }
  return {
    title: `Studies matching “${query}”`,
    description: `Published GreyScienx studies whose questions, claims, assumptions, or results match “${query}”.`,
  };
}

export default async function ResearchPage({ searchParams }: ResearchPageProps) {
  const params = await searchParams;
  const query = queryFrom(params.q);
  const seriesFilter = queryFrom(params.series);
  const topicFilter = queryFrom(params.topic);
  const geographyFilter = queryFrom(params.geography);
  const typeFilter = queryFrom(params.type);
  const methodFilter = queryFrom(params.method);
  const codeFilter = queryFrom(params.code);
  const hits = query ? searchResearch(query) : [];
  const hitOrder = new Map(hits.map((hit, index) => [hit.slug, index]));
  const active = Boolean(
    query || seriesFilter || topicFilter || geographyFilter || typeFilter || methodFilter || codeFilter,
  );
  const methods = discoveryMethods();
  const visible = researchObjects
    .filter((study) => {
      if (query && !hitOrder.has(study.slug)) return false;
      if (seriesFilter && study.series_slug !== seriesFilter) return false;
      if (topicFilter && !study.topics.includes(topicFilter)) return false;
      if (geographyFilter && !study.geographies.includes(geographyFilter)) return false;
      if (typeFilter && study.research_type !== typeFilter) return false;
      if (!matchesDiscovery(study.id, methodFilter, codeFilter)) return false;
      return true;
    })
    .sort((a, b) => (query ? (hitOrder.get(a.slug) ?? 0) - (hitOrder.get(b.slug) ?? 0) : a.id.localeCompare(b.id)));
  const visibleSlugs = new Set(visible.map((study) => study.slug));
  const topics = listTopicRecords();
  const geographies = [...new Set(researchObjects.flatMap((study) => study.geographies))].sort();

  return (
    <>
      <SiteHeader />
      <main>
        <section className="hero hero-solo archive-hero">
          <div className="brand-wave wave-one" aria-hidden="true" />
          <div className="brand-wave wave-two" aria-hidden="true" />
          <div className="hero-copy">
            <p className="eyebrow">The archive</p>
            <h1>
              Research,
              <br />
              <em>by inquiry.</em>
            </h1>
            <p className="dek">
              The full GreyScienx record, arranged in connected series. Each entry opens to a
              permanent article page and the complete manuscript.
            </p>
            <p className="archive-links">
              <Link href="/series">Series</Link>
              <Link href="/topics">Topics</Link>
              <Link href="/standards/mathematical-writing">Mathematical standard</Link>
              <Link href="/research/graph">Graph</Link>
              <Link href="/community">Community</Link>
              <a href="/feed.xml">Feed</a>
            </p>
          </div>
        </section>

        <section className="number-band" aria-label="Research archive summary">
          <div>
            <strong>{papers.length}</strong>
            <span>published studies</span>
          </div>
          <div>
            <strong>{researchSeries.length}</strong>
            <span>series</span>
          </div>
          <div>
            <strong>PDF</strong>
            <span>full manuscripts</span>
          </div>
          <div>
            <strong>Open</strong>
            <span>public access</span>
          </div>
        </section>

        <section className="question-search" aria-label="Search studies by question">
          <p className="kicker">Ask a research question</p>
          <form action="/research" method="get" role="search">
            <label htmlFor="research-question">
              Question or keywords
              <input
                id="research-question"
                name="q"
                type="search"
                defaultValue={query}
                placeholder="What happens to housing if population declines?"
              />
            </label>
            <div className="question-filters">
              <label>
                Series
                <select name="series" defaultValue={seriesFilter}>
                  <option value="">Any series</option>
                  {researchSeries.map((series) => (
                    <option key={series.slug} value={series.slug}>
                      {series.title}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                Topic
                <select name="topic" defaultValue={topicFilter}>
                  <option value="">Any topic</option>
                  {topics.map((topic) => (
                    <option key={topic.slug} value={topic.slug}>
                      {topic.title}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                Country or place
                <select name="geography" defaultValue={geographyFilter}>
                  <option value="">Any place</option>
                  {geographies.map((place) => (
                    <option key={place} value={place}>
                      {place}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                Research type
                <select name="type" defaultValue={typeFilter}>
                  <option value="">Any type</option>
                  <option value="exploratory_simulation">Exploratory simulation</option>
                  <option value="counterfactual">Counterfactual</option>
                </select>
              </label>
              <label>
                Method
                <select name="method" defaultValue={methodFilter}>
                  <option value="">Any method</option>
                  {methods.map((method) => (
                    <option key={method} value={method}>
                      {method}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                Reproducibility
                <select name="code" defaultValue={codeFilter}>
                  <option value="">Any code record</option>
                  <option value="recorded">Code recorded</option>
                  <option value="unrecorded">Code not recorded</option>
                </select>
              </label>
            </div>
            <button className="button button-primary" type="submit">
              Search
            </button>
          </form>
          <p className="form-note">
            Search matches published questions, claims, assumptions, results, and limitations,
            including related wording such as houses for housing.
            A match names the claim and the assumptions it uses. Method is the recorded
            software. Reproducibility is whether code is recorded. Every published study is
            modelled, dated in its machine record, and has no external critique unless the community record says otherwise.
            AI assistance is disclosed for the publication.
          </p>
        </section>

        {active ? (
          <section className="series-stack" aria-live="polite">
            <section className="series-block">
              <header className="series-heading">
                <div>
                  <span>{visible.length}</span>
                  <p>Matches</p>
                </div>
                <div>
                  <h2>Studies for this view</h2>
                  <p>{query || "Filtered by series, topic, place, research type, method, or code record."}</p>
                </div>
              </header>
              {visible.length > 0 ? (
                <div className="paper-list">
                  {visible.map((study) => {
                    const hit = hitOrder.has(study.slug) ? hits.find((item) => item.slug === study.slug) : undefined;
                    const claim = hit?.most_relevant_claim?.claim;
                    const assumptions = hit?.key_assumptions.map((item) => item.name) ?? [];
                    const detail = claim
                      ? assumptions.length > 0
                        ? `${claim} Key assumptions: ${assumptions.join("; ")}.`
                        : claim
                      : undefined;
                    return (
                      <PaperRow
                        key={study.id}
                        number={study.id}
                        title={study.title}
                        description={study.primary_question}
                        detail={detail}
                        href={`/research/${study.series_slug}/${study.slug}`}
                        meta={`${researchTypeLabel(study.research_type)} · Modelled`}
                      />
                    );
                  })}
                </div>
              ) : (
                <p className="search-empty">No published GreyScienx study matches that view yet.</p>
              )}
            </section>
          </section>
        ) : null}

        <nav className="series-index" aria-label="Research series">
          {researchSeries.map((series) => (
            <a href={`#${series.slug}`} key={series.slug}>
              <span>{series.number}</span>
              {series.title}
            </a>
          ))}
        </nav>

        <div className="series-stack">
          {researchSeries.map((series) => {
            const shown = series.papers.filter((paper) => !active || visibleSlugs.has(paper.slug));
            if (shown.length === 0) return null;
            return (
            <section className="series-block" id={series.slug} key={series.slug}>
              <header className="series-heading">
                <div>
                  <span>{series.number}</span>
                  <p>Series</p>
                </div>
                <div>
                  <h2>
                    <Link href={`/series/${series.slug}`}>{series.title}</Link>
                  </h2>
                  <p>{series.description}</p>
                </div>
                <p className="series-count">
                  {shown.length} {shown.length === 1 ? "paper" : "papers"}
                </p>
              </header>

              <div className="paper-list">
                {shown.map((paper) => (
                  <PaperRow
                    key={paper.slug}
                    number={`${series.number}.${paper.number}`}
                    title={paper.title}
                    description={paper.description}
                    href={articlePath(series, paper)}
                    meta={`${paper.pages} pages · ${paper.size}`}
                  />
                ))}
              </div>
            </section>
            );
          })}
        </div>
      </main>
      <SiteFooter />
    </>
  );
}
