# Deploy the Rulewise MCP server to Azure

Hosted server = users add Rulewise by web address, nothing to install (brief D23).
It runs `rulewise --public` from the [Dockerfile](../Dockerfile): stateless HTTP on `$PORT`,
max `RULEWISE_RATE_LIMIT` requests per minute per client (default 60), no access log
(it would hold IP addresses), logs counts only.

Service: **Azure Container Apps** (sleeps when unused; small use fits the monthly free grant).
`az containerapp up --source .` also creates a container registry (Basic, about USD 5/month).

## First deploy (once)

```sh
brew install azure-cli
az login
az extension add --name containerapp --upgrade
az provider register --namespace Microsoft.App
az provider register --namespace Microsoft.OperationalInsights

# from the repo root
az containerapp up --name rulewise --resource-group rulewise --location southeastasia \
  --source . --ingress external --target-port 8000

# keep cost small: sleep when idle, at most 2 copies
az containerapp update --name rulewise --resource-group rulewise \
  --min-replicas 0 --max-replicas 2 --cpu 0.25 --memory 0.5Gi

# the address
az containerapp show --name rulewise --resource-group rulewise \
  --query properties.configuration.ingress.fqdn -o tsv
```

Check it: `curl https://<address>/api/health` gives `{"status":"ok","rules":57}`.

## Users add it

```sh
claude mcp add --transport http rulewise https://<address>/mcp
```
Cursor / VS Code / Codex: an MCP server of type `http` with url `https://<address>/mcp`.

## Update after a change

```sh
az containerapp up --name rulewise --resource-group rulewise --source .
```

## Notes
- After a sleep, the first request takes a few seconds (cold start).
- Region: `southeastasia` (Singapore). The server receives only facts and country codes,
  never idea text, code or personal data, and stores nothing.
- Test locally first: `docker build -t rulewise . && docker run -p 127.0.0.1:8200:8000 rulewise`,
  then `claude mcp add --transport http rulewise http://127.0.0.1:8200/mcp`.
