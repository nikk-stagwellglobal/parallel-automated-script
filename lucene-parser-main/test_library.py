"""Test script to verify the lucene_query_parser library works correctly."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from lucene_query_parser import LuceneQueryParser, QueryResult, TextNormalizer


def test_basic_parsing():
    """Test basic query parsing."""
    print("Testing basic parsing...")
    parser = LuceneQueryParser()
    
    result = parser.parse('("Python" OR "Java")')
    
    assert isinstance(result, QueryResult)
    assert result.query == '("Python" OR "Java")'
    assert len(result.deterministic_text) > 0
    assert len(result.narrative_text) > 0
    assert isinstance(result.ast_json, dict)
    
    print("✓ Basic parsing works")


def test_error_handling():
    """Test error handling for invalid queries."""
    print("Testing error handling...")
    parser = LuceneQueryParser()
    
    try:
        parser.parse('((unclosed')
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert 'syntax' in str(e).lower()
    
    print("✓ Error handling works")


def test_to_dict():
    """Test converting result to dictionary."""
    print("Testing to_dict conversion...")
    parser = LuceneQueryParser()
    
    result = parser.parse('test')
    result_dict = result.to_dict()
    
    assert isinstance(result_dict, dict)
    assert 'deterministic_text' in result_dict
    assert 'narrative_text' in result_dict
    assert 'ast_json' in result_dict
    assert 'query' in result_dict
    
    print("✓ to_dict works")


def test_normalizer():
    """Test TextNormalizer separately."""
    print("Testing TextNormalizer...")
    normalizer = TextNormalizer()
    
    technical = 'Include items that match ANY of: ("Python"; "Java")'
    narrative = normalizer.normalize(technical)
    
    assert len(narrative) > 0
    assert narrative.endswith('.')
    assert 'Search for' in narrative
    
    print("✓ TextNormalizer works")


def test_complex_queries():
    """Test various complex queries."""
    print("Testing complex queries...")
    parser = LuceneQueryParser()
    
    queries = [
        'test',
        '"exact phrase"',
        '("Python" OR "Java")',
        '("A" OR "B") NOT "C"',
        'title:"Machine Learning"',
        'title:("Python" OR "Java")',
        '(title:"AI" OR title:"ML") AND status:published'
    ]
    
    for query in queries:
        result = parser.parse(query)
        assert result.query == query
        assert len(result.deterministic_text) > 0
        assert len(result.narrative_text) > 0
    
    print(f"✓ All {len(queries)} complex queries parsed successfully")


def main():
    """Run all tests."""
    print("=" * 80)
    print("Testing lucene_query_parser Library")
    print("=" * 80)
    print()
    
    try:
        test_basic_parsing()
        test_error_handling()
        test_to_dict()
        test_normalizer()
        test_complex_queries()
        
        print()
        print("=" * 80)
        print("✅ All tests passed!")
        print("=" * 80)
        
        print()
        print("Example usage:")
        print("-" * 80)
        parser = LuceneQueryParser()
        result = parser.parse('("Python" OR "Java") NOT "JavaScript"')
        print(f"Query: {result.query}")
        print(f"Narrative: {result.narrative_text}")
        print(f"Deterministic: {result.deterministic_text}")
        
    except Exception as e:
        print()
        print("=" * 80)
        print(f"❌ Test failed: {e}")
        print("=" * 80)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
