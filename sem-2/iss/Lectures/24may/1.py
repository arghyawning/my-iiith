"""
with open('file1.csv', 'r') as f:
    data = f.read()
print(type(data))
"""

"""
path = "file1.csv"
f = open(path, 'r')
for line in f:
    line = line.strip()
    line = line.split(',')
    print(line)
f.close()
"""

"""
path = "file1.csv"
f = open(path, 'r')
header = next(f)
for line in f:
    line = line.strip()
    line = line.split(',')
    part1 = line[2].strip("'")
    part2 = line[3].strip("'")
    print("first part: ", line[2])
    partM = int(part1)*float(part2)
    print(partM)
f.close()
"""
"""
import csv
path = "file1.csv"
f = open(path, 'r')
row = csv.reader(f)
header = next(f)
for line in row:
    part1 = line[2].strip("'")
    part2 = line[3].strip("'")
    print(line)
    partM = int(part1)*float(part2)
    print(partM)
f.close()
"""

"""
exception handling
"""

import csv
path = "file2.csv"
f = open(path, 'r')
row = csv.reader(f)
header = next(f)
for line in row:
    try:
        part1 = line[2].strip("'")
        part2 = line[3].strip("'")
        print(line)
        partM = int(part1)*float(part2)
        print(partM)
    except ValueError as err:
        print("bad data: ", err)
        continue
f.close()
