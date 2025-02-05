#!/bin/bash
##########################################
# remotediff - compare two files on remote machines
#########################################
filepath="$1"
hostname=`hostname`
if [ "$hostname" = 'edex.x.gina.alaska.edu' ]
then
   remotehost=edex-test.x.gina.alaska.edu
else
   remotehost=edex.x.gina.alaska.edu
fi
#
srcdir=`dirname $filepath`
if [ "$srcdir" = '.' ]
then
   filepath="`pwd`/$filepath"
fi
#echo "ssh $remotehost "cat $filepath" | diff  - $filepath"
ssh $remotehost "cat $filepath" | diff  - $filepath

