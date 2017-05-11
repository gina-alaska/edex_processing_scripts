#!/bin/bash
############################
yyyymmdd=`date +%Y%m%d`
(
ingestDir="/awips2/edex/data/manual"
srcDir="/data_store/download"
#
cd $srcDir
# first look for the compressed GINA files
for filenm in `ls $srcDir`
do
   #filenm=`echo $filenm | sed 's/.VIIRS_ALASK//'`
   if echo $filenm | grep -q "gzVIIRS_ALASK"
   then
      newfilenm=`echo $filenm | sed 's/gzVIIRS_ALASK/gz/'`
      mv $filenm $newfilenm
      filenm=$newfilenm
   fi
   # 
   if echo $filenm | grep -q ".gz"
   then
      gunzip $filenm
      filenm="${filenm%.*}"
   fi
   #
   if echo $filenm | grep -q "SSEC"
   then
      gunzip -c $filenm > $filenm".nc"
      rm -f $filenm
      filenm=$filenm".nc"
   fi
   # 
   newfilenm="Alaska_"$filenm
   echo "mv $filenm $ingestDir/$newfilenm"
   mv $filenm $ingestDir/$newfilenm
done

#
) >> /awips2/edex/logs/edex-ingest-LDMsat-$yyyymmdd".log" 2>&1

