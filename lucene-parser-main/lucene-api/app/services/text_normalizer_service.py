import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from lucene_query_parser import TextNormalizer
from app.core.logging import get_logger


logger = get_logger(__name__)


class TextNormalizerService:
    """Service wrapper for TextNormalizer library.
    
    This service wraps the standalone lucene_query_parser.TextNormalizer to integrate
    it with the FastAPI application's logging and architecture.
    """
    
    def __init__(self):
        self.normalizer = TextNormalizer(enable_logging=False)
        logger.info("TextNormalizerService initialized with lucene_query_parser library")
    
    def normalize_to_narrative(self, deterministic_text: str) -> str:
        """Convert deterministic text to natural narrative form using the library.
        
        Args:
            deterministic_text: The technical deterministic text to convert
            
        Returns:
            Natural language narrative version of the text
        """
        logger.info("Normalizing deterministic text to narrative form")
        result = self.normalizer.normalize(deterministic_text)
        logger.debug(f"Normalized text: {result[:100]}...")
        return result
