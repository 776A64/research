import re
from collections import Counter

def extract(text, start_str, end_str, flags=0):
    # 转义特殊字符并构造正则模式
    pattern = r'{}(.*?){}'.format(re.escape(start_str), re.escape(end_str))
    
    # 使用非贪婪模式匹配
    matches = re.findall(pattern, text, flags=flags | re.DOTALL)

    return matches[0] if matches else ''
    

result = []
with open(r'.\research\data\tagged\DeepSpeed.txt', 'r', encoding='utf-8') as infile:
    for i in infile.readlines():
        if (not i.startswith('https://github.com/')) and (not i == '\n'):
            result.append(i.strip())
            
word_counter = Counter()

pattern = [
    ('这是一个', '的issue'), 
    ('这是一个', '，'),
    ('这个issue类型是', '，'),
    ('此issue为', '，'),
    ('这是一个关于', '的Issue'),
    ('该issue属于', '类型'), 
    ('这是一个', '类的issue'),
    ('这是一个关于', '，'),
]

for x, y in pattern:
    for i in result:
        word_counter.update([extract(i, x, y)])

print(word_counter)