#!/bin/sh

# git add & commit & push shell script by Jade

#DATE=`date +%Y-%m-%d" "%H:%M`
DATE=`date +%Y-%m-%d`
MSG="$DATE"
if [ $# -gt 0 ]; then
    MSG="$1"
fi

#git checkout master

git diff --numstat origin/master

git add --all
git commit -am "${MSG}"

git push origin master
