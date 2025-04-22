import csv
csv.field_size_limit(10 * 1024 * 1024)

data_name ='tensorflow'

for year in range(2022, 2026):
    input_csv = rf'C:\pyprogram\research\data\{data_name}\{year}\{data_name}_{year}.csv'
    output_file = rf'{data_name}_{year}_user_collect.txt'

    # 使用集合来存储不重复的第一列数据
    unique_values = set()

    # 读取 CSV 文件
    with open(input_csv, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:  # 如果行不为空
                unique_values.add(row[0].strip())  # 添加第一列，并去掉可能的前后空白

    # 将不重复的数据写入 TXT 文件，每个值占一行
    with open(output_file, 'w', encoding='utf-8') as txtfile:
        for value in unique_values:
            txtfile.write(value + '\n')
