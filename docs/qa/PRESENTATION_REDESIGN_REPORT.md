# Presentation Redesign Report

## Executive Summary

This pass turned the verified Moltbook deck into a stronger Dutch live presentation. The analytical posture stayed narrow and source-safe, but the slide surface moved away from report-like layouts toward clearer keynote roles, stronger rhythm, and less on-slide text.

## Design Diagnosis Of The Old Deck

The previous deck had three structural design problems:

1. Slides 2–8 still felt like a verified research document poured into slide boxes.
2. Too many slides relied on the same pattern: title, medium screenshot, medium text block.
3. The presenter-facing language stayed too English and too audit-shaped for a Dutch live talk.

The strongest existing direction was slide 1: darker, more branded, and more event-like. That became the anchor for the redesign.

## What Changed Structurally

- rebuilt slides 2–8 around clearer presentation jobs instead of repeating one layout pattern
- moved several slides from screenshot-led layouts to claim / meaning / caution compositions
- reduced visible text and shifted nuance back into speaker notes
- made dark slides carry synthesis, caution, and closing emphasis
- used light slides where data or contrast benefited from it

## What Changed Visually

- extended the BoostMeUp dark keynote language beyond the title slide
- added stronger cards, stat blocks, takeaway bands, and pill labels
- removed the generic “grey document panel” feel as the default pattern
- simplified the trend visual into a more presentation-readable chart
- improved the preview renderer so QA can reflect dark slide backgrounds more honestly

## What Changed Linguistically For Dutch Delivery

- translated the slide surface into Dutch
- removed or reduced English audit phrasing on the slide surface
- tightened titles into shorter spoken-stage language
- kept English only where the original source phrase itself matters

Important preserved line:

> De prijskloof is duidelijker dan de kwaliteitskloof.

That keeps the exact meaning of the verified English framing.

## Slide-By-Slide Improvements

### Slide 1

- kept the dark branded anchor
- tightened the title into a stronger Dutch opening
- made the thesis more stage-like and less repo-like

### Slide 2

- replaced “source screenshot plus explanation” with a clearer claims-versus-limits contrast
- made the legal tension visually explicit

### Slide 3

- replaced documentation-dump energy with a simplified architectural reading
- kept the source anchor in notes and with a small visual reference

### Slide 4

- made scenario-versus-measurement explicit through layout, not just caveat text
- foregrounded the context-reload burden instead of a dense multi-panel chart

### Slide 5

- turned autonomy uncertainty into memorable stat cards
- made the conclusion legible in seconds

### Slide 6

- simplified the trend figure for live readability
- pushed the cautious interpretation into a clear side panel and takeaway band

### Slide 7

- turned the MiniMax slide into a crisp price-versus-quality framing
- preserved caution without making the slide defensive

### Slide 8

- reduced spreadsheet energy
- kept the forecast as a scenario tool with visible methodological restraint
- emphasized floor constraints as the real model lesson

### Slide 9

- sharpened the synthesis into four bottleneck cards
- made the payoff more keynote-like

### Slide 10

- strengthened the Dutch closing thesis
- demoted discussion prompts beneath the final takeaway

## Tradeoffs Between Punch And Caution

1. The trend slide stays more restrained than a hype deck because bounded-benchmark caution remains visible.
2. The MiniMax slide foregrounds price and keeps quality caveats explicit rather than chasing a harder comparison headline.
3. The forecast slide became less data-dense on purpose so the audience remembers the methodological lesson instead of a pseudo-precise date.

## Files Changed

- [scripts/build_deck.ts](../../scripts/build_deck.ts)
- [scripts/export_slide_previews.py](../../scripts/export_slide_previews.py)
- [analyses/ai_trends.py](../../analyses/ai_trends.py)
- [slides/slides-main.md](../../slides/slides-main.md)
- [assets/ai_trends.png](../../assets/ai_trends.png)
- [release/Moltbook.pptx](../../release/Moltbook.pptx)
- [docs/qa/previews/contact-sheet.png](previews/contact-sheet.png)

## Exact Commands Run

```bash
MPLCONFIGDIR=/tmp/matplotlib UV_CACHE_DIR=.uv-cache uv run analyses/ai_trends.py
BUN_TMPDIR=/tmp BUN_INSTALL_CACHE_DIR=.bun-cache bun run build:deck
UV_CACHE_DIR=.uv-cache uv run scripts/export_slide_previews.py
```

## Clean-Worktree Proof

At handoff, the intended proof standard is:

- the deck has been rebuilt
- previews have been regenerated
- the redesign changes are committed
- `git status --short` is clean
