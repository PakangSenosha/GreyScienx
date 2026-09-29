import type { Metadata } from "next";
import { CasinoShell } from "./_components/CasinoShell";

export const metadata: Metadata = {
  title: "Virtual Casino Research",
  description: "Independent simulations of house edge, survival, behaviour, chance, fixed budgets and rare payouts. No real money or visitor wagering.",
};

export default function VirtualCasinoLayout({ children }: LayoutProps<"/experiments/virtual-casino">) {
  return <CasinoShell>{children}</CasinoShell>;
}
