# Wallet Audit Trail

An explainable, time-bound screening and audit layer for crypto payments.

## Status

Project initialized from the supplied pitch deck. No application or live integrations have been implemented yet. Technology choices are still open.

## Product concept

Assess an exact payment intent, collect bounded wallet evidence, and return `ALLOW`, `HOLD`, or `DENY` with reasons, coverage, freshness, and policy version. Preserve decisions and corrections in an auditable history.

The proposed MVP includes:

- A wallet screening and evidence dashboard.
- A deterministic payment policy API.
- An audit history and export with correction records.
- A guarded testnet payment flow that checks the intent before signing.

## Source material

[Original pitch deck](docs/pitch-deck.md), copied unchanged from the supplied document. Its integration targets, dates, and submission requirements are proposals from that document and have not been independently verified.

## Initial implementation sequence

1. Define payment intent, assessment, evidence, and audit record schemas.
2. Implement policy evaluation and intent-bound approvals.
3. Add provider and transaction-history adapters.
4. Build screening, evidence, and review views.
5. Connect the guarded testnet payment flow and validate allowed and held paths.

## Proposed MVP boundaries

Ethereum-first, bounded transaction coverage, and testnet payments only. Missing required evidence results in a hold. No detected risk is not a safety guarantee. Synthetic fixtures must be distinguishable from live findings.
