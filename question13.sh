#!/bin/bash

# Create and switch to new branch
git checkout -b assignment-branch

# Remove all previous .sh files from the branch
git rm *.sh

# Create and commit a new file named file13.txt
echo "This is file13 content" > file13.txt
git add file13.txt
git commit -m "Add file13.txt and remove previous .sh files"

# Push new branch to GitHub
git push -u origin assignment-branch
