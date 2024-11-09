import json
import numpy as np
import matplotlib.pyplot as plt
from math import pi

class ModelAnalysis:
    def __init__(self, json_path):
        # 初始化类并加载JSON文件
        self.json_path = json_path
        self.data = self.load_data()

    def load_data(self):
        # 加载JSON数据
        with open(self.json_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_metrics_for_model(self, model_folder):
        # 提取同一模型在各科目上的指定指标
        data = {
            'sub': [],
            'completeness_avg': [],
            'innovation_avg': [],
            'reasoning_avg': [],
            'correct_rate': []
        }
        for subject, metrics in self.data.get(model_folder, {}).items():
            data['sub'].append(subject)
            data['completeness_avg'].append(metrics.get('completeness_avg', 0) )  # 转换到0-10范围
            data['innovation_avg'].append(metrics.get('innovation_avg', 0) )
            data['reasoning_avg'].append(metrics.get('reasoning_avg', 0) )
            data['correct_rate'].append(metrics.get('correct_rate', 0) *5)  # 保持在0-10范围
        return data




    def get_all_subjects(self):
        # 获取所有科目名称
        subjects = set()
        for model_data in self.data.values():
            subjects.update(model_data.keys())
        return list(subjects)
    def get_all_model(self):
        models = []
        for model in self.data.keys():
            models.append(model)
        return list(models)
    
    def get_metrics_for_subject(self, model_folder, subject):
        # 获取特定模型和科目的数据
        metrics = self.data.get(model_folder, {}).get(subject, {})
        if metrics:
            return [
                metrics.get('completeness_avg', 0),
                metrics.get('innovation_avg', 0),
                metrics.get('reasoning_avg', 0),
                metrics.get('correct_rate', 0)
            ]
        return {}
    def get_ave_metrics(self, model_folder):
        subjects = self.get_all_subjects()
        sum_metrics = [0, 0, 0, 0]  # 初始化为0的列表
        for subject in subjects:
            # 获取每个主体的度量值
            metrics = self.get_metrics_for_subject(model_folder, subject)
            # 对应位置的元素相加
            sum_metrics = [sum_metrics[i] + metrics[i] for i in range(4)]
        
        # 计算平均值
        num_subjects = len(subjects)
        if num_subjects > 0:  # 防止除以0的情况
            average_metrics = [metric / num_subjects for metric in sum_metrics]
        else:
            average_metrics = sum_metrics  # 如果没有主体，则返回全0的结果
        
        return average_metrics
def Comprehensive(analysis):
    for subject in analysis.get_all_subjects():
        plt.figure(figsize=(8, 8))
        angles = np.linspace(0, 2 * pi, 4, endpoint=False).tolist()
        angles += angles[:1]  # 闭合环

        max_range = 5  # 设置更大的坐标轴范围

        for model_folder in analysis.data.keys():
            data = analysis.get_metrics_for_subject(model_folder, subject)
            if not data:
                continue
            data[3]*=5
            data += data[:1]  # 闭合环

            plt.polar(angles, data, label=model_folder, linewidth=2, marker='o')  # 加粗线条和标记

        plt.title(f"Radar Chart for {subject}")
        plt.xticks(angles[:-1], ['Completeness', 'Innovation', 'Reasoning', 'Correct Rate'])
        plt.ylim(0, max_range)  # 设置Y轴的最大值
        plt.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))
        plt.show()
def Correctness2(analysis):
    import matplotlib.pyplot as plt
    import numpy as np
    import seaborn as sns
    import pandas as pd

    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
    plt.rcParams['axes.unicode_minus'] = False  # 显示负号
    models = analysis.get_all_model()
    subjects = {subject: [] for subject in analysis.get_all_subjects()}
    for model in models:
        for subject in analysis.get_all_subjects():
            subjects[subject].append(analysis.get_metrics_for_subject(model,subject)[3])
    scores_df = pd.DataFrame(subjects, index=models)
    # 2.4 表现矩阵热力图展示
    plt.figure(figsize=(10, 6))
    sns.heatmap(scores_df, annot=True, fmt=".2f", cmap="YlGnBu", cbar=True)
    plt.title('模型在各科目上正确率表现')
    plt.xlabel('维度')
    plt.ylabel('模型')
    plt.tight_layout()

    # 显示热力图
    plt.show()

def Correctness(analysis):
    import json
    import pandas as pd
    data=analysis.data
    # 提取 correct_rate 并创建 DataFrame
    result = {}
    for model, subjects in data.items():
        result[model] = {subject: info.get('correct_rate', None) for subject, info in subjects.items()}
    # 创建一个DataFrame
    df_correct_rate = pd.DataFrame(result).transpose()
    # 保存 DataFrame 到 CSV 文件
    output_path = r"correct_rate_table.csv"
    df_correct_rate.to_csv(output_path)
    print("表格已成功保存到", output_path)

def Completeness_and_Innovation(analysis):
    # 按这个生成：1.3 完整性与创新性（Completeness & Innovation）
    # 指标：completeness_score 和 innovation_score 的平均值。
    # 分析：分别考察模型回答的完整性和创新性，以区分模型在回答细节和独特回答方面的表现。
    import matplotlib.pyplot as plt
    import numpy as np
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
    plt.rcParams['axes.unicode_minus'] = False  # 显示负号
    # 示例模型名称
    models = analysis.get_all_model()
    completeness_scores=[]
    innovation_scores=[]
    for model in models:
        res=analysis.get_ave_metrics(model)
        completeness_scores.append(res[0])
        innovation_scores.append(res[1])


    # 绘制散点图
    plt.figure(figsize=(10, 10))
    plt.scatter(completeness_scores, innovation_scores)

    # 标注模型
    for i, model in enumerate(models):
        plt.annotate(model, (completeness_scores[i], innovation_scores[i]), textcoords="offset points", xytext=(0, 5), ha='center')

    # 添加标题和标签
    plt.title('各模型的完整性与创新性得分')
    plt.xlabel('完整性得分 (0-5)')
    plt.ylabel('创新性得分 (0-5)')
    plt.xlim(0, 5)
    plt.ylim(0, 5)
    plt.grid()

    # 显示图形
    plt.tight_layout()
    plt.show()

def Reasoning(analysis):
    # 1.4 推理能力与逻辑性（Reasoning Ability）
    # 指标：reasoning_score 的均值。
    # 分析：该分数反映模型推理的严谨性和逻辑性，考察模型在理解复杂问题、推理和解释方面的能力。
    # 对比方法：可以结合完整性与创新性一并展示，或单独用柱状图对比每个模型的逻辑得分。
    import matplotlib.pyplot as plt
    import numpy as np
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
    plt.rcParams['axes.unicode_minus'] = False  # 显示负号
    # 示例模型名称
    models = analysis.get_all_model()
    reasoning_scores=[]
    for model in models:
        res=analysis.get_ave_metrics(model)
        reasoning_scores.append(res[2])


    # 绘制柱状图
    plt.figure(figsize=(10, 6))
    bars = plt.bar(models, reasoning_scores, color='skyblue')

    # 添加数据标签
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')

    # 添加标题和标签
    plt.title('各模型的推理能力与逻辑性得分')
    plt.xlabel('模型')
    plt.ylabel('推理得分 (0-5)')
    plt.ylim(0, 5)
    plt.grid(axis='y')

    # 显示图形
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def Student_Level(analysis):
    import json
    import pandas as pd
    data=analysis.data
    # 提取 correct_rate 并创建 DataFrame
    result = {}
    for model, subjects in data.items():
        result[model] = {subject: info.get('level_rate', None) for subject, info in subjects.items()}
    # 创建一个DataFrame
    df_correct_rate = pd.DataFrame(result).transpose()
    # 保存 DataFrame 到 CSV 文件
    output_path = r"level_rate.csv"
    df_correct_rate.to_csv(output_path)
    print("表格已成功保存到", output_path)
 
json_path = r'5_analysis\analysis_results.json'
analysis = ModelAnalysis(json_path)
Comprehensive(analysis)
Completeness_and_Innovation(analysis)
Correctness2(analysis)
Correctness(analysis)
Reasoning(analysis)
Student_Level(analysis)