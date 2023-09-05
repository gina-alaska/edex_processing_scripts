#!/home/dmmaltos/miniconda3/bin/python3
# Creates plots found at hippy.gina.alaska.edu/distro/stats/awips/

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import glob, os
from datetime import datetime, timedelta

# Creates plot for data volume
def plotDataVolume():
    modis_path = "outputs/modis/"
    avhrr_path = "outputs/avhrr/"
    viirs_path = "outputs/viirs/"
    mosaic_path = "outputs/mosaic/"
    df_modis_list = []
    df_avhrr_list = []
    df_viirs_list = []
    df_mosaic_list = []
    current_date = datetime.now().date() - timedelta(days=1)
    for file in glob.glob(modis_path + "*.csv"):
        df_modis = pd.read_csv(file, parse_dates=['date'])
        if 'total_filesize' in df_modis.columns:
            df_modis_list.append(df_modis)
    for file in glob.glob(avhrr_path + "*.csv"):
        df_avhrr = pd.read_csv(file, parse_dates=['date'])
        if 'total_filesize' in df_avhrr.columns:
            df_avhrr_list.append(df_avhrr)
    for file in glob.glob(viirs_path + "*.csv"):
        df_viirs = pd.read_csv(file, parse_dates=['date'])
        if 'total_filesize' in df_viirs.columns:
            df_viirs_list.append(df_viirs)
    for file in glob.glob(mosaic_path + "*.csv"):
        df_mosaic = pd.read_csv(file, parse_dates=['date'])
        if 'total_filesize' in df_mosaic.columns:
            df_mosaic_list.append(df_mosaic)
    df_modis = pd.concat(df_modis_list)
    df_avhrr = pd.concat(df_avhrr_list)
    df_viirs = pd.concat(df_viirs_list)
    df_mosaic = pd.concat(df_mosaic_list)
    df_modis = df_modis.drop_duplicates(subset='date')
    df_avhrr = df_avhrr.drop_duplicates(subset='date')
    df_viirs = df_viirs.drop_duplicates(subset='date')
    df_mosaic = df_mosaic.drop_duplicates(subset='date')
    df_modis.sort_values(by='date', inplace=True)
    df_avhrr.sort_values(by='date', inplace=True)
    df_viirs.sort_values(by='date', inplace=True)
    df_mosaic.sort_values(by='date', inplace=True)
    modis_dates = df_modis['date']
    modis_data = df_modis['total_filesize']
    avhrr_dates = df_avhrr['date']
    avhrr_data = df_avhrr['total_filesize']
    viirs_dates = df_viirs['date']
    viirs_data = df_viirs['total_filesize']
    mosaic_dates = df_mosaic['date']
    mosaic_data = df_mosaic['total_filesize']
    # Plotting
    fig, ax = plt.subplots()
    if not df_modis.empty:
        ax.plot(modis_dates, modis_data, label='MODIS')
    if not df_avhrr.empty:
        ax.plot(avhrr_dates, avhrr_data, label='AVHRR')
    if not df_viirs.empty:
        ax.plot(viirs_dates, viirs_data, label='VIIRS')
    if not df_mosaic.empty:
        ax.plot(mosaic_dates, mosaic_data, label='MOSAIC')
    # Customize the plot
    ax.set_title(f"Total NRT Data Volume Received in AWIPS")
    ax.set_xlabel('Date')
    ax.set_ylabel('Data Volume (GB)')
    ax.legend()
    ax.set_ylim(0, 50)
    # Format the date on the x-axis
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))
    fig.autofmt_xdate()  # Auto-format the x-axis date labels
    # Adjust the figure layout to increase the bottom margin
    fig.tight_layout(rect=[0, 0.01, 1, 1])
    # Generate the filename with the current date - 1
    filename = f"goesr_data_volume.png"
    # Specify the directory path
    directory = "plots/avm/data_volume/"
    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)
    # Save the plot as a PNG file in the specified directory
    filepath = os.path.join(directory, filename)
    plt.savefig(filepath)
    # Display the plot
    plt.show()

# Creates plot of data volume for each data type on seperate lines.
def plotDailyTotalsDataVolumeSeperate():
    dmw_path = "outputs/daily_totals/dmw/"
    goesr_path = "outputs/daily_totals/goesr/"
    griddednucaps_path = "outputs/daily_totals/griddednucaps/"
    pointset_path = "outputs/daily_totals/pointset/"
    regionalsat_path = "outputs/daily_totals/regionalsat/"
    df_dmw_list = []
    df_goesr_list = []
    df_griddednucaps_list = []
    df_pointset_list = []
    df_regionalsat_list = []
    current_date = datetime.now().date() - timedelta(days=1)
    for file in glob.glob(dmw_path + "*.csv"):
        df_dmw = pd.read_csv(file, parse_dates=['date'])
        if 'total_filesize' in df_dmw.columns:
            df_dmw_list.append(df_dmw)
    for file in glob.glob(goesr_path + "*.csv"):
        df_goesr = pd.read_csv(file, parse_dates=['date'])
        if 'total_filesize' in df_goesr.columns:
            df_goesr_list.append(df_goesr)
    for file in glob.glob(griddednucaps_path + "*.csv"):
        df_griddednucaps = pd.read_csv(file, parse_dates=['date'])
        if 'total_filesize' in df_griddednucaps.columns:
            df_griddednucaps_list.append(df_griddednucaps)
    for file in glob.glob(pointset_path + "*.csv"):
        df_pointset = pd.read_csv(file, parse_dates=['date'])
        if 'total_filesize' in df_pointset.columns:
            df_pointset_list.append(df_pointset)
    for file in glob.glob(regionalsat_path + "*.csv"):
        df_regionalsat = pd.read_csv(file, parse_dates=['date'])
        if 'total_filesize' in df_regionalsat.columns:
            df_regionalsat_list.append(df_regionalsat)
    df_dmw = pd.concat(df_dmw_list)
    df_goesr = pd.concat(df_goesr_list)
    df_griddednucaps = pd.concat(df_griddednucaps_list)
    df_pointset = pd.concat(df_pointset_list)
    df_regionalsat = pd.concat(df_regionalsat_list)
    df_dmw = df_dmw.drop_duplicates(subset='date')
    df_goesr = df_goesr.drop_duplicates(subset='date')
    df_griddednucaps = df_griddednucaps.drop_duplicates(subset='date')
    df_pointset = df_pointset.drop_duplicates(subset='date')
    df_regionalsat = df_regionalsat.drop_duplicates(subset='date')
    df_dmw.sort_values(by='date', inplace=True)
    df_goesr.sort_values(by='date', inplace=True)
    df_griddednucaps.sort_values(by='date', inplace=True)
    df_pointset.sort_values(by='date', inplace=True)
    df_regionalsat.sort_values(by='date', inplace=True)
    dmw_dates = df_dmw['date']
    dmw_data = df_dmw['total_filesize']
    goesr_dates = df_goesr['date']
    goesr_data = df_goesr['total_filesize']
    griddednucaps_dates = df_griddednucaps['date']
    griddednucaps_data = df_griddednucaps['total_filesize']
    pointset_dates = df_pointset['date']
    pointset_data = df_pointset['total_filesize']
    regionalsat_dates = df_regionalsat['date']
    regionalsat_data = df_regionalsat['total_filesize']
    # Plotting
    fig, ax = plt.subplots()
    if not df_dmw.empty:
        ax.plot(dmw_dates, dmw_data, label='DMW')
    if not df_goesr.empty:
        ax.plot(goesr_dates, goesr_data, label='GOESR')
    if not df_griddednucaps.empty:
        ax.plot(griddednucaps_dates, griddednucaps_data, label='GRIDDEDNUCAPS')
    if not df_pointset.empty:
        ax.plot(pointset_dates, pointset_data, label='POINTSET')
    if not df_regionalsat.empty:
        ax.plot(regionalsat_dates, regionalsat_data, label='REGIONALSAT')
    # Customize the plot
    ax.set_title(f"NRT Data Volume Received in AWIPS by Data Type")
    ax.set_xlabel('Date')
    ax.set_ylabel('Data Volume (GB)')
    ax.legend()
    # Format the date on the x-axis
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))
    fig.autofmt_xdate()  # Auto-format the x-axis date labels
    # Adjust the figure layout to increase the bottom margin
    fig.tight_layout(rect=[0, 0.01, 1, 1])
    # Generate the filename with the current date - 1
    filename = f"datatype_totals_data_volume_seperate.png"
    # Specify the directory path
    directory = "plots/datatype_totals_data_volume_seperate/"
    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)
    # Save the plot as a PNG file in the specified directory
    filepath = os.path.join(directory, filename)
    plt.savefig(filepath)
    # Display the plot
    plt.show()

# Creates plot of the combined daily total data volume
def plotDailyTotalsDataVolumeCombined():
    dmw_path = "outputs/daily_totals/dmw/"
    goesr_path = "outputs/daily_totals/goesr/"
    griddednucaps_path = "outputs/daily_totals/griddednucaps/"
    pointset_path = "outputs/daily_totals/pointset/"
    regionalsat_path = "outputs/daily_totals/regionalsat/"
    df_dmw_list = []
    df_goesr_list = []
    df_griddednucaps_list = []
    df_pointset_list = []
    df_regionalsat_list = []
    current_date = datetime.now().date() - timedelta(days=1)
    for file in glob.glob(dmw_path + "*.csv"):
        df_dmw = pd.read_csv(file, parse_dates=['date'])
        if 'total_filesize' in df_dmw.columns:
            df_dmw_list.append(df_dmw)       
    for file in glob.glob(goesr_path + "*.csv"):
        df_goesr = pd.read_csv(file, parse_dates=['date'])
        if 'total_filesize' in df_goesr.columns:
            df_goesr_list.append(df_goesr)
            
    for file in glob.glob(griddednucaps_path + "*.csv"):
        df_griddednucaps = pd.read_csv(file, parse_dates=['date'])
        if 'total_filesize' in df_griddednucaps.columns:
            df_griddednucaps_list.append(df_griddednucaps)       
    for file in glob.glob(pointset_path + "*.csv"):
        df_pointset = pd.read_csv(file, parse_dates=['date'])
        if 'total_filesize' in df_pointset.columns:
            df_pointset_list.append(df_pointset)  
    for file in glob.glob(regionalsat_path + "*.csv"):
        df_regionalsat = pd.read_csv(file, parse_dates=['date'])
        if 'total_filesize' in df_regionalsat.columns:
            df_regionalsat_list.append(df_regionalsat)
    df_dmw = pd.concat(df_dmw_list)
    df_goesr = pd.concat(df_goesr_list)
    df_griddednucaps = pd.concat(df_griddednucaps_list)
    df_pointset = pd.concat(df_pointset_list)
    df_regionalsat = pd.concat(df_regionalsat_list)
    df_dmw = df_dmw.drop_duplicates(subset='date')
    df_goesr = df_goesr.drop_duplicates(subset='date')
    df_griddednucaps = df_griddednucaps.drop_duplicates(subset='date')
    df_pointset = df_pointset.drop_duplicates(subset='date')
    df_regionalsat = df_regionalsat.drop_duplicates(subset='date')
    df_dmw.sort_values(by='date', inplace=True)
    df_goesr.sort_values(by='date', inplace=True)
    df_griddednucaps.sort_values(by='date', inplace=True)
    df_pointset.sort_values(by='date', inplace=True)
    df_regionalsat.sort_values(by='date', inplace=True)
    dmw_dates = df_dmw['date']
    dmw_data = df_dmw['total_filesize']
    goesr_dates = df_goesr['date']
    goesr_data = df_goesr['total_filesize']
    griddednucaps_dates = df_griddednucaps['date']
    griddednucaps_data = df_griddednucaps['total_filesize']
    pointset_dates = df_pointset['date']
    pointset_data = df_pointset['total_filesize']
    regionalsat_dates = df_regionalsat['date']
    regionalsat_data = df_regionalsat['total_filesize']
    # Combine all the data frames into a single list
    all_dfs = [df_dmw, df_goesr, df_griddednucaps, df_pointset, df_regionalsat]
    df_combined = pd.DataFrame(columns=['date', 'total_filesize'])
    # Sum the 'total_filesize' for each data frame and add to the combined DataFrame
    for df in all_dfs:
        if not df.empty:
            df_filtered = df.drop_duplicates(subset='date')
            df_sum = df_filtered.groupby('date')['total_filesize'].sum().reset_index()
            df_combined = pd.concat([df_combined, df_sum])     
    df_combined = df_combined.groupby('date')['total_filesize'].sum().reset_index()
    # Sort the combined data frame by date
    df_combined.sort_values(by='date', inplace=True)
    # Plotting
    fig, ax = plt.subplots()
    if not df_combined.empty:
        ax.plot(df_combined['date'], df_combined['total_filesize'], label='TOTAL', color='black')
    if not df_dmw.empty:
        ax.plot(dmw_dates, dmw_data, label='DMW')
    if not df_goesr.empty:
        ax.plot(goesr_dates, goesr_data, label='GOESR')
    if not df_griddednucaps.empty:
        ax.plot(griddednucaps_dates, griddednucaps_data, label='GRIDDEDNUCAPS')
    if not df_pointset.empty:
        ax.plot(pointset_dates, pointset_data, label='POINTSET')
    if not df_regionalsat.empty:
        ax.plot(regionalsat_dates, regionalsat_data, label='REGIONALSAT')
    # Customize the plot
    ax.set_title(f"Total NRT Data Volume Received in AWIPS")
    ax.set_xlabel('Date')
    ax.set_ylabel('Data Volume (GB)')
    ax.legend(prop={'size': 6})
    # Format the date on the x-axis
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))
    fig.autofmt_xdate()  # Auto-format the x-axis date labels
    # Adjust the figure layout to increase the bottom margin
    fig.tight_layout(rect=[0, 0.01, 1, 1])
    # Generate the filename with the current date - 1
    current_date = datetime.now().date() - timedelta(days=1)
    filename = f"datatype_totals_data_volume_combined.png"
    # Specify the directory path
    directory = "plots/datatype_totals_data_volume_combined/"

    # Save the plot as a PNG file in the specified directory
    filepath = os.path.join(directory, filename)
    plt.savefig(filepath)
    # Display the plot
    plt.show()

# Creates plot for all latency
def plotAllLatency():
    modis_path = "outputs/modis/"
    avhrr_path = "outputs/avhrr/"
    viirs_path = "outputs/viirs/"
    mosaic_path = "outputs/mosaic/"
    df_modis_list = []
    df_avhrr_list = []
    df_viirs_list = []
    df_mosaic_list = []
    current_date = datetime.now().date() - timedelta(days=1)
    for file in glob.glob(modis_path + "*.csv"):
        df_modis = pd.read_csv(file, parse_dates=['date'])
        if 'average_latency' in df_modis.columns:
            df_modis_list.append(df_modis)
    for file in glob.glob(avhrr_path + "*.csv"):
        df_avhrr = pd.read_csv(file, parse_dates=['date'])
        if 'average_latency' in df_avhrr.columns:
            df_avhrr_list.append(df_avhrr)
    for file in glob.glob(viirs_path + "*.csv"):
        df_viirs = pd.read_csv(file, parse_dates=['date'])
        if 'average_latency' in df_viirs.columns:
            df_viirs_list.append(df_viirs)
    for file in glob.glob(mosaic_path + "*.csv"):
        df_mosaic = pd.read_csv(file, parse_dates=['date'])
        if 'average_latency' in df_mosaic.columns:
            df_mosaic_list.append(df_mosaic)
    # Concatenate all dataframes into a single dataframe
    df_modis = pd.concat(df_modis_list)
    df_avhrr = pd.concat(df_avhrr_list)
    df_viirs = pd.concat(df_viirs_list)
    df_mosaic = pd.concat(df_mosaic_list)
    # Drop duplicate values based on the 'date' column
    df_modis = df_modis.drop_duplicates(subset='date')
    df_avhrr = df_avhrr.drop_duplicates(subset='date')
    df_viirs = df_viirs.drop_duplicates(subset='date')
    df_mosaic = df_mosaic.drop_duplicates(subset='date')
    # Sort the dataframes by date
    df_modis.sort_values(by='date', inplace=True)
    df_avhrr.sort_values(by='date', inplace=True)
    df_viirs.sort_values(by='date', inplace=True)
    df_mosaic.sort_values(by='date', inplace=True)
    # Extract the desired columns
    modis_dates = df_modis['date']
    modis_avg_data = df_modis['average_latency']
    modis_min_data = df_modis['minimum_latency']
    modis_max_data = df_modis['maximum_latency']
    avhrr_dates = df_avhrr['date']
    avhrr_avg_data = df_avhrr['average_latency']
    avhrr_min_data = df_avhrr['minimum_latency']
    avhrr_max_data = df_avhrr['maximum_latency']
    viirs_dates = df_viirs['date']
    viirs_avg_data = df_viirs['average_latency']
    viirs_min_data = df_viirs['minimum_latency']
    viirs_max_data = df_viirs['maximum_latency']
    mosaic_dates = df_mosaic['date']
    mosaic_avg_data = df_mosaic['average_latency']
    mosaic_min_data = df_mosaic['minimum_latency']
    mosaic_max_data = df_mosaic['maximum_latency']
    # Plotting
    fig, ax = plt.subplots()
    if not df_modis.empty:
        ax.plot(modis_dates, modis_avg_data, label='MODIS (Average)', linestyle='-', color='red')
        ax.plot(modis_dates, modis_min_data, label='MODIS (Minimum)', linestyle='--', color='red')
        ax.plot(modis_dates, modis_max_data, label='MODIS (Maximum)', linestyle=':', color='red')
    if not df_avhrr.empty:
        ax.plot(avhrr_dates, avhrr_avg_data, label='AVHRR (Average)', linestyle='-', color='green')
        ax.plot(avhrr_dates, avhrr_min_data, label='AVHRR (Minimum)', linestyle='--', color='green')
        ax.plot(avhrr_dates, avhrr_max_data, label='AVHRR (Maximum)', linestyle=':', color='green')
    if not df_viirs.empty:
        ax.plot(viirs_dates, viirs_avg_data, label='VIIRS (Average)', linestyle='-', color='blue')
        ax.plot(viirs_dates, viirs_min_data, label='VIIRS (Minimum)', linestyle='--', color='blue')
        ax.plot(viirs_dates, viirs_max_data, label='VIIRS (Maximum)', linestyle=':', color='blue')
    if not df_mosaic.empty:
        ax.plot(mosaic_dates, mosaic_avg_data, label='MOSAIC (Average)', linestyle='-', color='black')
        ax.plot(mosaic_dates, mosaic_min_data, label='MOSAIC (Minimum)', linestyle='--', color='black')
        ax.plot(mosaic_dates, mosaic_max_data, label='MOSAIC (Maximum)', linestyle=':', color='black')
    # Customize the plot
    ax.set_title(f"Total NRT Product Latency: Pass Acquisition to AWIPS Ingest")
    ax.set_xlabel('Date')
    ax.set_ylabel('Latency (Minutes)')
    ax.legend(prop={'size': 6})
    ax.set_ylim(0, 100)
    # Format the date on the x-axis
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))
    fig.autofmt_xdate()  # Auto-format the x-axis date labels
    # Adjust the figure layout to increase the bottom margin
    fig.tight_layout(rect=[0, 0.01, 1, 1])
    # Generate the filename with the current date - 1
    filename = f"total_nrt_latency.png"
    # Specify the directory path
    directory = "plots/avm/all_latency/"
    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)
    # Save the plot as a PNG file in the specified directory
    filepath = os.path.join(directory, filename)
    plt.savefig(filepath)
    # Display the plot
    plt.show()

# Creates plot for average latency
def plotAverageLatency():
    modis_path = "outputs/modis/"
    avhrr_path = "outputs/avhrr/"
    viirs_path = "outputs/viirs/"
    df_modis_list = []
    df_avhrr_list = []
    df_viirs_list = []
    current_date = datetime.now().date() - timedelta(days=1)
    for file in glob.glob(modis_path + "*.csv"):
        df_modis = pd.read_csv(file, parse_dates=['date'])
        if 'average_latency' in df_modis.columns:
            df_modis_list.append(df_modis)
    for file in glob.glob(avhrr_path + "*.csv"):
        df_avhrr = pd.read_csv(file, parse_dates=['date'])
        if 'average_latency' in df_avhrr.columns:
            df_avhrr_list.append(df_avhrr)
    for file in glob.glob(viirs_path + "*.csv"):
        df_viirs = pd.read_csv(file, parse_dates=['date'])
        if 'average_latency' in df_viirs.columns:
            df_viirs_list.append(df_viirs)
    # Concatenate all dataframes into a single dataframe
    df_modis = pd.concat(df_modis_list)
    df_avhrr = pd.concat(df_avhrr_list)
    df_viirs = pd.concat(df_viirs_list)
    # Drop duplicate values based on the 'date' column
    df_modis = df_modis.drop_duplicates(subset='date')
    df_avhrr = df_avhrr.drop_duplicates(subset='date')
    df_viirs = df_viirs.drop_duplicates(subset='date')
    # Sort the dataframes by date
    df_modis.sort_values(by='date', inplace=True)
    df_avhrr.sort_values(by='date', inplace=True)
    df_viirs.sort_values(by='date', inplace=True)
    # Extract the desired columns
    modis_dates = df_modis['date']
    modis_data = df_modis['average_latency']
    avhrr_dates = df_avhrr['date']
    avhrr_data = df_avhrr['average_latency']
    viirs_dates = df_viirs['date']
    viirs_data = df_viirs['average_latency']
    # Plotting
    fig, ax = plt.subplots()
    if not df_modis.empty:
        ax.plot(modis_dates, modis_data, label='MODIS')
    if not df_avhrr.empty:
        ax.plot(avhrr_dates, avhrr_data, label='AVHRR')
    if not df_viirs.empty:
        ax.plot(viirs_dates, viirs_data, label='VIIRS')
    # Customize the plot
    ax.set_title(f"Daily Average Latency (LDM - Pass Start)")
    ax.set_xlabel('Date')
    ax.set_ylabel('Latency (Minutes)')
    ax.legend()
    # Format the date on the x-axis
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))
    fig.autofmt_xdate()  # Auto-format the x-axis date labels
    # Adjust the figure layout to increase the bottom margin
    fig.tight_layout(rect=[0, 0.01, 1, 1])
    # Generate the filename with the current date - 1
    filename = f"average_latency.png"
    # Specify the directory path
    directory = "plots/avm/average_latency/"
    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)
    # Save the plot as a PNG file in the specified directory
    filepath = os.path.join(directory, filename)
    plt.savefig(filepath)
    # Display the plot
    plt.show()
    
# Call the functions to create the graphs
plotDataVolume()
plotAverageLatency()
plotAllLatency()
plotDailyTotalsDataVolumeSeperate()
plotDailyTotalsDataVolumeCombined()