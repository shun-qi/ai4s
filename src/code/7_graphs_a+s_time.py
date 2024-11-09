import os
import re
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager

# 设置中文字体
font_path = '/System/Library/Fonts/STHeiti Light.ttc'  # 替换为你系统中的字体路径
font_prop = font_manager.FontProperties(fname=font_path)

# 加载学科题目数量
def load_subject_nums(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

science_subject_nums = load_subject_nums("../S_subject_nums_map.json")
arts_subject_nums = load_subject_nums("../A_subject_nums_map.json")

# 读取模型文件夹
model_folders = os.listdir("../data/4_infer_2_res")
data_science = []
data_arts = []

# 遍历模型文件夹并计算平均时间
for model in model_folders:
    time_count_path = os.path.join("../data/4_infer_2_res", model, "time_count.txt")

    if os.path.isfile(time_count_path):
        model_data_science = {'Model': model}
        model_data_arts = {'Model': model}

        with open(time_count_path, 'r', encoding='utf-8') as file:
            for line in file:
                match = re.search(r'处理(\w+\.jsonl)文件耗时：(\d+)小时\s+(\d+)分钟\s+(\d+)秒', line)
                if match:
                    subject = match.group(1).replace('.jsonl', '')
                    hours = int(match.group(2))
                    minutes = int(match.group(3))
                    seconds = int(match.group(4))
                    total_time = hours * 3600 + minutes * 60 + seconds

                    # 计算理科和文科的平均时间
                    if subject in science_subject_nums:
                        average_time = total_time / science_subject_nums[subject]
                        model_data_science[subject] = average_time
                    elif subject in arts_subject_nums:
                        average_time = total_time / arts_subject_nums[subject]
                        model_data_arts[subject] = average_time

        data_science.append(model_data_science)
        data_arts.append(model_data_arts)

# 将数据转换为 DataFrame，并处理缺失值
df_science = pd.DataFrame(data_science).fillna(0)
df_arts = pd.DataFrame(data_arts).fillna(0)

# 绘制雷达图的函数
def plot_radar_chart(df, subject_type, output_path):
    labels = df.columns[1:]
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))

    for _, row in df.iterrows():
        values = row[1:].values.flatten().tolist()
        values += values[:1]
        ax.fill(angles, values, alpha=0.25)
        ax.plot(angles, values, label=row['Model'])

    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontproperties=font_prop)
    plt.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1), prop=font_prop)
    plt.title(f'{subject_type}各模型平均每道题处理时间雷达图(单位秒)', fontproperties=font_prop)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"{subject_type}雷达图已保存到：{output_path}")

# 分别绘制理科和文科的雷达图
plot_radar_chart(df_science, "理科", "../data/6_graphs/23-24/S_science_average_time_radar_chart.png")
plot_radar_chart(df_arts, "文科", "../data/6_graphs/23-24/A_arts_average_time_radar_chart.png")
