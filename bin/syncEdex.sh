#!/bin/bash
#############################################
if [[ "$1"X = X ]]
then
   echo ""
   echo "No pathname defined! Using current directory"
   path=`pwd`
   path="$path/"
   #echo ""
   #echo "Syntax: $0 pathname"
   #exit
else
   path="$1/"
fi
hostnm=`hostname`
if [ "$hostnm" = "edex.x.gina.alaska.edu" ]
then
   otherhost="edex-test.x.gina.alaska.edu"
elif [ "$hostnm" = "edex-test.x.gina.alaska.edu" ]
then
   otherhost="edex.x.gina.alaska.edu"
else
   echo "Not an EDEX server! Exiting..."
   exit
fi
echo rsync -avnc --exclude='*.md5' --delete $path $otherhost:$path
rsync -n -avrc --exclude='*.md5' --delete $path $otherhost:$path | sed '/\/$/d'

