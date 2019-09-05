#!/bin/bash
##########################################################
# wget - pull files with wget 
##########################################################
#
while [ "${URL[0]}" != "q" ]
do
   echo -n "Enter URL (or q to quit): "
   read -a URL
   #echo "${URL[@]}"
   if [ "${URL[0]}" != "q" ]
   then
      wget --user=alaska-carl.dierking --password='n0rain4Me' "${URL[@]}"
   fi
done
#

