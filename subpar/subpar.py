import pandas as pd
import matplotlib.pyplot as plt
import os.path as path

from . import g, arguments

def load_df(infile):
    s = None
    with open(infile,'r') as f:
        s = pd.read_csv(f, delimiter=',')
    s['AddedTime'] = pd.to_datetime(s['AddedTime'], 
            format = '%m/%d/%Y %H:%M')
    s['RemovedTime'] = pd.to_datetime(s['RemovedTime'],
            format = '%m/%d/%Y %H:%M', errors='ignore')
    return s

def filter_time(subbed, ed=None):
    if not ed:
        ed = g.end_date
    subs_bfr = subbed.loc[(subbed['AddedTime'] < ed)]
    subs_btwn = subs_bfr.loc[(subs_bfr['SubscriberStatus'] == 'Subscribed')
            | (subs_bfr['RemovedTime'] > ed)]
    return subs_btwn

def get_year(subbed):
    s = []
    m = g.date_zero
    for i in range(0,13):
        m = g.date_zero + pd.DateOffset(months=i)
        d = g.date_zero + pd.DateOffset(months=(i+1))
        x = filter_time(subbed, d)
        key = f"{g.months[m.month]} {m.year}"
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
    g.input_file = path.normpath('./subs.csv')
    g.date_zero = pd.to_datetime('2018-05-01')
    arguments.init_args()
    subbed = load_df(g.input_file)
    subs_btwn = filter_time(subbed)
    subs_over_time = get_year(subbed)
    print(subs_over_time)
    p = subs_over_time.set_index('Month').plot(grid=True)
    plt.savefig(g.img_path)
    gen_report(subs_btwn, g.output_file)

