import { permanentRedirect } from "next/navigation";

export default async function LegacyPlayerPage({ params }: PageProps<"/experiments/virtual-casino/players/[playerId]">) {
  const { playerId } = await params;
  permanentRedirect(`/experiments/virtual-casino/house-edge/players/${playerId}`);
}
