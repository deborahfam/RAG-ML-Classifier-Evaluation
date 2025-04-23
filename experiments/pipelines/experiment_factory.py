from typing import Dict, Type
from .base_experiment import BaseExperiment
from .chain_of_thought_experiment import ChainOfThoughtExperiment
# Import other experiment classes as they are created

class ExperimentFactory:
    _experiments: Dict[str, Type[BaseExperiment]] = {
        "chain_of_thought": ChainOfThoughtExperiment,
        # Add other experiments as they are created
    }

    @classmethod
    def create_experiment(
        cls,
        strategy_name: str,
        embedder,
        generator,
        model_name: str,
        **kwargs
    ) -> BaseExperiment:
        """
        Create an experiment instance based on the strategy name
        
        Args:
            strategy_name: Name of the strategy to use
            embedder: Embedding service instance
            generator: Generator service instance
            model_name: Name of the model to use
            **kwargs: Additional arguments to pass to the experiment constructor
            
        Returns:
            BaseExperiment: An instance of the appropriate experiment class
            
        Raises:
            ValueError: If the strategy name is not recognized
        """
        if strategy_name not in cls._experiments:
            raise ValueError(f"Unknown strategy: {strategy_name}")
            
        experiment_class = cls._experiments[strategy_name]
        return experiment_class(
            embedder=embedder,
            generator=generator,
            strategy_name=strategy_name,
            model_name=model_name,
            **kwargs
        ) 