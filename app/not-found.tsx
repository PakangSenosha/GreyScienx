import Link from "next/link";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";

export default function NotFound() {
  return (
    <>
      <SiteHeader />
      <main className="page-shell">
        <p className="eyebrow">404</p>
        <div className="hub-copy">
          <h2>We could not find that page.</h2>
          <p>The address may have changed, or the page may no longer be available.</p>
          <p>
            <Link className="button button-ghost" href="/research">
              Go to the research archive
            </Link>
          </p>
        </div>
      </main>
      <SiteFooter />
    </>
  );
}
