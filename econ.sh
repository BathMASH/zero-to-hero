#!/usr/bin/env bash
#
# This script copies the econ folder and updates it to git.
#
echo rendering econ version
quarto render --profile econ
echo copying to econ
cp -r -u ./_econ/* ../econ
cd ../econ
git add .
git commit -m 'updated website'
echo pushing to github
git push origin master
cd ../base
echo done