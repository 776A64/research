from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
import re
import csv
import string

nltk.data.path.append(r'C:\Users\THEWJ\AppData\Roaming\nltk_data')
csv.field_size_limit(10 * 1024 * 1024)
lemmatizer = WordNetLemmatizer()

data_name = 'tensorflow'

keywords = [
    "llm", "langchain", "llama", "chromadb", "finetuning", "mistral", "peft",
    "rag", "pinecone", "gpt", "agent", "transformer", "langgraph", "lmstudio",
    "claude", "dspy", "anthropic", "flowise", "gemma", "langsmith", "baichuan",
    "glm", "chat", "qwen", "deepseek", "yi", "pangu", "mixtral", "llava", "grok", "opensora", "vlm"
]

keyphrases = [
    ["large", "language", "model"],
    ["text", "generation"], 
    ["amazon", "bedrock"],
    ["few", "shot"], 
    ["text", "chunking"]
]

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
            text = row[1] + row[2]  # 根据有无用户名调整
            
            # 去除特殊字符
            text = re.sub(r'[^\w\s,.\-]', '', text)
            # 转小写
            text = text.lower()
            # 去除标点符号
            text = text.translate(str.maketrans('', '', string.punctuation))
            # 分词
            words = word_tokenize(text)
            #词形还原
            words = [lemmatizer.lemmatize(word) for word in words]

            for i in keywords:
                for word in words:
                    if i in word: 
                        flag = True
                        key = i

            # 是否有keyphrase
            for keyphrase in keyphrases:
                if all([any([key in word for word in words]) for key in keyphrase]):
                    key = keyphrase
                    flag = True
                    
            if flag:
                if isinstance(key, str):
                    writer.writerow([key] + row)
                else:
                    writer.writerow([' '.join(key)] + row)
                    print("1")
    
    outfile.close()

# 示例调用
for year in range(2022, 2026):
    input_csv = rf'C:\pyprogram\research\data\{data_name}\{year}\{data_name}_{year}.csv'
    filter_csv(input_csv, rf'C:\pyprogram\research\data\{data_name}\{year}\{data_name}_{year}_filtered.csv')