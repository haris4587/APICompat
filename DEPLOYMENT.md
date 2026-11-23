# Deployment

Network: GenLayer Studionet, chain ID **61999**.

- Contract: [`0xfbf25Bae6d94E20A6bDB13096D7927225eAA1d83`](https://explorer-studio.genlayer.com/address/0xfbf25Bae6d94E20A6bDB13096D7927225eAA1d83)
- Deployment: [`0xfdb4ee78fe030ae3565c72fd33e1aefe5d7662fd054d65106a102fcfc854f9d1`](https://explorer-studio.genlayer.com/transactions/0xfdb4ee78fe030ae3565c72fd33e1aefe5d7662fd054d65106a102fcfc854f9d1)
- RPC: `https://studio.genlayer.com/api`
- Website: https://apicompat.mohamedansaf222.chatgpt.site

The deployment used GenLayer Studio’s inbuilt account `0x67Da51Fd9AC1d52F34F5d01d06da8548979fC514`, Normal (Full Consensus), with no constructor arguments. Source is pinned to the dependency in the Python file’s first line. Earlier development instances are superseded and are not the website’s configured deployment. The release source was verified byte-for-byte against the deployed contract.

## Reproduce

1. Open GenLayer Studio and load `contracts/apicompat.py`.
2. Choose Normal (Full Consensus), deploy with no arguments, and wait for FINALIZED.
3. Update `public/deployment.json` with the returned contract and transaction hash. Do not reuse a transaction or address from a different network.
4. Run `npm ci`, `npm test`, `npm run build`, and `npm run verify:live` after recording actual live review IDs.
5. Publish `dist/` using the tracked ChatGPT Sites configuration. The repository contains no wallet secrets or hosting credentials.

For MetaMask, install an EIP-1193 wallet in the browser and connect using the website button. The SDK requests the Studionet configuration. For Studio, choose Prepare Studio calls, paste the named inputs into the corresponding contract method, sign in Studio, then refresh the review on the website. The Studio wallet is not exposed to external websites as a browser wallet provider.

Pending direct-wallet transaction hashes are stored locally as `apicompat.pending`; reload resumes polling. Clear a pending item only after inspecting its explorer status. Do not resend a transaction merely because an interface times out.
