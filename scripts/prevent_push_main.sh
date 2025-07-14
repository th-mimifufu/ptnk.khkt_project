#!/bin/bash

branch=$(git symbolic-ref --short HEAD)

if [[ "$branch" == "main" ]]; then
  echo "❌ Push to 'main' is blocked. Please create a pull request instead!"
  exit 1
fi

exit 0
