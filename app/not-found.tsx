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
          <h2>This page is not on GreyScienx.</h2>
          <p>The address does not match a published paper or page.</p>
          <p>
            <Link className="button button-ghost" href="/research">
              Open the research archive
            </Link>
          </p>
        </div>
      </main>
      <SiteFooter />
    </>
  );
}
