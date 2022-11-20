#!/bin/bash
#############################################
if [[ "$1"X = X ]]
then
   echo ""
   echo "No pathname defined!" 
   echo ""
   echo "Syntax: $0 pathname"
   exit
fi
path="$1/"
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

