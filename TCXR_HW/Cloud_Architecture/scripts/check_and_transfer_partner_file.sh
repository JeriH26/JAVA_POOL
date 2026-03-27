#!/usr/bin/env bash

set -euo pipefail

SFTP_HOST="${SFTP_HOST:-sftp.partner-example.com}"
SFTP_USER="${SFTP_USER:-partner_user}"
SFTP_REMOTE_DIR="${SFTP_REMOTE_DIR:-/exports/inventory}"
LOCAL_DIR="${LOCAL_DIR:-/tmp/partner_inventory}"
BUCKET="${BUCKET:-gs://xyz-inventory-landing/raw/partner}"
DATE_UTC="$(date -u +%Y%m%d)"
EXPECTED_FILE="inventory_${DATE_UTC}.csv"

mkdir -p "${LOCAL_DIR}"

echo "Checking for ${EXPECTED_FILE} on partner SFTP..."

sftp "${SFTP_USER}@${SFTP_HOST}" <<EOF
cd ${SFTP_REMOTE_DIR}
lcd ${LOCAL_DIR}
get ${EXPECTED_FILE}
bye
EOF

LOCAL_FILE="${LOCAL_DIR}/${EXPECTED_FILE}"

if [[ ! -f "${LOCAL_FILE}" ]]; then
  echo "Expected file not found: ${EXPECTED_FILE}"
  exit 1
fi

if [[ ! -s "${LOCAL_FILE}" ]]; then
  echo "File exists but is empty: ${EXPECTED_FILE}"
  exit 1
fi

gsutil mv "${LOCAL_FILE}" "${BUCKET}/${EXPECTED_FILE}"

echo "Transferred ${EXPECTED_FILE} to ${BUCKET}/${EXPECTED_FILE}"
