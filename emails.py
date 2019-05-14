#!/usr/bin/python
import pandas as pd
import argparse
import datetime as dt

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--date', 
        help="Enter a date, ex: 'July 2012'.")
parser.add_argument('-f', '--file',
        help="Specify a csv file to examine.")
date = None
args = parser.parse_args()
if args.date:
    try: date = pd.to_datetime(args.date)
    except ValueError: 
        print("Incorrect date format. Use -h for help.")
        raise
else:
    date = pd.to_datetime('now')

if args.file:
    input_file = args.file
else:
    input_file = 'subs.csv'

# Declare variables
start_date = '2018-10-01'
end_date = '2018-10-31'
month = 'april2019'
filename = f'cure_emails/{month}_subs.csv'

# Open and read csv into pandas dataframe object
subbed = None
with open(input_file,'r') as f:
    subbed = pd.read_csv(f, delimiter=',')

#subbed['pAddTime'] = pd.to_datetime(subbed['AddedTime'],errors='coerce')
#subbed['pRemoveTime'] = pd.to_datetime(subbed['RemovedTime'],errors='coerce')

# Filter dataframe
subs = subbed.loc[(subbed['AddedTime'] < end_date) 
        & (subbed['RemovedTime'] > end_date)] 
cleaned = subbed.loc[(subbed['SubscriberStatus'] == 'Cleaned') 
        & (subbed['AddedTime'] >= start_date) 
        & (subbed['RemovedTime'] <= end_date)]
cleanEmails = cleaned[['Email Address']]
totalsubs = subs.loc[~subs['Email Address'].isin(cleanEmails)].reset_index()

# Print filtered results
print(totalsubs[['Email Address', 'AddedTime',
    'RemovedTime', 'SubscriberStatus']])

# Write resutls to file
#with open(filename, 'w') as f:
#    totalsubs.to_csv(f)
