# 并行运行 Python 命令
# 注意评估都是使用72B，统一填的。不要填错了
#python 6_analysis.py --model_name_or_path="Qwen2-72B-Instruct-AWQ" --input_path="../data/4_infer_2_res/23-24/Qwen2-72B-Instruct-AWQ/" --output_path="../data/5_analysis/23-24/Qwen2-72B-Instruct-AWQ" --call="vllm"
#python 6_analysis.py --model_name_or_path="Qwen2-72B-Instruct-AWQ" --input_path="../data/4_infer_2_res/23-24/qwen2.5-7b-instruct/" --output_path="../data/5_analysis/23-24/qwen2.5-7b-instruct" --call="vllm"
#python 6_analysis.py --model_name_or_path="Qwen2-72B-Instruct-AWQ" --input_path="../data/4_infer_2_res/23-24/gemini-pro/" --output_path="../data/5_analysis/23-24/gemini-pro" --call="vllm"
#python 6_analysis.py --model_name_or_path="Qwen2-72B-Instruct-AWQ" --input_path="../data/4_infer_2_res/23-24/Doubao-pro-4k/" --output_path="../data/5_analysis/23-24/Doubao-pro-4k" --call="vllm"
#python 6_analysis.py --model_name_or_path="Qwen2-72B-Instruct-AWQ" --input_path="../data/4_infer_2_res/23-24/glm-4-flash/" --output_path="../data/5_analysis/23-24/glm-4-flash" --call="vllm"&
#python 6_analysis.py --model_name_or_path="Qwen2-72B-Instruct-AWQ" --input_path="../data/4_infer_2_res/23-24/gpt-3.5-turbo/" --output_path="../data/5_analysis/23-24/gpt-3.5-turbo" --call="vllm"
#python 6_analysis.py --model_name_or_path="Qwen2-72B-Instruct-AWQ" --input_path="../data/4_infer_2_res/23-24/gpt-4o-mini/" --output_path="../data/5_analysis/23-24/gpt-4o-mini" --call="vllm"
#python 6_analysis.py --model_name_or_path="Qwen2-72B-Instruct-AWQ" --input_path="../data/4_infer_2_res/23-24/hunyuan-lite/" --output_path="../data/5_analysis/23-24/hunyuan-lite" --call="vllm"
#python 6_analysis.py --model_name_or_path="Qwen2-72B-Instruct-AWQ" --input_path="../data/4_infer_2_res/23-24/Llama-3-1-8B-Instruct/" --output_path="../data/5_analysis/23-24/Llama-3-1-8B-Instruct" --call="vllm"
#python 6_analysis.py --model_name_or_path="Qwen2-72B-Instruct-AWQ" --input_path="../data/4_infer_2_res/23-24/mistral-7b-instruct/" --output_path="../data/5_analysis/23-24/mistral-7b-instruct" --call="vllm"
#python 6_analysis.py --model_name_or_path="Qwen2-72B-Instruct-AWQ" --input_path="../data/4_infer_2_res/23-24/DeepSeek-V2.5/" --output_path="../data/5_analysis/23-24/DeepSeek-V2.5" --call="vllm"

python 6_analysis.py --model_name_or_path="Qwen2-72B-Instruct-AWQ" --input_path="../data/4_infer_2_res/23-24/qwen2_7b_instruct/" --output_path="../data/5_analysis/23-24/qwen2_7b_instruct" --call="vllm"#千问2复杂prompt
python 6_analysis.py --model_name_or_path="Qwen2-72B-Instruct-AWQ" --input_path="../data/2_infer_res/23-24/qwen2.5-7b-instruct/" --output_path="../data/5_analysis/23-24/qwen2.5-7b-instruct_simple_prompt" --call="vllm"#千问2.5的简单prompt
python 6_analysis.py --model_name_or_path="Qwen2-72B-Instruct-AWQ" --input_path="../data/2_infer_res/23-24/qwen2_7b_instruct/" --output_path="../data/5_analysis/23-24/qwen2_7b_instruct_simple_prompt" --call="vllm"#千问2的简单prompt

# 去掉了&，使整体串型运行，防止大模型出错，重新运行时都擦出一个文档，开销太大。这样出错只用擦一个文档

echo "所有任务已完成！"
