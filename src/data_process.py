import os
import json
import glob


def process_json_file(file_path, assessment_type, output_dir, subject_map):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Extract keywords for ID field
    file_id = data.get("keywords", "")

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
            "type": "",  # Placeholder
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


def process_directory(input_dir, assessment_type, output_dir, subject_map):
    for file_path in glob.glob(os.path.join(input_dir, "*.json")):
        process_json_file(file_path, assessment_type, output_dir, subject_map)


def main():
    # Define directories
    obj_questions_dir = "/Users/circle/PycharmProjects/AI4S/others/GAOKAO-Bench/Data/Objective_Questions/"
    subj_questions_dir = "/Users/circle/PycharmProjects/AI4S/others/GAOKAO-Bench/Data/Subjective_Questions/"
    output_dir = "/Users/circle/PycharmProjects/AI4S/src/data_processed/"

    # Define subject mapping to filenames
    # filename:subject
    subject_map = {
        "English": "English",
        "Biology": "Biology",
        "Chemistry": "Chemistry",
        "Chinese": "Chinese",
        "Geography": "Geography",
        "History": "History",
        "Math": "Math",
        "Physics": "Physics",
        "Political": "Politics" #注意原文件是Political
    }

    # Process both directories
    process_directory(obj_questions_dir, "objective", output_dir, subject_map)
    process_directory(subj_questions_dir, "subjective", output_dir, subject_map)


if __name__ == "__main__":
    main()
