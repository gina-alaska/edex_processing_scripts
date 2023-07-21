#!/bin/bash
source /home/dmmaltos/miniconda3/bin/activate
conda activate /home/dmmaltos/miniconda3
cd /mnt/noaa-case-study-data/latencystats
python3 /mnt/noaa-case-study-data/latencystats/plots.py
conda deactivate
