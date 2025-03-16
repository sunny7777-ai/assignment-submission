#!/bin/bash

# Create directory 'dir2'
mkdir -p dir2

# Move all .txt files to 'dir2'
mv *.txt dir2/

# Stage changes
git add dir2/*.txt

# Commit changes
git commit -m "Move all .txt files into dir2"

