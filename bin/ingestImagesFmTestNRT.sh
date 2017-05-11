#!/bin/bash
############################
downDir="/data_store/download"
rmtUrl="$1"
destDir="/awips2/edex/data/manual"
#
cd $downDir
wget -e robots=off --cut-dirs=3 --user-agent=Mozilla/5.0 --reject="index.html*" --no-parent --recursive --relative --level=1 --no-directories $rmtUrl
#
for filenm in `ls UAF_*.gz`
do
   gunzip $filenm
   filenm="${filenm%.*}"
   newfilenm="Alaska_"$filenm
   mv $filenm $newfilenm
   echo "mv $newfilenm $destDir"
   mv $newfilenm $destDir
done
