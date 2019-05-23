#!/usr/bin/python3
import pandas as pd
import argparse
import matplotlib.pyplot as plt
import os.path as path

# Variables
info = None                     #First day of desired month
start_date = pd.to_datetime('2018-05-01')  # Earliest supported date
end_date = None                 # First day of the month after desired
input_file = path.normpath('./subs.csv')        # csv file to read
output_file = None              # csv file to save to
ytd_df = None

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
        info = pd.to_datetime(args.date)
        end_date = info + pd.DateOffset(months=1)
    except ValueError: 
        print("Could not parse date. Use -h for help.")
        raise
else:
    print("Date not specified. Defaulting to current month...")
    m = pd.to_datetime('today').month
    y = pd.to_datetime('today').year
    info = pd.to_datetime(f"{y}-{m}")
    end_date = info + pd.DateOffset(months=1)

if args.in_file:
    input_file = path.normpath(args.in_file)
if args.out_file:
    output_file = path.normpath(args.out_file)
else:
    output_file = path.normpath(f"../Reports/{info.month}-{info.year}.csv")

def load_df(infile):
    s = None
    with open(infile,'r') as f:
        s = pd.read_csv(f, delimiter=',')
    s['AddedTime'] = pd.to_datetime(s['AddedTime'], 
            format = '%m/%d/%Y %H:%M')
    s['RemovedTime'] = pd.to_datetime(s['RemovedTime'],
            format = '%m/%d/%Y %H:%M', errors='ignore')
    return s

def filter_time(subbed, ed=end_date):
    subs_bfr = subbed.loc[(subbed['AddedTime'] < ed)]
    subs_btwn = subs_bfr.loc[(subs_bfr['SubscriberStatus'] == 'Subscribed')
            | (subs_bfr['RemovedTime'] > ed)]
    return subs_btwn

def get_year(subbed):
    s = []
    m = start_date
    for i in range(0,13):
        m = start_date + pd.DateOffset(months=i)
        d = start_date + pd.DateOffset(months=(i+1))
        x = filter_time(subbed, d)
        key = f"{m.month}/{m.year}"
        s.append([key, x.shape[0]])
    subs_over_time = pd.DataFrame(s, columns=['Month', 'Subscribers'])
    return subs_over_time

def gen_report(df, of):
    with open(of, 'w') as f:
        df.to_csv(f)
    rows = df.shape[0]
    print(f"Full data written to {of}.")
    print(f"There were {rows} total entries.")

def run():
    subbed = load_df(input_file)
    subs_btwn = filter_time(subbed)
    subs_over_time = get_year(subbed)
    print(subs_over_time)
    p = subs_over_time.set_index('Month').plot(grid=True)
    plt.savefig(path.normpath('../Reports/graph.png'))
    gen_report(subs_btwn, output_file)

if __name__ == "__main__":
    run()

