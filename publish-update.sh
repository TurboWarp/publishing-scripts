#!/bin/bash

set -euf -o pipefail

dirname=$(dirname "$0")

fatal () {
    echo "Fatal error: $1"
    exit 1
}

if [[ ! -f "package.json" ]] || [[ ! -f "package-lock.json" ]]; then
    fatal "Not in a module's root folder"
fi

if [[ $(git status --porcelain) ]]; then
    fatal "Uncommitted changes"
fi

current_date=$(date +"%Y%m%d%H%M")
git_shorthash=$(git rev-parse --short HEAD)
new_version="$current_date-$git_shorthash"

echo "Publishing version $new_version"

# set this first in case the version number somehow breaks build or test
"$dirname/update-package-version.py" "$new_version"

# get to a known clean state
rm -rf dist
npm ci

# make sure its a valid release
# test often needs build to succeed first
npm run build
npm test

# upload production version to npm
npm publish --access=public

# reset temporary changes
git checkout -- package.json package-lock.json
