"""Batch processing example using the Lucene Query Parser library."""

from lucene_query_parser import LuceneQueryParser
from typing import List, Dict
import pandas as pd
from functools import lru_cache
import time


@lru_cache(maxsize=1000)
def parse_query_cached(query: str) -> dict:
    """Cached version of query parsing for better performance."""
    parser = LuceneQueryParser()
    result = parser.parse(query)
    return result.to_dict()


def process_queries_simple(queries: List[str]) -> pd.DataFrame:
    """Process multiple queries and return results as DataFrame.
    
    Args:
        queries: List of Lucene query strings
        
    Returns:
        DataFrame with query results and error information
    """
    parser = LuceneQueryParser()
    results = []
    
    for i, query in enumerate(queries, 1):
        print(f"Processing query {i}/{len(queries)}: {query[:50]}...")
        
        try:
            result = parser.parse(query)
            results.append({
                'query': query,
                'narrative': result.narrative_text,
                'deterministic': result.deterministic_text,
                'valid': True,
                'error': None,
                'ast_depth': _calculate_depth(result.ast_json)
            })
        except ValueError as e:
            results.append({
                'query': query,
                'narrative': None,
                'deterministic': None,
                'valid': False,
                'error': str(e),
                'ast_depth': None
            })
    
    return pd.DataFrame(results)


def process_queries_with_caching(queries: List[str]) -> pd.DataFrame:
    """Process queries with caching for better performance.
    
    This is useful when you have duplicate queries in your batch.
    """
    results = []
    
    for query in queries:
        try:
            result = parse_query_cached(query)
            results.append({
                'query': query,
                'narrative': result['narrative_text'],
                'deterministic': result['deterministic_text'],
                'valid': True,
                'error': None
            })
        except ValueError as e:
            results.append({
                'query': query,
                'narrative': None,
                'deterministic': None,
                'valid': False,
                'error': str(e)
            })
    
    return pd.DataFrame(results)


def _calculate_depth(node: dict, depth: int = 0) -> int:
    """Calculate the depth of the AST tree."""
    max_depth = depth
    
    if 'children' in node and node['children']:
        for child in node['children']:
            child_depth = _calculate_depth(child, depth + 1)
            max_depth = max(max_depth, child_depth)
    elif 'expr' in node and node['expr']:
        max_depth = max(max_depth, _calculate_depth(node['expr'], depth + 1))
    
    return max_depth


def analyze_query_complexity(df: pd.DataFrame) -> Dict:
    """Analyze the complexity of queries in the DataFrame."""
    valid_df = df[df['valid'] == True]
    
    return {
        'total_queries': len(df),
        'valid_queries': len(valid_df),
        'invalid_queries': len(df[df['valid'] == False]),
        'avg_narrative_length': valid_df['narrative'].str.len().mean() if len(valid_df) > 0 else 0,
        'avg_deterministic_length': valid_df['deterministic'].str.len().mean() if len(valid_df) > 0 else 0,
        'avg_ast_depth': valid_df['ast_depth'].mean() if 'ast_depth' in valid_df.columns else 0
    }


def main():
    print("=" * 80)
    print("Lucene Query Parser - Batch Processing Examples")
    print("=" * 80)
    print()
    
    sample_queries = [
        '("Python" OR "Java")',
        'title:"Machine Learning"',
        '((invalid query',
        'status:published AND category:tech',
        '"Data Science"',
        '("A" OR "B") NOT "C"',
        'field:value',
        '((unclosed',
        '(title:"AI" OR title:"ML") AND status:published',
        'author:"John Doe" AND year:2024'
    ]
    
    print("Example 1: Simple Batch Processing")
    print("-" * 80)
    start_time = time.time()
    df = process_queries_simple(sample_queries)
    elapsed = time.time() - start_time
    
    print(f"\nProcessed {len(sample_queries)} queries in {elapsed:.2f} seconds")
    print(f"\nResults:")
    print(df[['query', 'valid', 'narrative']].to_string())
    print()
    
    print("Example 2: Analyzing Valid vs Invalid Queries")
    print("-" * 80)
    valid_queries = df[df['valid'] == True]
    invalid_queries = df[df['valid'] == False]
    
    print(f"Valid queries: {len(valid_queries)}")
    print(f"Invalid queries: {len(invalid_queries)}")
    print()
    
    if len(invalid_queries) > 0:
        print("Invalid queries and errors:")
        for _, row in invalid_queries.iterrows():
            print(f"  - {row['query'][:50]}: {row['error']}")
        print()
    
    print("Example 3: Query Complexity Analysis")
    print("-" * 80)
    stats = analyze_query_complexity(df)
    for key, value in stats.items():
        print(f"{key}: {value}")
    print()
    
    print("Example 4: Exporting Results")
    print("-" * 80)
    output_file = '/tmp/query_analysis.csv'
    df.to_csv(output_file, index=False)
    print(f"Results exported to: {output_file}")
    print()
    
    print("Example 5: Performance with Caching")
    print("-" * 80)
    duplicate_queries = sample_queries * 5
    
    start_time = time.time()
    df_cached = process_queries_with_caching(duplicate_queries)
    elapsed_cached = time.time() - start_time
    
    print(f"Processed {len(duplicate_queries)} queries (with duplicates) in {elapsed_cached:.2f} seconds")
    print(f"Average time per query: {elapsed_cached/len(duplicate_queries)*1000:.2f} ms")
    print()
    
    print("Example 6: Filtering and Analysis")
    print("-" * 80)
    valid_df = df[df['valid'] == True]
    
    if len(valid_df) > 0:
        print("Queries with 'OR' operations:")
        or_queries = valid_df[valid_df['deterministic'].str.contains('ANY')]
        print(f"  Count: {len(or_queries)}")
        
        print("\nQueries with field searches:")
        field_queries = valid_df[valid_df['deterministic'].str.contains(':')]
        print(f"  Count: {len(field_queries)}")
        
        print("\nQueries with exclusions:")
        not_queries = valid_df[valid_df['deterministic'].str.contains('EXCLUDE')]
        print(f"  Count: {len(not_queries)}")
    print()


if __name__ == "__main__":
    main()
