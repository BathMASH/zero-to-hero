#!/usr/bin/env bash
#
# This script copies the cs folder and updates it to git.
#
echo rendering cs version
quarto render --profile cs
echo copying to cs
cp -r -u ./_cs/* ../cs
cd ../cs
git add .
git commit -m 'updated website'
echo pushing to github
git push origin master
cd ../base
echo done