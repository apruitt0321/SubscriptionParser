#!/usr/bin/python3
import pandas as pd
import argparse

# Variables
start_date = None
end_date = None
input_file = 'subs.csv'
output_file = None
subbed = None

def gen_report(df, of):
    r = ['Email Address', 'FirstName', 'LastName', 
        'SubscriberStatus', 'AddedTime', 'RemovedTime']
    with open(of, 'w') as f:
        df.to_csv(f)
    rows = df[r].shape[0]
    print(f"Full data written to {of}.")
    print(f"There were {rows} total entries.")

# Add CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--date', 
        help="Enter a date, ex: 'July 2012'.")
parser.add_argument('-if', '--in_file',
        help="Specify the path to a csv file as input.")
parser.add_argument('-of', '--out_file',
        help="Specify the path to an output file.")
args = parser.parse_args()

# Parse date argument. If no date argument is provided, defaults to current
# month and year.
if args.date:
    try:
        start_date = pd.to_datetime(args.date)
        m = start_date.month
        y = start_date.year
        if m == 12:
            m = 0
            y += 1
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

# Parse file arguments.
if args.in_file:
    input_file = args.in_file
if args.out_file:
    output_file = args.out_file
else:
    output_file = f"{args.date}.csv"

# Open and read csv into pandas dataframe object
print("Loading csv file into dataframe...")
with open(input_file,'r') as f:
    subbed = pd.read_csv(f, delimiter=',')
print("Done.")

# Convert times to datetime objects. Time intesive.
print("Converting 'AddedTime'...")
subbed['AddedTime'] = pd.to_datetime(subbed['AddedTime'])
print("Done.")
print("Converting 'RemovedTime'...")
subbed['RemovedTime'] = pd.to_datetime(subbed['RemovedTime'],errors='ignore')
print("Done.")

# Filter dataframe. Takes slice of all entries subscribed before end_date,
# then returns slice of those who are still subscribed or whose unsubscription
# date is after end_date.
subs_bfr = subbed.loc[(subbed['AddedTime'] < end_date)]
subs_btwn = subs_bfr.loc[(subs_bfr['SubscriberStatus'] == 'Subscribed')
        | (subs_bfr['RemovedTime'] > end_date)]

# Generate report by writing resutls to file
# Need to remove 'AddedTime' and 'RemovedTime' in favor of 'Atime' and 'Rtime'
gen_report(subs_btwn, output_file)


