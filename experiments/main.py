import logging
import os
import sys
import json
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from experiments.json_formats.reasoning import ClassificationModel
from experiments.strategies.prompts import PROMPT_TEMPLATES as STRATEGY_PROMPTS
from services.context_fetcher import fetch_context_from_query, load_context
from services.generator.base import BaseGenerator

from pathlib import Path
from typing import Dict, List, Optional
from services.generator.openai_generator import OpenAIGenerator
from services.generator.base import BaseGenerator
from services.results_manager import ResultsManager
from services.embedder.lmstudio import LMStudioEmbeddingService
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LARGE_MODELS = [
    "accounts/fireworks/models/llama-v3p1-405b-instruct",
    "accounts/fireworks/models/qwen3-235b-a22b"
    "accounts/fireworks/models/deepseek-v3",
]

MEDIUM_MODELS = [
    "accounts/fireworks/models/llama-v3p3-70b-instruct",
    "accounts/fireworks/models/mistral-7b-instruct-v0p2",
    "accounts/yi-01-ai/models/yi-large"
]

SMALL_MODELS = [
    "accounts/fireworks/models/qwen3-30b-a3b",
    "accounts/fireworks/models/gemma2-9b-it",
    "accounts/fireworks/models/llama-v3p1-8b-instruct"
]


class ExperimentRunner:
    def __init__(
        self,
        generator: BaseGenerator,
        output_dir: str = "outputs"
    ):
        self.generator = generator
        self.embedder = LMStudioEmbeddingService()
        self.results_manager = ResultsManager(output_dir)

    def run_experiment(
        self,
        query: str,
        context: str,
        strategy_name: str
    ) -> Dict:
        logger.info(f"Running experiment: strategy={strategy_name}")        

        if strategy_name not in STRATEGY_PROMPTS:
            raise ValueError(f"Estrategia no reconocida: {strategy_name}")

        prompt_template = STRATEGY_PROMPTS[strategy_name]
        prompt = prompt_template.render(query=query, context=context)


        response: ClassificationModel = self.generator.generate_json(
            prompt=prompt,
            model="accounts/fireworks/models/llama-v3p1-405b-instruct",
            json_model= ClassificationModel
        )

        result = {
            "model": response.model,
            "strategy_name": strategy_name,
            "context_used": context,
            "query": query,
            "strategy_prompt": prompt,
            "completion_tokens": response.usage.completion_tokens,
            "prompt_tokens": response.usage.prompt_tokens,
            "total_tokens": response.usage.total_tokens,
            "response": response.choices[0].message.parsed.model_dump()
        }

        # self.results_manager.save_result(result)
        return result

    def run_batch_experiments(
        self,
        queries: List[str],
        strategies: List[str],
        experiment_id: Optional[str] = None
    ) -> List[Dict]:
        all_results = []
        context = load_context(Path(__file__).parent / "data" / "context.json")
        for strategy in strategies:
            results = []
            output_file = Path(self.results_manager.output_dir) / f"{strategy}.json"
            os.makedirs(output_file.parent, exist_ok=True)
            existing_results = []
            if output_file.exists():
                 with open(output_file, "r", encoding="utf-8") as f:
                      existing_results = json.load(f)
                      result = existing_results
            else:
                print(f"🔄 No se encontró el archivo {output_file}")
            start_index = len(existing_results) if existing_results else 0
            print(f"🔄 Iniciando desde el índice {start_index}")

            for i, query in enumerate(queries[start_index:], start=start_index):
                print(f"🔄 Procesando query {i} de {len(queries)}")
                result = self.run_experiment(
                    query=query,
                    strategy_name=strategy,
                    context=context[i]
                )
                results.append(result)
                self.results_manager.save_batch_results(results, f"{results[0]['strategy_name']}")
        return results

def load_problems(file_path: str) -> List[str]:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return [item['problem'] for item in data]

if __name__ == "__main__":
    generator = OpenAIGenerator(use_fireworks=True)
    runner = ExperimentRunner(generator=generator)
    problems_file = Path(__file__).parent / "data" / "problems.json"
    problems = load_problems(problems_file)

    strategies = list(STRATEGY_PROMPTS.keys()) 

    results = runner.run_batch_experiments(
        queries=problems,
        strategies=strategies
    )

    print(f"✅ Completados {len(results)} experimentos {results[0]['model']}_{results[0]['strategy_name']}.")
    print(f"📝 Resultados guardados en: {runner.results_manager.output_dir}")