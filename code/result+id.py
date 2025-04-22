import csv

csv.field_size_limit(10 * 1024 * 1024)
with open('tagged.csv', 'r', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    with open('DeepSpeed.txt', 'w') as outfile:
        for row in reader:
            outfile.write(row[8] + '\n' + row[0] + '\n\n')