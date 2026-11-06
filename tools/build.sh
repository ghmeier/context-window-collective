#!/bin/sh
# Rebuild index.html from tools/page-source.html (the page body and styles)
# and tools/index.head (the document head). Run from the repo root.
D=$(dirname "$0"); S="$D/page-source.html"; O="$D/../index.html"
{ cat "$D/index.head"
  sed -n '1,/^<\/style>/p' "$S" | grep -v 'claude:viewport-fit-sides'
  echo '</head>'; echo '<body>'
  sed -n '/^<\/style>/,$p' "$S" | tail -n +2
  echo '</body>'; echo '</html>'; } > "$O"
