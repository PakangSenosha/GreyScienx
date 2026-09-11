import Link from "next/link";
import { Brand } from "./Brand";

type SiteHeaderProps = {
  links?: { href: string; label: string }[];
  action?: { href: string; label: string; download?: boolean };
};

export function SiteHeader({
  links = [
    { href: "/researchers", label: "Researchers" },
    { href: "/about", label: "About" },
  ],
  action = { href: "/submit", label: "Submit research" },
}: SiteHeaderProps) {
  return (
    <header className="site-header">
      <Brand />
      <nav aria-label="Primary navigation">
        {links.map((link) => (
          <Link key={link.href} href={link.href}>
            {link.label}
          </Link>
        ))}
        <Link
          className="nav-download"
          href={action.href}
          download={action.download || undefined}
        >
          {action.label}
        </Link>
      </nav>
    </header>
  );
}
