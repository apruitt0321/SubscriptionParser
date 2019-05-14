#!/usr/bin/python
import pandas as pd
import argparse

# Variables
start_date = None
end_date = None
input_file = 'subs.csv'
month = 'april2019'
filename = f'cure_emails/{month}_subs.csv'
subbed = None

# Add CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--date', 
        help="Enter a date, ex: 'July 2012'.")
parser.add_argument('-f', '--file',
        help="Specify a csv file to examine.")
args = parser.parse_args()

# Parses date argument. If no date argument is provided, defaults to current
# month and year.
if args.date:
    try:
        start_date = pd.to_datetime(args.date)
        m = start_date.month
        y = start_date.year
        if m == 12:
            m = 0
            y = start_date.year + 1
        end_date = pd.to_datetime(f"{y}-{m+1}")
    except ValueError: 
        print("Could not parse date. Use -h for help.")
        raise
else:
    print("Date not specified. Defaulting to current month...")
    m = pd.to_datetime('today').month
    y = pd.to_datetime('today').year
    start_date = pd.to_datetime(f"{y}-{m}")
    if m == 12:
        m = 0
        y += 1
    end_date = pd.to_datetime(f"{y}-{m+1}")

# Parses file arguments. Defaults to 'subs.csv'.
if args.file:
    input_file = args.file

# Open and read csv into pandas dataframe object
with open(input_file,'r') as f:
    subbed = pd.read_csv(f, delimiter=',')

# Convert times to datetime objects. Time intesive.
subbed['Atime'] = pd.to_datetime(subbed['AddedTime'])
subbed['Rtime'] = pd.to_datetime(subbed['RemovedTime'],errors='ignore')

# Filter dataframe.
subs_bfr = subbed.loc[(subbed['Atime'] < end_date)]
subs_btwn = subs_bfr.loc[(subs_bfr['SubscriberStatus'] == 'Subscribed')
        | (subs_bfr['Rtime'] > end_date)]

# Print filtered results. Mostly for debugging. 
r = ['Email Address', 'FirstName', 'LastName', 
        'SubscriberStatus', 'Atime', 'Rtime']
print(subs_btwn[r])
print(start_date)
print(end_date)

# Generate report by writing resutls to file
#with open(filename, 'w') as f:
#    totalsubs.to_csv(f)
