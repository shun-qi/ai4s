import pandas as pd
import os
import re
import numpy as np
import matplotlib.pyplot as plt

# 初始化一个空列表以存储 DataFrame 的数据
data = []

# 遍历每个模型文件夹
model_folders = os.listdir("../data/4_infer_2_res")
for model in model_folders:
    time_count_path = os.path.join("../data/4_infer_2_res", model, "time_count.txt")

    if os.path.isfile(time_count_path):
        model_data = {'Model': model}

        with open(time_count_path, 'r', encoding='utf-8') as file:
            for line in file:
                match = re.search(r'处理(\w+\.jsonl)文件耗时：(\d+)小时\s+(\d+)分钟\s+(\d+)秒', line)
                if match:
                    subject = match.group(1).replace('.jsonl', '')
                    hours = int(match.group(2))
                    minutes = int(match.group(3))
                    seconds = int(match.group(4))
                    total_time = hours * 3600 + minutes * 60 + seconds
                    model_data[subject] = total_time

        data.append(model_data)

# 从数据列表创建 DataFrame
df = pd.DataFrame(data)

# 用 0 替换任何缺失的学科数据
df.fillna(0, inplace=True)

# 准备绘制雷达图
labels = df.columns[1:]  # 不包含模型名称
num_vars = len(labels)

# 设置雷达图的角度
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

# 完成循环并闭合雷达图
angles += angles[:1]

# 创建图形和坐标轴
fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))

# 绘制每个模型的雷达图
for index, row in df.iterrows():
    values = row[1:].values.flatten().tolist()
    values += values[:1]  # 闭合图形
    ax.fill(angles, values, alpha=0.25)  # 填充颜色
    ax.plot(angles, values, label=row['Model'])  # 绘制边框

# 添加标签
ax.set_yticklabels([])  # 隐藏 y 轴标签
ax.set_xticks(angles[:-1])  # 设置 x 轴刻度
ax.set_xticklabels(labels)  # 设置 x 轴标签

# 添加图例
plt.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))
plt.title('各模型学科处理时间雷达图')
plt.show()
