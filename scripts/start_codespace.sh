#!/usr/bin/env bash
# Wakes (starts) a stopped GitHub Codespace via the REST API so the
# Keshav AI API becomes reachable on its forwarded public port again.
#
# Requires:
#   GITHUB_TOKEN   - a GitHub PAT (classic) with the "codespace" scope
#   CODESPACE_NAME - the codespace's internal name, e.g. "keshav-ai-xyz123"
#                    (get it with: curl -H "Authorization: Bearer $GITHUB_TOKEN" \
#                     https://api.github.com/user/codespaces)
#
# Usage:
#   GITHUB_TOKEN=ghp_xxx CODESPACE_NAME=keshav-ai-xyz123 ./scripts/start_codespace.sh

set -euo pipefail

: "${GITHUB_TOKEN:?Set GITHUB_TOKEN to a PAT with the 'codespace' scope}"
: "${CODESPACE_NAME:?Set CODESPACE_NAME to the codespace's internal name}"

curl -sS -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer ${GITHUB_TOKEN}" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/user/codespaces/${CODESPACE_NAME}/start"
