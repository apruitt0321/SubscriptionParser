#!/usr/bin/python
import pandas as pd
import argparse
import datetime as dt

date = None
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

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--date', 
        help="Enter a date, ex: 'July 2012'.")
parser.add_argument('-f', '--file',
        help="Specify a csv file to examine.")
args = parser.parse_args()
if args.date:
    try:
        adate = args.date.lower().split(" ")
        if adate[0] == 'december':
            adate[1] = str(int(adate[1]) + 1)
        adate[0] = m_incr[adate[0]]
        date = pd.to_datetime(adate[0]+" "+adate[1])
    except ValueError: 
        print("Incorrect date format. Use -h for help.")
        raise
else:
    date = pd.to_datetime('now')
print(date)

if args.file:
    input_file = args.file
else:
    input_file = 'subs.csv'

# Declare variables
start_date = '2019-04-01'
end_date = '2019-05-01'
month = 'april2019'
filename = f'cure_emails/{month}_subs.csv'
# Open and read csv into pandas dataframe object
subbed = None
with open(input_file,'r') as f:
    subbed = pd.read_csv(f, delimiter=',')

# Convert times to datetime objects. Time intesive.
#subbed['pAtime'] = pd.to_datetime(subbed['AddedTime'])
#subbed['pRtime'] = pd.to_datetime(subbed['RemovedTime'],errors='ignore')

# Filter dataframe.
#subs_bfr = subbed.loc[(subbed['pAtime'] < pd.to_datetime(end_date))]
#subs_btwn = subs_bfr.loc[(subs_bfr['SubscriberStatus'] == 'Subscribed')
#        | (subs_bfr['pRtime'] > pd.to_datetime(end_date))]

# Print filtered results
r = ['Email Address', 'FirstName', 'LastName', 
        'SubscriberStatus', 'pAtime', 'pRtime']
#print(subs_btwn[r])

# Write resutls to file
#with open(filename, 'w') as f:
#    totalsubs.to_csv(f)
