#!/home/dmmaltos/miniconda3/bin/python3
# Used to create temperature plots using xmACIS temperature data for determining the dates to set up the new antenna.

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

# Creates plot for College temperature
def plotCollege():
    data_path = "temperature/college.csv"
    df_college = pd.read_csv(data_path)
    df_college['date'] = pd.to_datetime(df_college['date'], format='%m%d')
    date = df_college['date']
    record_low = df_college['record_low']
    average_low = df_college['average_low']
    percent_days_below_20f = df_college['percent_days_below_20f']
    # Plotting
    fig, ax = plt.subplots()
    if not df_college.empty:
        ax.plot(date, record_low, label='Record Low')
    if not df_college.empty:
        ax.plot(date, average_low, label='Average Low')
    if not df_college.empty:
        ax.plot(date, percent_days_below_20f, label='% Days Below -20', color='black')
    # Customize the plot
    ax.set_title(f"Temperature - College, AK")
    ax.set_xlabel('Date')
    ax.set_ylabel('Temperature (°F)')
    ax.legend()
    # Format the date on the x-axis
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    fig.autofmt_xdate(rotation=45)    # Auto-format the x-axis date labels
    # Adjust the figure layout to increase the bottom margin
    fig.tight_layout(rect=[0, 0.01, 1, 1])
    filename = f"college_temperature.png"
    # Specify the directory path
    directory = "temperature/"
    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)
    # Save the plot as a PNG file in the specified directory
    filepath = os.path.join(directory, filename)
    plt.savefig(filepath)
    # Display the plot
    plt.show()
    
# Creates plot for North Pole temperature
def plotNorthPole():
    data_path = "temperature/northpole.csv"
    df_college = pd.read_csv(data_path)
    df_college['date'] = pd.to_datetime(df_college['date'], format='%m%d')
    date = df_college['date']
    record_low = df_college['record_low']
    average_low = df_college['average_low']
    percent_days_below_20f = df_college['percent_days_below_20f']
    # Plotting
    fig, ax = plt.subplots(figsize=(12, 6))
    if not df_college.empty:
        ax.plot(date, record_low, label='Record Low')
    if not df_college.empty:
        ax.plot(date, average_low, label='Average Low')
    if not df_college.empty:
        ax.plot(date, percent_days_below_20f, label='% Days Below -20', color='black')
    # Customize the plot
    ax.set_title(f"Temperature - North Pole, AK")
    ax.set_xlabel('Date')
    ax.set_ylabel('Temperature (°F)')
    ax.legend()
    # Format the date on the x-axis
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    fig.autofmt_xdate(rotation=45)  # Auto-format the x-axis date labels
    # Adjust the figure layout to increase the bottom margin
   # fig.tight_layout(rect=[0, 0.01, 1, 1])
    # Generate the filename with the current date - 1
    filename = f"northpole_temperature.png"
    # Specify the directory path
    directory = "temperature/"
    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)
    # Save the plot as a PNG file in the specified directory
    filepath = os.path.join(directory, filename)
    plt.savefig(filepath)
    # Display the plot
    plt.show()
    

def plotStreaks():
    data = pd.read_csv('temperature/streaks.csv', parse_dates=['EndDate'])
    data['StartDate'] = data['EndDate'] - pd.to_timedelta(data['Streak'] - 1, unit='D')
    fig, ax = plt.subplots(figsize=(10, 6))
    for index, row in data.iterrows():
        start_day = (row['StartDate'] - pd.Timestamp(row['StartDate'].year, 1, 1)).days + 1
        end_day = (row['EndDate'] - pd.Timestamp(row['EndDate'].year, 1, 1)).days + 1
        year = row['EndDate'].year
        y_coords = [year] * (end_day - start_day + 1)
        x_coords = list(range(start_day, end_day + 1))
        ax.plot(x_coords, y_coords, color='blue', linewidth=3)
    ax.set_ylim(pd.Timestamp('1990-01-01').year, pd.Timestamp('2023-12-31').year)
    ax.set_yticks(range(pd.Timestamp('1990-01-01').year, pd.Timestamp('2024-01-01').year))
    ax.set_yticklabels(range(pd.Timestamp('1990-01-01').year, pd.Timestamp('2024-01-01').year), rotation=0)
    ax.set_xlim(1, 367)
    major_ticks = range(1, 368, 10)
    ax.set_xticks(major_ticks)
    minor_ticks = range(1, 368, 2)
    ax.set_xticks(minor_ticks, minor=True)
    major_labels = [pd.Timestamp('2023-01-01') + pd.DateOffset(days=i-1) for i in major_ticks]
    ax.set_xticklabels([d.strftime('%m/%d') for d in major_labels], rotation=45)
    ax.set_xlabel('Day of Year')
    ax.set_ylabel('Year')
    ax.set_title('College Observatory - Streaks of Temperature Above -20°F')
    plt.tight_layout()
    plt.show()
    filename = f"streaks.png"
    directory = "temperature/"
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)
    plt.savefig(filepath)
    
plotCollege()
plotNorthPole()
plotStreaks()