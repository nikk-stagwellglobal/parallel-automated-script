from functools import lru_cache
from app.services.query_parser_service import QueryParserService
from app.services.text_normalizer_service import TextNormalizerService
from app.controllers.query_controller import QueryController


@lru_cache()
def get_query_parser_service() -> QueryParserService:
    """Dependency injection for QueryParserService"""
    return QueryParserService()


@lru_cache()
def get_text_normalizer_service() -> TextNormalizerService:
    """Dependency injection for TextNormalizerService"""
    return TextNormalizerService()


def get_query_controller() -> QueryController:
    """Dependency injection for QueryController"""
    parser_service = get_query_parser_service()
    normalizer_service = get_text_normalizer_service()
    
    return QueryController(
        parser_service=parser_service,
        normalizer_service=normalizer_service
    )
