from .base_experiment import BaseExperiment
from ..strategies.chain_of_thought import CHAIN_OF_THOUGHT_PROMPT

class ChainOfThoughtExperiment(BaseExperiment):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prompt_template = CHAIN_OF_THOUGHT_PROMPT

    def build_prompt(self, context: str, query: str) -> str:
        """Build the prompt using the chain of thought strategy"""
        return self.prompt_template.format(
            context=context,
            query=query
        ) 