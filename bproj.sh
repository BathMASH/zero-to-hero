#!/usr/bin/env bash
#
# This script builds the project and then copies it to the respective folder and updates it to git.
#
# The folder must exisit and git initialised before you can use this shortcut

if [[ $# -eq 0 ]] ; then
    echo 'supply project name. for example ./bproj.sh apeb'
    exit 1
fi
echo rendering $1 version
quarto render --profile $1
echo copying to $1
cp -r -u ./_$1/* ../$1
cd ../$1
git add .
git commit -m 'updated website'
echo pushing to github
git push origin master
cd ../base
echo done