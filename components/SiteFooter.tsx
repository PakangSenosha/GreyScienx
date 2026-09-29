import Link from "next/link";
import { site } from "@/lib/site";

type SiteFooterProps = {
  left?: string;
  right?: string;
};

export function SiteFooter({
  left = site.name,
  right = site.tagline,
}: SiteFooterProps) {
  return (
    <footer>
      <p>{left}</p>
      <nav className="footer-links" aria-label="Publication policies">
        <Link href="/privacy">Privacy</Link>
        <Link href="/terms">Terms</Link>
        <Link href="/support">Support</Link>
      </nav>
      <p>{right}</p>
    </footer>
  );
}
