#!/bin/bash
##################################
# chg to download directory
dataDir="/awips2/edex/data/hdf5"
totfiles=`find $dataDir -type f | wc -l`
recentfiles=`find $dataDir -mtime +"$1" -type f | wc -l`
echo "In $dataDir..."
echo "Total files: $totfiles with $recentfiles more than $1 day(s) old"
#
dataDir="/data_store/manual"
totfiles=`find $dataDir -type f | wc -l`
recentfiles=`find $dataDir -mtime +"$1" -type f | wc -l`
echo "In $dataDir..."
echo "Total files: $totfiles with $recentfiles more than $1 day(s) old"
#
