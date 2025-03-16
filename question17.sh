#!/bin/bash

# Branch: main configuration
git checkout main
mkdir -p dir1 dir3
mv dir1/foo dir1/dir2/foo
cp dir3/bar dir3/bar_copy
git add .
git commit -m "Configure main branch"

# Branch: branch1 configuration
git checkout -b branch1 main
rm -rf dir1/dir2 dir3/bar_copy
mv dir1/dir2/foo dir1/foo
touch newfile1
git add .
git commit -m "Configure branch1"

# Branch: branch2 configuration
git checkout main
git checkout -b branch2
mv dir1/dir2/foo dir1/dir2/foo_modified
git add dir1/dir2/foo_modified
git commit -m "Rename foo to foo_modified in branch2"
