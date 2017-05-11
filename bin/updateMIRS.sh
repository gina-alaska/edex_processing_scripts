#!/bin/bash
############################
destDir="/awips2/edex/data/manual"
#
cd /data_store/download
wget -e robots=off --cut-dirs=3 --user-agent=Mozilla/5.0 --reject="index.html*" --no-parent --recursive --relative --level=1 --no-directories http://hippy.gina.alaska.edu/distro/carl/Latest/
#
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
   mv $newfilenm $destDir
done
#
echo Done!
