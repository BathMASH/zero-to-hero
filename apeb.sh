#!/usr/bin/env bash
#
# This script copies the apeb folder and updates it to git.
#
echo rendering apeb version
quarto render --profile apeb
echo copying to apeb
cp -r -u ./_apeb/* ../apeb
cd ../apeb
git add .
git commit -m 'updated website'
echo pushing to github
git push origin master
cd ../base
echo done