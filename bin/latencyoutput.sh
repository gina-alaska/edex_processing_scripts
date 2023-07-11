#!/bin/bash

# Assign output file paths.
viirs_output_file="/home/dmmaltos/dev/viirslatency.csv"
modis_output_file="/home/dmmaltos/dev/modislatency.csv"
avhrr_output_file="/home/dmmaltos/dev/avhrrlatency.csv"

# Write the CSV headers.
echo "date,products_found,total_filesize,average_latency,maximum_latency,minimum_latency" > "$viirs_output_file"
echo "date,products_found,total_filesize,average_latency,maximum_latency,minimum_latency" > "$modis_output_file"
echo "date,products_found,total_filesize,average_latency,maximum_latency,minimum_latency" > "$avhrr_output_file"

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
