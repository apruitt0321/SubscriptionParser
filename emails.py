#!/usr/bin/python
import pandas as pd
import argparse
import datetime as dt

# Variables
start_date = None
end_date = None
m_incr = { 'january': 'february',
            'february': 'march',
            'march': 'april',
            'april': 'may',
            'may': 'june',
            'june': 'july',
            'july': 'august',
            'august': 'september',
            'september': 'october',
            'october': 'november',
            'november': 'december',
            'december': 'january'}
input_file = 'subs.csv'
month = 'april2019'
filename = f'cure_emails/{month}_subs.csv'
subbed = None

# Handle CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--date', 
        help="Enter a date, ex: 'July 2012'.")
parser.add_argument('-f', '--file',
        help="Specify a csv file to examine.")
args = parser.parse_args()
if args.date:
    try:
        adate = args.date.lower().split(" ")
        start_date = pd.to_datetime(adate[0]+" "+adate[1])
        if adate[0] == 'december':
            adate[1] = str(int(adate[1]) + 1)
        adate[0] = m_incr[adate[0]]
        end_date = pd.to_datetime(adate[0]+" "+adate[1])
    except ValueError: 
        print("Could not parse date. Use -h for help.")
        raise
else:
    print("Date not specified. Defaulting to current month...")
    m = pd.to_datetime('today').month
    y = pd.to_datetime('today').year
    start_date = pd.to_datetime(f"{y}-{m}")
    end_date = pd.to_datetime(f"{y}-{m+1}")
if args.file:
    input_file = args.file

# Open and read csv into pandas dataframe object
with open(input_file,'r') as f:
    subbed = pd.read_csv(f, delimiter=',')

# Convert times to datetime objects. Time intesive.
subbed['pAtime'] = pd.to_datetime(subbed['AddedTime'])
subbed['pRtime'] = pd.to_datetime(subbed['RemovedTime'],errors='ignore')

# Filter dataframe.
subs_bfr = subbed.loc[(subbed['pAtime'] < pd.to_datetime(end_date))]
subs_btwn = subs_bfr.loc[(subs_bfr['SubscriberStatus'] == 'Subscribed')
        | (subs_bfr['pRtime'] > pd.to_datetime(end_date))]

# Print filtered results. Mostly for debugging. 
r = ['Email Address', 'FirstName', 'LastName', 
        'SubscriberStatus', 'pAtime', 'pRtime']
print(subs_btwn[r])

# Generate report by writing resutls to file
#with open(filename, 'w') as f:
#    totalsubs.to_csv(f)
