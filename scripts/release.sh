#!/bin/bash
set -e

VERSION=$1

if [ -z "$VERSION" ]; then
  echo "Usage: ./scripts/release.sh v1.1.0"
  exit 1
fi

# Update version files
VERSION_NUM=${VERSION#v}
echo "__version__ = \"$VERSION_NUM\"" > astro_analysis_service/__version__.py
sed -i '' "s/version = \".*\"/version = \"$VERSION_NUM\"/" pyproject.toml
sed -i '' "s/Version \".*\"/Version \"$VERSION_NUM\"/" Singularity.def

# Commit and tag
git add astro_analysis_service/__version__.py pyproject.toml Singularity.def
git commit -m "Bump version to $VERSION"
git push origin master
git tag -a $VERSION -m "Release $VERSION"
git push origin $VERSION

echo "Release $VERSION created! Check GitHub Actions."