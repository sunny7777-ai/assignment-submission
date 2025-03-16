#!/bin/bash

# Switch back to branch2
git checkout branch2

# Restore stashed changes (without losing data)
git stash pop

# Stage and commit the restored changes
git add file4
git commit -m "Modified file4 after switching back to branch2"
