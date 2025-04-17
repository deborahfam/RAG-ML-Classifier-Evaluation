import json

def write_qa_pairs(output_path, qa_pairs):
    with open(output_path, 'w', encoding='utf-8') as f:
        for pair in qa_pairs:
            json_line = json.dumps(pair, ensure_ascii=False)
            f.write(json_line + '\n')