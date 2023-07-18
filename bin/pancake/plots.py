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
    df_modis_list = []
    df_avhrr_list = []
    df_viirs_list = []
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
    df_modis = pd.concat(df_modis_list)
    df_avhrr = pd.concat(df_avhrr_list)
    df_viirs = pd.concat(df_viirs_list)
    df_modis = df_modis.drop_duplicates(subset='date')
    df_avhrr = df_avhrr.drop_duplicates(subset='date')
    df_viirs = df_viirs.drop_duplicates(subset='date')
    df_modis.sort_values(by='date', inplace=True)
    df_avhrr.sort_values(by='date', inplace=True)
    df_viirs.sort_values(by='date', inplace=True)
    modis_dates = df_modis['date']
    modis_data = df_modis['total_filesize']
    avhrr_dates = df_avhrr['date']
    avhrr_data = df_avhrr['total_filesize']
    viirs_dates = df_viirs['date']
    viirs_data = df_viirs['total_filesize']
    # Plotting
    fig, ax = plt.subplots()
    if not df_modis.empty:
        ax.plot(modis_dates, modis_data, label='MODIS')
    if not df_avhrr.empty:
        ax.plot(avhrr_dates, avhrr_data, label='AVHRR')
    if not df_viirs.empty:
        ax.plot(viirs_dates, viirs_data, label='VIIRS')
    # Customize the plot
    ax.set_title(f"Total NRT Data Volume Received in AWIPS")
    ax.set_xlabel('Date')
    ax.set_ylabel('Data Volume (MB)')
    ax.legend()
    # Format the date on the x-axis
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    fig.autofmt_xdate()  # Auto-format the x-axis date labels
    # Adjust the figure layout to increase the bottom margin
    fig.tight_layout(rect=[0, 0.01, 1, 1])
    # Generate the filename with the current date - 1
    filename = f"data_volume_{current_date.strftime('%Y%m%d')}.png"
    # Specify the directory path
    directory = "plots/avm/data_volume/"
    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)
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
    # Customize the plot
    ax.set_title(f"Total NRT Product Latency: Pass Acquisition to AWIPS Ingest")
    ax.set_xlabel('Date')
    ax.set_ylabel('Latency (Minutes)')
    ax.legend(prop={'size': 6})
    ax.set_ylim(0, 100)
    # Format the date on the x-axis
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    fig.autofmt_xdate()  # Auto-format the x-axis date labels
    # Adjust the figure layout to increase the bottom margin
    fig.tight_layout(rect=[0, 0.01, 1, 1])
    # Generate the filename with the current date - 1
    filename = f"all_latency_{current_date.strftime('%Y%m%d')}.png"
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
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    fig.autofmt_xdate()  # Auto-format the x-axis date labels
    # Adjust the figure layout to increase the bottom margin
    fig.tight_layout(rect=[0, 0.01, 1, 1])
    # Generate the filename with the current date - 1
    filename = f"average_latency_{current_date.strftime('%Y%m%d')}.png"
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