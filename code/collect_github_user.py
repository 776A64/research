import requests
import re
import os
import csv
from concurrent.futures import ThreadPoolExecutor

os.environ["http_proxy"] = "http://127.0.0.1:7890"  # 替换为您的代理地址和端口
os.environ["https_proxy"] = "http://127.0.0.1:7890"  # 替换为您的代理地址和端口
csv.field_size_limit(10 * 1024 * 1024)
data_name = 'jax'
github_token = os.getenv("GITHUB_TOKEN")
if not github_token:
    raise ValueError("未找到环境变量 GITHUB_TOKEN")


def get_issue_creator(issue_url):
    """
    根据 GitHub issue 的 URL 获取创建者的昵称，并使用 GitHub 的 Token 进行认证。
    URL 示例: https://github.com/pytorch/pytorch/issues/70597
    """
    # 使用正则表达式解析 URL，提取 owner、repo 以及 issue 编号
    match = re.search(r'github\.com/([^/]+)/([^/]+)/issues/(\d+)', issue_url)
    if not match:
        raise ValueError("无效的 GitHub issue URL")
    owner, repo, issue_number = match.groups()

    # 构造 GitHub API 的 URL
    api_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
    
    # 设置认证的请求头
    headers = {
        "Authorization": f"Bearer {github_token}"
    }
    
    # 发起 GET 请求获取 issue 的 JSON 数据
    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"获取 issue 信息失败，状态码: {response.status_code}")
    
    data = response.json()
    
    # 从返回的 JSON 数据中提取创建者的昵称（login 字段）
    creator = data.get("user", {}).get("login")
    return creator


def deal_one_issue(row, output_csv):
    issue_url = row[7]
    try:
        creator_nickname = get_issue_creator(issue_url)
    except Exception as e:
        creator_nickname = '未能获取用户名'
    row.insert(0, creator_nickname)
    with open(output_csv, mode='a', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(row)
        
def process_batch(input_csv, output_csv, executor, start_row, max_batch_size=5000):
    processed = 0
    with open(input_csv, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        # 跳过已处理的行
        for _ in range(start_row):
            next(reader, None)
        futures = []
        cnt = 0
        for row in reader:
            if cnt >= max_batch_size:
                break
            futures.append(executor.submit(deal_one_issue, row, output_csv))
            cnt += 1
        processed = cnt
    return processed
'''
if __name__ == "__main__":
    for year in range(2024, 2025):
        input_csv = rf'C:\pyprogram\research\data\{data_name}\{year}\{data_name}_{year}.csv'
        output_csv = rf'C:\pyprogram\research\data\{data_name}\{year}\{data_name}_{year}_user.csv'
        processed_total = 6343
        with ThreadPoolExecutor(max_workers=20) as executor:
            while True:
                # 处理一批，最多5000行
                batch_processed = process_batch(input_csv, output_csv, executor, processed_total)
                if batch_processed == 0:
                    break  # 所有行处理完毕
                processed_total += batch_processed
                # 如果本批处理达到5000，暂停一小时
                if batch_processed >= 5000:
                    print(f"已达到5000行，暂停一小时。已处理总数: {processed_total}")
                    time.sleep(3600)  # 等待1小时
                else:
                    print(f"最后一批处理完成，总数: {processed_total}")
        time.sleep(3600)
'''

def check_one_issue(row, output_csv):
    if "未能获取用户名" in row[0]:
        issue_url = row[8]
        try:
            creator_nickname = get_issue_creator(issue_url)
        except Exception as e:
            creator_nickname = '未能获取用户名'
        row[0] = creator_nickname
    with open(output_csv, mode='a', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(row)

def check():
    for year in range(2022, 2025):
        input_csv = rf'C:\pyprogram\research\data\{data_name}\{year}\{data_name}_{year}_user.csv'
        output_csv = rf'C:\pyprogram\research\data\{data_name}\{year}\{data_name}_{year}_user_check.csv'
        with open(input_csv, 'r', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            for row in reader:
                with ThreadPoolExecutor(max_workers=40) as executor:
                    futures = []
                    futures.append(executor.submit(check_one_issue, row, output_csv))
            
            for future in futures:
                future.result()

check()