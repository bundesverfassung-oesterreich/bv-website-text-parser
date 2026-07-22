#!/usr/bin/env bash
set -euo pipefail

STYLESHEETS_DIR="third_party/tei-stylesheets"
BASE_TEI_DIR="tmp/base-tei"
DOCX_DIR="tmp"

if [[ ! -d "$STYLESHEETS_DIR" ]]; then
  echo "Missing stylesheets directory: $STYLESHEETS_DIR" >&2
  exit 1
fi

if ! command -v ant >/dev/null 2>&1; then
  echo "Missing ant. Install Apache Ant before running this script." >&2
  exit 1
fi

chmod +x "$STYLESHEETS_DIR/bin/transformtei" "$STYLESHEETS_DIR/bin/docxtotei"
mkdir -p "$BASE_TEI_DIR" tei

mapfile -d '' DOCX_FILES < <(find "$DOCX_DIR" -maxdepth 1 -type f -name '*.docx' -print0)
if [[ "${#DOCX_FILES[@]}" -eq 0 ]]; then
  echo "No DOCX files found in $DOCX_DIR" >&2
  exit 1
fi

for input_docx in "${DOCX_FILES[@]}"; do
  output_tei="$BASE_TEI_DIR/$(basename "${input_docx%.docx}").xml"
  "$STYLESHEETS_DIR/bin/docxtotei" "$input_docx" "$output_tei"
  test -s "$output_tei"
  echo "Converted $input_docx -> $output_tei"
done
