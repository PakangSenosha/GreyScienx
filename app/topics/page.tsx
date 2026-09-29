import type { Metadata } from "next";
import Link from "next/link";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { listTopicRecords } from "@/lib/research/registry";

export const metadata: Metadata = {
  title: "Topics",
  description: "Topic hubs for the GreyScienx research archive.",
};

export default function TopicsPage() {
  const topics = listTopicRecords();

  return (
    <>
      <SiteHeader />
      <main>
        <section className="hero hero-solo">
          <div className="brand-wave wave-one" aria-hidden="true" />
          <div className="brand-wave wave-two" aria-hidden="true" />
          <div className="hero-copy">
            <p className="eyebrow">Concepts</p>
            <h1>
              Topics,
              <br />
              <em>tied to studies.</em>
            </h1>
            <p className="dek">
              Each topic names the studies that address it. A topic appears here only when at
              least one published study carries it.
            </p>
          </div>
        </section>

        <div className="series-stack">
          {topics.map((topic) => (
            <section className="series-block" key={topic.slug}>
              <header className="series-heading">
                <div>
                  <span>{topic.study_count}</span>
                  <p>{topic.study_count === 1 ? "study" : "studies"}</p>
                </div>
                <div>
                  <h2>
                    <Link href={`/topics/${topic.slug}`}>{topic.title}</Link>
                  </h2>
                  <p>{topic.definition}</p>
                </div>
              </header>
            </section>
          ))}
        </div>
      </main>
      <SiteFooter />
    </>
  );
}
