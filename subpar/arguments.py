import sys
import os
import argparse
from pandas import to_datetime, DateOffset
from . import g

def init_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--date', 
            help="Enter a date, ex: 'July 2012'.")
    parser.add_argument('-if', '--in_file',
            help="Specify the path to a csv file as input.")
    parser.add_argument('-of', '--out_file',
            help="Specify the path to an output file.")

    args = parser.parse_args()

    if args.in_file:
        g.input_file = args.in_file
    else: 
        #print('No input file. Defaulting to "subs.csv" in current directory.')
        #g.input_file = './subs.csv'
        print('No input file specified.')
        sys.exit()

    if args.date:
        try:
            g.start_date = to_datetime(args.date)
            g.end_date = g.start_date + DateOffset(months=1)
        except ValueError: 
            print("Could not parse date. Use -h for help.")
            sys.exit()
    else:
        print("Date not specified. Defaulting to current month...")
        m = to_datetime('today').month
        y = to_datetime('today').year
        g.start_date = to_datetime(f"{y}-{m}")
        g.end_date = g.start_date + DateOffset(months=1)

    if args.out_file:
        g.output_file = args.out_file
    else:
        m = g.months[g.start_date.month]
        fpath = f"{m} {g.start_date.year}.csv"
        g.output_file = os.path.join(g.report_path, fpath)


