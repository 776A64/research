from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
import nltk
import re
from gensim.corpora import Dictionary
from gensim.models import LdaModel
import csv
from tqdm import tqdm

csv.field_size_limit(10 * 1024 * 1024)
nltk.data.path.append(r'C:\Users\THEWJ\AppData\Roaming\nltk_data')

data_name = 'jax'

# 停用词列表
stop_words = set(stopwords.words('english'))
# 自定义停用词列表
custom_stopwords = [ 
    'test', 'testing', 'improve', 'python', 'make', 'view', 'model', 'move', 'file', 'merge',
    'add', 'warning', 'update', 'failed', 'failing', 'call', 'operation', 'backward', 'function',
    'dont', 'fails', 'result', 'change', 'without', 'case', 'support', 'state', 'exception', 'running',
    'work', 'allow', 'using', 'enable', 'disabled', 'use', 'different', 'device', 'forward', 'part', 'reduce',
    'unused', 'instead', 'option', 'adding', 'pr', 'operator', 'build', 'averaging', 'typing', 'ha',
    'wip', 'ref', 'doesnt', 'jax', 'failure', 'added', 'adding', 'fix', 'remove', 'input', 'export'
]
# 批量添加停用词
stop_words.update(custom_stopwords)


keywords = [
]

keyphrases = [
]

# 返回body中是否有keyword或keyphrase
def preproces_body(text):
    flag = False

    # 去除特殊字符
    text = re.sub(r'[^\w\s,.\-]', '', text)
    # 去除CC()
    # text = re.sub(r'CC\((.*?)\)', r'\1', text)
    # 转小写
    text = text.lower()
    # 去除标点符号
    text = text.translate(str.maketrans('', '', string.punctuation))
    # 分词
    words = word_tokenize(text)

    # 词形还原
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]

    
    # 是否有keyword
    for key in keywords:
        for word in words:
            if key == word: 
                flag = True

    # 是否有keyphrase
    if any([all([key in words for key in keyphrase]) for keyphrase in keyphrases]):
        flag = True
        
    return flag

# 预处理函数
def preprocess_title(text, body):
    # flag = preproces_body(body)
    
    # 去除特殊字符
    text = re.sub(r'[^\w\s,.\-]', '', text)
    # 去除CC()
    # text = re.sub(r'CC\((.*?)\)', r'\1', text)
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
    
    '''
    # 是否有keywords
    for key in keywords:
        for word in words:
            if key in word: 
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
    words = ['docs' if word == 'doc' else word for word in words]
    
    words = [word for word in words if word not in stop_words]
    return words

def train_one_lda(year):
    
    input_file = rf'C:\pyprogram\research\data\{data_name}\{year}\result.csv'
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
    # 去除空列表
    processed_data = [doc for doc in processed_data if doc]
    # 去除长度超过18的单词
    processed_data = [[word for word in sentense if 2 <= len(word) <= 18] for sentense in processed_data]




    # 创建词典
    dictionary = Dictionary(processed_data)

    # 筛选出现不少于3次，出现频率不高于50%的前3500个单词
    # dictionary.filter_extremes(no_below=3, no_above=0.5, keep_n=3500)

    # 将文本转换为词袋向量
    corpus = [dictionary.doc2bow(text) for text in processed_data]

    # 生成的主题个数，每个主题10个单词
    for num_topics in range(10, 15, 5):
        f = open(rf"C:\pyprogram\research\data\{data_name}\{year}\topics.txt", "a", encoding='utf-8')
        # 创建 LDA 模型
        lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, random_state=42, passes=12)

        # 显示进度条
        for _ in tqdm(range(lda_model.passes), desc="Training LDA Model", unit="pass"):
            lda_model.update(corpus)  # 每个 pass 更新模型
            
        # 输出每个主题的关键词
        f.write(f"topics_num = {num_topics}\n")
        for idx, topic in lda_model.print_topics(num_topics=num_topics):
            f.write(f"主题 {idx + 1}: {topic}\n")
        f.write('\n\n\n')
        f.close()
        
        
for year in range(2022, 2025):
    train_one_lda(year)