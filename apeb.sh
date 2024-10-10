#!/usr/bin/env bash
#
# This script copies the global policy folder and updates it to git.
#
echo rendering global policy version
quarto render --profile global-policy
echo copying to stat-tastic-global
cp -r -u ./_global-policy/* ../stat-tastic-global
cd ../stat-tastic-global
git add .
git commit -m 'updated website'
echo pushing to github
git push origin master
cd ../stat-tastic
echo done