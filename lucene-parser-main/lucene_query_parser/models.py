"""Data models for Lucene Query Parser results."""

from typing import Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class QueryResult:
    """Result object containing parsed query information.
    
    Attributes:
        deterministic_text: Technical interpretation of the query
        narrative_text: Human-friendly natural language explanation
        ast_json: Abstract Syntax Tree as a JSON-serializable dictionary
        query: The original query string that was parsed
    """
    deterministic_text: str
    narrative_text: str
    ast_json: Dict[str, Any]
    query: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the result to a dictionary.
        
        Returns:
            Dictionary representation of the query result
        """
        return asdict(self)
