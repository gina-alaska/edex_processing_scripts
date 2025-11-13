#!/bin/bash
##########################################
pscnt=`ps -ef | grep ldmd | grep -v color | wc -l`
if [ $pscnt -gt 0 ]
then
   echo "LDM running: $pscnt processes"
else
   echo "LDM not running"
fi


