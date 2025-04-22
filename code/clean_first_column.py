import csv

csv.field_size_limit(10 * 1024 * 1024)
def process_csv(input_file, output_file):
    with open(input_file, 'r', newline='') as infile, \
         open(output_file, 'w', newline='') as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # 处理首行（保留完整）
        header = next(reader)
        writer.writerow(header)

        # 处理后续行（删除第一列）
        for row in reader:
            writer.writerow(row[1:])

for year in range(2022, 2025):
    input_file = rf"C:\pyprogram\research\data\mindspore\{year}\result.csv"
    output_file = rf'C:\pyprogram\research\data\mindspore\{year}\output.csv'
    process_csv(input_file, output_file)