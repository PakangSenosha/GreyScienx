import { NextResponse } from "next/server";
import {
  DISTILL_PROMPT,
  distillSchema,
  heuristicDistill,
  toPreviewRecord,
  type DistillInput,
} from "@/lib/distill";

export const maxDuration = 60;

function readInput(body: Record<string, unknown>): DistillInput {
  const manuscript = String(body.manuscript ?? "").trim();
  if (manuscript.length < 80) {
    throw new Error("Paste at least a short manuscript, abstract, or results section.");
  }

  return {
    researcherName: String(body.researcherName ?? "").trim() || "Independent researcher",
    affiliation: String(body.affiliation ?? "").trim() || "Unaffiliated",
    role: String(body.role ?? "").trim() || "Independent researcher",
    email: String(body.email ?? "").trim(),
    title: String(body.title ?? "").trim(),
    field: String(body.field ?? "").trim(),
    manuscript: manuscript.slice(0, 24000),
  };
}

export async function POST(request: Request) {
  let input: DistillInput | null = null;

  try {
    const body = (await request.json()) as Record<string, unknown>;
    input = readInput(body);

    const apiKey = process.env.XAI_API_KEY;
    if (!apiKey) {
      const distilled = heuristicDistill(input);
      return NextResponse.json({
        source: "heuristic",
        ...toPreviewRecord(input, distilled),
      });
    }

    const { generateText, Output } = await import("ai");
    const { createXai } = await import("@ai-sdk/xai");
    const xai = createXai({ apiKey });

    const { output } = await generateText({
      model: xai("grok-4.6"),
      output: Output.object({ schema: distillSchema }),
      system: DISTILL_PROMPT,
      prompt: [
        `Researcher: ${input.researcherName}`,
        `Affiliation: ${input.affiliation}`,
        `Role: ${input.role}`,
        input.title ? `Working title: ${input.title}` : "",
        input.field ? `Field: ${input.field}` : "",
        "",
        "Manuscript:",
        input.manuscript,
      ]
        .filter(Boolean)
        .join("\n"),
    });

    const distilled = distillSchema.parse(output);
    return NextResponse.json({
      source: "model",
      ...toPreviewRecord(input, distilled),
    });
  } catch (error) {
    const message = error instanceof Error ? error.message : "Distillation failed.";
    if (input) {
      const distilled = heuristicDistill(input);
      return NextResponse.json({
        source: "heuristic",
        warning: message,
        ...toPreviewRecord(input, distilled),
      });
    }
    return NextResponse.json({ error: message }, { status: 400 });
  }
}
