#!/bin/bash

# Set the current date in the desired format
current_date=$(date -d "1 day ago" +%Y%m%d)

# Copy and rename the files
scp dmmaltos@edex.x.gina.alaska.edu:/home/dmmaltos/dev/avhrrlatency.csv /mnt/noaa-case-study-data/latencystats/outputs/avhrr/avhrr_"$current_date".csv
scp dmmaltos@edex.x.gina.alaska.edu:/home/dmmaltos/dev/modislatency.csv /mnt/noaa-case-study-data/latencystats/outputs/modis/modis_"$current_date".csv
scp dmmaltos@edex.x.gina.alaska.edu:/home/dmmaltos/dev/viirslatency.csv /mnt/noaa-case-study-data/latencystats/outputs/viirs/viirs_"$current_date".csv
scp dmmaltos@edex.x.gina.alaska.edu:/home/dmmaltos/dev/mosaiclatency.csv /mnt/noaa-case-study-data/latencystats/outputs/mosaic/mosaic_"$current_date".csv
scp dmmaltos@edex.x.gina.alaska.edu:/home/dmmaltos/dev/datatype_totals/dmw.csv /mnt/noaa-case-study-data/latencystats/outputs/daily_totals/dmw/dmw_"$current_date".csv
scp dmmaltos@edex.x.gina.alaska.edu:/home/dmmaltos/dev/datatype_totals/goesr.csv /mnt/noaa-case-study-data/latencystats/outputs/daily_totals/goesr/goesr_"$current_date".csv
scp dmmaltos@edex.x.gina.alaska.edu:/home/dmmaltos/dev/datatype_totals/griddednucaps.csv /mnt/noaa-case-study-data/latencystats/outputs/daily_totals/griddednucaps/griddednucaps_"$current_date".csv
scp dmmaltos@edex.x.gina.alaska.edu:/home/dmmaltos/dev/datatype_totals/pointset.csv /mnt/noaa-case-study-data/latencystats/outputs/daily_totals/pointset/pointset_"$current_date".csv
scp dmmaltos@edex.x.gina.alaska.edu:/home/dmmaltos/dev/datatype_totals/regionalsat.csv /mnt/noaa-case-study-data/latencystats/outputs/daily_totals/regionalsat/regionalsat_"$current_date".csv
scp dmmaltos@edex.x.gina.alaska.edu:/home/dmmaltos/dev/longwave_ir_bands/avhrr.csv /mnt/noaa-case-study-data/latencystats/outputs/longwave_ir/avhrr/avhrr_longwave_ir_"$current_date".csv
scp dmmaltos@edex.x.gina.alaska.edu:/home/dmmaltos/dev/longwave_ir_bands/modis.csv /mnt/noaa-case-study-data/latencystats/outputs/longwave_ir/modis/modis_longwave_ir_"$current_date".csv
scp dmmaltos@edex.x.gina.alaska.edu:/home/dmmaltos/dev/longwave_ir_bands/viirs.csv /mnt/noaa-case-study-data/latencystats/outputs/longwave_ir/viirs/viirs_longwave_ir_"$current_date".csv