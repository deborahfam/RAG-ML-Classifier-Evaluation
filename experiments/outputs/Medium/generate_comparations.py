import os
import json
import pandas as pd
from pathlib import Path

root_path = Path("./")
output_md_path = Path("./")

strategy_files = {
    "baseline": "baseline.json",
    "zero shots": "zero_shot.json",
    "few shots": "few_shot.json",
    "simple questions": "simple_question.json",
    "chain of thought": "chain_of_thought.json"
}

for model_dir in root_path.iterdir():
    if model_dir.is_dir() and model_dir.name != "comparaciones_md":
        df = pd.DataFrame(index=range(1, 31), columns=strategy_files.keys())

        for col_name, filename in strategy_files.items():
            file_path = model_dir / filename
            if file_path.exists():
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for i, entry in enumerate(data):
                        classification = entry.get("response", {}).get("classification", "")
                        df.at[i + 1, col_name] = classification

        # Generar contenido Markdown
        markdown_table = df.to_markdown(tablefmt="github", index=True)
        markdown_content = f"### {model_dir.name}\n\n{markdown_table}\n"

        # Guardar archivo Markdown
        md_filename = f"{model_dir.name.replace(' ', '_')}.md"
        md_filepath = output_md_path / md_filename
        with open(md_filepath, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        print(f"✅ Guardado: {md_filepath}")
