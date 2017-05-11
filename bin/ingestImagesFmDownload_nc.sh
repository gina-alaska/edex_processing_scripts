#!/bin/bash
############################
destDir="/awips2/edex/data/manual"
#mv /home/awips/Downloads/UAF_*.nc .
for filenm in `ls UAF_*.nc`
do
   if [[ $filenm == *"metopa_mhs"* ]]
   then
      /home/awips/bin/chgattr.py -a satelliteName -n AMSU -f $filenm
   fi

   #filenm="${filenm%.*}"
   newfilenm="Alaska_"$filenm
   mv $filenm $newfilenm
   echo "mv $newfilenm $destDir"
   #mv $newfilenm $destDir
   cp $newfilenm $destDir
done
