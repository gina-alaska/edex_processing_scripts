#!/home/dmmaltos/miniconda3/bin/python3
# Creates appended CSV total_processing_time_by_day.csv found at hippy.gina.alaska.edu/distro/stats/

import os
import pandas as pd

directory = '/mnt/raid/stockpile/distro/stats'
proccesing_time_files = [file for file in os.listdir(directory) if file.endswith('total_processing_time_by_day.csv')]

combined_dfs = []
skip_first = True
count = 0

for proccesing_time_file in proccesing_time_files:
    count += 1
    if skip_first and count == 1:
        skip_first = False
        continue
    if count == len(proccesing_time_files):
        break
    file_path = os.path.join(directory, proccesing_time_file)
    df = pd.read_csv(file_path)
    df['source'] = os.path.splitext(proccesing_time_file)[0]
    combined_dfs.append(df)

combined_df = pd.concat(combined_dfs, ignore_index=True)
 
output_csv_file = 'total_processing_time_by_day_combined.csv'
combined_df.to_csv(output_csv_file, index=False)