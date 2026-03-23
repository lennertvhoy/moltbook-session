import { mkdirSync } from "node:fs";
import path from "node:path";

import PptxGenJS from "pptxgenjs";
import {
  BOOSTMEUP_BRAND,
  addBoostMeUpImage,
  addBoostMeUpPanel,
  addBoostMeUpShell,
  configureBoostMeUpPresentation,
} from "./pptx-brand";

type SlideVariant = "light" | "dark";

const root = path.resolve(import.meta.dir, "..");
const asset = (...parts: string[]) => path.join(root, ...parts);

const pptx = new PptxGenJS();
configureBoostMeUpPresentation(pptx);
pptx.subject = "Nederlandstalige Moltbook keynote";
pptx.title = "Moltbook: signaal, geen bewijs";

const colors = {
  navy: BOOSTMEUP_BRAND.colors.navy,
  white: BOOSTMEUP_BRAND.colors.white,
  red: BOOSTMEUP_BRAND.colors.red,
  gold: BOOSTMEUP_BRAND.colors.gold,
  ink: BOOSTMEUP_BRAND.colors.textDark,
  muted: BOOSTMEUP_BRAND.colors.textMuted,
  line: BOOSTMEUP_BRAND.colors.lineLight,
  panel: BOOSTMEUP_BRAND.colors.panelLight,
  darkPanel: "1C2540",
  darkLine: "394258",
  softRed: "FDE8E6",
  softGold: "FEF3C7",
  softBlue: "E8EEF9",
} as const;

function inkFor(variant: SlideVariant): string {
  return variant === "dark" ? colors.white : colors.ink;
}

function mutedFor(variant: SlideVariant): string {
  return variant === "dark" ? "D7DCE7" : colors.muted;
}

function addTextBlock(
  slide: PptxGenJS.Slide,
  text: string,
  x: number,
  y: number,
  w: number,
  h: number,
  options: {
    size?: number;
    color?: string;
    bold?: boolean;
    italic?: boolean;
    align?: PptxGenJS.TextProps["align"];
    valign?: PptxGenJS.TextProps["valign"];
    fontFace?: string;
  } = {},
): void {
  slide.addText(text, {
    x,
    y,
    w,
    h,
    margin: 0,
    fit: "shrink",
    fontFace: options.fontFace ?? BOOSTMEUP_BRAND.fonts.body,
    fontSize: options.size ?? 16,
    color: options.color ?? colors.ink,
    bold: options.bold ?? false,
    italic: options.italic ?? false,
    align: options.align,
    valign: options.valign,
  });
}

function addPill(
  slide: PptxGenJS.Slide,
  text: string,
  x: number,
  y: number,
  w: number,
  fill: string,
  color: string,
): void {
  slide.addShape("roundRect", {
    x,
    y,
    w,
    h: 0.36,
    rectRadius: 0.08,
    fill: { color: fill },
    line: { color: fill, transparency: 100 },
  });
  addTextBlock(slide, text, x + 0.16, y + 0.08, w - 0.32, 0.18, {
    size: 9,
    color,
    bold: true,
  });
}

function addFramedImage(
  slide: PptxGenJS.Slide,
  imagePath: string,
  x: number,
  y: number,
  w: number,
  h: number,
  variant: SlideVariant = "light",
): void {
  addBoostMeUpPanel(slide, x, y, w, h, variant);
  addBoostMeUpImage(slide, imagePath, x + 0.12, y + 0.12, w - 0.24, h - 0.24);
}

function addStatCard(
  slide: PptxGenJS.Slide,
  value: string,
  label: string,
  note: string,
  x: number,
  y: number,
  w: number,
  variant: SlideVariant,
  accent: string,
): void {
  addBoostMeUpPanel(slide, x, y, w, 2.0, variant);
  addTextBlock(slide, value, x + 0.2, y + 0.2, w - 0.4, 0.55, {
    size: 28,
    bold: true,
    color: accent,
    fontFace: BOOSTMEUP_BRAND.fonts.head,
  });
  addTextBlock(slide, label, x + 0.2, y + 0.86, w - 0.4, 0.26, {
    size: 12,
    bold: true,
    color: inkFor(variant),
  });
  addTextBlock(slide, note, x + 0.2, y + 1.2, w - 0.4, 0.5, {
    size: 11,
    color: mutedFor(variant),
  });
}

function addTakeawayBand(
  slide: PptxGenJS.Slide,
  text: string,
  y: number,
  variant: SlideVariant,
): void {
  const fill = variant === "dark" ? colors.darkPanel : colors.softBlue;
  const line = variant === "dark" ? colors.darkLine : colors.line;
  slide.addShape("roundRect", {
    x: 0.78,
    y,
    w: 11.95,
    h: 0.7,
    rectRadius: 0.08,
    fill: { color: fill },
    line: { color: line, pt: 1 },
  });
  addTextBlock(slide, text, 1.02, y + 0.18, 11.45, 0.22, {
    size: 12,
    bold: true,
    color: inkFor(variant),
  });
}

function addMetricBar(
  slide: PptxGenJS.Slide,
  label: string,
  value: string,
  ratio: number,
  x: number,
  y: number,
  w: number,
  color: string,
): void {
  addTextBlock(slide, label, x, y, w, 0.2, {
    size: 11,
    color: colors.muted,
    bold: true,
  });
  slide.addShape("roundRect", {
    x,
    y: y + 0.26,
    w,
    h: 0.26,
    rectRadius: 0.08,
    fill: { color: "EEF2F7" },
    line: { color: "EEF2F7", transparency: 100 },
  });
  slide.addShape("roundRect", {
    x,
    y: y + 0.26,
    w: Math.max(w * ratio, 0.18),
    h: 0.26,
    rectRadius: 0.08,
    fill: { color },
    line: { color, transparency: 100 },
  });
  addTextBlock(slide, value, x + w - 0.9, y + 0.02, 0.9, 0.18, {
    size: 11,
    color: colors.ink,
    bold: true,
    align: "right",
  });
}

function addProcessNode(
  slide: PptxGenJS.Slide,
  title: string,
  subline: string,
  x: number,
  y: number,
): void {
  addBoostMeUpPanel(slide, x, y, 2.08, 1.1, "dark");
  addTextBlock(slide, title, x + 0.16, y + 0.18, 1.76, 0.22, {
    size: 14,
    color: colors.gold,
    bold: true,
  });
  addTextBlock(slide, subline, x + 0.16, y + 0.5, 1.76, 0.34, {
    size: 10,
    color: "D7DCE7",
  });
}

function buildSlides(): void {
  const slide1 = addBoostMeUpShell(pptx, {
    title: "Moltbook: signaal, geen bewijs",
    kicker: "NEDERLANDSTALIGE KEYNOTE",
    footer: "Gebaseerd op repo-code, screenshots en gecontroleerde bronnen. Rebuild: 2026-03-23.",
    variant: "dark",
    showFullLogo: true,
  });
  addTextBlock(slide1, "Wat een sociaal netwerk voor AI-agenten wel en niet laat zien", 0.78, 2.24, 6.0, 0.36, {
    size: 18,
    color: "D7DCE7",
  });
  addBoostMeUpPanel(slide1, 0.78, 2.82, 5.5, 2.35, "dark");
  addPill(slide1, "KERNFRAMING", 1.04, 3.08, 1.4, colors.gold, colors.navy);
  addTextBlock(
    slide1,
    "Niet interessant omdat autonomie al bewezen is.\nWel interessant omdat het zichtbaar maakt wat nog ontbreekt.",
    1.04,
    3.58,
    4.8,
    0.9,
    {
      size: 18,
      color: colors.white,
      bold: true,
      fontFace: BOOSTMEUP_BRAND.fonts.head,
    },
  );
  addTextBlock(slide1, "identiteit  •  geheugen  •  governance  •  kostdiscipline", 1.04, 4.56, 4.9, 0.22, {
    size: 12,
    color: colors.gold,
    bold: true,
  });
  addFramedImage(slide1, asset("assets", "moltbook_homepage.png"), 6.88, 1.58, 5.55, 4.92, "dark");
  addPill(slide1, "live stresstest", 9.06, 1.86, 1.58, colors.red, colors.white);
  slide1.addNotes(
    [
      "Open met de spanning, niet met de definities.",
      "Sterke zin voor op het podium: Moltbook is minder bewijs dan stresstest.",
      "[Sources]",
      "- Moltbook homepage: https://www.moltbook.com/ (geraadpleegd 2026-03-23).",
    ].join("\n"),
  );

  const slide2 = addBoostMeUpShell(pptx, {
    title: "Moltbook verkoopt autonomie, maar borgt ze niet",
    kicker: "PRIMAIRE BRONNEN",
    footer: "Bronnen: Moltbook-homepage en Terms of Service, geraadpleegd op 2026-03-23.",
  });
  addPill(slide2, "publiek verhaal", 0.94, 1.3, 1.44, colors.red, colors.white);
  addFramedImage(slide2, asset("assets", "moltbook_homepage.png"), 0.78, 1.62, 5.48, 1.72);
  addBoostMeUpPanel(slide2, 0.78, 3.52, 5.48, 2.52);
  addTextBlock(slide2, "\"A Social Network for AI Agents\"", 1.04, 3.78, 4.9, 0.42, {
    size: 21,
    color: colors.red,
    bold: true,
    fontFace: BOOSTMEUP_BRAND.fonts.head,
  });
  addTextBlock(slide2, "Humans welcome to observe.\nAgentparticipatie is dus echt onderdeel van het productverhaal.", 1.04, 4.34, 4.9, 0.72, {
    size: 14,
  });

  slide2.addShape("line", {
    x: 6.6,
    y: 1.54,
    w: 0,
    h: 4.86,
    line: { color: colors.line, pt: 1.25 },
  });
  addPill(slide2, "juridische limiet", 7.0, 1.3, 1.7, colors.gold, colors.navy);
  addFramedImage(slide2, asset("assets", "moltbook_terms_eligibility.png"), 6.98, 1.62, 5.4, 1.72);
  addBoostMeUpPanel(slide2, 6.98, 3.52, 5.4, 2.52, "dark");
  addTextBlock(slide2, "Geen legal eligibility", 7.26, 3.84, 4.5, 0.32, {
    size: 21,
    color: colors.gold,
    bold: true,
    fontFace: BOOSTMEUP_BRAND.fonts.head,
  });
  addTextBlock(slide2, "De menselijke account owner blijft verantwoordelijk.\nDat is geen detail: het begrenst juridische en governance-autonomie meteen.", 7.26, 4.28, 4.6, 0.84, {
    size: 14,
    color: colors.white,
  });
  addTakeawayBand(slide2, "Takeaway: agentparticipatie is reëel; juridische en governance-autonomie zijn dat nog niet.", 6.02, "light");
  slide2.addNotes(
    [
      "Breng hier de centrale spanning: marketingclaim versus juridische realiteit.",
      "Niet zeggen dat Moltbook 'fake' is. Wel zeggen dat autonomie hier niet netjes geborgd is.",
      "[Sources]",
      "- Homepage copy: 'A Social Network for AI Agents' en 'Humans welcome to observe.'",
      "- Terms of Service: AI agents hebben geen legal eligibility; verantwoordelijkheid blijft bij de mens.",
    ].join("\n"),
  );

  const slide3 = addBoostMeUpShell(pptx, {
    title: "Een agentnetwerk is vooral een systeem",
    kicker: "OPENCLAW",
    footer: "Bronnen: OpenClaw context docs en multi-agent docs; vereenvoudigde schemaweergave op basis van die documentatie.",
    variant: "dark",
  });
  addTextBlock(slide3, "De praktische definitie is niet mystiek maar operationeel.", 0.78, 1.28, 5.5, 0.24, {
    size: 15,
    color: "D7DCE7",
  });
  addPill(slide3, "model + instructies + context + tools + state", 0.78, 1.64, 3.82, colors.gold, colors.navy);
  slide3.addShape("line", {
    x: 1.24,
    y: 3.18,
    w: 10.45,
    h: 0,
    line: { color: colors.red, pt: 2 },
  });
  addProcessNode(slide3, "Instructies", "rol, regels,\nAGENTS.md", 0.96, 2.56);
  addProcessNode(slide3, "Context", "geschiedenis,\nretrieval, files", 3.16, 2.56);
  addProcessNode(slide3, "Tools", "schema's,\nrechten", 5.36, 2.56);
  addProcessNode(slide3, "Model", "redenatie,\noutput", 7.56, 2.56);
  addProcessNode(slide3, "State", "routing,\nexterne geheugenlaag", 9.76, 2.56);
  addBoostMeUpPanel(slide3, 0.78, 4.52, 7.16, 1.38, "dark");
  addTextBlock(slide3, "Wat OpenClaw expliciet toont", 1.02, 4.8, 2.4, 0.22, {
    size: 14,
    color: colors.gold,
    bold: true,
  });
  addTextBlock(slide3, "Routing, sandboxes en tool policy zijn technisch echt.\nMaar multi-agent setups zijn ook token-heavy en operationeel fragiel.", 1.02, 5.14, 6.4, 0.56, {
    size: 14,
    color: colors.white,
  });
  addFramedImage(slide3, asset("assets", "openclaw_context_docs.png"), 8.3, 4.22, 4.28, 2.1, "dark");
  addTakeawayBand(slide3, "Takeaway: dit is een architectuurverhaal, geen bewijs van één stabiel digitaal organisme.", 6.02, "dark");
  slide3.addNotes(
    [
      "Zeg expliciet dat dit schema een vereenvoudigde interpretatie is van de docs, geen letterlijk diagram van OpenClaw.",
      "Nuttige podiumzin: wat als autonomie voelt, is vaak een georkestreerde loop.",
      "[Sources]",
      "- OpenClaw docs: 'Context is everything OpenClaw sends to the model for a run.'",
      "- Multi-agent docs: per-agent sandboxes, tool policies en routing.",
    ].join("\n"),
  );

  const slide4 = addBoostMeUpShell(pptx, {
    title: "De kost zit vooral in herladen context",
    kicker: "KOSTEN",
    footer: "OpenClaw voorbeeld + expliciete repo-aannames. $0,377 is reproduceerbare scenario-rekenkunde, geen gemeten Moltbook-trace.",
  });
  addBoostMeUpPanel(slide4, 0.78, 1.38, 4.58, 4.88);
  addPill(slide4, "scenario, geen meting", 1.04, 1.66, 1.66, colors.gold, colors.navy);
  addTextBlock(slide4, "87%", 1.0, 2.2, 3.0, 0.78, {
    size: 42,
    color: colors.red,
    bold: true,
    fontFace: BOOSTMEUP_BRAND.fonts.head,
  });
  addTextBlock(slide4, "van de totale cyclus zit in het herladen van context", 1.02, 3.02, 3.6, 0.6, {
    size: 18,
    bold: true,
  });
  addTextBlock(slide4, "$0,377 per read-reply-post-cyclus op Opus 4.6", 1.02, 4.08, 3.9, 0.34, {
    size: 18,
    color: colors.ink,
    bold: true,
    fontFace: BOOSTMEUP_BRAND.fonts.head,
  });
  addTextBlock(slide4, "Dat bedrag komt uit expliciete aannames in deze repo.", 1.02, 4.56, 3.6, 0.28, {
    size: 12,
    color: colors.muted,
  });
  addBoostMeUpPanel(slide4, 5.66, 1.38, 6.82, 4.88);
  addTextBlock(slide4, "Waar de tokens echt naartoe gaan", 5.96, 1.7, 3.4, 0.24, {
    size: 16,
    bold: true,
    color: colors.ink,
  });
  addMetricBar(slide4, "Context laden (3x)", "60.900", 0.87, 5.96, 2.14, 5.8, colors.red);
  addMetricBar(slide4, "Timeline + reply + post", "8.900", 0.13, 5.96, 2.94, 5.8, colors.gold);
  addMetricBar(slide4, "OpenClaw docs voorbeeld", "~14.250", 0.20, 5.96, 3.74, 5.8, "0F766E");
  addTextBlock(slide4, "Interpretatie", 5.96, 4.52, 1.8, 0.22, {
    size: 14,
    color: colors.red,
    bold: true,
  });
  addTextBlock(slide4, "De kost zit hier niet in één slimme reply. Ze zit in het telkens opnieuw laden van systeemcontext, instructies en geschiedenis.", 5.96, 4.86, 5.9, 0.72, {
    size: 14,
  });
  addTakeawayBand(slide4, "Takeaway: kostdruk is echt; het headline-getal blijft een scenario-uitkomst, geen observatie.", 6.02, "light");
  slide4.addNotes(
    [
      "Zeg hier expliciet dat $0,377 niet uit een Moltbook trace komt.",
      "De sterkste live boodschap is richting, niet precisie: context reload domineert.",
      "[Sources]",
      "- OpenClaw docs voorbeeld voor sessietokens.",
      "- Anthropic pricing voor Opus 4.6.",
      "- Repo-aannames: data/token_usage_assumptions.json.",
    ].join("\n"),
  );

  const slide5 = addBoostMeUpShell(pptx, {
    title: "Sociaal gedrag is nog geen heldere autonomie",
    kicker: "ATTRIBUTIE",
    footer: "Bronnen: Tsinghua-paper 'The Moltbook Illusion' en Moltbook Terms.",
    variant: "dark",
  });
  addTextBlock(slide5, "De data ondersteunt geen eenvoudig verhaal over 'volledig autonome' activiteit.", 0.78, 1.28, 6.5, 0.24, {
    size: 15,
    color: "D7DCE7",
  });
  addStatCard(slide5, "26,5%", "meer autonoom", "van classificeerbare auteurs", 0.78, 1.78, 3.55, "dark", colors.red);
  addStatCard(slide5, "36,8%", "meer menselijk", "van classificeerbare auteurs", 4.58, 1.78, 3.17, "dark", colors.gold);
  addStatCard(slide5, "36,7%", "ambigu", "geen nette toewijzing", 7.98, 1.78, 2.8, "dark", "7DD3FC");
  addBoostMeUpPanel(slide5, 10.98, 1.78, 1.5, 2.0, "dark");
  addTextBlock(slide5, "Terms", 11.18, 2.04, 1.05, 0.18, {
    size: 12,
    color: colors.gold,
    bold: true,
  });
  addTextBlock(slide5, "mens blijft juridisch verantwoordelijk", 11.18, 2.42, 1.05, 0.7, {
    size: 10,
    color: colors.white,
  });
  addBoostMeUpPanel(slide5, 0.78, 4.38, 7.05, 1.6, "dark");
  addTextBlock(slide5, "De les is niet: 'alles is fake'.\nDe les is: attributie is rommelig genoeg dat sterke autonomieclaims te hard zijn.", 1.02, 4.76, 6.4, 0.72, {
    size: 20,
    color: colors.white,
    bold: true,
    fontFace: BOOSTMEUP_BRAND.fonts.head,
  });
  addFramedImage(slide5, asset("assets", "moltbook_terms_eligibility.png"), 8.08, 4.3, 4.4, 1.76, "dark");
  addTakeawayBand(slide5, "Takeaway: Moltbook is een interessant experiment in AI-coördinatie onder zware menselijke governance.", 6.02, "dark");
  slide5.addNotes(
    [
      "Gebruik het woord 'rommelig' bewust. Dat maakt de nuance spreektaal zonder de ernst te verliezen.",
      "Niet afronden naar 27/37/37. Gebruik de paperwaarden.",
      "[Sources]",
      "- Tsinghua paper: The Moltbook Illusion (2026-02-07).",
      "- Moltbook Terms voor de governancekant.",
    ].join("\n"),
  );

  const slide6 = addBoostMeUpShell(pptx, {
    title: "De stevigste signalen zitten in economie en infrastructuur",
    kicker: "TRENDS",
    footer: "Bronnen: Stanford HAI, Epoch en officiële vendor pricing. Methodologische nuance blijft zichtbaar op de slide.",
  });
  addFramedImage(slide6, asset("assets", "ai_trends.png"), 0.78, 1.34, 8.25, 4.96);
  addBoostMeUpPanel(slide6, 9.24, 1.34, 3.49, 4.96, "dark");
  addPill(slide6, "wat dit wél toont", 9.48, 1.64, 1.56, colors.red, colors.white);
  addTextBlock(slide6, "grote benchmarksprongen\n>280x kostdaling\nsterke compute- en efficiencygroei", 9.48, 2.12, 2.8, 1.28, {
    size: 16,
    color: colors.white,
    bold: true,
  });
  addPill(slide6, "wat dit níét zegt", 9.48, 3.78, 1.66, colors.gold, colors.navy);
  addTextBlock(slide6, "niet elke capability-curve blijft netjes exponentieel\nbounded benchmarks kunnen satureren", 9.48, 4.26, 2.82, 0.98, {
    size: 14,
    color: colors.white,
  });
  addTakeawayBand(slide6, "Takeaway: kijk harder naar kosten, compute en efficiency dan naar één spectaculaire scorelijn.", 6.02, "light");
  slide6.addNotes(
    [
      "Deze slide moet snel landen: de harde curves zitten in economie en infrastructuur.",
      "ECI-nuance mondeling meegeven: single benchmarks satureren; daarom bestaan samengestelde kaders.",
      "[Sources]",
      "- Stanford HAI AI Index 2025.",
      "- Epoch trend snapshot en ECI-pagina.",
      "- Vendor pricing snapshots voor de economische context.",
    ].join("\n"),
  );

  const slide7 = addBoostMeUpShell(pptx, {
    title: "MiniMax is vooral een prijsverhaal",
    kicker: "MODELVERGELIJKING",
    footer: "Bronnen: officiële MiniMax- en Anthropic-pagina's. Vendor-reported, geen neutrale matched eval sheet.",
    variant: "dark",
  });
  addBoostMeUpPanel(slide7, 0.78, 1.42, 5.4, 3.12, "dark");
  addPill(slide7, "officiële list prices", 1.02, 1.7, 1.72, colors.red, colors.white);
  addTextBlock(slide7, "16,7x goedkoper op input\n20,8x goedkoper op output", 1.02, 2.24, 4.8, 0.96, {
    size: 26,
    color: colors.gold,
    bold: true,
    fontFace: BOOSTMEUP_BRAND.fonts.head,
  });
  addTextBlock(slide7, "MiniMax M2.7: $0,30 / $1,20\nClaude Opus 4.6: $5 / $25", 1.02, 3.38, 3.4, 0.62, {
    size: 14,
    color: colors.white,
  });
  addBoostMeUpPanel(slide7, 6.4, 1.42, 6.33, 3.12, "dark");
  addPill(slide7, "zelfde benchmark, smallere gap", 6.64, 1.7, 2.28, colors.gold, colors.navy);
  addTextBlock(slide7, "Terminal Bench", 6.64, 2.28, 2.0, 0.2, {
    size: 13,
    color: "D7DCE7",
    bold: true,
  });
  addTextBlock(slide7, "57,0%", 6.64, 2.62, 1.7, 0.46, {
    size: 28,
    color: colors.white,
    bold: true,
    fontFace: BOOSTMEUP_BRAND.fonts.head,
  });
  addTextBlock(slide7, "MiniMax M2.7", 6.64, 3.08, 1.7, 0.18, {
    size: 11,
    color: "D7DCE7",
  });
  addTextBlock(slide7, "65,4%", 9.18, 2.62, 1.7, 0.46, {
    size: 28,
    color: colors.gold,
    bold: true,
    fontFace: BOOSTMEUP_BRAND.fonts.head,
  });
  addTextBlock(slide7, "Claude Opus 4.6", 9.18, 3.08, 1.8, 0.18, {
    size: 11,
    color: "D7DCE7",
  });
  addTextBlock(slide7, "MMClaw-verwijzing bij MiniMax gaat over Sonnet 4.6, niet Opus 4.6.", 6.64, 3.72, 5.3, 0.32, {
    size: 12,
    color: "D7DCE7",
  });
  addTakeawayBand(slide7, "Takeaway: de prijskloof is duidelijker dan de kwaliteitskloof.", 4.86, "dark");
  addBoostMeUpPanel(slide7, 0.78, 5.72, 11.95, 0.6, "dark");
  addTextBlock(slide7, "Veilige podiumframing: uitzonderlijk goedkoop en op sommige agentic/coding taken competitief. Niet: 'in wezen gelijk aan Opus'.", 1.0, 5.92, 11.4, 0.2, {
    size: 12,
    color: colors.white,
  });
  slide7.addNotes(
    [
      "Behoud exact de betekenis van de safe line: de prijskloof is duidelijker dan de kwaliteitskloof.",
      "Zeg ook expliciet dat dit vendor-reported blijft.",
      "[Sources]",
      "- MiniMax model page en pricing docs voor M2.7.",
      "- Anthropic Opus 4.6 page.",
      "- Gebruik geen parity-taal.",
    ].join("\n"),
  );

  const slide8 = addBoostMeUpShell(pptx, {
    title: "Vooruitblik: nuttig als scenario-tool",
    kicker: "VOORUITBLIK",
    footer: "Monte Carlo barrier model met expliciete aannames. Geen deterministische voorspelling.",
  });
  addTextBlock(slide8, "Niet vragen: welk jaar belooft dit model?\nWel vragen: welke aannames duwen de uitkomst echt?", 0.78, 1.3, 6.2, 0.54, {
    size: 20,
    color: colors.ink,
    bold: true,
    fontFace: BOOSTMEUP_BRAND.fonts.head,
  });
  addStatCard(slide8, "28,1%", "basisscenario tegen 2040", "kans op crossing", 0.78, 2.1, 3.35, "light", colors.red);
  addStatCard(slide8, "2038", "mediaan in basisscenario", "geen datum-belofte", 4.34, 2.1, 2.8, "light", colors.gold);
  addStatCard(slide8, "71,9%", "crosst niet tegen 2040", "onder huidige aannames", 7.36, 2.1, 3.24, "light", "0F766E");
  addBoostMeUpPanel(slide8, 10.84, 2.1, 1.89, 2.0);
  addTextBlock(slide8, "label", 11.06, 2.34, 1.2, 0.16, {
    size: 10,
    color: colors.muted,
    bold: true,
  });
  addTextBlock(slide8, "assumptie-gedreven", 11.06, 2.66, 1.2, 0.52, {
    size: 15,
    color: colors.red,
    bold: true,
  });
  addBoostMeUpPanel(slide8, 0.78, 4.52, 11.95, 1.46, "dark");
  addTextBlock(slide8, "Belangrijkste modelinzicht", 1.02, 4.82, 2.6, 0.2, {
    size: 14,
    color: colors.gold,
    bold: true,
  });
  addTextBlock(slide8, "In deze parameterisatie binden floors eerder dan de headline threshold. Dus memory, reliability, network en governance wegen zwaarder dan één headline-getal.", 1.02, 5.16, 10.8, 0.5, {
    size: 16,
    color: colors.white,
  });
  addPill(slide8, "memory", 1.02, 5.62, 0.9, colors.red, colors.white);
  addPill(slide8, "reliability", 2.02, 5.62, 1.02, colors.gold, colors.navy);
  addPill(slide8, "network", 3.16, 5.62, 0.92, "0F766E", colors.white);
  addPill(slide8, "governance", 4.18, 5.62, 1.12, "2563EB", colors.white);
  addTakeawayBand(slide8, "Takeaway: gebruik dit model om onzekerheid te ordenen, niet om 2038 als lot uit te spreken.", 6.08, "light");
  slide8.addNotes(
    [
      "Deze slide mag bewust minder spreadsheet-achtig zijn dan vroeger.",
      "De nuance blijft: scenario-tool, geen profetie.",
      "[Sources]",
      "- Forecast code en inputs: analyses/forecast_model.py en data/forecast_scenarios.json.",
      "- Belangrijke audituitkomst: floors binden vóór de headline threshold.",
    ].join("\n"),
  );

  const slide9 = addBoostMeUpShell(pptx, {
    title: "Wat nog ontbreekt voor een echte agentsamenleving",
    kicker: "SYNTHESE",
    footer: "Synthese van gecontroleerde bevindingen; deze slide introduceert geen nieuwe cijfers.",
    variant: "dark",
  });
  addTextBlock(slide9, "Dit zijn geen randvoorwaarden. Dit zijn de bottlenecks.", 0.78, 1.28, 6.0, 0.24, {
    size: 15,
    color: "D7DCE7",
  });
  const cardY = 1.76;
  const cardW = 2.75;
  addBoostMeUpPanel(slide9, 0.78, cardY, cardW, 4.55, "dark");
  addBoostMeUpPanel(slide9, 3.79, cardY, cardW, 4.55, "dark");
  addBoostMeUpPanel(slide9, 6.8, cardY, cardW, 4.55, "dark");
  addBoostMeUpPanel(slide9, 9.81, cardY, cardW, 4.55, "dark");
  addTextBlock(slide9, "Identiteit", 1.02, 2.04, 2.0, 0.24, {
    size: 18,
    color: colors.gold,
    bold: true,
    fontFace: BOOSTMEUP_BRAND.fonts.head,
  });
  addTextBlock(slide9, "Wie is echt autonoom?\nWie is hybrid?\nWie blijft juridisch de actor?", 1.02, 2.54, 2.0, 1.1, {
    size: 14,
    color: colors.white,
  });
  addTextBlock(slide9, "Zonder heldere attributie blijft 'agentsamenleving' retoriek.", 1.02, 4.82, 2.12, 0.62, {
    size: 12,
    color: "D7DCE7",
  });

  addTextBlock(slide9, "Geheugen", 4.03, 2.04, 2.0, 0.24, {
    size: 18,
    color: colors.gold,
    bold: true,
    fontFace: BOOSTMEUP_BRAND.fonts.head,
  });
  addTextBlock(slide9, "Minder context herladen\nMeer persistente state\nBetere continuïteit over sessies", 4.03, 2.54, 2.0, 1.1, {
    size: 14,
    color: colors.white,
  });
  addTextBlock(slide9, "Anders blijft 'autonomie' vooral reconstructiewerk per run.", 4.03, 4.82, 2.12, 0.62, {
    size: 12,
    color: "D7DCE7",
  });

  addTextBlock(slide9, "Governance", 7.04, 2.04, 2.0, 0.24, {
    size: 18,
    color: colors.gold,
    bold: true,
    fontFace: BOOSTMEUP_BRAND.fonts.head,
  });
  addTextBlock(slide9, "Controle moet matchen\nmet aansprakelijkheid\nén met echte beslissingsmacht", 7.04, 2.54, 2.0, 1.1, {
    size: 14,
    color: colors.white,
  });
  addTextBlock(slide9, "Mensen juridisch laten opdraaien voor schijn-autonomie houdt niet lang stand.", 7.04, 4.82, 2.18, 0.72, {
    size: 12,
    color: "D7DCE7",
  });

  addTextBlock(slide9, "Economics", 10.05, 2.04, 2.0, 0.24, {
    size: 18,
    color: colors.gold,
    bold: true,
    fontFace: BOOSTMEUP_BRAND.fonts.head,
  });
  addTextBlock(slide9, "Unit economics voorbij demo's\nGoedkopere loops\nMinder contextwaste", 10.05, 2.54, 2.0, 1.1, {
    size: 14,
    color: colors.white,
  });
  addTextBlock(slide9, "Zonder kostdiscipline blijft sociale schaal vooral theater.", 10.05, 4.82, 2.12, 0.62, {
    size: 12,
    color: "D7DCE7",
  });
  slide9.addNotes("Dit is de payoff-slide: vier bottlenecks, geen bijzaken.");

  const slide10 = addBoostMeUpShell(pptx, {
    title: "Moltbook is een signaal. Nog geen bewijs.",
    kicker: "SLOT",
    footer: "Native .pptx build via bun + PptxGenJS. Rebuild met: bun run build:deck",
    variant: "dark",
  });
  addTextBlock(slide10, "De juiste vraag is niet of de demo sociaal oogt.", 0.78, 1.62, 11.0, 0.54, {
    size: 26,
    color: colors.white,
    bold: true,
    fontFace: BOOSTMEUP_BRAND.fonts.head,
    align: "center",
  });
  addTextBlock(slide10, "De juiste vraag is of identiteit, geheugen, governance en kost standhouden zodra je schaal en verantwoordelijkheid serieus neemt.", 1.14, 2.48, 10.3, 0.98, {
    size: 24,
    color: colors.gold,
    bold: true,
    fontFace: BOOSTMEUP_BRAND.fonts.head,
    align: "center",
  });
  addBoostMeUpPanel(slide10, 1.06, 4.18, 11.2, 1.1, "dark");
  addTextBlock(slide10, "Onthoud dit", 1.38, 4.5, 1.4, 0.2, {
    size: 14,
    color: colors.gold,
    bold: true,
  });
  addTextBlock(slide10, "Agentnetwerken zijn technisch indrukwekkend. Maar de geloofwaardigheid zit pas in wat standhoudt onder identiteit, governance en economie.", 1.38, 4.82, 10.2, 0.34, {
    size: 15,
    color: colors.white,
    align: "center",
  });
  addBoostMeUpPanel(slide10, 1.06, 5.56, 11.2, 0.76, "dark");
  addTextBlock(slide10, "Gespreksvragen: welke delen van uw agentstack worden vandaag nog telkens gereconstrueerd? Waar breekt governance eerst? Welke cijfers zijn gemeten, en welke zijn nog scenario-aannames?", 1.3, 5.82, 10.7, 0.2, {
    size: 11,
    color: "D7DCE7",
    align: "center",
  });
  slide10.addNotes(
    [
      "Laat deze slide rustig landen. Niet te snel naar de vragen springen.",
      "Slotzin: het gaat niet om sociale schijn, maar om wat standhoudt onder schaal en verantwoordelijkheid.",
    ].join("\n"),
  );
}

async function main(): Promise<void> {
  buildSlides();
  mkdirSync(asset("release"), { recursive: true });
  await pptx.writeFile({ fileName: asset("release", "Moltbook.pptx") });
  console.log("Saved deck: release/Moltbook.pptx");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
