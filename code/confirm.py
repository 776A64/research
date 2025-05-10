import requests
import csv
import re
import time
import os

access_token = os.getenv("GITHUB_TOKEN")
if not access_token:
    raise ValueError("未找到环境变量 GITHUB_TOKEN")

repo_list = [('pytorch', 'pytorch')]

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

def confirm_csv(csv_filename, owner_name, repo_name):
    with open(csv_filename.split('.')[0] + '_confirmed.csv', mode='w', encoding='utf-8', newline='') as csvfile:
        pass
    with open(csv_filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        last_number = 153145
        retry = True
        for row in reader:
            try:
                number = int(row[8][-6:])
            except:
                print(row)
            if last_number <= number:
                continue
            while last_number - number != 1:
                last_number -= 1
                try:
                    issue_url = f"https://api.github.com/repos/{owner_name}/{repo_name}/issues/{str(last_number)}"
                    issue_response = requests.get(issue_url, headers=headers)
                    issue_data = issue_response.json()                    
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
                    with open(csv_filename.split('.')[0] + '_confirmed.csv', mode='a', encoding='utf-8', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(result_ls)   
                    print(f'{last_number}缺少，已写入')
                    retry = True
                except:
                    print(f'{last_number}缺少，写入时发生错误')
                    if retry:
                        last_number += 1
                        retry = False
                    time.sleep(2)
            with open(csv_filename.split('.')[0] + '_confirmed.csv', mode='a', encoding='utf-8', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(row)   
            last_number = number
                


if __name__ == '__main__':
    for repo in repo_list:
        csv_filename = rf"C:\pyprogram\research\data\{repo[1]}\2025\{repo[1]}_2025_user.csv"
        confirm_csv(csv_filename, repo[0], repo[1])