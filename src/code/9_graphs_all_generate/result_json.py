import os
import json


#用于提取处理好的json文件

"""
这个代码的主要功能是遍历一个文件夹中的所有子文件夹，
读取并分析每个文件夹中的.jsonl文件，
将评分信息汇总并保存到最终的 JSON 文件中
"""
def analyze_ratings(file_path):
    correctness_total = 0
    completeness_total = 0
    innovation_total = 0
    reasoning_total = 0
    level = [0, 0, 0]
    count = 0
    is_correct_total = 0

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            try:
                # 解析每行 JSON 数据
                element = json.loads(line)
                if isinstance(element['rating'], str):
                    data = json.loads(element['rating'])
                else:
                    data = element['rating']
            except (json.JSONDecodeError, TypeError) as e:
                print(f"Warning: Failed to decode line {i+1} in {file_path}: {e}")
                continue  # 跳过当前行，继续下一个

            if isinstance(data, dict):  # 确保 data 是字典
                count += 1
                
                # 检查每个字段是否存在
                if "correctness_score" in data:
                    correctness_total += data["correctness_score"]
                if "completeness_score" in data:
                    completeness_total += data["completeness_score"]
                if "innovation_score" in data:
                    innovation_total += data["innovation_score"]
                if "reasoning_score" in data:
                    reasoning_total += data["reasoning_score"]

                if "is_correct" in data and data["is_correct"] is True:
                    is_correct_total += 1

                if "student_level" in data:
                    if data["student_level"] == "大学":
                        level[0] += 1
                    elif data["student_level"] == "高中":
                        level[1] += 1
                    else:
                        level[2] += 1

    if count > 0:
        correctness_avg = correctness_total / count
        completeness_avg = completeness_total / count
        innovation_avg = innovation_total / count
        reasoning_avg = reasoning_total / count
        correct_rate = is_correct_total / count
        level_rate = [element / count for element in level]
        
        return {
            "correctness_avg": correctness_avg,
            "completeness_avg": completeness_avg,
            "innovation_avg": innovation_avg,
            "reasoning_avg": reasoning_avg,
            "correct_rate": correct_rate,
            "level_rate": level_rate
        }
    else:
        return None

def func(directory):
    results = {}  # 用于存储最终所有文件夹的结果

    for root, dirs, files in os.walk(directory):
        if root == directory:
            continue
        
        folder_name = os.path.basename(root)
        folder_results = {}  # 用于存储当前文件夹中每个文件的结果

        for file in files:
            if file.endswith(".jsonl"):
                file_path = os.path.join(root, file)
                result = analyze_ratings(file_path)
                
                if result:
                    # 将文件结果添加到当前文件夹的字典中
                    folder_results[file] = result

        # 将当前文件夹的结果添加到总结果字典中
        if folder_results:
            results[folder_name] = folder_results

    # 将最终结果保存为 JSON 文件
    output_file_path = os.path.join(directory, "analysis_results.json")
    with open(output_file_path, 'w', encoding='utf-8') as out_file:
        json.dump(results, out_file, ensure_ascii=False, indent=4)

# 使用示例
func("5_analysis")
