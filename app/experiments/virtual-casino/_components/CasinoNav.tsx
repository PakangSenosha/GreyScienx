"use client";

import { useEffect, useRef } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";

const base = "/experiments/virtual-casino";

const hubLinks = [
  [base, "Experiments"],
  [`${base}/house-edge`, "House edge"],
  [`${base}/make-it-big`, "Make It Big"],
] as const;

const houseEdgeLinks = [
  [base, "All experiments"],
  [`${base}/house-edge`, "Overview"],
  [`${base}/house-edge/players`, "Players"],
  [`${base}/house-edge/cohorts`, "Cohorts"],
  [`${base}/house-edge/games`, "Games"],
  [`${base}/house-edge/worlds`, "Worlds"],
  [`${base}/house-edge/methods`, "Methods"],
  [`${base}/house-edge/safety`, "Safety"],
] as const;

const makeItBigLinks = [
  [base, "All experiments"],
  [`${base}/make-it-big`, "Overview"],
  [`${base}/make-it-big/results`, "Results"],
  [`${base}/make-it-big/strategies`, "Strategies"],
  [`${base}/make-it-big/games`, "Games"],
  [`${base}/make-it-big/survival`, "Survival"],
  [`${base}/make-it-big/methods`, "Methods"],
  [`${base}/make-it-big/safety`, "Safety"],
] as const;

const legacyHouseEdgeSegments = ["players", "cohorts", "games", "worlds", "methods", "safety", "downloads"];

export function CasinoNav() {
  const pathname = usePathname();
  const navRef = useRef<HTMLElement>(null);
  const isMakeItBig = pathname.startsWith(`${base}/make-it-big`);
  const isHouseEdge = pathname.startsWith(`${base}/house-edge`) || legacyHouseEdgeSegments.some((segment) => pathname.startsWith(`${base}/${segment}`));
  const links = isMakeItBig ? makeItBigLinks : isHouseEdge ? houseEdgeLinks : hubLinks;

  useEffect(() => {
    navRef.current
      ?.querySelector<HTMLElement>("[aria-current='page']")
      ?.scrollIntoView({ block: "nearest", inline: "center" });
  }, [pathname]);

  return (
    <nav ref={navRef} aria-label="Experiment navigation">
      {links.map(([href, label]) => {
        const pathOnly = href.split("#")[0];
        const isStudyOverview = pathOnly === `${base}/house-edge` || pathOnly === `${base}/make-it-big`;
        const isActive = href.includes("#")
          ? false
          : pathname === pathOnly || (!isStudyOverview && pathOnly !== base && pathname.startsWith(`${pathOnly}/`));

        return (
          <Link href={href} key={href} aria-current={isActive ? "page" : undefined}>
            {label}
          </Link>
        );
      })}
    </nav>
  );
}

export function CasinoDataLink() {
  const pathname = usePathname();
  const isMakeItBig = pathname.startsWith(`${base}/make-it-big`);
  const isHouseEdge = pathname.startsWith(`${base}/house-edge`) || legacyHouseEdgeSegments.some((segment) => pathname.startsWith(`${base}/${segment}`));
  const href = isMakeItBig ? `${base}/make-it-big/downloads` : isHouseEdge ? `${base}/house-edge/downloads` : `${base}#experiments`;
  return <Link className="vc-download-link" href={href}>{isMakeItBig || isHouseEdge ? "Download data ↓" : "View studies ↓"}</Link>;
}
