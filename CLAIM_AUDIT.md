# Claim Audit

| Claim text | Location | Source(s) | Verification status | Reproduction status | Action taken | Notes |
|---|---|---|---|---|---|---|
| Moltbook is "A Social Network for AI Agents" and humans may observe | Slide 2, `content/01-intro.md` | Moltbook homepage | Verified | Source-supported, not code-derived | Kept | Directly supported by homepage copy |
| Moltbook Terms deny legal eligibility to AI agents and keep responsibility with the human owner | Slide 2, `content/04-kritiek.md` | Moltbook Terms of Service | Verified | Source-supported, not code-derived | Kept | Strong primary-source support |
| OpenClaw treats context as everything sent to the model for a run | Slide 3, `content/03-agents-md.md` | OpenClaw docs | Verified | Source-supported, not code-derived | Kept | Core architectural framing |
| Multi-agent OpenClaw setups use per-agent sandbox and tool policies | Slide 3, `content/02-ai-agents.md` | OpenClaw multi-agent docs | Verified | Source-supported, not code-derived | Kept | Good support for "agent network" system framing |
| One social cycle costs about $0.38 on Claude Opus 4.6 | Slide 4, `content/03-agents-md.md` | OpenClaw docs anchor, Anthropic pricing, repo assumptions | Reframed | Reproduced from code but assumption-driven | Narrowed | Now explicitly labeled illustrative, not measured |
| Moltbook identity claims are shaky because author activity is mixed across autonomous-leaning, human-leaning, and ambiguous categories | Slide 5, `content/04-kritiek.md` | Tsinghua paper | Verified | Source-supported, not code-derived | Kept | Replaced rounded repo percentages with paper values |
| Frontier capability and efficiency trends are moving fast | Slide 6, `content/05-trends.md` | Stanford HAI, Epoch | Verified | Reproduced from source-backed data file | Kept | Strongest trend claim preserved |
| Stanford HAI reports >280x decline in cost to reach GPT-3.5-level quality between Nov 2022 and Oct 2024 | Slide 6, `content/05-trends.md` | Stanford HAI | Verified | Reproduced from normalized endpoints in code | Kept | Now visualized as a normalized derived curve |
| ECI uses exactly 37 benchmarks | Old slides and notes | Epoch ECI page | Ambiguous / source mismatch | Not directly reproduced | Rewritten | Deck now says "dozens of benchmarks" because Epoch page is internally inconsistent |
| MiniMax M2.7 is ~19x cheaper than Claude Opus 4.6 with only ~6% lower quality | Old deck only | Artificial Analysis claim intended but not aligned | Unsupported / source mismatch | Not reproduced | Removed | Current model/version comparison could not support this precision |
| The forecast median is 2038 in the base case | Slide 8, `content/06-forecast.md` | Repo forecast code | Verified | Reproduced from code | Kept with caveat | Now explicitly labeled assumption-driven |
| Threshold changes alone move the forecast substantially | Old implied framing | Repo forecast model | Not supported in current parameterization | Reproduced and contradicted | Rewritten | Floors bind before the headline threshold in current setup |
| Moltbook proves autonomous digital society is already here | Old rhetorical framing | None | Unsupported | Not applicable | Removed | Replaced with narrower thesis |
