#!/bin/bash

VERSION=$(python3 -m poetry version -s)

docker build -t harbor.wahlberger.dev/ranch/ranch-bot-staging:$VERSION .
docker image tag harbor.wahlberger.dev/ranch/ranch-bot-staging:$VERSION harbor.wahlberger.dev/ranch/ranch-bot-staging:latest
docker push harbor.wahlberger.dev/ranch/ranch-bot-staging:$VERSION
docker push harbor.wahlberger.dev/ranch/ranch-bot-staging:latest