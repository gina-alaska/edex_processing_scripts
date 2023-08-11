#!/bin/bash

# Assign output file paths.
viirs_output_file="/home/dmmaltos/dev/viirslatency.csv"
modis_output_file="/home/dmmaltos/dev/modislatency.csv"
avhrr_output_file="/home/dmmaltos/dev/avhrrlatency.csv"
dmw_output_file="/home/dmmaltos/dev/datatype_totals/dmw.csv"
goesr_output_file="/home/dmmaltos/dev/datatype_totals/goesr.csv"
griddednucaps_output_file="/home/dmmaltos/dev/datatype_totals/griddednucaps.csv"
pointset_output_file="/home/dmmaltos/dev/datatype_totals/pointset.csv"
regionalsat_output_file="/home/dmmaltos/dev/datatype_totals/regionalsat.csv"

# Write the CSV headers.
echo "date,products_found,total_filesize,average_latency,maximum_latency,minimum_latency" > "$viirs_output_file"
echo "date,products_found,total_filesize,average_latency,maximum_latency,minimum_latency" > "$modis_output_file"
echo "date,products_found,total_filesize,average_latency,maximum_latency,minimum_latency" > "$avhrr_output_file"
echo "date,products_found,total_filesize,average_latency,maximum_latency,minimum_latency" > "$dmw_output_file"
echo "date,products_found,total_filesize,average_latency,maximum_latency,minimum_latency" > "$goesr_output_file"
echo "date,products_found,total_filesize,average_latency,maximum_latency,minimum_latency" > "$griddednucaps_output_file"
echo "date,products_found,total_filesize,average_latency,maximum_latency,minimum_latency" > "$pointset_output_file"
echo "date,products_found,total_filesize,average_latency,maximum_latency,minimum_latency" > "$regionalsat_output_file"

# Run the command for viirs and append the data to the respective CSV files.
viirs_output=$(python3 /home/dmmaltos/dev/showdstore.py -t goesr -m viirs -lo)
viirs_date=$(echo "$viirs_output" | sed -n '1p')
viirs_products_found=$(echo "$viirs_output" | sed -n '2p' | awk '{print $3}')
viirs_total_filesize=$(echo "$viirs_output" | sed -n '3p' | awk '{print $4}')
viirs_average_latency=$(echo "$viirs_output" | sed -n '4p' | awk '{print $3}')
viirs_maximum_latency=$(echo "$viirs_output" | sed -n '5p' | awk '{print $3}')
viirs_minimum_latency=$(echo "$viirs_output" | sed -n '6p' | awk '{print $3}')
echo "$viirs_date,$viirs_products_found,$viirs_total_filesize,$viirs_average_latency,$viirs_maximum_latency,$viirs_minimum_latency" >> "$viirs_output_file"

# Run the command for modis and append the data to the respective CSV files.
modis_output=$(python3 /home/dmmaltos/dev/showdstore.py -t goesr -m modis -lo)
modis_date=$(echo "$modis_output" | sed -n '1p')
modis_products_found=$(echo "$modis_output" | sed -n '2p' | awk '{print $3}')
modis_total_filesize=$(echo "$modis_output" | sed -n '3p' | awk '{print $4}')
modis_average_latency=$(echo "$modis_output" | sed -n '4p' | awk '{print $3}')
modis_maximum_latency=$(echo "$modis_output" | sed -n '5p' | awk '{print $3}')
modis_minimum_latency=$(echo "$modis_output" | sed -n '6p' | awk '{print $3}')
echo "$modis_date,$modis_products_found,$modis_total_filesize,$modis_average_latency,$modis_maximum_latency,$modis_minimum_latency" >> "$modis_output_file"

# Run the command for avhrr and append the data to the respective CSV files.
avhrr_output=$(python3 /home/dmmaltos/dev/showdstore.py -t goesr -m avhrr -lo)
avhrr_date=$(echo "$avhrr_output" | sed -n '1p')
avhrr_products_found=$(echo "$avhrr_output" | sed -n '2p' | awk '{print $3}')
avhrr_total_filesize=$(echo "$avhrr_output" | sed -n '3p' | awk '{print $4}')
avhrr_average_latency=$(echo "$avhrr_output" | sed -n '4p' | awk '{print $3}')
avhrr_maximum_latency=$(echo "$avhrr_output" | sed -n '5p' | awk '{print $3}')
avhrr_minimum_latency=$(echo "$avhrr_output" | sed -n '6p' | awk '{print $3}')
echo "$avhrr_date,$avhrr_products_found,$avhrr_total_filesize,$avhrr_average_latency,$avhrr_maximum_latency,$avhrr_minimum_latency" >> "$avhrr_output_file"

# Run the command for dmw and append the data to the respective CSV files.
dmw_output=$(python3 /home/dmmaltos/dev/showdstore.py -t dmw -lo)
dmw_date=$(echo "$dmw_output" | sed -n '1p')
dmw_products_found=$(echo "$dmw_output" | sed -n '2p' | awk '{print $3}')
dmw_total_filesize=$(echo "$dmw_output" | sed -n '3p' | awk '{print $4}')
dmw_average_latency=$(echo "$dmw_output" | sed -n '4p' | awk '{print $3}')
dmw_maximum_latency=$(echo "$dmw_output" | sed -n '5p' | awk '{print $3}')
dmw_minimum_latency=$(echo "$dmw_output" | sed -n '6p' | awk '{print $3}')
echo "$dmw_date,$dmw_products_found,$dmw_total_filesize,$dmw_average_latency,$dmw_maximum_latency,$dmw_minimum_latency" >> "$dmw_output_file"

# Run the command for goesr and append the data to the respective CSV files.
goesr_output=$(python3 /home/dmmaltos/dev/showdstore.py -t goesr -e WCONUS -lo)
goesr_date=$(echo "$goesr_output" | sed -n '1p')
goesr_products_found=$(echo "$goesr_output" | sed -n '2p' | awk '{print $3}')
goesr_total_filesize=$(echo "$goesr_output" | sed -n '3p' | awk '{print $4}')
goesr_average_latency=$(echo "$goesr_output" | sed -n '4p' | awk '{print $3}')
goesr_maximum_latency=$(echo "$goesr_output" | sed -n '5p' | awk '{print $3}')
goesr_minimum_latency=$(echo "$goesr_output" | sed -n '6p' | awk '{print $3}')
echo "$goesr_date,$goesr_products_found,$goesr_total_filesize,$goesr_average_latency,$goesr_maximum_latency,$goesr_minimum_latency" >> "$goesr_output_file"

# Run the command for griddednucaps and append the data to the respective CSV files.
griddednucaps_output=$(python3 /home/dmmaltos/dev/showdstore.py -t griddednucaps -lo)
griddednucaps_date=$(echo "$griddednucaps_output" | sed -n '1p')
griddednucaps_products_found=$(echo "$griddednucaps_output" | sed -n '2p' | awk '{print $3}')
griddednucaps_total_filesize=$(echo "$griddednucaps_output" | sed -n '3p' | awk '{print $4}')
griddednucaps_average_latency=$(echo "$griddednucaps_output" | sed -n '4p' | awk '{print $3}')
griddednucaps_maximum_latency=$(echo "$griddednucaps_output" | sed -n '5p' | awk '{print $3}')
griddednucaps_minimum_latency=$(echo "$griddednucaps_output" | sed -n '6p' | awk '{print $3}')
echo "$griddednucaps_date,$griddednucaps_products_found,$griddednucaps_total_filesize,$griddednucaps_average_latency,$griddednucaps_maximum_latency,$griddednucaps_minimum_latency" >> "$griddednucaps_output_file"

# Run the command for pointset and append the data to the respective CSV files.
pointset_output=$(python3 /home/dmmaltos/dev/showdstore.py -t pointset -lo)
pointset_date=$(echo "$pointset_output" | sed -n '1p')
pointset_products_found=$(echo "$pointset_output" | sed -n '2p' | awk '{print $3}')
pointset_total_filesize=$(echo "$pointset_output" | sed -n '3p' | awk '{print $4}')
pointset_average_latency=$(echo "$pointset_output" | sed -n '4p' | awk '{print $3}')
pointset_maximum_latency=$(echo "$pointset_output" | sed -n '5p' | awk '{print $3}')
pointset_minimum_latency=$(echo "$pointset_output" | sed -n '6p' | awk '{print $3}')
echo "$pointset_date,$pointset_products_found,$pointset_total_filesize,$pointset_average_latency,$pointset_maximum_latency,$pointset_minimum_latency" >> "$pointset_output_file"

# Run the command for regionalsat and append the data to the respective CSV files.
regionalsat_output=$(python3 /home/dmmaltos/dev/showdstore.py -t regionalsat -e sport -lo)
regionalsat_date=$(echo "$regionalsat_output" | sed -n '1p')
regionalsat_products_found=$(echo "$regionalsat_output" | sed -n '2p' | awk '{print $3}')
regionalsat_total_filesize=$(echo "$regionalsat_output" | sed -n '3p' | awk '{print $4}')
regionalsat_average_latency=$(echo "$regionalsat_output" | sed -n '4p' | awk '{print $3}')
regionalsat_maximum_latency=$(echo "$regionalsat_output" | sed -n '5p' | awk '{print $3}')
regionalsat_minimum_latency=$(echo "$regionalsat_output" | sed -n '6p' | awk '{print $3}')
echo "$regionalsat_date,$regionalsat_products_found,$regionalsat_total_filesize,$regionalsat_average_latency,$regionalsat_maximum_latency,$regionalsat_minimum_latency" >> "$regionalsat_output_file"