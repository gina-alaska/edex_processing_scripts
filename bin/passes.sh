#!/bin/bash
####################
if [ "$1" = "-y" ]
then 
   # display passes from yesterday
   yday=`date +%d --date='yesterday'`
   echo "NOAA-21 Passes for yesterday ($yday)"
   /home/awips/bin/showdstore.py -t goesr -m noaa21_viirs_i05 -d $yday | cut -d'_' -f 12- | grep 2023 | grep "_" | sed 's/.nc//'| sort -r | uniq
   echo "NOAA020 Passes for yesterday ($yday)"
   /home/awips/bin/showdstore.py -t goesr -m noaa20_viirs_i05 -d $yday | cut -d'_' -f 12- | grep 2023 | grep "_" | sed 's/.nc//'| sort -r | uniq
   echo "SNPP Passes for yesterday ($yday)"
   /home/awips/bin/showdstore.py -t goesr -m npp_viirs_i05 -d $yday | cut -d'_' -f 12- | grep 2023 | grep "_" | sed 's/.nc//' | sort -r | uniq
else
   # display passes for today
   echo "NOAA-21 Passes for today"
   /home/awips/bin/showdstore.py -t goesr -m noaa21_viirs_i05 | cut -d'_' -f 12- | grep 2023 | grep "_" | sed 's/.nc//'| sort -r | uniq
   echo "NOAA-20 Passes for today"
   /home/awips/bin/showdstore.py -t goesr -m noaa20_viirs_i05 | cut -d'_' -f 12- | grep 2023 | grep "_" | sed 's/.nc//'| sort -r | uniq
   echo "SNPP Passes for today"
   /home/awips/bin/showdstore.py -t goesr -m npp_viirs_i05 | cut -d'_' -f 12- | grep 2023 | grep "_" | sed 's/.nc//' | sort -r | uniq
fi

