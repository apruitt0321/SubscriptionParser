""" Global varibales """
import os
import sys

args = []
date_zero = None
start_date = None
end_date = None
input_file = None
output_file = None
df = None
mswin = False
uHome = os.path.expanduser('~')
report_path = os.path.join(uHome, 'Reports')
img_path = os.path.join(report_path, 'graph.png')
months = { 1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
        7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

