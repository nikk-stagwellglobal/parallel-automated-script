"""Examples of error handling patterns with the Lucene Query Parser."""

from lucene_query_parser import LuceneQueryParser
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_with_error_handling(parser: LuceneQueryParser, query: str) -> dict:
    """Parse a query with comprehensive error handling.
    
    Args:
        parser: LuceneQueryParser instance
        query: Query string to parse
        
    Returns:
        Dictionary with success status and result or error
    """
    try:
        result = parser.parse(query)
        logger.info(f"Successfully parsed: {query[:50]}")
        return {
            'success': True,
            'query': query,
            'data': result.to_dict(),
            'error': None
        }
    except ValueError as e:
        logger.error(f"Validation error for '{query}': {e}")
        return {
            'success': False,
            'query': query,
            'data': None,
            'error': {
                'type': 'ValidationError',
                'message': str(e)
            }
        }
    except Exception as e:
        logger.exception(f"Unexpected error for '{query}': {e}")
        return {
            'success': False,
            'query': query,
            'data': None,
            'error': {
                'type': 'UnexpectedError',
                'message': str(e)
            }
        }


def main():
    parser = LuceneQueryParser(enable_logging=True)
    
    print("=" * 80)
    print("Lucene Query Parser - Error Handling Examples")
    print("=" * 80)
    print()
    
    test_queries = [
        '("Python" OR "Java")',
        '((unclosed parenthesis',
        '',
        'valid:query',
        '"just a phrase"',
        '(A AND B) OR (C NOT D)',
        ')))invalid(((',
        'field:',
        'title:"Machine Learning" AND status:published'
    ]
    
    print("Testing queries with error handling:")
    print("-" * 80)
    
    successful = 0
    failed = 0
    
    for query in test_queries:
        result = parse_with_error_handling(parser, query)
        
        if result['success']:
            successful += 1
            print(f"✓ SUCCESS: {query[:50]}")
            print(f"  Narrative: {result['data']['narrative_text'][:70]}...")
        else:
            failed += 1
            print(f"✗ FAILED: {query[:50]}")
            print(f"  Error: {result['error']['message']}")
        print()
    
    print("=" * 80)
    print(f"Summary: {successful} successful, {failed} failed")
    print("=" * 80)


if __name__ == "__main__":
    main()
