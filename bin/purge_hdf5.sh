#!/bin/sh
#########################

cd /awips2/edex/data/hdf5/satellite/grid203

for dir in */
do
   echo "$dir"
   rm "$dir"satellite-2017-02-*
   rm "$dir"satellite-2017-03-*
   rm "$dir"satellite-2017-04-0*
   rm "$dir"satellite-2017-04-10*
   rm "$dir"satellite-2017-04-11*
   rm "$dir"satellite-2017-04-12*
   rm "$dir"satellite-2017-04-13*
   echo "-----"
done
