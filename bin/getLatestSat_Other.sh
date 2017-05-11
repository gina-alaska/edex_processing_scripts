#!/bin/bash
##################################
# chg to download directory
ddtt=`date +%Y%m%d`
(
export PYTHONPATH=/awips2/fxa/bin/src
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/awips2/python/lib
#
echo "+++++ Starting GINA product download (OTHER): `date` ++++++"
# CHECK IF EDEX IS UP
edex_ingest_ps=`ps aux | grep ingest | grep -v ingestGrib | grep -v ingestDat | awk '{ print $15 }'`
if [ -z $edex_ingest_ps ]; then
	echo 'EDEXingest is not running. Exiting... No downloads attempted. '
        exit
else
	edex_ingest_pid=`ps aux | grep ingest | grep -v ingestGrib | grep -v ingestDat | awk '{ print $2 }'`
	echo 'EDEXingest is running :: pid '$edex_ingest_pid''
fi
#
baseDir="/data_store/download"
ingestDir="/awips2/edex/data/manual"
testDir="/home/awips/tmp"
cd $baseDir
#
arglist=""
for var in "$@"
do
   if [ "$var" = "sport" -o "$var" = "geocat" ]
   then
      echo "Requesting: $var"
      arglist=$arglist" $var"
   elif [ "$var" = "sport:rgb" ]
   then
      echo "Requesting: $var"
      arglist=$arglist" sport -p rgb"
   elif [ "$var" = "sport:qpe" ]
   then
      echo "Requesting: $var"
      arglist=$arglist" sport -p qpe"
   elif [ "$var" = "geocat:fogst" ]
   then
      echo "Requesting: $var"
      arglist=$arglist" geocat -p fogst"
   elif [ "$var" = "geocat:ash" ]
   then
      echo "Requesting: $var"
      arglist=$arglist" geocat -p ash"
   else
      echo "Unknown datatype type ($var)!"
   fi
   echo "ARGLIST: $arglist"
done
#
if [ -z "$arglist" ]
then
   echo "No command line arguments. Default is all data types"
   echo ""
   arglist="sport geocat"
fi
#
echo "/home/awips/bin/getOtherSat.py $arglist"
/home/awips/bin/getOtherSat.py $arglist
#
#
touch SSEC_MARKER
# next unzip and rename the files
for srcname in `ls SSEC*`
do
   if [ "$srcname" = "SSEC_MARKER" ]
   then
      rm $srcname
   else
      destname="Alaska_$srcname"".gz"
      ncname="Alaska_$srcname"
      prodsrc=`echo $srcname | cut -f3 -d'_'`
      echo "mv $srcname $destname"
      mv $srcname $destname
      gunzip $destname 
      mv $ncname $ingestDir
   fi
done
#
touch MARKER_sport.gz
for srcname in `ls *_sport*.gz`
do
   if [ "$srcname" = "MARKER_sport.gz" ]
   then
      rm $srcname
   else
      destname="Alaska_$srcname"
      ncname=`echo $destname | sed 's/.gz//'`
      prodtype=`echo $srcname | cut -f6 -d'_'`
      prodsrc=`echo $srcname | cut -f4 -d'_'`
      echo "mv $srcname $destname"
      mv $srcname $destname
      gunzip $destname 
      ### qpe products need some attribute changes
      if [ "$prodsrc" = "nesdis" ]
      then
         if [ "$prodtype" = "qpe000hr.gz" ]
         then
            echo "Change Attributes: satelliteName channel depictorName"
            /home/awips/bin/chgattr.py -f $ncname -a satelliteName -n "GOES Imager"
            /home/awips/bin/chgattr.py -f $ncname -a channel -n "NESDIS QPE 000"
            /home/awips/bin/chgattr.py -f $ncname -a depictorName -n "alaskaRegion"
         elif [ "$prodtype" = "qpe001hr.gz" ]
         then
            echo "Change Attributes: satelliteName channel depictorName"
            /home/awips/bin/chgattr.py -f $ncname -a satelliteName -n "GOES Imager"
            /home/awips/bin/chgattr.py -f $ncname -a channel -n "NESDIS QPE 001"
            /home/awips/bin/chgattr.py -f $ncname -a depictorName -n "alaskaRegion"
         elif [ "$prodtype" = "qpe003hr.gz" ]
         then
            echo "Change Attributes: satelliteName channel depictorName"
            /home/awips/bin/chgattr.py -f $ncname -a satelliteName -n "GOES Imager"
            /home/awips/bin/chgattr.py -f $ncname -a channel -n "NESDIS QPE 003"
            /home/awips/bin/chgattr.py -f $ncname -a depictorName -n "alaskaRegion"
         elif [ "$prodtype" = "qpe006hr.gz" ]
         then
            echo "Change Attributes: satelliteName channel depictorName"
            /home/awips/bin/chgattr.py -f $ncname -a satelliteName -n "GOES Imager"
            /home/awips/bin/chgattr.py -f $ncname -a channel -n "NESDIS QPE 006"
            /home/awips/bin/chgattr.py -f $ncname -a depictorName -n "alaskaRegion"
         elif [ "$prodtype" = "qpe012hr.gz" ]
         then
            echo "Change Attributes: satelliteName channel depictorName"
            /home/awips/bin/chgattr.py -f $ncname -a satelliteName -n "GOES Imager"
            /home/awips/bin/chgattr.py -f $ncname -a channel -n "NESDIS QPE 012"
            /home/awips/bin/chgattr.py -f $ncname -a depictorName -n "alaskaRegion"
         elif [ "$prodtype" = "sfr.gz" ]
         then
            echo "Change Attribute: satelliteName"
            /home/awips/bin/chgattr.py -f $ncname -a satelliteName -n "POES"
         fi
      elif [ "$prodsrc" = "viirs" ]
      then
         ncname2=$ncname"_leo"
         cp $ncname $ncname2
         echo "Change Attribute: satelliteName"
         /home/awips/bin/chgattr.py -f $ncname2 -a satelliteName -n SPoRT-VIIRS
         echo "mv $ncname2 $ingestDir"
         mv $ncname2 $ingestDir
      elif [ "$prodsrc" = "modis" ]
      then
         ncname2=$ncname"_leo"
         cp $ncname $ncname2
         echo "Change Attribute: satelliteName"
         /home/awips/bin/chgattr.py -f $ncname2 -a satelliteName -n SPoRT-MODIS
         echo "PRODTYPE: $prodtype"
         echo "mv $ncname2 $ingestDir"
         mv $ncname2 $ingestDir
      fi
      mv $ncname $ingestDir
      #cp $ncname $ingestDir
   fi
done 
#
echo "Ingest directory:"
ls $ingestDir
ddtt=`date +%Y%m%d`
echo "===== End GINA product download: `date` ======"
) >> /awips2/edex/logs/edex-ingest-lclregsat-$ddtt".log" 2>&1
#
