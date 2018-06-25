#!/bin/bash
if [ "X$1" = "X" ]
then
   echo "Missing argument!"
   echo "Syntax: ldmqueue.sh match-pattern"
   exit
fi
pqcat -p "$1" -v /opt/ldm/var/queues/ldm.pq > /dev/null

