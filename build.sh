#!/usr/bin/env bash
FORMAT="gfm"

mkdir -p 'build'

for f in *.md; do
  filename="$(basename "$f")"
  base="${filename%.*}"
  ext="${filename##*.}"
  pandoc "$f" --template=eisvogel -F mermaid-filter -f $FORMAT -o "build/${base}.pdf"
done
