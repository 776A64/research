import requests
import json
import csv
import re
import os

platform = 'github'
data_name = 'DeepSpeed'
url = "https://cn2us02.opapi.win/v1/chat/completions"
csv.field_size_limit(10 * 1024 * 1024)

token = os.getenv("Ohmygpt")
if not token:
    raise ValueError("未找到环境变量 Ohmygpt")

def count(input_file):
    result = [] 
    with open(input_file, mode='r', encoding='utf-8') as infile:    
        reader = csv.reader(infile)

        for row in reader:
            cleaned_row = [re.sub(r'```.*?```', r'', cell) for cell in row]
            result.append(cleaned_row)
        
        length = []
        for row in result:
            length.append(len(row[2]))
        length.sort()
        
        limit = length[int(len(length) * 0.8)]
            
        return limit 
    
def ask(content):
    payload = json.dumps({
    "model": "gpt-3.5-turbo",
    "messages": [  
                {
                    "role": "system",
                    "content": "你是一个协助标注文本内容的AI助手",
                },
                {
                    "role": "user",
                    "content": content
                }
        ]
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()


input = fr'.\research\data\{data_name}.csv'
limit = count(input)
print(limit)
with open(input, 'r', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    for _ in range(6236):
        next(reader)
    for row in reader:
        content =  f'以下是一个{platform}上的{data_name}下的一个issue， 标题是"{row[1]}"， 内容是 "{re.sub(r'```.*?```', r'', row[2])[:limit]}"。\
                    用一句简短的话描述这个issue类型是bug报告还是其它类型（例如用户提出需求，请教问题等），该问题单涉及的主要对象（例如）是什么？最后分析一下由于什么样的原因导致了什么样症状的bug或者用户提出了关于什么的问题或者寻求什么样的帮助？你的回答只需要包含这个句子，不需要包含其他内容'
        try:
            row[0] = ask(content).get('choices')[0].get('message').get('content')
        except:
            row[0] = "获取错误，请重新获取"
        with open('tagged.csv', 'a', encoding='utf-8', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(row)