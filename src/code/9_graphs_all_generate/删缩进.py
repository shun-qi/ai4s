import os

def remove_code_blocks(directory):
    # 遍历主文件夹和其子文件夹
    for root, _, files in os.walk(directory):
        for file in files:
            # 仅处理 .jsonl 文件
            if file.endswith(".jsonl"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # 移除 ``` 和 ```json 标记
                updated_content = content.replace("```", "").replace("```json", "").replace("json", "")

                # 将更新后的内容写回文件
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(updated_content)
                print(f"Processed file: {file_path}")

# 使用主文件夹路径
remove_code_blocks("5_analysis")