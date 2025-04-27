import csv

csv.field_size_limit(10 * 1024 * 1024)
data_names = [
    'vllm', 'TensorRT-LLM', 'ColossalAI', 'mindnlp', 'MindSpeed', 'mindformers'
]
for name in data_names:
    with open(rf'.\research\data\tagged_origin\{name}.csv', 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        with open(rf'.\research\data\tagged\{name}.txt', 'w') as outfile:
            for row in reader:
                outfile.write(row[8] + '\n' + row[0] + '\n\n')