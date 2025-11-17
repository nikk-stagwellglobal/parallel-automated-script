"""Text normalization service for converting technical output to natural language."""

import logging


logger = logging.getLogger(__name__)


class TextNormalizer:
    """Converts deterministic query text to natural narrative form.
    
    This class takes the technical deterministic text output and transforms
    it into human-friendly natural language that's easier to understand for
    non-technical users.
    
    Example:
        >>> normalizer = TextNormalizer()
        >>> technical = 'Include items that match ANY of: ("Python"; "Java")'
        >>> narrative = normalizer.normalize(technical)
        >>> print(narrative)
        Search for documents containing any of the following: "Python", "Java".
    """
    
    def __init__(self, enable_logging: bool = False):
        """Initialize the normalizer.
        
        Args:
            enable_logging: Whether to enable logging output (default: False)
        """
        if enable_logging:
            logging.basicConfig(level=logging.INFO)
    
    def normalize(self, deterministic_text: str) -> str:
        """Convert deterministic text to natural narrative form.
        
        Args:
            deterministic_text: The technical deterministic text to convert
            
        Returns:
            Natural language narrative version of the text
            
        Example:
            >>> normalizer = TextNormalizer()
            >>> result = normalizer.normalize('EXCLUDE items where: ("test")')
            >>> print(result)
            But exclude documents where "test".
        """
        logger.info("Normalizing deterministic text to narrative form")
        
        narrative = deterministic_text
        
        narrative = narrative.replace(
            "Include items that match ANY of: (",
            "Search for documents containing any of the following: "
        )
        
        narrative = narrative.replace(
            "Include items that match ALL of: (",
            "Search for documents that must contain all of the following: "
        )
        
        narrative = narrative.replace(
            "EXCLUDE items where: (",
            "but exclude documents where "
        )
        
        narrative = narrative.replace(
            "but exclude documents where Search for documents containing any of the following: ",
            "but exclude documents containing any of: "
        )
        
        narrative = narrative.replace('contains "', 'the term "')
        
        narrative = narrative.replace(": contains the EXACT PHRASE", " must contain the exact phrase")
        narrative = narrative.replace(": contains ANY of [", " contains any of [")
        narrative = narrative.replace(": contains ALL of [", " must contain all of [")
        
        narrative = narrative.replace("; ", ", ")
        
        narrative = narrative.replace(")", "")
        
        narrative = narrative.strip()
        if not narrative.endswith("."):
            narrative += "."
        
        narrative = narrative[0].upper() + narrative[1:] if narrative else ""
        
        logger.debug(f"Normalized text: {narrative[:100]}...")
        return narrative
