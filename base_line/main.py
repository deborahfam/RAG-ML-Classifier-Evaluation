import json
from prompt import BASELINE_TEMPLATE
from src.generator.gemini_generator import GeminiGenerator
from src.writer import write_qa_pairs

def main():
    temperature = 0.7
    top_p = 1.0

    input_path = './src/data/problems.json'
    
    # Read JSON file
    with open(input_path, 'r', encoding='utf-8') as f:
        problems = json.load(f)

    generator = GeminiGenerator()
    qa_pairs = []

    for i, problem_data in enumerate(problems):
        problem = problem_data['problem']
        if not problem.strip():
            continue

        try:
            query = BASELINE_TEMPLATE.replace("query", problem)
            response = generator.generate_json(
                temperature=temperature,
                top_p=top_p,
                prompt=query,
            )
            content = response
            print("response: ", content)
            qa = eval(content) if isinstance(content, str) else content
            qa_pairs.append(qa)

        except Exception as e:
            print(f"Error en el problema #{i + 1}: {e}")
            continue

    # Guardar resultados
    output_path = 'outputs/qa_pairs.jsonl'
    write_qa_pairs(output_path, qa_pairs)

if __name__ == "__main__":
    main()
