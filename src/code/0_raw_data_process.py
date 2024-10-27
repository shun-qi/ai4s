# import os
# import json
# import glob
#
#
# def process_json_file(file_path, assessment_type, output_dir, subject_map):
#     with open(file_path, 'r', encoding='utf-8') as f:
#         data = json.load(f)
#
#     # Extract keywords for ID field
#     file_id = data.get("keywords", "")
#
#     # Process each example
#     processed_data = []
#     for example in data.get("example", []):
#         year = example.get("year", "")
#         category = example.get("category", "")
#
#         # Use join to ensure we get a string
#         question = ''.join(example.get("question", [])).replace("\n", "")
#         answer = ''.join(example.get("answer", [])).replace("\n", "")
#         analysis = ''.join(example.get("analysis", [])).replace("\n", "")
#
#         index = example.get("index", "")
#         score = example.get("score", "")
#
#         # Create the new JSONL structure
#         new_entry = {
#             "year": year,
#             "id": file_id,
#             "category": category,
#             "subject": "",  # Will set based on filename
#             "type": "",  # Placeholder
#             "assessmentType": assessment_type,
#             "index": index,
#             "score": score,
#             "input": question,
#             "instruct": "",  # Placeholder for prompt
#             "golden_label": answer,
#             "analysis": analysis,
#             "modality": "t",  # Default as text-only
#             "image_urls": []  # Default empty
#         }
#         processed_data.append(new_entry)
#
#     # Determine output file based on file name
#     for subject, filename in subject_map.items():
#         if subject in file_path:
#             output_path = os.path.join(output_dir, f"{filename}.jsonl")
#             with open(output_path, 'a', encoding='utf-8') as out_f:
#                 for entry in processed_data:
#                     entry['subject'] = subject
#                     json.dump(entry, out_f, ensure_ascii=False)
#                     out_f.write('\n')
#             break
#
#
# def process_directory(input_dir, assessment_type, output_dir, subject_map):
#     for file_path in glob.glob(os.path.join(input_dir, "*.json")):
#         process_json_file(file_path, assessment_type, output_dir, subject_map)
#
#
# def main():
#     # Define directories
#     obj_questions_dir = "/Users/circle/PycharmProjects/AI4S/others/GAOKAO-Bench/Data/Objective_Questions/"
#     subj_questions_dir = "/Users/circle/PycharmProjects/AI4S/others/GAOKAO-Bench/Data/Subjective_Questions/"
#     output_dir = "/Users/circle/PycharmProjects/AI4S/src/data/"
#
#     # Define subject mapping to filenames
#     # filename:subject
#     subject_map = {
#         "English": "English",
#         "Biology": "Biology",
#         "Chemistry": "Chemistry",
#         "Chinese": "Chinese",
#         "Geography": "Geography",
#         "History": "History",
#         "Math": "Math",
#         "Physics": "Physics",
#         "Political": "Politics" #注意原文件是Political
#     }
#
#     # Process both directories
#     process_directory(obj_questions_dir, "objective", output_dir, subject_map)
#     process_directory(subj_questions_dir, "subjective", output_dir, subject_map)
#
#
# if __name__ == "__main__":
#     main()


import os
import json
import glob
import csv


def load_type_map(csv_file):
    type_map = {}
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Assuming 'file_name' and 'type' are the headers in your CSV
                type_map[row['file_name']] = row['type']
    except FileNotFoundError:
        print(f"Type map file {csv_file} not found.")
    except Exception as e:
        print(f"Error reading type map file: {e}")
    return type_map


def process_json_file(file_path, assessment_type, output_dir, subject_map, type_map):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Extract keywords for ID field
    file_id = data.get("keywords", "")

    # Determine the type based on the file name
    file_name = os.path.basename(file_path)
    entry_type = type_map.get(file_name, "O")  # Default to "O" if not found

    # Process each example
    processed_data = []
    for example in data.get("example", []):
        year = example.get("year", "")
        category = example.get("category", "")

        # Use join to ensure we get a string
        question = ''.join(example.get("question", [])).replace("\n", "")
        answer = ''.join(example.get("answer", [])).replace("\n", "")
        analysis = ''.join(example.get("analysis", [])).replace("\n", "")

        index = example.get("index", "")
        score = example.get("score", "")

        # Create the new JSONL structure
        new_entry = {
            "year": year,
            "id": file_id,
            "category": category,
            "subject": "",  # Will set based on filename
            "type": entry_type,  # Set based on type map
            "assessmentType": assessment_type,
            "index": index,
            "score": score,
            "input": question,
            "instruct": "",  # Placeholder for prompt
            "golden_label": answer,
            "analysis": analysis,
            "modality": "t",  # Default as text-only
            "image_urls": []  # Default empty
        }
        processed_data.append(new_entry)

    # Determine output file based on file name
    for subject, filename in subject_map.items():
        if subject in file_path:
            output_path = os.path.join(output_dir, f"{filename}.jsonl")
            with open(output_path, 'a', encoding='utf-8') as out_f:
                for entry in processed_data:
                    entry['subject'] = subject
                    json.dump(entry, out_f, ensure_ascii=False)
                    out_f.write('\n')
            break


def process_directory(input_dir, assessment_type, output_dir, subject_map, type_map):
    for file_path in glob.glob(os.path.join(input_dir, "*.json")):
        process_json_file(file_path, assessment_type, output_dir, subject_map, type_map)


def main():
    # Define directories
    # 获取当前脚本所在目录，即 src/code
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 项目根目录路径：从 src/code 返回到项目根目录 AI4S
    project_root = os.path.abspath(os.path.join(current_dir, "../../"))
    # 构建 Biology.jsonl 的相对路径

    obj_questions_dir = os.path.join(project_root, "others", "GAOKAO-Bench", "Data", "Objective_Questions")
    subj_questions_dir = os.path.join(project_root, "others", "GAOKAO-Bench", "Data", "Subjective_Questions")
    output_dir = os.path.join(project_root, "src", "data", "0_raw")

    # Load the type map from CSV
    type_map = load_type_map(os.path.join(project_root, "src","type_map.csv"))

    # Define subject mapping to filenames
    subject_map = {
        "English": "English",
        "Biology": "Biology",
        "Chemistry": "Chemistry",
        "Chinese": "Chinese",
        "Geography": "Geography",
        "History": "History",
        "Math": "Math",
        "Physics": "Physics",
        "Political": "Politics"  # 注意原文件是Political
    }

    # Process both directories
    process_directory(obj_questions_dir, "objective", output_dir, subject_map, type_map)
    process_directory(subj_questions_dir, "subjective", output_dir, subject_map, type_map)


if __name__ == "__main__":
    main()
