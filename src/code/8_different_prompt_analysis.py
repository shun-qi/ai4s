import time
import os
from tqdm import tqdm
import requests
import json
import fire
from openai import OpenAI

# 推理

# vllm deployment test
# 使用本地vllm本地部署的千问去处理。搞清楚这个query是什么
max_retries=20
backoff_factor=2
prompt_template = """### 角色描述 ###
你是一名高考数学资深教师，擅长数学解题分析和批判性思维。

### 任务说明 ###
你需要审查和评估考生对以下数学题的解答。根据题目和考生的解题过程，对以下评估指标进行评分。

### 评估标准 ###
1. **答案正确性**：确认考生解答（inference中answer）是否与标准答案（golden_label）严格一致，并根据题目分值（score）对正确性评分。
2. **解答完整性**：评估解答的逻辑步骤是否清晰、完整。inference中analysis包含多种解法，不同解法用 `[]` 分隔，每种解法的步骤用 `[]` 分隔。
3. **方法创新性**：对解答中的推理方法进行创新性评分（若存在多种解法，评估其新颖性），按照inference中的analysis内容，不同解法用 `[]` 分隔。
4. **逻辑推理能力**：评估解答的逻辑推理水平，检查inference中每种解法的步骤与整体分析的逻辑一致性。
5. **学术水平**：评估考生解答的综合水平，判断其学术水平（小学、初中/高中、大学）。

### 输出格式 ### { "is_correct": true/false, "correctness_score": [0-题目分值], # 答案正确性评分，最大值为题目分值 "completeness_score": [0-5], # 解答完整性评分 "innovation_score": [0-5], # 方法创新性评分 "reasoning_score": [0-5], # 逻辑推理能力评分 "student_level": "<学生能达到的水平：小学/初中/高中/大学>"} 注意返回的是一个json格式{"":"","":"",...}，请严格按照上述格式作答，不要输出其它内容，不要插入\,\\n等。
### 输入数据 ###"""

def vllm_chat(model_name, query):
    # 设置 OpenAI 的 API key 和 API base，以使用 vLLM 的 API 服务器
    if 'gpt-4o-mini' in model_name:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {"sk-RYZZYxzl5tJNor5896B47cE0Fe284126Bd6b74E45b99EdA5"}'
        }
        request_data = {
            'messages': [
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': query}
            ],
            'stream': False,
            'model': model_name,
            'temperature': 0,
            'presence_penalty': 0,
            'frequency_penalty': 0,
            'top_p': 1
        }
        for attempt in range(max_retries):
            try:
                response = requests.post('https://aihubmix.com/v1/chat/completions', headers=headers, json=request_data)
                response.raise_for_status()  # 如果响应状态码不是200，抛出异常
                data = response.json()
                return data['choices'][0]['message']['content']
            except requests.exceptions.RequestException as e:
                print(f"请求失败: {e}")
                if attempt < max_retries - 1:
                    sleep_time = backoff_factor ** attempt  # 指数回退
                    print(f"等待 {sleep_time} 秒后重试...")
                    time.sleep(sleep_time)
                else:
                    print("达到最大重试次数，无法完成请求。")
                    return None  # 或者抛出异常
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
            max_tokens=200,  # 设置返回结果的最大 token 数
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
    exclude=[] #记录排除那些数据不处理
    ensure_dir_exists(output_path)
    record_path=os.path.join(output_path,'time_count.txt')
    if not os.path.exists(record_path):
        exclude.append("time_count.txt")
    else :
        with open(record_path, 'r', encoding='utf-8') as file:
            exclude=[line.strip() for line in file]
            exclude.append("time_count.txt")    #推理的时候原数据文件中没有时间，而现在打分原数据中有个time_count.txt文件需要排除

    for file_name in os.listdir(input_path):
        # 这里一定要注意，是判断file_name是否在ex中，ex中除了有file_name还有时间，写反了就不起效。
        if any(file_name in ex for ex in exclude): #实现动态过滤，如果推理中断，可以检查后，排除已经推理过的继续推理
            continue
        else:
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
            # 清空写，方便调用失败后，重新开始
            with open(output_file, 'w', encoding='utf-8') as file:
                for input_text in tqdm(data):
                    instruct = (
                            prompt_template +
                            " score: " + str(input_text.get("score", "")) +
                            " golden_label: " + str(input_text.get("golden_label", "")) +
                            " analysis: " + str(input_text.get("analysis", "")) +
                            " inference: " + str(input_text.get("inference", ""))
                    )
                    if call == "vllm":
                        response = call_func(model_name_or_path, instruct)
                    else:
                        raise NotImplementedError

                    input_text['rating'] = response
                    file.write(json.dumps(input_text, ensure_ascii=False) + '\n')
            #计算时间
            e_time=time.time()
            time_count=e_time-s_time
            h,rem=divmod(time_count,3600)
            min,sec=divmod(rem,60)
            # time_count.txt必须追加写，因为是不断增加记录
            with open(os.path.join(output_path,"time_count.txt"), 'a', encoding='utf-8') as file:
                file.write(f"处理{file_name.split(',')[0]}文件耗时：{int(h)}小时 {int(min)}分钟 {int(sec)}秒"+'\n')

if __name__ == '__main__':
    fire.Fire(run_inference)

