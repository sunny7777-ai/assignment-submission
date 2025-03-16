#!/bin/bash

# Fetch all branches
git fetch origin

# Checkout branch3 and merge into current branch (assuming main)
git checkout branch2
git merge origin/branch3

# (Resolve any conflicts manually)

# Stage and commit resolved conflicts
git add .
git commit -m "Merge branch3 into branch2 and resolve conflicts"

# Delete branch3
git branch -d branch3
