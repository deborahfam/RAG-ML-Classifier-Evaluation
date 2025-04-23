import logging
import json
from pathlib import Path
from typing import Dict, List, Optional
from langchain_core.embeddings import Embeddings
from services.generator.base import BaseGenerator
from services.generator.gemini_generator import GeminiGenerator
from pipelines.experiment_factory import ExperimentFactory
from pipelines.results_manager import ResultsManager
from services.embedder.gemini import GeminiEmbeddingService
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExperimentRunner:
    def __init__(
        self,
        embedder: Embeddings,
        output_dir: str = "outputs"
    ):
        self.embedder = embedder
        self.generator = GeminiGenerator()  # Only using Gemini
        self.results_manager = ResultsManager(output_dir)

    def run_experiment(
        self,
        query: str,
        strategy_name: str,
        experiment_id: Optional[str] = None
    ) -> Dict:
        """
        Run a single experiment
        
        Args:
            query: The query to run the experiment on
            strategy_name: Name of the strategy to use
            experiment_id: Optional experiment ID for result tracking
            
        Returns:
            Dict: The experiment results
        """
        logger.info(f"Running experiment: strategy={strategy_name}")
        
        experiment = ExperimentFactory.create_experiment(
            strategy_name=strategy_name,
            embedder=self.embedder,
            generator=self.generator,
            model_name="gemini-1.5-flash"  # Fixed model name for Gemini
        )
        
        result = experiment.run(query)
        self.results_manager.save_result(result, experiment_id)
        
        return result

    def run_batch_experiments(
        self,
        queries: List[str],
        strategies: List[str],
        experiment_id: Optional[str] = None
    ) -> List[Dict]:
        """
        Run multiple experiments
        
        Args:
            queries: List of queries to run experiments on
            strategies: List of strategies to use
            experiment_id: Optional experiment ID for result tracking
            
        Returns:
            List[Dict]: List of experiment results
        """
        results = []
        
        for query in queries:
            for strategy in strategies:
                try:
                    result = self.run_experiment(
                        query=query,
                        strategy_name=strategy,
                        experiment_id=experiment_id
                    )
                    results.append(result)
                except Exception as e:
                    logger.error(f"Error running experiment: {str(e)}")
                    continue
        
        self.results_manager.save_batch_results(results, experiment_id)
        return results

def load_problems(file_path: str) -> List[str]:
    """
    Load problems from a JSON file
    
    Args:
        file_path: Path to the JSON file containing problems
        
    Returns:
        List[str]: List of problems
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return [item['problem'] for item in data]

if __name__ == "__main__":
    # Initialize services
    embedder = GeminiEmbeddingService()
    
    # Create runner
    runner = ExperimentRunner(embedder)
    
    # Load problems from file
    problems_file = Path(__file__).parent / "data" / "problems.json"
    problems = load_problems(problems_file)
    
    # Define strategies to test
    strategies = [
        "zero_shot",
        "one_shot",
        "few_shot",
        "simple_question"
        "chain_of_thought",
    ]
    
    # Run experiments
    results = runner.run_batch_experiments(
        queries=problems,
        strategies=strategies,
        experiment_id="ml_classification_problems"
    )
    
    print(f"Completed {len(results)} experiments")
    print(f"Results saved in: {runner.results_manager.output_dir}")