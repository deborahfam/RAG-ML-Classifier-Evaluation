import logging
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

# from strategies.zero_shot import ZERO_SHOT_PROMPT
# from strategies.simple_question import SIMPLE_QUESTION_PROMPT
# from strategies.few_shot import FEW_SHOT_PROMPT
# from strategies.chain_of_thought import CHAIN_OF_THOUGHT_PROMPT

# STRATEGY_PROMPTS = {
#     "zero_shot": ZERO_SHOT_PROMPT,
#     "simple_question": SIMPLE_QUESTION_PROMPT,
#     "few_shot": FEW_SHOT_PROMPT,
#     "chain_of_thought": CHAIN_OF_THOUGHT_PROMPT
# }


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

        # prompt_template = STRATEGY_PROMPTS[strategy_name]
        # prompt = prompt_template.format(context=context, query=query)

        prompt_template = STRATEGY_PROMPTS[strategy_name]
        prompt = prompt_template.render(query=query, context=context)


        response: ClassificationModel = self.generator.generate_json(
            prompt=prompt,
            model="accounts/fireworks/models/qwen3-30b-a3b",
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
        results = []
        context = load_context(Path(__file__).parent / "data" / "context.json")
        for strategy in strategies:
            for i, query in enumerate(queries):
                    result = self.run_experiment(
                        query=query,
                        strategy_name=strategy,
                        context=context[i]
                    )
                    results.append(result)
            self.results_manager.save_batch_results(results, f"{results[0]['model']}_{results[0]['strategy_name']}")
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

    strategies = ["simple_question"]  

    results = runner.run_batch_experiments(
        queries=problems,
        strategies=strategies
    )

    print(f"✅ Completados {len(results)} experimentos.")
    print(f"📝 Resultados guardados en: {runner.results_manager.output_dir}")