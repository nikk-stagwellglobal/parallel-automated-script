"""Basic usage examples for the Lucene Query Parser library."""

from lucene_query_parser import LuceneQueryParser


def main():
    parser = LuceneQueryParser()
    
    print("=" * 80)
    print("Lucene Query Parser - Basic Usage Examples")
    print("=" * 80)
    print()
    
    print("Example 1: Simple Word Query")
    print("-" * 40)
    result = parser.parse('test')
    print(f"Query: {result.query}")
    print(f"Narrative: {result.narrative_text}")
    print(f"Deterministic: {result.deterministic_text}")
    print()
    
    print("Example 2: Phrase Query")
    print("-" * 40)
    result = parser.parse('"Python Programming"')
    print(f"Query: {result.query}")
    print(f"Narrative: {result.narrative_text}")
    print()
    
    print("Example 3: OR Operation")
    print("-" * 40)
    result = parser.parse('("Python" OR "Java")')
    print(f"Query: {result.query}")
    print(f"Narrative: {result.narrative_text}")
    print(f"Deterministic: {result.deterministic_text}")
    print()
    
    print("Example 4: Complex Boolean Query")
    print("-" * 40)
    result = parser.parse('("H.B. Fuller" OR "Arkema") NOT "Albemarle County"')
    print(f"Query: {result.query}")
    print(f"Narrative: {result.narrative_text}")
    print(f"Deterministic: {result.deterministic_text}")
    print()
    
    print("Example 5: Field-Specific Search")
    print("-" * 40)
    result = parser.parse('title:("Machine Learning" OR "AI")')
    print(f"Query: {result.query}")
    print(f"Narrative: {result.narrative_text}")
    print(f"Deterministic: {result.deterministic_text}")
    print()
    
    print("Example 6: Very Complex Query")
    print("-" * 40)
    result = parser.parse('(title:"Python" OR title:"Java") AND status:published NOT archived')
    print(f"Query: {result.query}")
    print(f"Narrative: {result.narrative_text}")
    print()
    
    print("Example 7: Converting to Dictionary")
    print("-" * 40)
    result = parser.parse('("A" OR "B")')
    result_dict = result.to_dict()
    print(f"Result as dict keys: {list(result_dict.keys())}")
    print(f"Narrative from dict: {result_dict['narrative_text']}")
    print()
    
    print("Example 8: Error Handling")
    print("-" * 40)
    try:
        result = parser.parse('((unclosed parenthesis')
    except ValueError as e:
        print(f"Caught error: {e}")
    print()
    
    print("Example 9: AST JSON Structure")
    print("-" * 40)
    result = parser.parse('("Python" OR "Java")')
    import json
    print(f"AST JSON:\n{json.dumps(result.ast_json, indent=2)}")
    print()


if __name__ == "__main__":
    main()
