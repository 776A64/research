from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
import re
import csv
import string

nltk.data.path.append(r'C:\Users\THEWJ\AppData\Roaming\nltk_data')
csv.field_size_limit(10 * 1024 * 1024)

data_name = 'pytorch'

keywords = [
    "llm", "langchain", "llama", "chromadb", "finetuning", "mistral", "peft", "few shot", "text chunking"
    "rag", "pinecone", "gpt", "agent", "transformer", "langgraph", "lmstudio", "amazon bedrock"
    "claude", "dspy", "anthropic", "flowise", "gemma", "langsmith", "baichuan", "text generation"
    "glm", "chat", "qwen", "deepseek", "yi", "pangu", "mixtral", "llava", "grok", "opensora", "vlm", "large language model"
]

with open(rf'C:\pyprogram\research\data\1.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for i in reader:
        if i[0] == 'PyTorch':
            keywords.append(i[1])

keywords = [word.lower() for word in keywords]
print(keywords)

def filter_csv(input_file, output_file):
    
    outfile = open(output_file, mode='w', encoding='utf-8', newline='')
    writer = csv.writer(outfile)
    
    with open(input_file, mode='r', encoding='utf-8') as infile:    
        reader = csv.reader(infile)
        next(reader)
        
        # 遍历剩余行，筛选符合条件的行
        for row in reader:
            key = ''
            flag = False
            text = (row[1] + row[2]).lower()  # 根据有无用户名调整

            for i in keywords:
                if i in text: 
                    flag = True
                    key = i
                    
            if flag:
                writer.writerow([key] + row)
    
    outfile.close()

# 示例调用
for year in range(2025, 2026):
    input_csv = rf'C:\pyprogram\research\data\{data_name}\{year}\{data_name}_{year}_user.csv'
    filter_csv(input_csv, rf'C:\pyprogram\research\data\{data_name}\{year}\{data_name}_{year}_filtered.csv')