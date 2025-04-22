from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
import nltk
import re
import csv
from bertopic import BERTopic
import pandas as pd

csv.field_size_limit(10 * 1024 * 1024)
nltk.data.path.append(r'C:\Users\THEWJ\AppData\Roaming\nltk_data')

# 分组规模
N = 40

# 停用词列表
stop_words = set(stopwords.words('english'))
# 自定义停用词列表
custom_stopwords = [
    'test', 'testing', 'improve', 'python', 'make', 'view', 'model', 'move', 'file', 'merge',
    'add', 'warning', 'update', 'failed', 'failing', 'call', 'operation', 'backward', 'function',
    'dont', 'fails', 'result', 'change', 'without', 'case', 'support', 'state', 'exception', 'running',
    'work', 'allow', 'using', 'enable', 'disabled', 'use', 'different', 'device', 'forward', 'part', 'reduce',
    'unused', 'instead', 'option', 'adding', 'pr', 'operator', 'build', 'averaging', 'typing', 'inductor'
    'wip', 'ref', 'doesnt', 'pytorch', 'torch', 'failure', 'added', 'adding', 'fix', 'remove', 'input', 'export'
]
# 批量添加停用词
stop_words.update(custom_stopwords)

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
    
# 预处理函数
def preprocess_title(text, body):
    # flag = preproces_body(body)
    
    # 去除特殊字符
    text = re.sub(r'[^\w\s,.\-]', '', text)
    # 去除CC()
    text = re.sub(r'CC\((.*?)\)', r'\1', text)
    # 去除单行代码块
    text = re.sub(r'`([^`]*)`', r'', text)
    # 转小写
    text = text.lower()
    # 去除标点符号
    text = text.translate(str.maketrans('', '', string.punctuation))
    # 分词
    words = word_tokenize(text)

    # 词形还原
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]

    # 还原被错误还原的单词
    words = ['mps' if word == 'mp' else word for word in words]
    words = ['docs' if word == 'doc' else word for word in words]
    words = ['ops' if word == 'op' else word for word in words]    
    # 去除停用词
    words = [word for word in words if word not in stop_words]
    # 是否有keywords
    '''
    for key in keywords:
        for word in words:
            if key == word: 
                flag = True

    # 是否有keyphrase
    if any([all([key in words for key in keyphrase]) for keyphrase in keyphrases]):
        flag = True
        
    # 如果title或body中有keyword或keyphrase
    if flag:
        # 去除停用词
        words = [word for word in words if word not in stop_words]
        return words
    else:
        return []
    '''
    return words
    
def train_one(year):
    input_file = rf'C:\pyprogram\research\data\{year}\result.csv'

    # title
    data = []

    bodies = []

    # 逐行读取CSV文件
    with open(input_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row[0])
            bodies.append(row[1])
    
    # 将每一句预处理
    processed_data = [preprocess_title(data[i], bodies[i]) for i in range(len(data))]

    # 去除长度超过18或小于2的单词
    processed_data = [[word for word in sentense if 2 <= len(word) <= 18] for sentense in processed_data]
    # 去除空列表
    processed_data = [doc for doc in processed_data if doc]

    processed_data = [' '.join(words) for words in processed_data]


    
    for N in range(20, 70, 10):
        data = []
        
        for i in range(len(processed_data) // N):
            data.append(' '.join(processed_data[(i * N) : ((i + 1) * N)]))
            
        # 构建BERTopic模型    
        topic_model = BERTopic()
        
        # 数据训练
        topics, probs = topic_model.fit_transform(data)
        
        topic_info = topic_model.get_topic_info()

        print(topic_info)
        
        f = open(rf"C:\pyprogram\research\data\{year}\bertopic_{year}.txt", "a", encoding='utf-8')
        
        f.write(f"topics_num = {len(topic_info)}\n")
        for i in range(-1, len(topic_info) - 1, 1):
            f.write(f"主题{i + 2}:" + str(topic_model.get_topic(i)) + "\n")
        f.write('\n\n\n')
            
        f.close()

        print(f"N = {N}, year = {year} 完成， topics_num = {len(topic_info)}")

    
for year in range(2022, 2025):
    train_one(year)