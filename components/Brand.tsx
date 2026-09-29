import Image from "next/image";
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
      <span className="brand-wordmark" aria-hidden="true">
        <Image
          src="/brand/greyscienx-wordmark.svg"
          alt=""
          width={480}
          height={60}
          priority
          sizes="138px"
        />
      </span>
      <span className="brand-division">{division}</span>
    </Link>
  );
}
