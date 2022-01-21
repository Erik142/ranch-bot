#!/bin/bash
OLD_VERSION=$(python3 -m poetry version -s)
case $1 in 
    dev)
    OLD_VERSION_PREFIX=${OLD_VERSION%-*}
    SUFFIX=$(date -u +%s)
    python3 -m poetry version "$OLD_VERSION_PREFIX-$SUFFIX"
    ;;
    patch)
    python3 -m poetry version patch
    ;;
    minor)
    python3 -m poetry version minor
    ;;
    major)
    python3 -m poetry version major
    ;;
esac

NEW_VERSION=$(python3 -m poetry version -s)
git add pyproject.toml
git commit -m "Bump version from $OLD_VERSION to $NEW_VERSION"
git tag -a v$NEW_VERSION -m "Bump version from $OLD_VERSION to $NEW_VERSION"