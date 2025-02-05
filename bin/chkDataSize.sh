#!/bin/bash
###########################################
# script to make sure data is being purged
###########################################
#
ddtt=`date`
echo "------- `date` --------"
#echo "/data_store/manual"
du /data_store/manual -sh
du /data_store/download -sh
du /data_store/dropbox -sh
#echo "/awips2/edex/data/hdf5"
du /awips2/edex/data/hdf5 -sh
echo "---------------------------------------------"

