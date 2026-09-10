import type { Metadata } from "next";
import { PreviewSite } from "@/components/PreviewSite";

export const metadata: Metadata = {
  title: "Distillation preview",
  robots: { index: false, follow: false },
};

export default function PreviewPage() {
  return <PreviewSite />;
}
