import { site } from "@/lib/site";

type SiteFooterProps = {
  left?: string;
  right?: string;
};

export function SiteFooter({
  left = site.name,
  right = `${site.founder.name} · ${site.founder.role}`,
}: SiteFooterProps) {
  return (
    <footer>
      <p>{left}</p>
      <p>{right}</p>
    </footer>
  );
}
