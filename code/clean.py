import re
import csv

csv.field_size_limit(10 * 1024 * 1024)

data_name = 'mindspore'

def filter_csv(input_file, output_file):
    
    outfile = open(output_file, mode='w', encoding='utf-8', newline='')
    writer = csv.writer(outfile)
    result = []
    
    with open(input_file, mode='r', encoding='utf-8') as infile:    
        reader = csv.reader(infile)

        for row in reader:
            cleaned_row = [re.sub(r'```.*?```', r'', cell) for cell in row]
            result.append(cleaned_row)
        
        length = []
        for row in result:
            length.append(len(row[3]))
        length.sort()
        
        limit = length[int(len(length) * 0.8)]
        
        for i in range(len(result)):
            result[i][3] = result[i][3][:limit]
            
        writer.writerows(result)
    
    outfile.close()

# 示例调用
for year in range(2022, 2026):
    input_csv = rf'C:\pyprogram\research\data\{data_name}\{year}\{data_name}_{year}_filtered.csv'
    filter_csv(input_csv, rf'C:\pyprogram\research\data\{data_name}\{year}\{data_name}{year}.csv')