#!/bin/bash

# Assign output file path.
viirs_output_file="/home/dmmaltos/dev/viirslatency.out"
modis_output_file="/home/dmmaltos/dev/modislatency.out"
avhrr_output_file="/home/dmmaltos/dev/avhrrlatency.out"

# Create output file with latency summary for for viirs, modis, and avhrr.
python showdstore.py -t goesr -m viirs -lo > "$viirs_output_file"
python showdstore.py -t goesr -m modis -lo > "$modis_output_file"
python showdstore.py -t goesr -m avhrr -lo > "$avhrr_output_file"
