import os
import json

# Input and output directories
input_dir = "/Users/circle/PycharmProjects/AI4S/src/data/0_raw"
output_dir = "/Users/circle/PycharmProjects/AI4S/src/data/1_QA"

# Define a prompt template
prompt_template = "你是一个{}专家，解决所给题目"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Process each JSONL file in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(".jsonl"):
        filepath = os.path.join(input_dir, filename)
        subject = filename.split(".")[0]  # Use filename (without extension) as the subject

        # Output file path based on the subject
        output_filepath = os.path.join(output_dir, f"{subject}.jsonl")

        with open(filepath, 'r', encoding='utf-8') as f_in, open(output_filepath, 'a', encoding='utf-8') as f_out:
            for line in f_in:
                data = json.loads(line.strip())
                data["instruct"] = prompt_template.format(subject)  # Populate instruct based on filename
                f_out.write(json.dumps(data, ensure_ascii=False) + "\n")

print("Processing complete! JSONL files have been created for each subject based on filename.")
