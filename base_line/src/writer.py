import json

def write_qa_pairs(output_path, qa_content):
    with open(output_path, 'w', encoding='utf-8') as file:
        for line in qa_content.strip().split('\n'):
            if line.startswith("Pregunta:") or line.startswith("Respuesta:"):
                file.write(json.dumps({"text": line}) + '\n')