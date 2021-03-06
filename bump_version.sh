#!/bin/bash
OLD_VERSION=$(python3 -m poetry version -s)
OLD_VERSION_PREFIX=${OLD_VERSION%-*}
case $1 in 
    dev)
    SUFFIX=$(date -u +%s)
    
    if [[ "$OLD_VERSION" == "$OLD_VERSION_PREFIX" ]]
    then
        python3 -m poetry version patch
        TEMP_VERSION=$(python3 -m poetry version -s)
        TEMP_VERSION_PREFIX=${TEMP_VERSION%-*}
        NEW_VERSION="$TEMP_VERSION_PREFIX-$SUFFIX"
    else
        NEW_VERSION="$OLD_VERSION_PREFIX-$SUFFIX"
    fi

    python3 -m poetry version "$NEW_VERSION"
    ;;
    patch)
    if [[ "$OLD_VERSION" != "$OLD_VERSION_PREFIX" ]]
    then
        python3 -m poetry version "$OLD_VERSION_PREFIX"
    else
        python3 -m poetry version patch
    fi
    ;;
    minor)
    if [[ "$OLD_VERSION" != "$OLD_VERSION_PREFIX" ]]
    then
        python3 -m poetry version "$OLD_VERSION_PREFIX"
    else
        python3 -m poetry version minor
    fi
    ;;
    major)
    if [[ "$OLD_VERSION" != "$OLD_VERSION_PREFIX" ]]
    then
        python3 -m poetry version "$OLD_VERSION_PREFIX"
    else
        python3 -m poetry version major
    fi
    ;;
esac

NEW_VERSION=$(python3 -m poetry version -s)
git add pyproject.toml
git commit -m "Bump version from $OLD_VERSION to $NEW_VERSION"
git tag -a v$NEW_VERSION -m "Bump version from $OLD_VERSION to $NEW_VERSION"