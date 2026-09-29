import Link from "next/link";
import { ShareResearch } from "./ShareResearch";

export function PaperRow({
  number,
  title,
  description,
  detail,
  href,
  meta,
}: {
  number: string;
  title: string;
  description: string;
  detail?: string;
  href: string;
  meta: string;
}) {
  return (
    <article className="paper-row">
      <Link className="paper-row-link" href={href}>
        <span className="paper-number">{number}</span>
        <span className="paper-copy">
          <strong>{title}</strong>
          <span>{description}</span>
          {detail ? <span>{detail}</span> : null}
        </span>
        <span className="paper-meta">{meta}</span>
      </Link>
      <ShareResearch href={href} title={title} />
    </article>
  );
}
