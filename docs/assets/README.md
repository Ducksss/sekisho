# Sekisho presentation assets

Brand direction: midnight navy, luminous signal blue, translucent checkpoint imagery,
and tightly set type, distilled from the user-supplied Investflow reference. See
[the full direction brief](../BRAND-DIRECTION.md). Keep the existing checkpoint mark
and clear ALLOW / HOLD / BLOCK labels in the product. The pitch is **“Before the agent signs.”** The companion
one-liner is **“The compliance checkpoint for AI agent payments.”** The console runtime has not been restyled by this package.

| Asset | Use and provenance |
|---|---|
| [logo.svg](logo.svg) | Existing mark from `dashboard/app/icon.svg`, with an accessible label; original project vector artwork |
| [wordmark.svg](wordmark.svg) | Text lockup on a white background, suitable for light or dark README themes |
| [checkpoint-hero.png](checkpoint-hero.png) | Original imagegen illustration: frosted-glass checkpoint and blue payment path |
| [banner.png](banner.png) | 1280×640 repository banner, rendered from [presentation.html](source/presentation.html) |
| [social-preview.png](social-preview.png) | 1280×640 social card with repository address; provided as a file, not configured in GitHub's social-preview setting |
| [console-decisions.png](console-decisions.png) | 1440×1000 actual fixture console: decisions and review queue |
| [console-case.png](console-case.png) | 1440×1000 actual fixture console: held case and officer review |
| [console-treasury.png](console-treasury.png) | 1440×1000 actual fixture console: balances and cumulative exposure |

Screenshots were captured on 26 September 2026 using Chromium against the running
Next.js fixture preview. They retain the fixture warning and simulated values. Only
Next.js developer controls were hidden. Screenshots are neither mockups nor proof of
live screening, settlement, deployed contracts, or measured provider latency.

## Palette and type

The application remains the source of truth: [tokens.css](../../dashboard/app/tokens.css)
and [DESIGN.md](../../DESIGN.md).

| Role | Color |
|---|---|
| Prussian blue | `#1b3f8f` |
| Paper / white | `#edf0f4` / `#ffffff` |
| Ink / secondary text | `#101b2b` / `#4f5b6c` |
| Allow / hold / block | `#0f6e47` / `#8a5700` / `#b42a1a` |

Artwork uses Inter Tight, distributed under SIL Open Font License 1.1 through
`@fontsource-variable/inter-tight` 5.3.0. The Latin variable font and its
[license](source/fonts/OFL.txt) are included for reproducible rendering. The SVG
wordmark uses a system sans-serif fallback. Japanese text uses a system Mincho font.
The original checkpoint illustration was generated using the built-in imagegen tool;
its full prompt is in [prompt 12](../prompts/12-investflow-direction.md). No paid template
artwork or logos were copied. The repository [MIT license](../../LICENSE) covers
original project assets; third-party fonts retain their own license.

## Reproduce

After `npm ci` in `dashboard/`, install or select a local Playwright/Chromium toolchain.
The capture helper is optional documentation tooling, not a runtime dependency.

```bash
# From the repository root; Playwright must be resolvable by Node.
node docs/assets/source/capture.cjs

# With a fixture console already running on port 3000:
CONSOLE_URL=http://localhost:3000 node docs/assets/source/capture.cjs
```

`PLAYWRIGHT_MODULE` can select an existing Playwright package and
`CHROMIUM_EXECUTABLE` can select an installed Chromium executable. The helper refuses
to capture a console without the visible fixture banner. Review regenerated files
before committing; timestamps and simulated streaming data can change between runs.
