#!/usr/bin/env bash
# Compile the report and verify one question per page.
# Usage: ./check_pages.sh report.tex
set -euo pipefail

tex="${1:-report.tex}"
pdf="${tex%.tex}.pdf"

/tmp/tectonic -X compile "$tex" >/dev/null 2>&1 || /tmp/tectonic -X compile "$tex"

pages=$(pdfinfo "$pdf" | awk '/^Pages:/ {print $2}')
qs=$(grep -c '\\question{' "$tex")

echo "pages=$pages questions=$qs"

# Page N should start with question N (header + heading carry 第N题).
pdftotext "$pdf" - | awk 'BEGIN {p=1}
  /\f/ {p++}
  $0 ~ /^第 ?[0-9]+ ?题/ && length($0) < 25 {print "p" p ": " $0}
' | sort -u

if [ "$pages" -ne "$qs" ]; then
  echo "MISMATCH: a question spans more than one page (or a page has none)."
  echo "Shrink figures/circuits, merge subsection headings, inline short equations."
  exit 1
fi

pdffonts "$pdf" | awk 'NR>2 && $(NF-4) != "yes" {print "font not embedded: " $0}'
echo "OK"
