#!/bin/bash
###########################################
# script to make sure data is being purged
###########################################
#
ddtt=`date`
echo "------- `date` --------"
#echo "/awips2/data"
du /awips2/data -sh
#echo "/awips2/edex/data/hdf5"
du /awips2/edex/data/hdf5 -sh
echo "---------------------------------------------"

