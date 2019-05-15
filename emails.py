#!/usr/bin/python3
import pandas as pd
import argparse

# Variables
start_date = None           # First day of the desired month
end_date = None             # First day of the month after desired
input_file = 'subs.csv'     # csv file to read
output_file = None          # csv file to save to
subbed = None               # Pandas dataframe object

# Function to write pandas dataframe to a csv file
def gen_report(df, of):
    with open(of, 'w') as f:
        df.to_csv(f)
    rows = df.shape[0]
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

# Parse date argument.
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
with open(input_file,'r') as f:
    subbed = pd.read_csv(f, delimiter=',')

# Convert times to datetime objects.
# Explicity specifying time format reduces runtime significantly.
subbed['AddedTime'] = pd.to_datetime(subbed['AddedTime'], 
        format = '%m/%d/%Y %H:%M')
subbed['RemovedTime'] = pd.to_datetime(subbed['RemovedTime'],
        format = '%m/%d/%Y %H:%M', errors='ignore')

# Filter dataframe.
subs_bfr = subbed.loc[(subbed['AddedTime'] < end_date)]
subs_btwn = subs_bfr.loc[(subs_bfr['SubscriberStatus'] == 'Subscribed')
        | (subs_bfr['RemovedTime'] > end_date)]

# Generate report by writing resutls to file
gen_report(subs_btwn, output_file)


