
#python 2_infer.py --model_name_or_path="gpt-3.5-turbo" --input_path="./data/2_ICL_QA/RE" --output_path="./data/3_inferenced_result/RE" --call="vllm" --use_icl="False"
python 2_infer.py --model_name_or_path="qwen2_7b_instruct" --input_path="../data/1_QA/" --output_path="../data/test_dir/qwen2_7b_instruct/" --call="vllm"
