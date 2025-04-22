import re
from collections import defaultdict

for year in range(2022, 2025):    
    # 读取文件内容
    with open(rf'C:\pyprogram\research\data\{year}\bertopic_{year}.txt', 'r') as file:
        content = file.read()

    # 使用正则表达式提取每个主题的关键词
    pattern = r'主题\d+:\[(.*?)\]'
    matches = re.findall(pattern, content)

    # 统计关键词出现次数
    keyword_count = defaultdict(int)

    for match in matches:
        # 提取每个关键词和权重
        keywords = re.findall(r"\('(.*?)',", match)
        for keyword in keywords:
            keyword_count[keyword] += 1

    keyword_count = sorted(keyword_count.items(), key=lambda x: x[1], reverse=True)
    
    with open('count_result.txt', 'a', encoding='utf-8') as output_file:
        output_file.write(f'--------------{year}--------------\n')
        for keyword, count in keyword_count:
            output_file.write(f"{keyword}: {count}\n")
            
        output_file.write('\n')