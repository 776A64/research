import requests
import csv
import re
import time
import os

access_token = os.getenv("GITHUB_TOKEN")
if not access_token:
    raise ValueError("未找到环境变量 GITHUB_TOKEN")

repo_list = [('mindspore-lab', 'mindnlp')]

headers = {
    "Authorization": f"Bearer {access_token}"
}

def replacer(match, owner_name, repo_name):
    issue_number = match.group(5)
    url = f"https://api.github.com/repos/{owner_name}/{repo_name}/issues/{issue_number}"
    resp = requests.get(url, headers=headers).json()
    return " CC(" + resp.get("title", "未找到相关数据") + ")"

def clean(text, owner_name, repo_name): # 净化文本内容
    if not text:
        return ""
    lines = text.splitlines()
    non_empty_lines = [line for line in lines if line.strip()]
    cleaned_text = ' '.join(non_empty_lines)
    
    cleaned_text = re.sub(r'Stack from \[ghstack\]\(https://github.com/ezyang/ghstack\) \(oldest at bottom\):?', "",  cleaned_text)
    cleaned_text = re.sub(r"(\*)?(\s?)(__->__)?(\s*)#(\d{1,6})", lambda m: replacer(m, owner_name, repo_name), cleaned_text)    # 将#number替换成title
    cleaned_text = re.sub(r'\bcc\b[\s@]+[\w-]+(?:[\s@]+[\w-]+)*', '', cleaned_text) # 删去cc@
    cleaned_text = re.sub(r'@\w+', '', cleaned_text)    # 删去@
    cleaned_text = re.sub(r'-+', '', cleaned_text)         # 删去---------------------
    cleaned_text = re.sub(r'<[^>]*>', '', cleaned_text) # 删去html标签
    cleaned_text = re.sub(r'-+', '', cleaned_text)
    cleaned_text = re.sub(r'\|.*\|', '', cleaned_text)  # 删去表格
    cleaned_text = re.sub(r'\|\|', '', cleaned_text)  
    cleaned_text = re.sub(r"#+", "", cleaned_text)  # 删去#
    cleaned_text = re.sub(rf"(https)(://github)(.com/{owner_name})(/{repo_name}/issues/)(\d{1,6})", lambda m: replacer(m, owner_name, repo_name), cleaned_text)
    cleaned_text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', cleaned_text)   # 删去链接
    
    return cleaned_text

def get_github_repository_issues(page, csv_filename, owner_name, repo_name):
    cnt = 1
    params = {
        "page": page,
        "per_page": 100,  # 每页最多返回100个issues，根据实际情况调整
        "state": "all"  # 包含Open和Closed状态的issues
    }
    issues_url = f"https://api.github.com/repos/{owner_name}/{repo_name}/issues"
    begin_time = time.time()
    while True:
        issues = requests.get(issues_url, headers=headers, params=params).json()
        if not issues:
            time.sleep(20)
            issues = requests.get(issues_url, headers=headers, params=params).json()
            if not issues:
                break
        for issue in issues:
            try:
                issue_url = f"https://api.github.com/repos/{owner_name}/{repo_name}/issues/{issue['number']}"
                issue_response = requests.get(issue_url, headers=headers)
                issue_data = issue_response.json()
                if int(issue_data['created_at'][:4]) < 2019:    # 五年前的数据丢弃
                    continue
                
                body = clean(issue_data["body"], owner_name, repo_name)

                result_ls = [
                    issue_data.get("user", {}).get("login"),
                    issue_data["title"],
                    body,
                    issue_data["created_at"],
                    " ".join(x["name"] for x in issue_data["labels"]),
                    issue_data["state"],
                    issue_data["reactions"]["total_count"],
                    issue_data["comments"],
                    f"https://github.com/{owner_name}/{repo_name}/issues/{issue_data["number"]}",
                ]
                
                if issue_data["comments"]:      # 如果有子评论，写入子评论
                    resp = requests.get(issue_data["comments_url"], headers=headers).json()
                    for i in resp:
                        result_ls.append(clean(i["body"], owner_name, repo_name))
                with open(csv_filename, mode='a', encoding='utf-8', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(result_ls)   

                if cnt % 20 == 0:
                    print(f"-------------------------{cnt}条issue完成, 用时{(time.time() - begin_time) / 60}分钟-------------------------")
                cnt += 1
                
            except:
                time.sleep(10)
                continue
                
        params['page'] += 1


if __name__ == '__main__':
    for repo in repo_list:
        csv_filename = rf"C:\pyprogram\research\data\{repo[1]}.csv"
        get_github_repository_issues(1, csv_filename, repo[0], repo[1])