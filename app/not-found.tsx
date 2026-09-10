import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";

export default function NotFound() {
  return (
    <>
      <SiteHeader />
      <main className="page-shell">
        <p className="eyebrow">404</p>
        <div className="hub-copy">
          <h2>This research site is not on GreyScienx.</h2>
          <p>The researcher home or paper path does not match a published site.</p>
          <p>
            <a className="button button-ghost" href="/">
              Back to the press
            </a>
          </p>
        </div>
      </main>
      <SiteFooter />
    </>
  );
}
