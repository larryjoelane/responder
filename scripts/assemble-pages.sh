#!/usr/bin/env bash
# Package docs/ and css/ for GitHub Pages.
#
# The manual lives in docs/ and links the library with ../css/, which is
# correct in the repository and for a raw HTML preview of that folder.
# Pages serves the manual at the site root, so this script copies the HTML
# up and rewrites those links to css/. It does not compile CSS.
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
site="$root/_site"

rm -rf "$site"
mkdir -p "$site/css" "$site/assets"

cp "$root"/docs/*.html "$root"/docs/*.css "$site/"
cp -a "$root"/docs/assets/. "$site/assets/"
cp -a "$root"/css/. "$site/css/"
sed -i 's|\.\./css/|css/|g' "$site"/*.html
touch "$site/.nojekyll"
