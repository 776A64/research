from collections import Counter
import csv
csv.field_size_limit(10 * 1024 * 1024)
 
bug_keywords = ['bug', 'Bug', 'BUG']
requirement_keywords = ['需求', '功能', '请求', '建议', '改进', '优化', '更新']
question_keywords = ['提问', '疑问', '提出问题', '帮助', '请教', '询问', '咨询'] 

bug_result = []
requirement_result = []
question_result = []

def deal_one_txt(name):
    with open(rf'.\research\data\tagged_origin\{name}.csv', 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        for row in reader:
            sentence = row[0].replace('，', ',')
            sentence = sentence.split(',')[0]
            if any([word in sentence for word in bug_keywords]):
                bug_result.append([name, row[0], row[8]])
            elif any([word in sentence for word in requirement_keywords]):
                requirement_result.append([name, row[0], row[8]])
            elif any([word in sentence for word in question_keywords]):
                question_result.append([name, row[0], row[8]])

data_names = [
    'DeepSpeed', 'Megatron-LM', 'vllm', 'TensorRT-LLM', 'ColossalAI', 'mindnlp', 'MindSpeed', 'mindformers'
]

for i in data_names:
    deal_one_txt(i)
    
with open(rf'.\research\data\tagged\bug.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(bug_result)

with open(rf'.\research\data\tagged\requirement.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(requirement_result)
    
with open(rf'.\research\data\tagged\question.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(question_result)