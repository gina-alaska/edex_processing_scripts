#!/bin/bash
##########################################
# remotecopy - copy specified files to remote machine
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
   srcdir=`pwd`
   filepath="$srcdir/$filepath"
fi
scp $filepath $remotehost:$srcdir
