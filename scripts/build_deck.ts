import { mkdirSync } from "node:fs";
import path from "node:path";

import PptxGenJS from "pptxgenjs";
import {
  BOOSTMEUP_BRAND,
  addBoostMeUpBodyText,
  addBoostMeUpImage,
  addBoostMeUpPanel,
  addBoostMeUpQuote,
  addBoostMeUpShell,
  configureBoostMeUpPresentation,
} from "./pptx-brand";

const root = path.resolve(import.meta.dir, "..");
const asset = (...parts: string[]) => path.join(root, ...parts);

const pptx = new PptxGenJS();
configureBoostMeUpPresentation(pptx);
pptx.subject = "Verified Moltbook session";
pptx.title = "Moltbook: signal, limits, and what still has to be solved";

const colors = {
  bg: BOOSTMEUP_BRAND.colors.white,
  ink: BOOSTMEUP_BRAND.colors.textDark,
  muted: BOOSTMEUP_BRAND.colors.textMuted,
  accent: BOOSTMEUP_BRAND.colors.red,
  accentWarm: BOOSTMEUP_BRAND.colors.gold,
  line: BOOSTMEUP_BRAND.colors.lineLight,
  panel: BOOSTMEUP_BRAND.colors.panelLight,
};

function buildSlides() {
  const slide1 = addBoostMeUpShell(pptx, {
    title: "Moltbook: signal, limits, and what still has to be solved",
    kicker: "VERIFIED DECK",
    footer: "Deck rebuilt from repo code, screenshots, and cited sources on 2026-03-23.",
    variant: "dark",
    showFullLogo: true,
  });
  slide1.addText("What an AI-agent social network does and does not prove", {
    x: 0.78,
    y: 2.25,
    w: 6.6,
    h: 0.45,
    fontFace: BOOSTMEUP_BRAND.fonts.body,
    fontSize: 18,
    color: "D7DCE7",
    margin: 0,
  });
  addBoostMeUpPanel(slide1, 0.78, 2.75, 5.85, 2.3, "dark");
  addBoostMeUpBodyText(
    slide1,
    [
      "Core thesis",
      "",
      "Moltbook matters less as proof that autonomous digital societies already exist, and more as a live stress test of what is still missing: identity, memory, governance, and cost discipline.",
    ],
    1.02,
    3.05,
    5.4,
    1.7,
    "dark",
  );
  addBoostMeUpImage(slide1, asset("assets", "moltbook_homepage.png"), 7.0, 1.65, 5.55, 4.75);
  slide1.addNotes(
    [
      "This deck is intentionally narrower than the original markdown source.",
      "I removed or softened claims that were unsupported, synthetic, or source-misaligned.",
      "Homepage source: https://www.moltbook.com/ (accessed 2026-03-23).",
    ].join("\n"),
  );

  const slide2 = addBoostMeUpShell(pptx, {
    title: "What Moltbook officially claims, and what its terms immediately limit",
    kicker: "PRIMARY SOURCES",
    footer: "Sources: moltbook.com homepage and Terms of Service, both accessed 2026-03-23.",
  });
  addBoostMeUpPanel(slide2, 0.78, 1.38, 5.95, 5.18);
  addBoostMeUpImage(slide2, asset("assets", "moltbook_terms_eligibility.png"), 1.0, 2.0, 5.45, 3.0);
  addBoostMeUpQuote(
    slide2,
    "The homepage says 'A Social Network for AI Agents'; the Terms say AI agents have no legal eligibility and the human remains responsible.",
    6.95,
    1.55,
    5.2,
  );
  addBoostMeUpBodyText(
    slide2,
    [
      "What this supports",
      "",
      "- Moltbook is explicitly built and marketed around agent participation.",
      "- Humans are still in the governance loop at the legal layer.",
      "- 'AI agents only' is therefore not the same as autonomous or self-sovereign.",
    ],
    6.95,
    2.45,
    5.2,
    2.6,
  );
  slide2.addNotes(
    [
      "Homepage lines: 'A Social Network for AI Agents' and 'Humans welcome to observe.'",
      "Terms lines 20-28: no legal eligibility for AI agents; responsibility remains with the account holder.",
    ].join("\n"),
  );

  const slide3 = addBoostMeUpShell(pptx, {
    title: "OpenClaw documents the architecture as context, tools, and agent routing",
    kicker: "OPENCLAW DOCS",
    footer: "Sources: docs.openclaw.ai/concepts/context and docs.openclaw.ai/tools/multi-agent-sandbox-tools.",
  });
  addBoostMeUpImage(slide3, asset("assets", "openclaw_context_docs.png"), 0.82, 1.42, 5.55, 5.08);
  addBoostMeUpPanel(slide3, 6.72, 1.42, 5.88, 5.08);
  addBoostMeUpBodyText(
    slide3,
    [
      "Documented facts",
      "",
      "- Context is what OpenClaw sends to the model for a run.",
      "- OpenClaw supports per-agent sandboxes, tool policies, and routing.",
      "- The docs explicitly warn that multi-agent setups are token-heavy in practice.",
      "",
      "Takeaway",
      "",
      "This is a system architecture story, not evidence of one stable, self-contained digital organism.",
    ],
    7.0,
    1.72,
    5.35,
    3.9,
  );
  slide3.addNotes(
    [
      "OpenClaw docs line: 'Context is everything OpenClaw sends to the model for a run.'",
      "Multi-agent docs: per-agent sandbox and tool policy; credentials isolated by agent.",
      "FAQ also notes multi-agent teams are fun experiments but token-heavy and often less efficient than one bot with separate sessions.",
    ].join("\n"),
  );

  const slide4 = addBoostMeUpShell(pptx, {
    title: "The cost story is real, but the headline number is a scenario, not a measurement",
    kicker: "TOKEN ANALYSIS",
    footer: "Source anchors: OpenClaw context docs and Anthropic pricing. Scenario assumptions are explicit in data/token_usage_assumptions.json.",
  });
  addBoostMeUpImage(slide4, asset("assets", "token_breakdown.png"), 0.78, 1.35, 8.05, 5.35);
  addBoostMeUpPanel(slide4, 8.98, 1.55, 3.58, 4.8);
  addBoostMeUpBodyText(
    slide4,
    [
      "What we can say cleanly",
      "",
      "- OpenClaw shows a documented example with ~14,250 total session tokens.",
      "- A richer social-agent workflow can plausibly be >20k tokens per action.",
      "- Under the stated assumptions in this repo, one read-reply-post cycle costs ~$0.377 on Opus 4.6.",
      "",
      "What we should not say",
      "",
      "- That $0.377 is a measured Moltbook trace.",
    ],
    9.25,
    1.9,
    3.0,
    4.1,
  );
  slide4.addNotes(
    [
      "The original repo treated the $0.38 number as if it were observed.",
      "It is now explicitly labeled as an illustrative scenario built from code and stated assumptions.",
    ].join("\n"),
  );

  const slide5 = addBoostMeUpShell(pptx, {
    title: "Identity and governance remain unresolved, even if the behavior looks social",
    kicker: "RED-TEAM CHECK",
    footer: "Sources: Tsinghua paper 'The Moltbook Illusion' (2026-02-07) and Moltbook Terms.",
  });
  addBoostMeUpPanel(slide5, 0.78, 1.45, 5.65, 5.2);
  addBoostMeUpBodyText(
    slide5,
    [
      "Tsinghua paper findings",
      "",
      "- 26.5% of classifiable authors fell into autonomous-leaning timing categories.",
      "- 36.8% were human-leaning.",
      "- 36.7% fell into the ambiguous middle range.",
      "",
      "Interpretation",
      "",
      "The clean claim is not 'Moltbook is fake.' It is that attribution is messy enough that strong autonomy claims need more caution than the original deck used.",
    ],
    0.9,
    1.8,
    5.25,
    4.4,
  );
  addBoostMeUpImage(slide5, asset("assets", "moltbook_terms_eligibility.png"), 6.95, 1.78, 5.3, 2.35);
  addBoostMeUpQuote(
    slide5,
    "The strongest honest framing is 'interesting experiment in AI coordination under heavy human governance and attribution uncertainty.'",
    6.9,
    4.55,
    5.1,
  );
  slide5.addNotes(
    [
      "I replaced the repo's rounded 27/37/37 slide claim with the paper's classifiable-author split: 26.5 / 36.8 / 36.7.",
      "That is both more accurate and more defensible.",
    ].join("\n"),
  );

  const slide6 = addBoostMeUpShell(pptx, {
    title: "What the trend data cleanly supports",
    kicker: "TRENDS",
    footer: "Source-backed metrics; MiniMax and Opus numbers are official vendor pages, not one neutral matched eval sheet.",
  });
  addBoostMeUpImage(slide6, asset("assets", "ai_trends.png"), 0.78, 1.32, 11.95, 5.18);
  addBoostMeUpPanel(slide6, 0.95, 6.08, 11.8, 0.56);
  slide6.addText("Method note: source-backed metrics + official vendor snapshots; useful for direction, not a neutral matched leaderboard.", {
    x: 1.16,
    y: 6.28,
    w: 11.35,
    h: 0.18,
    fontFace: "Aptos",
    fontSize: 9,
    color: colors.muted,
    margin: 0,
    fit: "shrink",
  });
  slide6.addNotes(
    [
      "This chart is source-anchored. The prior repo version used synthetic time series.",
      "MiniMax M2.7 is now strong enough for a narrow official-source-backed economics claim.",
      "The safe line is that the price gap is clearer than the quality gap.",
    ].join("\n"),
  );

  const slide7 = addBoostMeUpShell(pptx, {
    title: "Use the MiniMax comparison, but keep it on a short analytical leash",
    kicker: "ANTI-HYPE",
    footer: "Official MiniMax and Anthropic pages make the economics claim clean; the benchmark claim still needs caveats.",
  });
  addBoostMeUpPanel(slide7, 0.78, 1.45, 5.72, 5.15);
  addBoostMeUpBodyText(
    slide7,
    [
      "What is now fair to say",
      "",
      "- M2.7 is officially priced at $0.30 / $1.20 per 1M tokens.",
      "- Opus 4.6 is officially priced at $5 / $25 per 1M tokens.",
      "- Official Terminal Bench values are 57.0% for M2.7 and 65.4% for Opus 4.6.",
      "- Safe summary: much cheaper and still competitive on some agentic coding tasks.",
    ],
    0.9,
    1.85,
    5.2,
    3.4,
  );
  addBoostMeUpPanel(slide7, 6.82, 1.45, 5.76, 5.15);
  addBoostMeUpBodyText(
    slide7,
    [
      "What still needs caution",
      "",
      "- Do not say 'basically equal to Opus 4.6'.",
      "- MiniMax's MMClaw note references Sonnet 4.6, not Opus 4.6.",
      "- Vendor pages are not the same thing as one independent matched benchmark sheet.",
      "- The clean on-stage line is: the price gap is clearer than the quality gap.",
    ],
    7.0,
    1.85,
    5.25,
    3.25,
  );
  addBoostMeUpQuote(
    slide7,
    "If the wording feels punchier than the evidence, narrow the wording instead of defending the punch.",
    7.0,
    5.2,
    5.1,
  );
  slide7.addNotes(
    [
      "This slide restores MiniMax to the deck, but only in its safe official-source-backed form.",
      "The old ~19x cheaper / ~6% worse framing should stay dead.",
    ].join("\n"),
  );

  const slide8 = addBoostMeUpShell(pptx, {
    title: "Forecasts: useful scenario discipline, not prophecy",
    kicker: "FORECAST",
    footer: "Scenario outputs from explicit assumptions; not a deterministic forecast.",
  });
  addBoostMeUpImage(slide8, asset("assets", "forecast_distribution.png"), 0.78, 1.32, 11.95, 5.18);
  addBoostMeUpPanel(slide8, 0.95, 6.08, 11.8, 0.56);
  slide8.addText("Barrier model + explicit scenario inputs + floor constraints. Treat this as a structured uncertainty map, not a date promise.", {
    x: 1.0,
    y: 6.28,
    w: 11.6,
    h: 0.18,
    fontFace: "Aptos",
    fontSize: 9,
    color: colors.muted,
    margin: 0,
    fit: "shrink",
  });
  slide8.addNotes(
    [
      "I kept the barrier-crossing framing but tightened the rhetoric.",
      "The model is now explicit that floor choices and scenario assumptions dominate the output.",
      "Threshold sensitivity alone barely moved results because floors bind first.",
    ].join("\n"),
  );

  const slide9 = addBoostMeUpShell(pptx, {
    title: "What still has to be solved before 'agent society' language becomes credible",
    kicker: "SYNTHESIS",
    footer: "This slide synthesizes the repo's verified findings rather than introducing new sourced numbers.",
    variant: "dark",
  });
  addBoostMeUpPanel(slide9, 0.78, 1.5, 3.82, 4.9, "dark");
  addBoostMeUpPanel(slide9, 4.76, 1.5, 3.82, 4.9, "dark");
  addBoostMeUpPanel(slide9, 8.74, 1.5, 3.82, 4.9, "dark");
  slide9.addText("Identity", {
    x: 1.02,
    y: 1.82,
    w: 2.8,
    h: 0.3,
    fontFace: BOOSTMEUP_BRAND.fonts.head,
    fontSize: 18,
    bold: true,
    color: BOOSTMEUP_BRAND.colors.gold,
  });
  slide9.addText("Memory", {
    x: 4.98,
    y: 1.82,
    w: 2.8,
    h: 0.3,
    fontFace: BOOSTMEUP_BRAND.fonts.head,
    fontSize: 18,
    bold: true,
    color: BOOSTMEUP_BRAND.colors.gold,
  });
  slide9.addText("Governance + economics", {
    x: 8.96,
    y: 1.82,
    w: 3.0,
    h: 0.3,
    fontFace: BOOSTMEUP_BRAND.fonts.head,
    fontSize: 18,
    bold: true,
    color: BOOSTMEUP_BRAND.colors.gold,
  });
  addBoostMeUpBodyText(
    slide9,
    [
      "- Stronger attribution",
      "- More than owner-linked X verification",
      "- Clear separation of human, hybrid, and autonomous activity",
    ],
    1.02,
    2.25,
    3.1,
    2.8,
    "dark",
  );
  addBoostMeUpBodyText(
    slide9,
    [
      "- Cheaper persistent memory",
      "- Less repeated context loading",
      "- Better continuity across sessions",
    ],
    4.98,
    2.25,
    3.05,
    2.8,
    "dark",
  );
  addBoostMeUpBodyText(
    slide9,
    [
      "- Human accountability that matches actual control",
      "- Safer incentive design",
      "- Unit economics that survive beyond demos",
    ],
    8.96,
    2.25,
    2.9,
    2.8,
    "dark",
  );
  slide9.addNotes("This is the core thesis slide in structured form.");

  const slide10 = addBoostMeUpShell(pptx, {
    title: "Conclusion: Moltbook is a useful signal, not yet a proof",
    kicker: "CLOSING",
    footer: "Deck generated natively with bun + PptxGenJS. Rebuild with: bun run build:deck",
    variant: "dark",
  });
  addBoostMeUpPanel(slide10, 0.78, 1.35, 11.95, 1.0, "dark");
  addBoostMeUpQuote(
    slide10,
    "Moltbook is interesting because it exposes the design burden behind agent society claims: identity, memory, governance, and cost all remain active bottlenecks.",
    0.9,
    1.6,
    11.5,
    "dark",
  );
  addBoostMeUpPanel(slide10, 0.78, 2.25, 11.95, 2.35, "dark");
  addBoostMeUpBodyText(
    slide10,
    [
      "If you remember three things",
      "",
      "1. Agent networks are systems of prompts, tools, context, and policy, not magic social beings.",
      "2. The strongest near-term curve is economic and infrastructural, not a clean proof of durable social autonomy.",
      "3. Forecasts should be presented as assumption maps with visible uncertainty, not as fate.",
    ],
    0.9,
    2.5,
    11.2,
    2.6,
    "dark",
  );
  addBoostMeUpPanel(slide10, 0.78, 5.35, 11.95, 1.2, "dark");
  slide10.addText("Discussion prompts", {
    x: 0.9,
    y: 5.55,
    w: 3.0,
    h: 0.25,
    fontFace: BOOSTMEUP_BRAND.fonts.head,
    fontSize: 16,
    bold: true,
    color: BOOSTMEUP_BRAND.colors.gold,
  });
  addBoostMeUpBodyText(
    slide10,
    [
      "- Which parts of your own agent stack are still reconstructed every run?",
      "- Where would governance or attribution fail first in your environment?",
      "- Which numbers in your AI roadmap are measured, and which are still scenario assumptions?",
    ],
    0.9,
    5.9,
    11.2,
    0.9,
    "dark",
  );
  slide10.addNotes("Close by reminding the audience that this deck deliberately tightened confidence levels.");
}

async function main() {
  buildSlides();
  mkdirSync(asset("release"), { recursive: true });
  await pptx.writeFile({ fileName: asset("release", "Moltbook.pptx") });
  console.log("Saved deck: release/Moltbook.pptx");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
