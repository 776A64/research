import requests
import csv
from time import sleep
import time
import re
import os

# 配置
OWNER = "mindspore"   # 仓库所属用户或组织
REPO = "mindspore"  # 仓库名称
ACCESS_TOKEN = os.getenv("gitee_token")
if not ACCESS_TOKEN:
    raise ValueError("未找到环境变量 gitee_token")

def clean(text): # 净化文本内容
    if not text:
        return ""
    lines = text.splitlines()
    non_empty_lines = [line for line in lines if line.strip()]
    cleaned_text = ' '.join(non_empty_lines)
    
    cleaned_text = re.sub(r'Stack from \[ghstack\]\(https://github.com/ezyang/ghstack\) \(oldest at bottom\):?', "",  cleaned_text)
    cleaned_text = re.sub(r'\bcc\b[\s@]+[\w-]+(?:[\s@]+[\w-]+)*', '', cleaned_text) # 删去cc@
    cleaned_text = re.sub(r'@\w+', '', cleaned_text)    # 删去@
    cleaned_text = re.sub(r'-+', '', cleaned_text)         # 删去---------------------
    cleaned_text = re.sub(r'<[^>]*>', '', cleaned_text) # 删去html标签
    cleaned_text = re.sub(r'-+', '', cleaned_text)
    cleaned_text = re.sub(r'\|.*\|', '', cleaned_text)  # 删去表格
    cleaned_text = re.sub(r'\|\|', '', cleaned_text)  
    cleaned_text = re.sub(r"#+", "", cleaned_text)  # 删去#
    cleaned_text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', cleaned_text)   # 删去链接
    
    return cleaned_text


# Gitee API URL
BASE_URL = "https://gitee.com/api/v5/repos/{owner}/{repo}/issues"
COMMENTS_URL = "https://gitee.com/api/v5/repos/{owner}/{repo}/issues/{issue_id}/comments"

# CSV 文件初始化
csv_file = "gitee_issues.csv"
csv_columns = ["number", "title", "body", "Created At", "Tags", "State", "Reactions", "Comments_count", "Link", "Comments"]

# 创建 CSV 文件并写入标题行
with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(csv_columns)

# 获取 Issues 的函数
def get_issues(page=1):
    url = BASE_URL.format(owner=OWNER, repo=REPO)
    
    params = {
        "page" : page,
        "per_page" : 100,
        "access_token" : ACCESS_TOKEN,
        "state" : "all",
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(response.text)
        return []

# 获取评论的函数
def get_comments(issue_id):
    url = COMMENTS_URL.format(owner=OWNER, repo=REPO, issue_id=issue_id)
    params = {
        "page" : 1,
        "per_page" : 100,
        "access_token" : ACCESS_TOKEN,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(response.text)
        return []

# 获取 Issue 的详细信息
def process_issue(issue, cnt):
    issue_title = clean(issue['title'])
    issue_body = clean(issue.get('body', ""))
    issue_created_at = issue['created_at']
    issue_labels = ",".join(label['name'] for label in issue.get('labels', []))
    issue_state = issue['state']
    issue_reactions = issue.get('reactions', {}).get('total_count', 0)
    issue_comments_count = issue['comments']
    issue_url = issue['html_url']
    comment_texts = []
    if issue_comments_count:
        comments = get_comments(issue['number'])

        for comment in comments:
            commenter = comment['user']['name']
            if commenter.lower() == 'i-robot':
                issue_comments_count -= 1  # 排除 "i-robot" 的评论
                continue
            comment_texts.append(clean(comment['body']))

    # 保存数据到 CSV 文件
    with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([cnt, issue_title, issue_body, issue_created_at, issue_labels, issue_state, issue_reactions, issue_comments_count, issue_url, *comment_texts])

# 主函数
def main():
    page = 1
    cnt = 1 
    begin_time = time.time()
    while True:
        issues = get_issues(page)
        if not issues:
            break
        for issue in issues:
            process_issue(issue, cnt)
            if cnt % 20 == 0:
                print(f"-------------------------{cnt}条issue完成, 用时{(time.time() - begin_time) / 60}分钟-------------------------")
            cnt += 1
        page += 1




if __name__ == "__main__":
    main()