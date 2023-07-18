#!/bin/bash

# Set the current date in the desired format
current_date=$(date -d "1 day ago" +%Y%m%d)

# Copy and rename the files
scp dmmaltos@edex.x.gina.alaska.edu:/home/dmmaltos/dev/avhrrlatency.csv /mnt/noaa-case-study-data/latencystats/outputs/avhrr/avhrr_"$current_date".csv
scp dmmaltos@edex.x.gina.alaska.edu:/home/dmmaltos/dev/modislatency.csv /mnt/noaa-case-study-data/latencystats/outputs/modis/modis_"$current_date".csv
scp dmmaltos@edex.x.gina.alaska.edu:/home/dmmaltos/dev/viirslatency.csv /mnt/noaa-case-study-data/latencystats/outputs/viirs/viirs_"$current_date".csv