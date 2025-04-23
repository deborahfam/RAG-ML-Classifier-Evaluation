import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional

class ResultsManager:
    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def save_result(self, result: Dict[str, Any], experiment_id: Optional[str] = None) -> str:
        """
        Save a single experiment result
        
        Args:
            result: The experiment result to save
            experiment_id: Optional experiment ID to use in filename
            
        Returns:
            str: Path to the saved file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        experiment_id = experiment_id or f"{result['strategy']}_{result['model']}"
        filename = f"{experiment_id}_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
            
        return filepath

    def save_batch_results(self, results: List[Dict[str, Any]], experiment_id: Optional[str] = None) -> str:
        """
        Save multiple experiment results
        
        Args:
            results: List of experiment results to save
            experiment_id: Optional experiment ID to use in filename
            
        Returns:
            str: Path to the saved file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        experiment_id = experiment_id or "batch_results"
        filename = f"{experiment_id}_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
            
        return filepath

    def load_result(self, filepath: str) -> Dict[str, Any]:
        """Load a single experiment result"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def load_batch_results(self, filepath: str) -> List[Dict[str, Any]]:
        """Load multiple experiment results"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_latest_results(self, experiment_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get the most recent results for an experiment"""
        files = os.listdir(self.output_dir)
        if experiment_id:
            files = [f for f in files if f.startswith(experiment_id)]
        
        if not files:
            return []
            
        latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(self.output_dir, x)))
        return self.load_batch_results(os.path.join(self.output_dir, latest_file)) 