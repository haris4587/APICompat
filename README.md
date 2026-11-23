# APICompat

**Ship the update. Keep the promise.** APICompat helps API publishers and integration owners resolve compatibility disputes using fixed evidence, deterministic checks, independent GenLayer reasoning, and immutable receipts.

- [Website](https://apicompat.mohamedansaf222.chatgpt.site)
- [Studionet contract](https://explorer-studio.genlayer.com/address/0xfbf25Bae6d94E20A6bDB13096D7927225eAA1d83)
- [Live evidence](docs/live-evidence.json) · [Submission notes](SUBMISSION.md) · [Security](SECURITY.md) · [Deployment](DEPLOYMENT.md)

## The trust problem

A schema diff can identify a new required parameter, but it cannot determine whether “pagination has been simplified” invalidates existing client assumptions. A publisher’s own LLM summary also leaves integration owners relying on the publisher’s judgment. APICompat locks the comparison material and policy before assessment. GenLayer validators independently evaluate the same evidence rather than accepting a single model’s formatted response.

The product evaluates **documented compatibility**, not actual implementation behavior. Published bytes establish provenance and reproducibility; they do not prove the submitter owns the API or that release notes tell the truth.

## Use the website

1. Choose a synthetic example or upload/paste baseline and candidate OpenAPI JSON. Supply release notes and a compatibility policy.
2. Connect MetaMask on Studionet, or choose **Prepare Studio calls** to sign with GenLayer Studio’s inbuilt wallet.
3. Create the review. Its ID is the SHA-256 of the exact serialized bundle. The evidence cannot be edited.
4. Lock it with the submitting wallet, then request assessment.
5. Load the review to inspect quotations, structural findings, source verification, and locally verified receipt hashes.
6. An independent wallet can challenge once with a 30–2000 character explanation. Reassessment appends a receipt and preserves all previous decisions.

The browser directly uses `genlayer-js` for contract reads and signed writes. It displays signature requests, submission hashes, consensus status, acceptance, finalization, execution failures and timeouts. Pending hashes survive reloads. Acceptance is not treated as finality. Studio mode prepares the exact method arguments and requires signing in Studio; it does not pretend to possess the Studio private key.

**MetaMask availability:** wallet adapter and transaction lifecycle behavior are tested with provider doubles. Actual MetaMask extension signing is not verified in the hosted test browser. Live writes and full consensus were exercised using the Studio inbuilt wallet. See `docs/QA.md` for the precise verification scope.

## Contract decisions

| Outcome | Conditions |
| --- | --- |
| BREAKING | Verified artifacts contain a supported structural incompatibility, or independent semantic review establishes incompatible behavior under the locked policy. |
| COMPATIBLE | Supported structural checks pass and independent semantic review finds positive evidence that behavior is preserved. |
| INCONCLUSIVE | Source verification fails, changed structures exceed the supported subset, or semantic evidence cannot support a conclusion. |

If GenLayer cannot reach consensus, the transaction may fail or remain undetermined and **does not write a receipt**. That protocol outcome is distinct from an on-chain INCONCLUSIVE assessment.

### Deterministic subset

OpenAPI 3.0/3.1 JSON; 1–40 paths; at most 60,000 UTF-8 bytes for the entire bundle. Checks cover removed paths/operations, removed parameters under a conservative closed-world rule, optional-to-required and newly required inputs, request-body requirements and media removals, schema type changes, nullability direction, request-enum narrowing, response-enum widening, required-field direction, removed properties, arrays, and documented-response removal.

References are not resolved: any `$ref` makes an otherwise non-breaking assessment INCONCLUSIVE. Changed composition, advanced constraints, serialization, response metadata, security, components, and other unsupported constructs also prevent a COMPATIBLE verdict. A known structural break may still establish BREAKING even if other structures are unsupported. Structural safety rules are fixed in this version and cannot be relaxed by policy text. The engine is not a complete OpenAPI conformance validator. Supply well-formed specifications; malformed structures can reject the transaction. Some supported changes are conservatively classified as breaking even where a specific client might tolerate them.

### Semantic consensus

After source verification, the leader and each validator independently run the behavioral task against the same locked specs, release notes, policy and challenge claim. Quotes must be exact substrings of documentary notes or spec descriptions; policies and challenges are not quotation evidence. Decision fields must agree. For conclusive semantic results, a further grounded judgment checks that the leader’s quotation and reasoning support the verdict. Unsupported structures bypass the LLM and return INCONCLUSIVE. Structural breaks do not depend on model judgment.

Descriptions and release notes are untrusted data. Prompt instructions tell models to ignore embedded commands and use INCONCLUSIVE for missing, contradictory, vague or instruction-injecting material. Model-based controls reduce but do not eliminate prompt-injection or reasoning risk.

## Evidence and receipts

A review bundle has exactly `baseline`, `candidate`, `notes`, `policy`, `sources`, and `title`. Python canonical serialization uses sorted keys, ASCII escapes and compact separators; the frontend reproduces it for provided JSON examples. The create method validates the **exact input string** against the supplied digest. Receipts use canonical serialization and link to the prior receipt’s SHA-256. Do not submit secrets: every artifact and challenge is public on-chain.

A source descriptor contains `url`, `sha256`, and `bytes`. Up to three sources are allowed, each an HTTPS raw GitHub URL pinned to a full 40-character commit. Every source must equal the exact canonical JSON artifact pack containing only `baseline`, `candidate`, `notes`, and `policy`. Export this pack with **Export evidence**. Fetch status, byte length, SHA-256, and exact pack equality are checked independently by validators. URLs are allowlisted and cannot name arbitrary local/private hosts. A response is checked after retrieval; the application cannot guarantee transport-level download limits or availability of GitHub.

With no source, the scope is `SUBMITTER_SUPPLIED` and `source_verified` is false. This distinction is displayed explicitly. Public examples are synthetic test fixtures, not third-party API certification. Their commit-pinned publication is authoritative only for those fixture bytes.

## Lifecycle and bounds

`DRAFT → LOCKED → ASSESSED → CHALLENGED → ASSESSED`.

- Evidence is immutable even in DRAFT; create a new review for changed evidence.
- Only the submitting wallet can lock. Assessment is permissionless after lock.
- One non-owner wallet can challenge an assessed review. There is no staking, identity proof or challenge bond, so a funded adversary can occupy the single challenge slot.
- A conclusive assessment cannot be repeated unless challenged. INCONCLUSIVE assessments may retry up to three times in a phase; a challenge resets the phase attempt count.
- Every successful assessment appends a receipt; old receipts are never overwritten. There is no financial settlement or automatic deployment gate.

## Run and verify

```sh
npm ci
npm test
npm run build
npm run dev
npm run verify:live
```

Requires Node.js 22+ and Python 3.10+. Contract tests use explicit VM, web and LLM doubles; they are not evidence of live consensus. `verify:live` reads the deployed code/schema/receipts and recorded transactions, verifies hashes and published fixtures, and writes `docs/live-evidence.json`.

Deploy `contracts/apicompat.py` in GenLayer Studio with **Normal (Full Consensus)** and no constructor arguments. Update `public/deployment.json` for a new deployment. The current source dependency is pinned in the contract’s first line. The website is a Vite static build hosted on ChatGPT Sites; no Vercel deployment is used.

## Continued use

Teams can publish canonical packs from release pipelines, store review IDs in release tickets, and require an integration owner to inspect the final receipt before rollout. Future work includes a richer versioned OpenAPI comparator, signed publisher manifests, structured client profiles, CI ingestion, and multiple bonded challenges. Current contracts are development-network deployments, not production certification.

## Official references

- [Equivalence Principle](https://docs.genlayer.com/developers/intelligent-contracts/equivalence-principle)
- [GenLayerJS](https://docs.genlayer.com/api-references/genlayer-js)
- [Writing contract data](https://docs.genlayer.com/developers/decentralized-applications/writing-data)
- [OpenAPI specification](https://spec.openapis.org/oas/latest.html)
