import path from "node:path";

import PptxGenJS from "pptxgenjs";

const root = path.resolve(import.meta.dir, "..");

export const BOOSTMEUP_BRAND = {
  colors: {
    navy: "12192C",
    white: "FFFFFF",
    red: "E93325",
    gold: "F2AD18",
    textDark: "12192C",
    textMuted: "5B6476",
    lineLight: "D9DDE6",
    panelLight: "F7F8FB",
  },
  fonts: {
    head: "Aptos Display",
    body: "Aptos",
  },
  logos: {
    full: path.join(root, "assets", "brand", "boostmeup-logo.png"),
    mark: path.join(root, "assets", "brand", "boostmeup-mark.png"),
  },
} as const;

type ShellVariant = "light" | "dark";

export type ShellOptions = {
  title: string;
  kicker: string;
  footer: string;
  variant?: ShellVariant;
  showFullLogo?: boolean;
};

export function configureBoostMeUpPresentation(pptx: PptxGenJS): void {
  pptx.layout = "LAYOUT_WIDE";
  pptx.author = "OpenAI Codex";
  pptx.company = "BoostMeUp";
  pptx.lang = "nl-BE";
  pptx.theme = {
    headFontFace: BOOSTMEUP_BRAND.fonts.head,
    bodyFontFace: BOOSTMEUP_BRAND.fonts.body,
    lang: "nl-BE",
  };
}

export function addBoostMeUpShell(pptx: PptxGenJS, options: ShellOptions): PptxGenJS.Slide {
  const slide = pptx.addSlide();
  const variant = options.variant ?? "light";
  const isDark = variant === "dark";
  const bg = isDark ? BOOSTMEUP_BRAND.colors.navy : BOOSTMEUP_BRAND.colors.white;
  const ink = isDark ? BOOSTMEUP_BRAND.colors.white : BOOSTMEUP_BRAND.colors.textDark;
  const muted = isDark ? "D7DCE7" : BOOSTMEUP_BRAND.colors.textMuted;

  slide.background = { color: bg };

  slide.addShape(pptx.ShapeType.rect, {
    x: 0,
    y: 0,
    w: 13.333,
    h: 0.18,
    line: { color: BOOSTMEUP_BRAND.colors.red, transparency: 100 },
    fill: { color: BOOSTMEUP_BRAND.colors.red },
  });
  slide.addShape(pptx.ShapeType.rect, {
    x: 10.6,
    y: 0.18,
    w: 2.733,
    h: 0.08,
    line: { color: BOOSTMEUP_BRAND.colors.gold, transparency: 100 },
    fill: { color: BOOSTMEUP_BRAND.colors.gold },
  });

  if (options.showFullLogo) {
    slide.addImage({
      path: BOOSTMEUP_BRAND.logos.full,
      x: 0.62,
      y: 0.42,
      w: 2.45,
      h: 1.3,
      transparency: 0,
    });
  } else {
    slide.addImage({
      path: BOOSTMEUP_BRAND.logos.mark,
      x: 12.15,
      y: 0.42,
      w: 0.54,
      h: 0.92,
      transparency: 0,
    });
  }

  slide.addText(options.kicker, {
    x: options.showFullLogo ? 3.35 : 0.78,
    y: 0.46,
    w: options.showFullLogo ? 7.5 : 8.6,
    h: 0.2,
    fontFace: BOOSTMEUP_BRAND.fonts.body,
    fontSize: 9,
    color: isDark ? BOOSTMEUP_BRAND.colors.gold : BOOSTMEUP_BRAND.colors.red,
    bold: true,
    charSpace: 0.5,
    margin: 0,
  });

  slide.addText(options.title, {
    x: 0.78,
    y: options.showFullLogo ? 1.6 : 0.72,
    w: 10.8,
    h: options.showFullLogo ? 0.9 : 0.7,
    fontFace: BOOSTMEUP_BRAND.fonts.head,
    fontSize: options.showFullLogo ? 26 : 23,
    bold: true,
    color: ink,
    margin: 0,
    fit: "shrink",
  });

  slide.addShape(pptx.ShapeType.line, {
    x: 0.78,
    y: 6.96,
    w: 11.9,
    h: 0,
    line: { color: isDark ? "394258" : BOOSTMEUP_BRAND.colors.lineLight, pt: 1 },
  });
  slide.addText(options.footer, {
    x: 0.78,
    y: 7.0,
    w: 11.9,
    h: 0.18,
    fontFace: BOOSTMEUP_BRAND.fonts.body,
    fontSize: 8,
    color: muted,
    margin: 0,
    fit: "shrink",
  });

  return slide;
}

export function addBoostMeUpPanel(
  slide: PptxGenJS.Slide,
  x: number,
  y: number,
  w: number,
  h: number,
  variant: ShellVariant = "light",
): void {
  const isDark = variant === "dark";
  slide.addShape("roundRect", {
    x,
    y,
    w,
    h,
    rectRadius: 0.06,
    fill: { color: isDark ? "1C2540" : BOOSTMEUP_BRAND.colors.panelLight },
    line: { color: isDark ? "394258" : BOOSTMEUP_BRAND.colors.lineLight, pt: 1 },
  });
}

export function addBoostMeUpBodyText(
  slide: PptxGenJS.Slide,
  lines: string[],
  x: number,
  y: number,
  w: number,
  h: number,
  variant: ShellVariant = "light",
): void {
  slide.addText(
    lines.map((line) => ({ text: line, options: { breakLine: true } })),
    {
      x,
      y,
      w,
      h,
      fontFace: BOOSTMEUP_BRAND.fonts.body,
      fontSize: 16,
      color: variant === "dark" ? BOOSTMEUP_BRAND.colors.white : BOOSTMEUP_BRAND.colors.textDark,
      breakLine: false,
      margin: 0,
      valign: "top",
      fit: "shrink",
    },
  );
}

export function addBoostMeUpQuote(
  slide: PptxGenJS.Slide,
  text: string,
  x: number,
  y: number,
  w: number,
  variant: ShellVariant = "light",
): void {
  slide.addText(text, {
    x,
    y,
    w,
    h: 0.7,
    fontFace: BOOSTMEUP_BRAND.fonts.body,
    fontSize: 18,
    italic: true,
    color: variant === "dark" ? BOOSTMEUP_BRAND.colors.gold : BOOSTMEUP_BRAND.colors.red,
    margin: 0,
    fit: "shrink",
  });
}

export function addBoostMeUpImage(
  slide: PptxGenJS.Slide,
  imagePath: string,
  x: number,
  y: number,
  w: number,
  h: number,
): void {
  slide.addImage({ path: path.resolve(imagePath), x, y, w, h });
}
