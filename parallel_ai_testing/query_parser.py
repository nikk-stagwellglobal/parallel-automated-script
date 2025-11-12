import logging
from lucene_query_parser import LuceneQueryParser

logger = logging.getLogger(__name__)


async def parse_search_term_to_text(search_term: str) -> str:
    try:
        parser = LuceneQueryParser()
        result = parser.parse(search_term)
        return result.narrative_text
    except Exception as e:
        logger.error(f"Failed to parse search term '{search_term}': {str(e)}")
        return search_term
