#!/bin/bash
source /home/dmmaltos/miniconda3/bin/activate
conda activate /home/dmmaltos/miniconda3
cd /mnt/noaa-case-study-data/latencystats
python3 /mnt/noaa-case-study-data/latencystats/plots.py
conda deactivate
cp /mnt/noaa-case-study-data/latencystats/plots/avm/data_volume/goesr_data_volume.png /mnt/raid/stockpile/distro/stats/awips
cp /mnt/noaa-case-study-data/latencystats/plots/datatype_totals_data_volume_seperate/datatype_totals_data_volume_seperate.png /mnt/raid/stockpile/distro/stats/awips
cp /mnt/noaa-case-study-data/latencystats/plots/datatype_totals_data_volume_combined/datatype_totals_data_volume_combined.png /mnt/raid/stockpile/distro/stats/awips
cp /mnt/noaa-case-study-data/latencystats/plots/avm/all_latency/total_nrt_latency.png /mnt/raid/stockpile/distro/stats/awips
