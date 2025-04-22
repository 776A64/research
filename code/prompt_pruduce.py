import csv

platform = 'github'
csv.field_size_limit(10 * 1024 * 1024)
data_name = 'tensorflow'
for year in range(2022, 2026):
    input_file = rf'C:\pyprogram\research\data\{data_name}\{year}\{data_name}{year}.csv'
    output_file = rf'C:\pyprogram\research\data\{data_name}\{year}\{data_name}_{year}_prompt_nocode.csv'
    with open(input_file, 'r', encoding='utf-8') as infile:
        with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)
            for row in reader:
                prompt =  f"以下是一个{platform}上的{data_name}下的一个issue, 标题是({row[2]})， 内容是 ({row[3]})请根据以上内容标注这个issue,\
                用一句简短的话描述这个issue类型是bug报告还是其它类型（例如用户提出需求，请教问题等），设计的模型或者主要对象是什么，由于什么问题出现了什么bug，需要什么帮助。你的回答只需要包含这个句子，不需要包含其他内容"
                writer.writerow([len(prompt), prompt] + row)