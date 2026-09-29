import type { Metadata } from "next";
import Link from "next/link";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { communityIndex, listProfiles } from "@/lib/research/community";

export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "Community",
  description:
    "GreyScienx profiles, critiques, forks, revisions, and the review step that publishes them.",
};

export default async function CommunityPage() {
  const index = await communityIndex();
  const profiles = listProfiles();

  return (
    <>
      <SiteHeader />
      <main>
        <section className="hero hero-solo">
          <div className="brand-wave wave-one" aria-hidden="true" />
          <div className="brand-wave wave-two" aria-hidden="true" />
          <div className="hero-copy">
            <p className="eyebrow">
              <Link href="/research">Research</Link>
            </p>
            <h1>
              Community,
              <br />
              <em>after review.</em>
            </h1>
            <p className="dek">
              Profiles, critiques, forks, and revisions are research objects. A validator checks
              the shape. A person reviews the object before it joins the public record.
            </p>
            <div className="hero-actions">
              <a className="button button-primary" href="/api/v1/community">
                Community JSON
              </a>
              <Link className="button button-ghost" href="/researchers">
                Profiles
              </Link>
            </div>
          </div>
        </section>

        <section className="number-band" aria-label="Community record">
          <div>
            <strong>{index.counts.profiles}</strong>
            <span>{index.counts.profiles === 1 ? "profile" : "profiles"}</span>
          </div>
          <div>
            <strong>{index.counts.critiques}</strong>
            <span>critiques</span>
          </div>
          <div>
            <strong>{index.counts.forks}</strong>
            <span>forks</span>
          </div>
          <div>
            <strong>{index.counts.revisions}</strong>
            <span>revisions</span>
          </div>
        </section>

        <section className="page-shell">
          <p className="kicker">Publication rule</p>
          <p>{index.publication_rule}</p>
          <div className="review-queue">
            <p className="kicker">Awaiting review</p>
            {index.review_queue.length > 0 ? (
              <ul className="dossier-questions">
                {index.review_queue.map((item) => (
                  <li key={item.id}>
                    {item.id} · {item.object_type} · {item.summary}
                  </li>
                ))}
              </ul>
            ) : (
              <p>The review queue is empty.</p>
            )}
          </div>
          <p className="archive-links">
            <Link href="/api/v1/profiles">Profiles</Link>
            <a href="/api/v1/critiques">Critiques</a>
            <a href="/api/v1/forks">Forks</a>
            <a href="/api/v1/revisions">Revisions</a>
            <a href="/api/v1/submissions">Submissions</a>
          </p>
        </section>

        <div className="series-stack">
          <section className="series-block">
            <header className="series-heading">
              <div>
                <span>01</span>
                <p>Profiles</p>
              </div>
              <div>
                <h2>
                  <Link href="/researchers">Published authors</Link>
                </h2>
                <p>
                  {profiles.map((profile) => profile.name).join(", ")}{" "}
                  {profiles.length === 1 ? "is" : "are"} on the public record, with{" "}
                  {profiles.reduce((sum, profile) => sum + profile.study_count, 0)} study
                  attributions.
                </p>
              </div>
            </header>
          </section>

          <section className="series-block">
            <header className="series-heading">
              <div>
                <span>02</span>
                <p>Critiques</p>
              </div>
              <div>
                <h2>A critique names its target.</h2>
                <p>
                  The object records the study, the claim when one is named, the author, the
                  type, the argument, the evidence, and the proposed change. Types:{" "}
                  {index.critique_types.join(", ")}.
                </p>
              </div>
            </header>
          </section>

          <section className="series-block">
            <header className="series-heading">
              <div>
                <span>03</span>
                <p>Forks</p>
              </div>
              <div>
                <h2>A fork records the disagreement.</h2>
                <p>
                  It keeps the parent study and states the changed assumptions, data, and
                  methods, then the new results and conclusion with their evidence status and
                  limitation.
                </p>
              </div>
            </header>
          </section>

          <section className="series-block">
            <header className="series-heading">
              <div>
                <span>04</span>
                <p>Revisions and submissions</p>
              </div>
              <div>
                <h2>Version 1.0 is the public text.</h2>
                <p>
                  A revision names the study, the version it starts from, and the change. A
                  submission names the question, the research type, the evidence status, and the
                  AI assistance. A valid POST is kept for review and stays off the public record.
                </p>
              </div>
            </header>
          </section>
        </div>
      </main>
      <SiteFooter />
    </>
  );
}
