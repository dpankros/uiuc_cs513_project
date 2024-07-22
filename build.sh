#!/usr/bin/env bash
FORMAT="gfm"
FROM="markdown+grid_tables+backtick_code_blocks+multiline_tables"
mkdir -p 'build'

for f in *.md; do
  filename="$(basename "$f")"
  base="${filename%.*}"
  ext="${filename##*.}"
  pandoc "$f" --template=eisvogel -F mermaid-filter -f $FORMAT --from "$FROM" -o "build/${base}.pdf"
done
