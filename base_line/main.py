import json
from prompt import BASELINE_TEMPLATE
from src.generator import GeneratorService
from src.writer import write_qa_pairs

def main():
    # model_name = "accounts/fireworks/models/deepseek-r1"
    model_name="gemini-1.5-flash"
    temperature = 0.7
    top_p = 1.0

    input_path = './src/data/problems.json'
    
    # Read JSON file
    with open(input_path, 'r', encoding='utf-8') as f:
        problems = json.load(f)

    generator = GeneratorService()
    qa_pairs = []

    for i, problem_data in enumerate(problems):
        problem = problem_data['problem']
        if not problem.strip():
            continue  # skip empty problems

        try:
            query = BASELINE_TEMPLATE.replace("query", problem)
            response = generator.gemini_json_generator(
                model_name=model_name,
                temperature=temperature,
                top_p=top_p,
                prompt=query,
            )
            # content = response.choices[0].message.content
            print("response: ", response)
            content = response
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
