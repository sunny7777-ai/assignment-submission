#!/bin/bash

# Identify all remote branches
git fetch --all
git branch -r

# Merge branches starting with 'ready' into main
git checkout main
for branch in $(git branch -r | grep 'origin/ready'); do
    git merge "$branch"
    # Resolve conflicts manually if they appear, then continue:
    git add .
    git commit -m "Merge ${branch} into main"
done

# Delete merged branches
for branch in $(git branch -r | grep ready); do
    git push origin --delete ${branch#origin/}
done
