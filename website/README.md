# Sekisho public website

Live: [sekisho-phi.vercel.app](https://sekisho-phi.vercel.app).

Static brand and project-information site, deployed separately from the operational
Next.js console. It makes no gate requests, wallet connections, or payment mutations.
All product screenshots retain their synthetic-fixture labels. The live backend and
contract rehearsal are tracked in [readiness](../docs/readiness.md).

## Preview

From the repository root:

```bash
python3 -m http.server 3112 --bind 127.0.0.1 --directory website
```

Open `http://localhost:3112`. This is static HTML/CSS; there is no dependency installation
or build step. The source assets and font provenance are in [docs/assets](../docs/assets/README.md).

## Deploy

Vercel project: `sekisho`, scope: `ducksss-projects`. Publish only this directory.

```bash
vercel link --project sekisho --scope ducksss-projects --cwd website
vercel deploy --dry --json --cwd website
vercel deploy --prod --scope ducksss-projects --cwd website
```

Inspect the dry-run file list before publishing. `.env*` and `.vercel/` are ignored;
no environment variables or secrets are required by this site. The command creates a
static production deployment. CLI publication does not automatically enable Git-based
redeployment. Keep the Vercel project root set to `website` if Git integration is added.

## Verification

Desktop and 390px mobile layouts reviewed in Chromium; no horizontal overflow.
Verified heading structure, asset paths/dimensions, section anchors, keyboard FAQ,
source/readiness links, and fixture labels. Reduced motion disables smooth scrolling
and transitions; forced colors retain system semantics. Verify production `/`, asset
URLs, and the custom 404 after each deployment.
