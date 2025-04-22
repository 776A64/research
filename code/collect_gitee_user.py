import requests
import re
import csv
from concurrent.futures import ThreadPoolExecutor
import os

ACCESS_TOKEN = os.getenv("gitee_token")
if not ACCESS_TOKEN:
    raise ValueError("未找到环境变量 gitee_token")
csv.field_size_limit(10 * 1024 * 1024)
data_name = 'mindspore'

def get_issue_creator(issue_url):
    # 解析 URL 提取关键信息
    pattern = r"https://gitee.com/([^/]+)/([^/]+)/issues/([^/]+$)"
    match = re.match(pattern, issue_url)
    
    if not match:
        return "Invalid Gitee issue URL"
    
    owner, repo, issue_id = match.groups()
    
    # 构造 API 请求
    api_url = f"https://gitee.com/api/v5/repos/{owner}/{repo}/issues/{issue_id}"
    params = {'access_token': ACCESS_TOKEN}
    
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # 自动处理 HTTP 错误
        data = response.json()
        
        # 提取提出者信息
        if 'user' in data and 'login' in data['user']:
            return data['user']['login']
        else:
            return "Creator information not found"
            
    except requests.exceptions.RequestException as e:
        return f"API request failed: {str(e)}"

def deal_one_issue(row, output_csv):
    creator = get_issue_creator(row[7])
    row.insert(0, creator)
    with open(output_csv, 'a', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(row)
        
def check_one_issue(row, output_csv):
    with open(output_csv, 'a', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        if "API request failed" in row[0]:
            creator = get_issue_creator(row[8])
            row[0] = creator
            writer.writerow(row)
        else: 
            writer.writerow(row)

# 使用示例
'''
if __name__ == "__main__":
    for year in range(2022, 2025):
        input_csv = rf'C:\pyprogram\research\data\{data_name}\{year}\{data_name}_{year}.csv'
        output_csv = rf'C:\pyprogram\research\data\{data_name}\{year}\{data_name}_{year}_user.csv'
        with open(output_csv, 'w', encoding='utf-8', newline='') as outfile:
            pass
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = []
            with open(input_csv, 'r', encoding='utf-8') as infile:
                reader = csv.reader(infile)
                next(reader)
                for row in reader:
                    futures.append(executor.submit(deal_one_issue, row, output_csv))
        
            # 等待所有线程完成
            for future in futures:
                future.result()  # 等待每个线程的结果
'''
                
 
def check():            
    for year in range(2022, 2025):
        input_csv = rf'C:\pyprogram\research\data\{data_name}\{year}\{data_name}_{year}_user.csv'
        output_csv = rf'C:\pyprogram\research\data\{data_name}\{year}\{data_name}_{year}_user_check.csv'
        with open(output_csv, 'w', encoding='utf-8', newline='') as outfile:
            pass
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            with open(input_csv, 'r', encoding='utf-8') as infile:
                reader = csv.reader(infile)
                for row in reader:
                    futures.append(executor.submit(check_one_issue, row, output_csv))
        
            # 等待所有线程完成
            for future in futures:
                future.result()  # 等待每个线程的结果
            
check()