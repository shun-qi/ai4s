import time

from transformers import AutoModelForCausalLM, AutoTokenizer
import os
import numpy as np
from tqdm import tqdm
import requests
import json
import fire, random, logging
from openai import OpenAI
import openai




# 推理

# vllm deployment test
# 使用本地vllm本地部署的千问去处理。搞清楚这个query是什么
def vllm_chat(model_name, query):

    # 设置 OpenAI 的 API key 和 API base，以使用 vLLM 的 API 服务器
    if 'gpt-4' in model_name:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {"sk-sn3aju3NKPnrN88vD6030628723f41AeBfBdB392Bc9b0e56"}'
        }
        request_data = {
            'messages': [
                {'role': 'system', 'content': 'You are ChatGPT, a large language model trained by OpenAI.'},
                {'role': 'user', 'content': query}
            ],
            'stream': False,
            'model': model_name,
            'temperature': 0.5,
            'presence_penalty': 0,
            'frequency_penalty': 0,
            'top_p': 1
        }
        response = requests.post('https://api.132999.xyz/v1/chat/completions', headers=headers, json=request_data)
        data = response.json()
        # print(data['choices'][0]['message']['content'])
        return data['choices'][0]['message']['content']

    elif 'gpt-3.5' in model_name:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {"sk-sn3aju3NKPnrN88vD6030628723f41AeBfBdB392Bc9b0e56"}'
        }
        request_data = {
            'messages': [
                {'role': 'system', 'content': 'You are ChatGPT, a large language model trained by OpenAI.'},
                {'role': 'user', 'content': query}
            ],
            'stream': False,
            'model': model_name,
            'temperature': 0.5,
            'presence_penalty': 0,
            'frequency_penalty': 0,
            'top_p': 1
        }
        response = requests.post('https://api.132999.xyz/v1/chat/completions', headers=headers, json=request_data)
        data = response.json()
        # print(data['choices'][0]['message']['content'])
        return data['choices'][0]['message']['content']

    else :
    # vllm部署接口测试
        client = OpenAI(
            api_key="token-abc123",
            base_url="http://localhost:8081/v1",
             )

        completion = client.chat.completions.create(
            model=model_name,
            messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query}
            ],
            max_tokens=5000,  # 设置返回结果的最大 token 数
            temperature=0  # 设置生成的温度，控制生成内容的多样性
        )
        return completion.choices[0].message.content


# Updated helper function to create directories if they don't exist
def ensure_dir_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

# 解析json数据为list，json就是对应python中的list
def load_json(datapath):
    try:
        with open(datapath, 'r', encoding='utf-8') as file:
            data = [json.loads(line) for line in file]
    except:
        data = []
        with open(datapath, 'r', encoding='utf-8') as file:
            for line in tqdm(file.readlines()):
                data.append(eval(line))
    return data


# Main inference function
def run_inference(model_name_or_path, input_path, output_path, call):
    ensure_dir_exists(output_path)
    for file_name in os.listdir(input_path):
        s_time=time.time() #记录开始时间方便后面评估
        # Read the input data
        data = load_json(os.path.join(input_path, file_name))

        # Load model based on call type
        if call == "vllm":
            call_func = vllm_chat
        else:
            raise NotImplementedError

        output_file = os.path.join(output_path, file_name)

        # Save each JSON object on a new line in JSONL format
        with open(output_file, 'w', encoding='utf-8') as file:
            for input_text in tqdm(data):
                instruct = input_text['instruct'] + " ###题目###\n " + input_text['input']

                if call == "vllm":
                    response = call_func(model_name_or_path, instruct)
                else:
                    raise NotImplementedError

                input_text['inference'] = response
                file.write(json.dumps(input_text, ensure_ascii=False) + '\n')
        #计算时间
        e_time=time.time()
        time_count=e_time-s_time
        h,rem=divmod(time_count,3600)
        min,sec=divmod(rem,60)
        with open(os.path.join(output_path,"time_count.txt"), 'a', encoding='utf-8') as file:
            file.write(f"处理{file_name.split(',')[0]}文件耗时：{int(h)}小时 {int(min)}分钟 {int(sec)}秒"+'\n')

if __name__ == '__main__':
    fire.Fire(run_inference)
