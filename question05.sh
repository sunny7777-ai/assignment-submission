#!/bin/bash

# Create directory 'dir1' and a file 'file2' inside it
mkdir -p dir1
touch dir1/file2

# Stage the directory and all its contents (without committing)
git add dir1
