# logparser.py
# created 9/12/2023
# used for parsing a csv log for raw data going from the antenna to aws
# reads a csv using -r argument followed by the csv filename parses the arival time and creation time from @timestamp and @message columns of csv
# ex. python logparser.py -r logs-insights-results.csv

# import libraries 
import argparse
import pandas as pd
import numpy as np
import re  # import the 're' module for regular expressions

# function to extract and store as strings
def extract_large_int(text):
    match = re.search(r'c(\d+)_drlu_ops.h5', text)
    if match:
        return match.group(1)
    else:
        return None

# argument parser
parser = argparse.ArgumentParser(description='Parse and process a CSV file.')
parser.add_argument('-r', '--input-file', required=True, help='Input CSV file to read')
args = parser.parse_args()

# read the csv file into a pandas dataframe
try:
    df = pd.read_csv(args.input_file)
except FileNotFoundError:
    print(f"File '{args.input_file}' not found.")
    exit(1)

# extract arrival time and creation time
df['arrival_time'] = pd.to_datetime(df['@timestamp'], format='%Y-%m-%d %H:%M:%S.%f')
df['creation_time'] = df['@message'].apply(extract_large_int)
df['creation_time'] = pd.to_datetime(df['creation_time'], format='%Y%m%d%H%M%S%f')

# calculate the time difference as a timedelta
df['time_difference'] = df['arrival_time'] - df['creation_time']

# convert the time difference to seconds (float)
df['time_difference_in_s'] = df['time_difference'].dt.total_seconds()

# output a new csv file: parsed_logs.csv
output_file = 'parsed_logs.csv'
df.to_csv(output_file, index=False)
print(f"Processed data saved to '{output_file}'")
