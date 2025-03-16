#!/bin/bash

# Create and switch to a new branch named branch2
git checkout -b branch2

# Create and commit a new file named file4
echo "Initial content" > file4
git add file4
git commit -m "Create file4 in branch2"

# Modify file4 without committing
echo "Modified content" >> file4

# Stash uncommitted changes to preserve modifications safely
git stash

# Switch back to main branch without losing changes
git checkout main
