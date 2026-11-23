# APICompat — Intelligent API Breaking-Change Verification

## Project summary

APICompat helps API publishers and integration owners verify whether an update preserves documented compatibility. It locks OpenAPI specifications, release notes and a compatibility policy before review. A GenLayer Intelligent Contract detects supported structural breaks deterministically; independent validators assess behavioral changes such as pagination, defaults and error semantics. Exact commit-pinned evidence, grounded quotations and hash-linked receipts make the decision reproducible and auditable. Unavailable sources, unsupported constructs and weak evidence produce INCONCLUSIVE rather than false assurance.

## Why GenLayer is central

A schema-only tool misses semantic changes; a single publisher-controlled model cannot resolve a trust dispute. Every accepted behavioral assessment requires independent GenLayer validator reasoning against the locked artifacts. The contract owns lifecycle authorization, structural precedence, conservative outcomes and append-only receipts. The website directly reads it and provides signed-write integration plus Studio transaction preparation.

## How reviewers can use it

Open the website, choose Reviews & receipts and load a published example. Inspect its locked artifacts, source verification, quoted evidence and locally verified receipt chain. To create a review, choose an example or provide your own OpenAPI JSON, connect MetaMask or prepare calls for the Studio wallet, then create, lock and assess. A second wallet can challenge once; reassessment preserves the first receipt.

- Website: https://apicompat.mohamedansaf222.chatgpt.site
- GitHub: https://github.com/haris4587/APICompat
- Contract explorer: https://explorer-studio.genlayer.com/address/0x755A3a2b8dE98A06E8eB44B541034767A6B47647
- Source: `contracts/apicompat.py`
- Reproducible live evidence: `docs/live-evidence.json`
- Validation scope: `docs/QA.md`

## Scope

This version assesses supplied documentation, not actual server behavior or publisher identity. Its comparator supports a bounded OpenAPI subset, fails conservatively on unresolved references/unsupported changes, and uses synthetic public fixtures for reproducible examples. It includes no financial settlement, production deployment gate, or claim of exhaustive API certification. Actual MetaMask signing was unavailable in the hosted browser; live writes used the Studio inbuilt wallet. No public social posts or contribution form were submitted automatically.

## Short description

APICompat resolves API compatibility disputes using hash-locked OpenAPI specifications, release notes and policies. Its GenLayer contract deterministically detects structural breaks and requires independent AI validators to assess ambiguous behavioral changes with grounded quotations. Commit-pinned evidence, byte/digest verification and append-only hash-linked receipts support reproducible review. Users create, lock, assess, challenge and reassess through a responsive website with wallet integration and Studio signing support. Uncertain evidence and unsupported changes return INCONCLUSIVE. The repository includes tests, security limits and live Studionet transaction evidence.
