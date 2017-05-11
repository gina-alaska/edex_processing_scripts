#!/bin/bash
############################
destDir="/awips2/edex/data/manual"
mv /home/awips/Downloads/UAF*.gz .
for filenm in `ls UAF_*.gz`
do
   gunzip $filenm
   filenm="${filenm%.*}"
   newfilenm="Alaska_"$filenm
   mv $filenm $newfilenm
   echo "mv $newfilenm $destDir"
   mv $newfilenm $destDir
   #cp $newfilenm $destDir
done
