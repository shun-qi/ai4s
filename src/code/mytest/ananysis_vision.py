import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 假设我们有一些模型评分数据
data = {
    'Model': ['Model_A_v1', 'Model_A_v2', 'Model_B_v1', 'Model_B_v2'],
    'Accuracy': [8.5, 9.0, 7.5, 8.0],
    'Inference Speed': [7.0, 8.0, 6.5, 7.0],
    'Stability': [8.0, 8.5, 7.0, 7.5],
    'Memory Usage': [7.5, 8.0, 7.0, 6.5]
}

# 将数据转换为 DataFrame 格式
df = pd.DataFrame(data)

# 设置雷达图的标签和数据
labels = df.columns[1:]  # 跳过第一个 "Model" 列
num_vars = len(labels)

# 准备数据：标准化评分并添加回到起始点
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]

# 绘制雷达图
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

for i, row in df.iterrows():
    values = row.drop('Model').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, label=row['Model'])
    ax.fill(angles, values, alpha=0.25)

# 设置图标和标题
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)
plt.xticks(angles[:-1], labels)

# 添加图例
ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))

# 保存雷达图为 PNG 文件
plt.savefig('radar_chart.png', bbox_inches='tight')  # 'tight' 使得图形不被裁剪
plt.close()  # 关闭雷达图

# 计算每个模型的总评分
df['Total Score'] = df[['Accuracy', 'Inference Speed', 'Stability', 'Memory Usage']].mean(axis=1)

# 绘制柱状图
plt.figure(figsize=(10, 6))
plt.bar(df['Model'], df['Total Score'], color='skyblue')
plt.title('Total Score of Different Models')
plt.xlabel('Models')
plt.ylabel('Total Score')
plt.ylim(0, 10)  # 假设总评分的范围是0到10

# 保存柱状图为 PNG 文件
plt.savefig('bar_chart.png', bbox_inches='tight')  # 'tight' 使得图形不被裁剪
plt.close()  # 关闭柱状图

