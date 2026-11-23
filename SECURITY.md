# Security and trust boundaries

APICompat is a development-network assessment tool. It does not certify running APIs, publisher identity, legal compliance, or suitability for deployment.

## Controls

- Artifact bytes are SHA-256 bound at creation; no artifact editing method exists.
- The owner alone locks the review. A non-owner may challenge once; all post-lock assessments are permissionless.
- Source URLs allow only HTTPS raw GitHub files at full commit hashes. Exact byte lengths, digests and canonical artifact-pack equality are verified before a conclusion.
- Validators independently retrieve and reason over evidence, compare verdict/provenance, validate quotation grounding, and substantively check conclusive semantic findings.
- A known structural break cannot be overridden by a model’s COMPATIBLE response.
- Unsupported constructs and weak evidence cannot produce COMPATIBLE through structural checks alone.
- Receipt hashes bind their content and predecessor. All receipts remain queryable.
- Prompt data includes untrusted specs/notes/challenges. Instructions explicitly forbid obeying commands embedded in them.
- The frontend escapes untrusted HTML, never requests private keys, and does not treat ACCEPTED as FINALIZED.
- Signature rejection, reverts, consensus failure and timeouts are distinct. Saved transaction hashes prevent blind resubmission after reload.

## Remaining risks

- Matching published artifacts is not proof of publisher authority or documentation truthfulness. Submissions without sources are explicitly labeled SUBMITTER_SUPPLIED.
- LLMs can be wrong or manipulated despite independent verification. Model diversity and validator availability depend on the GenLayer network.
- This is a bounded comparator, not a complete OpenAPI parser/type system. JSON must be well formed. References are unresolved. Conservative rules can produce false positives or INCONCLUSIVE.
- Models may observe different source availability. No consensus means no state change; an INCONCLUSIVE receipt requires a successful transaction.
- The contract checks response size after download; it cannot enforce a transport-level cap. GitHub availability and commit retention are external dependencies.
- A single non-owner can consume the challenge slot. There is no identity system, bond, expiry or arbitration authority. The owner can always create a separate review with corrected evidence.
- All submitted material and challenge text are public on-chain. Never upload secrets, access tokens, customer data or confidential API descriptions.
- The website and network are separate availability boundaries. Operators must verify the configured address and chain before signing.
- Browser wallet signing requires the user’s installed extension. Actual MetaMask signing was not tested in the hosted browser; Studio transactions and wallet-adapter doubles were tested.

Report issues through a private GitHub security advisory if enabled. Otherwise avoid publishing credentials or personal data in public issues.
