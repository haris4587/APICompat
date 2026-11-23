# Verification scope

## Automated verification

- **36 contract tests** pass with explicit GenVM, network and model doubles.
- **15 frontend/client tests** pass for canonical bytes, hashes, receipt chains, HTML escaping, wallet adapter behavior, signature rejection, accepted/finalized separation, reverts, unavailable execution proof, consensus failure and pending timeout.
- Production Vite build passes.
- GitHub Actions `Verify` completed successfully for the implementation commit. The final source is also validated locally before publication.
- `npm run verify:live` checks the deployed code against the exact source, the seven-method schema, recorded finalized transactions, expected verdicts, source bytes/digests and complete receipt hash chains. The reproducible result is in `live-evidence.json`.

Local model doubles are not a claim of real consensus. Live verification is recorded separately.

## Live workflow

The release contract uses GenLayer Studionet, chain ID 61999, Normal (Full Consensus). Live cases include:

| Case | Expected outcome | Purpose |
| --- | --- | --- |
| Optional trace parameter, explicit preservation of behavior | COMPATIBLE | Independent semantic reasoning and grounded quotations |
| Cursor pagination replaced with page-number pagination | BREAKING | Behavioral incompatibility despite stable response shapes |
| Changed schema composition outside the supported subset | INCONCLUSIVE | Conservative unsupported-change handling |
| Independent challenge and reassessment | New linked receipt | Append-only history and challenger authorization |

Deployment, creation, locking, assessment, challenge and reassessment transaction hashes are listed in `../public/deployment.json` and verified in `live-evidence.json`. The submitting wallet is `0x67Da51Fd9AC1d52F34F5d01d06da8548979fC514`; the challenger is a different Studio account, `0xcD72fA5B6A496d84B4A10bCFF31D3B7c12346a9e`.

## Browser verification

Observed in the hosted Chrome browser:

- Website layout, example selection and form fields render correctly on desktop.
- Live contract read loads a finalized receipt with its exact quotation, source-verification state and locally verified chain.
- The unavailable-MetaMask path produces an actionable error, without claiming a wallet connection.
- Studio call preparation displays exact named arguments and a SHA-256 review ID matching the test fixture. Prepared values were executed through Studio and read back through the website.
- Public site access is enabled for reviewers. The final website URL is in the README.

## Limits

Actual MetaMask extension signing was **not** tested: the hosted browser has no MetaMask provider. Signing used the Studio inbuilt wallet. Direct-wallet writes, rejection handling and transaction polling are implemented and covered by adapter/lifecycle tests, not falsely reported as an extension-signed browser test. Mobile CSS is implemented; phone-device emulation was not completed. No live external production API was certified; fixtures are synthetic and published at immutable repository commits.
