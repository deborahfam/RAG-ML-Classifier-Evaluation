import sys
import os
from pathlib import Path
import json
from typing import Dict, Any, Optional, List, Union
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))
from experiments.prompts import PROMPT_STRATEGIES
from base_line.src.generator.generator import GeneratorService

class PromptEngineer:
    def __init__(self, model_name: str = "gemini-1.5-flash", temperature: float = 0.2, top_p: float = 0.9):
        self.generator = GeneratorService()
        self.model_name = model_name
        self.temperature = temperature
        self.top_p = top_p
        
    def apply_prompt_strategy(self, query: str, strategy_name: str) -> str:
        if strategy_name not in PROMPT_STRATEGIES:
            raise ValueError(f"Unknown prompt strategy: {strategy_name}")
            
        prompt_template = PROMPT_STRATEGIES[strategy_name]
        return prompt_template.format(query=query)
    
    def classify_ml_problem(self, query: str, strategy_name: str = "standard") -> Dict[str, Any]:
        prompt = self.apply_prompt_strategy(query, strategy_name)

        try:
            response = self.generator.gemini_json_generator(
                model_name=self.model_name,
                temperature=self.temperature,
                top_p=self.top_p,
                prompt=prompt
            )
            
            # Try to parse as JSON if possible
            try:
                result = json.loads(response)
            except json.JSONDecodeError:
                # If not JSON, return as text
                result = {"response": response}
                
            # Add metadata
            result["strategy"] = strategy_name
            result["query"] = query
            
            return result
            
        except Exception as e:
            return {
                "error": str(e),
                "strategy": strategy_name,
                "query": query
            }
    
    def evaluate_all_strategies(self, query: str) -> List[Dict[str, Any]]:
        results = []
        for strategy_name in PROMPT_STRATEGIES.keys():
            result = self.classify_ml_problem(query, strategy_name)
            results.append(result)
        return results
    
    def format_response(self, result: Dict[str, Any]) -> str:
        if "error" in result:
            return f"Error with {result['strategy']} strategy: {result['error']}"
            
        strategy = result.get("strategy", "unknown")
        query = result.get("query", "unknown")
        
        if "response" in result:
            response = result["response"]
        else:
            response = json.dumps(result, indent=2)
            
        return f"""
                Strategy: {strategy}
                Query: {query}
                Response:
                {response}
        """