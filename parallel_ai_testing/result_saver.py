import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class ResultSaver:
    def __init__(self, output_dir: str = "results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def save_results(
        self, 
        results: List[Dict[str, Any]], 
        filename: str = None
    ) -> str:
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"results_{timestamp}.json"
        
        filepath = self.output_dir / filename
        
        try:
            with open(filepath, 'w') as f:
                json.dump(results, f, indent=2)
            
            logger.info(f"Results saved to {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Error saving results to {filepath}: {str(e)}")
            raise
    
    def save_brand_results(
        self, 
        brand: str, 
        results: List[Dict[str, Any]]
    ) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{brand.lower().replace(' ', '_')}_{timestamp}.json"
        return self.save_results(results, filename)
    
    def load_results(self, filename: str) -> List[Dict[str, Any]]:
        filepath = self.output_dir / filename
        
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading results from {filepath}: {str(e)}")
            raise
