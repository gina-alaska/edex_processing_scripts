#!/bin/bash
source /home/dmmaltos/miniconda3/bin/activate
conda activate /home/dmmaltos/miniconda3
cd /mnt/noaa-case-study-data/latencystats
python3 /mnt/noaa-case-study-data/latencystats/total_processing_time.py
conda deactivate
cp /mnt/noaa-case-study-data/latencystats/total_processing_time_by_day_combined.csv /mnt/raid/stockpile/distro/stats