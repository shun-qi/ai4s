import os
import json
# Input and output directories
input_dir = "../data/0_raw/23-24"
output_dir = "../data/3_QA_2/23-24"

# Define a prompt template
prompt_template ="""
###身份###

	你是一名参加高考的考生，拥有强大的推理和分析能力。

###科目###

{ch_subject}

###指令###

	你将对以下题目进行解答，在阅读题目后，你会根据问题判断所属的类型（概念题，分析题，计算题，公式应用题），然后进行作答

###挑战###

如果可以，请尽可能一题多解

### 输出格式###

{{

	"type":"题目所属的类型",
	"analysis":[["解法一"],["解法二"],......]],
	#写尽可能多的写法，而非我限定的两种解法
	#如果解法有多个步骤，按1，2，3，4这样分点分析
	#每一个[]对应一种解法
	"answer":“你的答案”

}}

***注意，仅仅按***\### 输出格式###里的格式输出，不要输出其它内容

"""

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)


# Process each JSONL file in the input directory
for filename in os.listdir(input_dir):
    ch_subject=""
    if filename.endswith(".jsonl"):
        filepath = os.path.join(input_dir, filename)
        subject = filename.split(".")[0]  # Use filename (without extension) as the subject
        with open("../en_ch_map.json", "r") as f:
            en_ch_map = json.load(f)
            ch_subject=en_ch_map[subject]
        # Output file path based on the subject
        output_filepath = os.path.join(output_dir, f"{subject}.jsonl")
        with open(filepath, 'r', encoding='utf-8') as f_in, open(output_filepath, 'w', encoding='utf-8') as f_out:
            for line in f_in:
                data = json.loads(line.strip())
                if data["modality"]=='t':   #先仅推理单模态的题目
                    data["instruct"] = prompt_template.format(ch_subject=ch_subject)  # Populate instruct based on filename
                    f_out.write(json.dumps(data, ensure_ascii=False) + "\n")

print("Processing complete! JSONL files have been created for each subject based on filename.")
