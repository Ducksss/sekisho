# Public website deployment

Published 26 September 2026 at **https://sekisho-phi.vercel.app**.
Vercel project `sekisho`, account scope `ducksss-projects`, source directory `website/`.

The user selected a public landing page with GitHub and setup links. This release is
static project information, original brand artwork, and clearly labelled fixture
screenshots. It does not deploy the Python gate, Next.js console, contracts, payment
keys, or an interactive mock payment service. Live-stack readiness remains in
[readiness.md](readiness.md).

## Verification

- Desktop and 390×844 mobile rendered in Chromium. No horizontal document overflow;
  mobile artwork was adjusted to sit below the copy and actions.
- Section navigation, screenshot enlargement links, and keyboard-operated FAQ work.
- One h1 per page; image alt text and dimensions; local asset and fragment targets checked.
- Static design audit: 0 errors, 0 warnings. No runtime JavaScript or dependency build.
- Vercel dry-run reviewed: static website files only; `.env.local` and `.vercel/` excluded.
- Public production `/`, stylesheet, hero, screenshots, social card, and font returned
  HTTP 200 and matched source bytes without authentication. Custom missing-page route
  returned HTTP 404 and the Sekisho recovery page.
- The source and existing app tests are separate: no gate/contract/SDK behavior changed
  in this release, so their earlier test runs were not repeated for static publication.

## Operations

Use the commands in [website/README.md](../website/README.md) to preview and redeploy.
CLI deployment is configured; automatic Git deployment has not been enabled. No
custom domain, paid upgrade, analytics, or external form submission was added.
