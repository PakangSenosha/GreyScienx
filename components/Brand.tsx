import Link from "next/link";

type BrandProps = {
  href?: string;
  division?: string;
  inverted?: boolean;
};

export function Brand({
  href = "/",
  division = "Research",
  inverted = false,
}: BrandProps) {
  return (
    <Link
      className={`brand${inverted ? " brand-inverted" : ""}`}
      href={href}
      aria-label="GreyScienx home"
    >
      <span className="brand-word">
        GREY<span>SCIENX</span>
      </span>
      <span className="brand-division">{division}</span>
    </Link>
  );
}
