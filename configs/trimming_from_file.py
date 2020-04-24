import sys
import trimming_data

args = sys.argv
path = args[1]

with open(path) as f:
    line = [s.strip() for s in f.readlines()]

num = [i.split() for i in line[2:]]

for i in range(len(num)):
    trimming_data.main(line[0], int(num[i][0]), int(num[i][1]), line[1]+'_{}'.format(i))
