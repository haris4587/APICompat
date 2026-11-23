# Deployment

Network: GenLayer Studionet, chain ID **61999**.

- Contract: [`0x755A3a2b8dE98A06E8eB44B541034767A6B47647`](https://explorer-studio.genlayer.com/address/0x755A3a2b8dE98A06E8eB44B541034767A6B47647)
- Deployment: [`0x836a3d9671f8fec8666df5093e814086c3ed665d8672178821950f99b0cdd687`](https://explorer-studio.genlayer.com/transactions/0x836a3d9671f8fec8666df5093e814086c3ed665d8672178821950f99b0cdd687)
- RPC: `https://studio.genlayer.com/api`
- Website: https://apicompat.mohamedansaf222.chatgpt.site

The deployment used GenLayer Studio’s inbuilt account `0x67Da51Fd9AC1d52F34F5d01d06da8548979fC514`, Normal (Full Consensus), with no constructor arguments. Source is pinned to the dependency in the Python file’s first line. The original development instance at `0xa66a90517Bb8511e22402ff0714397eB627F40C6` is superseded and is not the website’s configured deployment.

## Reproduce

1. Open GenLayer Studio and load `contracts/apicompat.py`.
2. Choose Normal (Full Consensus), deploy with no arguments, and wait for FINALIZED.
3. Update `public/deployment.json` with the returned contract and transaction hash. Do not reuse a transaction or address from a different network.
4. Run `npm ci`, `npm test`, `npm run build`, and `npm run verify:live` after recording actual live review IDs.
5. Publish `dist/` using the tracked ChatGPT Sites configuration. The repository contains no wallet secrets or hosting credentials.

For MetaMask, install an EIP-1193 wallet in the browser and connect using the website button. The SDK requests the Studionet configuration. For Studio, choose Prepare Studio calls, paste the named inputs into the corresponding contract method, sign in Studio, then refresh the review on the website. The Studio wallet is not exposed to external websites as a browser wallet provider.

Pending direct-wallet transaction hashes are stored locally as `apicompat.pending`; reload resumes polling. Clear a pending item only after inspecting its explorer status. Do not resend a transaction merely because an interface times out.
