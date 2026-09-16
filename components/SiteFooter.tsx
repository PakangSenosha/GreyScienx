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
      <p>{right}</p>
    </footer>
  );
}
