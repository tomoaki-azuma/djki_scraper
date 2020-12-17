import csv

all_list = set()
get_list = set()

with open('all_number.csv', 'r') as f:
    reader = csv.reader(f)
    for line in reader:
        all_list.add(line[0])

with open('get_all_data.csv', 'r') as f:
    reader = csv.reader(f)
    for line in reader:
        if line:
            get_list.add(line[0])

diff_list = list(all_list - get_list)
result = []
for d in diff_list:
    result.append(d)
print(result)
with open('diff.csv', 'a', encoding='utf-8') as f:
    for r in result:
        f.write(r + '\n')