from typing import Dict, Any
from app.schemas.query_schema import QueryRequest, QueryResponse
from app.services.query_parser_service import QueryParserService
from app.services.text_normalizer_service import TextNormalizerService
from app.core.logging import get_logger


logger = get_logger(__name__)


class QueryController:
    """Controller for handling query parsing requests"""
    
    def __init__(
        self,
        parser_service: QueryParserService,
        normalizer_service: TextNormalizerService
    ):
        self.parser_service = parser_service
        self.normalizer_service = normalizer_service
        logger.info("QueryController initialized")
    
    def parse_query(self, request: QueryRequest) -> QueryResponse:
        """Process query parsing request using the lucene_query_parser library.
        
        The library handles parsing, AST generation, and text normalization internally.
        """
        logger.info(f"Processing query parse request")
        
        try:
            result = self.parser_service.parse_query(request.query)
            
            logger.debug(f"Generated deterministic text: {result.deterministic_text[:100]}...")
            logger.debug(f"Generated narrative text: {result.narrative_text[:100]}...")
            
            return QueryResponse(
                deterministic_text=result.deterministic_text,
                narrative_text=result.narrative_text,
                ast_json=result.ast_json
            )
        
        except ValueError as e:
            logger.error(f"Validation error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error processing query: {str(e)}")
            raise ValueError(f"Failed to process query: {str(e)}")
