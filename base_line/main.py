import streamlit as st
from src.generator import GeneratorService
from src.reader import read_text
from src.writer import write_qa_pairs

def main():
    st.title("Generador de Preguntas y Respuestas")

    model_name = "accounts/fireworks/models/deepseek-r1"
    temperature = 0.7
    top_p = 1.0

    input_path = 'data/problems.txt'
    lines = read_text(input_path).splitlines()

    generator = GeneratorService()
    qa_pairs = []

    for i, question in enumerate(lines):
        if not question.strip():
            continue  # saltar líneas vacías

        try:
            response = generator.json_generator(
                model_name=model_name,
                temperature=temperature,
                top_p=top_p,
                query=question,
            )
            content = response.choices[0].message.content
            qa = eval(content) if isinstance(content, str) else content
            qa_pairs.append(qa)

            st.markdown(f"**Pregunta:** {qa['pregunta']}")
            st.markdown(f"**Respuesta:** {qa['respuesta']}")
            st.markdown("---")

        except Exception as e:
            st.error(f"Error en la pregunta #{i + 1}: {e}")
            continue

    # Guardar resultados
    output_path = 'outputs/qa_pairs.jsonl'
    write_qa_pairs(output_path, qa_pairs)

if __name__ == "__main__":
    main()
