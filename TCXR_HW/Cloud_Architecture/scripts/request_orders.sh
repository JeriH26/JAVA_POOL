#!/usr/bin/env bash

set -euo pipefail

API_BASE_URL="${API_BASE_URL:-https://partner.example.com/api/v1/orders}"
API_TOKEN="${API_TOKEN:-replace_me}"
BUCKET="${BUCKET:-gs://xyz-inventory-landing/raw/orders}"
RUN_TS="$(date -u +%Y%m%dT%H%M%SZ)"
LOCAL_FILE="/tmp/orders_${RUN_TS}.csv"

curl -sS \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Accept: text/csv" \
  "${API_BASE_URL}?since=1hour" \
  -o "${LOCAL_FILE}"

if [[ ! -s "${LOCAL_FILE}" ]]; then
  echo "Downloaded file is empty. Exiting."
  exit 1
fi

gsutil cp "${LOCAL_FILE}" "${BUCKET}/orders_${RUN_TS}.csv"

echo "Order file uploaded to ${BUCKET}/orders_${RUN_TS}.csv"
