# Deploy the Rulewise MCP server to Azure

**Live (2026-11-15):** https://rulewise.victoriousdune-a7b660c5.centralindia.azurecontainerapps.io/mcp
(health: `/api/health`). Subscription "Azure for Students", resource group `rulewise`, region
**centralindia**, registry `caf42ef2eb61acr`, app `rulewise` (0-2 replicas, 0.25 CPU, 0.5 GiB).
Verified with a real Claude Code session over HTTP, 0 errors; Azure logs show counts only.

Hosted mode = `rulewise --public` from the [Dockerfile](../Dockerfile): stateless HTTP on `$PORT`,
max `RULEWISE_RATE_LIMIT` requests per minute per client (default 60), no access log (it would hold
IP addresses), logs counts only (brief D23).

Cost: the app sleeps when unused (about USD 0 at small use); the registry (Basic) is about USD 5/month.

## Limits of the student subscription (found 2026-11-15)
- Only these regions are allowed: centralindia, koreacentral, indiasouthcentral, malaysiawest, uaenorth.
- **ACR Tasks are blocked**, so `az containerapp up --source .` fails (`TasksOperationsNotAllowed`).
  Build the image on the Mac and push it instead (below).
- The Homebrew `azure-cli` 2.92.0 cask crashes on `az login` (charset_normalizer binary mismatch with
  Python 3.14.7). Use the official Docker image instead:
  `docker run -it --rm -v ~/.azure:/root/.azure -v "$PWD":/work -w /work mcr.microsoft.com/azure-cli`

## Update after a change (from the repo root)

```sh
TAG=v2   # new tag each time
R=caf42ef2eb61acr
AZ="docker run --rm -v $HOME/.azure:/root/.azure mcr.microsoft.com/azure-cli"

# 1. Build for Azure's servers (amd64). uv runs on the Mac's own chip; pip under emulation.
docker buildx build --platform linux/amd64 -t $R.azurecr.io/rulewise:$TAG --load .

# 2. Push (the token goes straight to docker login, never printed)
$AZ az acr login --name $R --expose-token --query accessToken -o tsv \
  | docker login $R.azurecr.io -u 00000000-0000-0000-0000-000000000000 --password-stdin
docker push $R.azurecr.io/rulewise:$TAG

# 3. Switch the app to the new image
$AZ az containerapp update --name rulewise --resource-group rulewise --image $R.azurecr.io/rulewise:$TAG -o none

# 4. Check
curl https://rulewise.victoriousdune-a7b660c5.centralindia.azurecontainerapps.io/api/health
```

## First deploy (how it was done, for a new subscription)
1. `az login --use-device-code` (inside the Docker image above).
2. Register providers: `Microsoft.App`, `Microsoft.OperationalInsights`, `Microsoft.ContainerRegistry`.
3. `az containerapp up --name rulewise --resource-group rulewise --location centralindia --source . ...`
   created the environment, Log Analytics workspace and registry, then failed at the build step
   (ACR Tasks blocked). The resources it made were kept.
4. Build and push the image as above (tag `v1`).
5. `az acr update -n <registry> --admin-enabled true`, then `az containerapp create --name rulewise
   --resource-group rulewise --environment rulewise-env --image <registry>.azurecr.io/rulewise:v1
   --registry-server ... --registry-username <registry> --registry-password <from az acr credential show>
   --ingress external --target-port 8000 --min-replicas 0 --max-replicas 2 --cpu 0.25 --memory 0.5Gi`.

## Users add it
```sh
claude mcp add --transport http rulewise https://rulewise.victoriousdune-a7b660c5.centralindia.azurecontainerapps.io/mcp
```
Cursor / VS Code / Codex: an MCP server with that `url` (VS Code: `"type": "http"`).

## Notes
- After a sleep, the first request takes a few seconds (cold start).
- The server receives only facts and country codes, never idea text, code or personal data, and stores nothing.
- Before a public launch, consider moving to a normal pay-as-you-go subscription (student credit is for
  learning and runs out) and a custom domain.
