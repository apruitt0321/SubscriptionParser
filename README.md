# SubscriptionParser #

A simple script for parsing a csv and returning the number of subscribers for a
given month.

## Requirements ##
SubscriptionParser requires pandas and matplotlib.

## How to use ##
SubscriptionParser currently must be called from the commandline. 
You must currently be in the directory in which the script is located. 
You may either call it using the python interpreter:

```
python sp -i <path/to/input_file.csv>
```

or by making it executable and calling it directly:

```
chmod +x sp
./sp -i <path/to/input_file.csv>
```

The default output file is '{month} {year}.csv'. This can be changed with the
`-of` (or `--out-file`) flag:

```
./sp -i <input_file> -of <path/to/outputfile.csv>
```

SubscriptionParser gives the total subscribers for the current month by
default. If you'd like to generate a report for a specific month, you can
specify the month and year by using the `-d` (`--date`) flag:

```
./sp -i <input_file> -d "January 2019"
./sp -i <input_file> -d "10/2018"
./sp -i <input_file> -d "12-2018"
```

Putting it all together:

```
./sp -i ./my_subscribers.csv -of ./NewFolder/03-19.csv -d "march 2019"
./sp -i ~/Docs/subs.csv -of ~/Docs/Dec18.csv -d "12/2018"
./sp -i file.csv --date "April 2019" -of C:\Users\Andy\Desktop\04_19.csv
```


