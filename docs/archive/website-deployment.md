# Public website deployment

Published 26 September 2026 at **https://getsekisho.vercel.app**.
Vercel project `sekisho`, account scope `ducksss-projects`, source directory `website/`.

The user selected a public landing page with GitHub and setup links. This release is
static project information, original brand artwork, clearly labelled fixture
screenshots, and a browser-only guided simulation. The simulation shows four fixed
synthetic scenarios plus simulated release/refund; it never calls a screening provider
or creates a signature, attestation, or payment. A tested SDK example is shown and
available to copy/download. It does not deploy the Python gate, Next.js console, contracts, payment
keys, or an interactive mock payment service. Live-stack readiness remains in
[readiness.md](readiness.md).

## Verification

- Desktop and 390×844 mobile rendered in Chromium. No horizontal document overflow;
  mobile artwork was adjusted to sit below the copy and actions.
- Section navigation, screenshot enlargement links, and keyboard-operated FAQ work.
- One h1 per page; image alt text and dimensions; local asset and fragment targets checked.
- Console static design audit: 0 errors, 0 warnings. The website audit reports eight
  actionless-button false positives because it does not resolve native module event
  listeners; the eight enabled buttons are wired in `demo.mjs` and browser-verified.
  Native JavaScript modules require no framework build.
- Vercel dry-run reviewed: static website files only; `.env.local` and `.vercel/` excluded.
- Public production `/`, stylesheet, hero, screenshots, social card, and font returned
  HTTP 200 and matched source bytes without authentication. Custom missing-page route
  returned HTTP 404 and the Sekisho recovery page.
- All 54 SDK tests (including seven example tests) and three walkthrough state tests pass. The source/example
  generation check passes. Console lint and production build pass after token changes.
  Gate policy, contracts, and payment execution code were not changed.

## Operations

Use the commands in [website/README.md](../website/README.md) to preview and redeploy.
Automatic Git deployment was enabled on 26 September 2026. Vercel is connected to
`Ducksss/sekisho`, with `main` as the production branch and `website` as the project
root. Pushes to `main` publish the public site after a successful deployment; other
branches create preview deployments. The project is on a Hobby team, which only builds
commits its owner authored, so during the event a `vercel-deploy.yml` workflow got
teammates' pushes to `main` deployed by committing a timestamped note under
`.github/deploys/` as the owner. The repository went public on 1 October 2026, which lets
Hobby build collaborators' commits directly, so the workflow and its notes were removed.
Automatic production domain assignment is enabled, and no ignored-build command is
configured. No paid upgrade, analytics, or external form submission was added.
