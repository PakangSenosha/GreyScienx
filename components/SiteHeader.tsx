import Link from "next/link";
import { Brand } from "./Brand";

type SiteHeaderProps = {
  links?: { href: string; label: string }[];
  action?: { href: string; label: string; download?: boolean };
};

export function SiteHeader({
  links = [
    { href: "/research", label: "Research" },
    { href: "/about", label: "About" },
    { href: "/about/pakang-senosha", label: "Founder" },
  ],
  action = { href: "/research", label: "Read the archive" },
}: SiteHeaderProps) {
  return (
    <header className="site-header">
      <Brand division="Research publication" />
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
