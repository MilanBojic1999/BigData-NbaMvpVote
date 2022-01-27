import csv

from numpy import sort

with open('player_stats/player_stats.csv') as csv_file:
    csv_reader = csv.reader(csv_file,delimiter=',')

    columns = set()
    for row in csv_reader:
        columns.add(row[3])

print(len(columns))
columns = list(columns)
columns.sort()
for c in columns:
    print(c)
        