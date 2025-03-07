#!/bin/bash
##################################
# chg to download directory
if [ "X$1" = "X" ]
then 
   echo "Syntax: $0 {num days}"
   exit
else
   numdays="$1"
fi
dataDir="/awips2/edex/data/hdf5"
totfiles=`find $dataDir -type f | wc -l`
recentfiles=`find $dataDir -mtime +"$numdays" -type f | wc -l`
echo "In $dataDir..."
echo "Total files: $totfiles with $recentfiles more than $numdays day(s) old"
#
dataDir="/data_store/manual"
totfiles=`find $dataDir -type f | wc -l`
recentfiles=`find $dataDir -mtime +"$numdays" -type f | wc -l`
echo "In $dataDir..."
echo "Total files: $totfiles with $recentfiles more than $numdays day(s) old"
#
