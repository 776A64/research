from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
import re
from gensim.corpora import Dictionary
from gensim.models import LdaModel
import csv
from tqdm import tqdm
import jieba

csv.field_size_limit(10 * 1024 * 1024)
nltk.data.path.append(r'C:\Users\THEWJ\AppData\Roaming\nltk_data')
jieba.initialize()
lemmatizer = WordNetLemmatizer()
    
data_name = 'mindspore'


# 停用词列表
stop_words = set(stopwords.words('english'))
# 自定义停用词列表
custom_stopwords = [ 
   'test', 'testing', 'improve', 'python', 'make', 'view', 'model', 'move', 'file', 'merge',
    'add', 'warning', 'update', 'failed', 'failing', 'call', 'operation', 'backward', 'function',
    'dont', 'fails', 'result', 'change', 'without', 'case', 'support', 'state', 'exception', 'running',
    'work', 'allow', 'using', 'enable', 'disabled', 'use', 'different', 'device', 'forward', 'part', 'reduce',
    'unused', 'instead', 'option', 'adding', 'pr', 'operator', 'build', 'averaging', 'typing', 'int', 
    'wip', 'ref', 'doesnt', 'mindspore', 'failure', 'added', 'adding', 'fix', 'remove', 'input', 'export', 'op', 'ha', '鹏城'           
]
# 批量添加停用词
stop_words.update(custom_stopwords)

cn_stop = set(open(r"C:\pyprogram\research\data\cn_stopwords.txt", encoding='utf-8').read().splitlines())
combined_stop = cn_stop.union(stop_words)


def mixed_segment(text):
    # 分离中英文
    english_part = re.findall(r'[a-zA-Z]+', text)
    chinese_part = re.sub(r'[a-zA-Z]+', '', text)
    
    # 中文分词
    chinese_words = list(jieba.cut(chinese_part))
    
    # 英文分词
    english_words = [lemmatizer.lemmatize(word.lower()) for word in english_part]
    
    return chinese_words + english_words

# 预处理函数
def preprocess_title(text, body):
    # 去除非字母/汉字的字符
    text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z]', ' ', text)
    # 去除单行代码块
    text = re.sub(r'`([^`]*)`', r'', text)
    # 混合分词
    words = mixed_segment(text)
    
    filtered = [
        word for word in words if word not in combined_stop and len(word) > 1 and not word.isdigit()
    ]
    return filtered

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