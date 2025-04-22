import csv

csv.field_size_limit(10 * 1024 * 1024)

ls = []
with open(r".\research\data\ColossalAI.csv", 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    with open("ColossalAI.csv", 'w', encoding='utf-8', newline='') as file1:
        writer = csv.writer(file1)
        for row in reader:
            if row[8] not in ls:
                ls.append(row[8])
                writer.writerow(row)
    