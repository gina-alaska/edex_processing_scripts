#!/bin/sh -l
DIR=`dirname $0`
PYS=`basename $0 .sh`
$DIR/$PYS.py $@
