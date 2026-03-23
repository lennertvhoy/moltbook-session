# Slide System Decision

## Decision

Use **PptxGenJS** as the production slide pipeline.

Keep Markdown only as a human-readable outline and speaker-note aid.

## Why the old workflow lost

The old repo state effectively treated Markdown as the main slide source, but the actual binary deck artifacts were already drifting away from the Markdown.

That failed on the key criteria:

- weak evidence of deterministic deck generation
- poor alignment between source and output
- hard to enforce citations, notes, and layout consistency
- no clear native editable PowerPoint path

## Comparison Matrix

| Option | Reproducibility | Visual control | Native `.pptx` | Notes support | Deterministic assets | Portability | Fit for this repo |
|---|---|---|---|---|---|---|---|
| Legacy Markdown workflow | Weak in current repo | Medium | No | Varies | Weak | Medium | Lost because source/output drift already happened |
| PptxGenJS | Strong | Strong | Yes | Yes | Strong | Strong for conference decks | Best fit |
| reveal.js | Strong | Strong for web | No | Presenter notes yes | Strong | Strong for web talks | Good alternative, not best here |
| Slidev / Marp | Medium to strong | Medium | Usually export-oriented, not native | Medium | Strong | Good for markdown-first teams | Easier, but lower control for this talk |

## Why PptxGenJS Wins

- native editable `.pptx` output
- deterministic build from code
- good support for images, text, tables, and speaker notes
- easier to keep citations and footer text consistent
- better fit for a branded conference deck than a markdown-first workflow

## Implemented Result

- added [package.json](../../package.json)
- added `bun` lockfile
- added [scripts/build_deck.ts](../../scripts/build_deck.ts)
- `bun run build:deck` now rebuilds [release/Moltbook.pptx](../../release/Moltbook.pptx)

## Build Commands

```bash
BUN_TMPDIR=/tmp BUN_INSTALL_CACHE_DIR=.bun-cache bun install
BUN_TMPDIR=/tmp BUN_INSTALL_CACHE_DIR=.bun-cache bun run build:deck
```

## Markdown's New Role

Markdown still has value here, but a narrower value:

- outline and speaker-note source
- repo-readable narrative draft
- audit-friendly text review

It is no longer the production deck system.
