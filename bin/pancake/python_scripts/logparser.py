# logparser.py
# created 9/12/2023
# used for parsing a csv log for raw data going from the antenna to aws, then creates plot for parsed csv log.
# reads a csv using -r argument followed by the csv filename parses the arival time and creation time from @timestamp and @message columns of csv
# ex. python logparser.py -r logs-insights-results.csv

# import libraries 
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import re  # import the 're' module for regular expressions

# argument parser
parser = argparse.ArgumentParser(description='Parse and process a CSV file.')
parser.add_argument('-r', '--input-file', required=True, help='Input CSV file to read')
args = parser.parse_args()

# function to extract and store as strings
def extract_large_int(text):
    match = re.search(r'c(\d+)_drlu_ops.h5', text)
    if match:
        return match.group(1)
    else:
        return None

def create_parsed_logs_csv():
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

# creates graph of newly generated parsed_logs.csv file
def graph_parsed_logs():
    df = pd.read_csv("parsed_logs.csv")
    df['date'] = pd.to_datetime(df['@timestamp'], format='%Y-%m-%d %H:%M:%S.%f')
    
    # filter the dataframe for _j01_ and _npp_ entries
    df_j01 = df[df['@message'].str.contains("_j01_")]
    df_npp = df[df['@message'].str.contains("_npp_")]

    # extract the relevant columns
    date_j01 = df_j01['date']
    transfer_time_j01 = df_j01['time_difference_in_s']
    date_npp = df_npp['date']
    transfer_time_npp = df_npp['time_difference_in_s']
    
    # plotting
    fig, ax = plt.subplots()
    
    if not df_j01.empty:
        ax.plot(date_j01, transfer_time_j01, label='NOAA20')  # Label for _j01_ entries
        
    if not df_npp.empty:
        ax.plot(date_npp, transfer_time_npp, label='NPP')  # Label for _npp_ entries

    # customize the plot
    ax.set_title(f"Time to Transfer to AWS")
    ax.set_xlabel('Date')
    ax.set_ylabel('Transfer Time (s)')
    ax.legend()
    
    # format the date on the x-axis
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    fig.autofmt_xdate(rotation=45)  # Auto-format the x-axis date labels
    
    # adjust the figure layout to increase the bottom margin
    fig.tight_layout(rect=[0, 0.01, 1, 1])
    
    filename = "parsed_log_graph.png"
    
    # save the plot as a PNG file in the specified directory
    filepath = os.path.join(filename)
    plt.savefig(filepath)
    
    # Display the plot
    plt.show()
    print(f"Plot saved to '{filename}'")

# call the functions in correct order
create_parsed_logs_csv()
graph_parsed_logs()