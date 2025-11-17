import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from typing import Dict, Any
from lucene_query_parser import LuceneQueryParser
from app.core.logging import get_logger


logger = get_logger(__name__)


class QueryParserService:
    """Service wrapper for LuceneQueryParser library.
    
    This service wraps the standalone lucene_query_parser library to integrate
    it with the FastAPI application's logging and architecture.
    """
    
    def __init__(self):
        self.parser = LuceneQueryParser(enable_logging=False)
        logger.info("QueryParserService initialized with lucene_query_parser library")
    
    def parse_query(self, query: str) -> Any:
        """Parse Lucene query string using the library.
        
        Args:
            query: Lucene query string to parse
            
        Returns:
            QueryResult object from the library
            
        Raises:
            ValueError: If the query has invalid syntax
        """
        logger.info(f"Parsing query: {query[:100]}...")
        try:
            result = self.parser.parse(query)
            logger.debug(f"Successfully parsed query")
            return result
        except ValueError as e:
            logger.error(f"Failed to parse query: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error parsing query: {str(e)}")
            raise ValueError(f"Invalid Lucene query syntax: {str(e)}")
