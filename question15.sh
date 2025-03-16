#!/bin/bash

# Fetch and checkout the remote branch causing conflict
git fetch origin branch1
git checkout -b branch1 origin/branch1

# Switch back to main and merge branch1 into main
git checkout main
git merge branch1

# Resolve conflicts manually if any occur
# (Resolve conflicts manually, then run these commands)
git add .
git commit -m "Merge branch1 into main with conflicts resolved"
