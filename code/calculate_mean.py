import csv
import os

def calculate_mean_and_rename(filename):
    # 读取第一列数据
    values = []
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:  # 跳过空行
                    continue
                if len(row) >= 1:
                    first_col = row[0].strip()
                    try:
                        num = float(first_col)
                        values.append(num)
                    except ValueError:
                        continue  # 跳过非数字内容
    except FileNotFoundError:
        print(f"错误：文件 '{filename}' 不存在")
        return

    # 检查有效数据
    if not values:
        print("错误：文件中没有有效的数字数据")
        return

    # 计算平均值（保留两位小数）
    average = round(sum(values) / len(values), 2)

    # 构建新文件名
    base, ext = os.path.splitext(filename)
    new_filename = f"{base}_mean={average}{ext}"

    # 重命名文件
    try:
        os.rename(filename, new_filename)
        print(f"文件已重命名为：{new_filename}")
        print(f"第一列数字平均值：{average}")
    except OSError as e:
        print(f"重命名失败：{e}")

for data_name in ['tensorflow', 'jax', 'mindspore', 'pytorch']:
    for year in range(2022, 2026):
        input_file = rf'C:\pyprogram\research\data\{data_name}\{year}\{data_name}_{year}_prompt_origin.csv'
        calculate_mean_and_rename(input_file)



        
