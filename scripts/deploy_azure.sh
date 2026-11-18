#!/usr/bin/env bash
# Deploy the Rulewise MCP server to Azure Container Apps (steps from docs/DEPLOY-AZURE.md).
#
#   ./scripts/deploy_azure.sh
#
# Needs Docker Desktop running and an Azure login in ~/.azure. If not logged in:
#   docker run -it --rm -v ~/.azure:/root/.azure mcr.microsoft.com/azure-cli az login --use-device-code
#
# It refuses to deploy uncommitted changes or failing tests, and at the end checks that the
# live server has the same number of rules as this folder.
set -euo pipefail
cd "$(dirname "$0")/.."

REGISTRY=caf42ef2eb61acr
APP=rulewise
GROUP=rulewise
URL=https://rulewise.victoriousdune-a7b660c5.centralindia.azurecontainerapps.io
TAG=v$(date +%Y%m%d-%H%M)
IMAGE=$REGISTRY.azurecr.io/rulewise:$TAG
AZ=(docker run --rm -v "$HOME/.azure:/root/.azure" mcr.microsoft.com/azure-cli)

say() { printf '\n== %s\n' "$*"; }

say "Checks"
if [ -n "$(git status --porcelain -- src rules Dockerfile pyproject.toml uv.lock)" ]; then
  echo "Uncommitted changes in src/, rules/ or build files. Commit first, so the live server matches git."
  exit 1
fi
branch=$(git rev-parse --abbrev-ref HEAD)
[ "$branch" = main ] || echo "Note: deploying from branch '$branch', not main."
docker info >/dev/null 2>&1 || { echo "Docker is not running. Open Docker Desktop."; exit 1; }
uv run pytest -q
expected=$(uv run python -c "from legal_check.library import load_library; print(len(load_library().rules))")
echo "Rules in this folder: $expected. Image tag: $TAG"

say "1/4 Build (linux/amd64)"
docker buildx build --platform linux/amd64 -t "$IMAGE" --load .

say "2/4 Push"
"${AZ[@]}" az acr login --name "$REGISTRY" --expose-token --query accessToken -o tsv \
  | docker login "$REGISTRY.azurecr.io" -u 00000000-0000-0000-0000-000000000000 --password-stdin
docker push "$IMAGE"

say "3/4 Switch the app to $TAG"
"${AZ[@]}" az containerapp update --name "$APP" --resource-group "$GROUP" --image "$IMAGE" -o none

say "4/4 Check the live server"
for i in $(seq 1 20); do
  live=$(curl -fsS "$URL/api/health" 2>/dev/null | sed -n 's/.*"rules":\([0-9]*\).*/\1/p' || true)
  if [ "$live" = "$expected" ]; then
    echo "Live: $live rules. Deployed $TAG."
    exit 0
  fi
  echo "Live has '${live:-no answer}' rules, waiting for $expected... ($i/20)"
  sleep 15
done
echo "The live server did not show $expected rules after 5 minutes. Check the app in the Azure portal."
exit 1
