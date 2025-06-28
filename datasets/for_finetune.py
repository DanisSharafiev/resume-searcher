import json

INPUT_FILE = 'inputs.txt'
MARKDOWN_FILE = 'outputs_markdown.md'
OUTPUT_JSONL_FILE = 'training_dataset.jsonl'

INSTRUCTION = "Your task is to transform the raw resume data into a well-formatted and concise summary in English using Markdown. Highlight key information such as experience, education, skills, and salary expectations."

def create_training_data():
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        inputs = [line.strip().strip('"') for line in f if line.strip()]
    with open(MARKDOWN_FILE, 'r', encoding='utf-8') as f:
        outputs = [summary.strip() for summary in f.read().split('---') if summary.strip()]
    if len(inputs) != len(outputs):
        return
    with open(OUTPUT_JSONL_FILE, 'w', encoding='utf-8') as f:
        for i in range(len(inputs)):
            data_record = {
                "instruction": INSTRUCTION,
                "input": inputs[i],
                "output": outputs[i]
            }
            f.write(json.dumps(data_record, ensure_ascii=False) + '\n')
create_training_data()