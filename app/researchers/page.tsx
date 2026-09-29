import type { Metadata } from "next";
import Link from "next/link";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { listProfiles } from "@/lib/research/community";

export const metadata: Metadata = {
  title: "Researchers",
  description: "Authors on the GreyScienx public record.",
};

export default function ResearchersPage() {
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
              <Link href="/community">Community</Link>
            </p>
            <h1>
              Researchers
              <br />
              <em>on the record.</em>
            </h1>
            <p className="dek">
              Each profile is the author record already published with the studies. Machine
              clients can read the same record as JSON.
            </p>
            <div className="hero-actions">
              <Link className="button button-primary" href="/api/v1/profiles">
                Profiles JSON
              </Link>
            </div>
          </div>
        </section>

        <div className="series-stack">
          {profiles.map((profile) => (
            <section className="series-block" key={profile.id}>
              <header className="series-heading">
                <div>
                  <span>{profile.study_count}</span>
                  <p>{profile.study_count === 1 ? "study" : "studies"}</p>
                </div>
                <div>
                  <h2>
                    <Link href={`/about/${profile.slug}`}>{profile.name}</Link>
                  </h2>
                  <p>
                    {profile.role}, {profile.affiliation}. {profile.bio}
                  </p>
                </div>
                <p className="series-count">
                  <a href={`/api/v1/profiles/${profile.slug}`}>{profile.id}</a>
                </p>
              </header>
            </section>
          ))}
        </div>
      </main>
      <SiteFooter />
    </>
  );
}
