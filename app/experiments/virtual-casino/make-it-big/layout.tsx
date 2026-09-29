import type { Metadata } from "next";
import type { ReactNode } from "react";

export const metadata: Metadata = {
  title: {
    default: "Make It Big | Virtual Casino Research",
    template: "%s | GreyScienx",
  },
  description: "A fixed-budget, first-passage study of rare synthetic payouts, with exact results and reproducible Monte Carlo evidence.",
};

export default function MakeItBigLayout({ children }: { children: ReactNode }) {
  return children;
}
