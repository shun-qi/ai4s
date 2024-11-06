# 并行运行 Python 命令
# 注意评估都是使用72B，统一填的。不要填错了
python 8_different_prompt_analysis.py --model_name_or_path="Qwen2-72B-Instruct-AWQ" --input_path="../data/2_infer_res/qwen2_7b_instruct" --output_path="../data/5_analysis/qwen2_7b_instruct_simple_prompt" --call="vllm"
# 去掉了&，使整体串型运行，防止大模型出错，重新运行时都擦出一个文档，开销太大。这样出错只用擦一个文档
echo "所有任务已完成！"

