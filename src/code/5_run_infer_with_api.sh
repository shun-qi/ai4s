#python 5_infer_with_api.py --model_name_or_path="Qwen2-72B-Instruct-AWQ" --input_path="../data/3_QA_2/" --output_path="../data/5_analysis/Qwen2-72B-Instruct-AWQ/" --call="vllm" &
#python 5_infer_with_api.py --model_name_or_path="gpt-4o-mini" --input_path="../data/3_QA_2/" --output_path="../data/4_infer_2_res/gpt-4o-mini" --call="vllm"  &
#python 5_infer_with_api.py --model_name_or_path="gpt-3.5-turbo" --input_path="../data/3_QA_2/" --output_path="../data/4_infer_2_res/gpt-3.5-turbo" --call="vllm" &
#python 5_infer_with_api.py --model_name_or_path="qwen2.5-7b-instruct" --input_path="../data/3_QA_2/" --output_path="../data/4_infer_2_res/qwen2.5-7b-instruct" --call="vllm" &
#python 5_infer_with_api.py --model_name_or_path="aihubmix-Llama-3-1-8B-Instruct" --input_path="../data/3_QA_2/" --output_path="../data/4_infer_2_res/Llama-3-1-8B-Instruct" --call="vllm" &
#python 5_infer_with_api.py --model_name_or_path="mistralai/mistral-7b-instruct:free" --input_path="../data/3_QA_2/" --output_path="../data/4_infer_2_res/mistral-7b-instruct" --call="vllm" &
python 5_infer_with_api.py --model_name_or_path="glm-4-flash" --input_path="../data/3_QA_2/" --output_path="../data/4_infer_2_res/glm-4-flash" --call="vllm" &
python 5_infer_with_api.py --model_name_or_path="gemini-pro" --input_path="../data/3_QA_2/" --output_path="../data/4_infer_2_res/gemini-pro" --call="vllm" &
python 5_infer_with_api.py --model_name_or_path="deepseek-ai/DeepSeek-V2.5" --input_path="../data/3_QA_2/" --output_path="../data/4_infer_2_res/DeepSeek-V2.5" --call="vllm"&
python 5_infer_with_api.py --model_name_or_path="babbage-002" --input_path="../data/3_QA_2/" --output_path="../data/4_infer_2_res/babbage-002" --call="vllm" &
python 5_infer_with_api.py --model_name_or_path="dall-e-3" --input_path="../data/3_QA_2/" --output_path="../data/4_infer_2_res/dall-e-3" --call="vllm" &
python 5_infer_with_api.py --model_name_or_path="hunyuan-lite" --input_path="../data/3_QA_2/" --output_path="../data/4_infer_2_res/hunyuan-lite" --call="vllm" &
python 5_infer_with_api.py --model_name_or_path="Doubao-pro-4k" --input_path="../data/3_QA_2/" --output_path="../data/4_infer_2_res/Doubao-pro-4k" --call="vllm" &


#python 5_infer_with_api.py --model_name_or_path="Yi-6B-200K" --input_path="../data/3_QA_2/" --output_path="../data/4_infer_2_res/Yi-6B-200K" --call="vllm"
#python 5_infer_with_api.py --model_name_or_path="chatglm2-6b" --input_path="../data/3_QA_2/" --output_path="../data/4_infer_2_res/chatglm2-6b" --call="vllm"

# 每行最后加&可以并发执行
