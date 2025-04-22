import requests
import csv
from typing import List

def fetch_labels(repo_full_name: str, token: str) -> List[dict]:
    """
    获取单个仓库的所有 labels（自动分页）。
    返回一个 dict 列表，每项包含 name 和 description。
    """
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    labels = []
    url = f"https://api.github.com/repos/{repo_full_name}/labels"
    params = {"per_page": 100, "page": 1}

    while True:
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        page_data = resp.json()
        if not page_data:
            break
        labels.extend(page_data)
        # 检查是否还有下一页
        if "next" in resp.links:
            params["page"] += 1
        else:
            break

    return labels

def main():
    # 从环境变量读取 GitHub Token
    token = "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"

    # 在这里填入你要爬取的仓库列表（格式：owner/repo）
    repos = [
        "jax-ml/jax",
        "pytorch/pytorch",
        'tensorflow/tensorflow',
        'NVIDIA/Megatron-LM',
        'deepspeedai/DeepSpeed',
        'vllm-project/vllm',
        'hpcaitech/ColossalAI',
        'NVIDIA/TensorRT-LLM'
    ]

    # 输出 CSV 文件
    output_file = "labels.csv"
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["repository", "label_name", "description"])

        for repo in repos:
            print(f"正在抓取 {repo} ...")
            try:
                labels = fetch_labels(repo, token)
            except requests.HTTPError as e:
                print(f"Error fetching {repo}: {e}")
                continue

            for lbl in labels:
                name = lbl.get("name", "")
                desc = lbl.get("description") or ""
                writer.writerow([repo, name, desc])

    print(f"Done! 所有 labels 已保存到 {output_file}")

if __name__ == "__main__":
    main()