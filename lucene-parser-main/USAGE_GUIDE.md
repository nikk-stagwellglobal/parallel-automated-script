# Lucene Query Parser - Comprehensive Usage Guide

This guide provides detailed instructions and examples for integrating the Lucene Query Parser library into various types of Python applications.

## Table of Contents

1. [Installation](#installation)
2. [Basic Usage](#basic-usage)
3. [Framework Integration](#framework-integration)
   - [Flask](#flask-integration)
   - [Django](#django-integration)
   - [FastAPI](#fastapi-integration)
4. [Advanced Use Cases](#advanced-use-cases)
5. [Performance Optimization](#performance-optimization)
6. [Error Handling](#error-handling)
7. [Testing](#testing)

## Installation

### Standard Installation

```bash
pip install lucene-query-parser
```

### Development Installation

```bash
git clone https://github.com/nikk3008/lucene-query-parser.git
cd lucene-query-parser
pip install -e .
```

## Basic Usage

### Simple Query Parsing

```python
from lucene_query_parser import LuceneQueryParser

parser = LuceneQueryParser()

result = parser.parse('("Python" OR "Java") NOT "JavaScript"')

print("Original Query:", result.query)
print("Narrative:", result.narrative_text)
print("Technical:", result.deterministic_text)
print("AST:", result.ast_json)
```

### Accessing Individual Fields

```python
from lucene_query_parser import LuceneQueryParser

parser = LuceneQueryParser()
result = parser.parse('title:"Machine Learning"')

result_dict = result.to_dict()
print(result_dict['narrative_text'])
print(result_dict['deterministic_text'])
print(result_dict['ast_json'])
```

### Using the Text Normalizer Separately

```python
from lucene_query_parser import TextNormalizer

normalizer = TextNormalizer()

technical = 'Include items that match ANY of: ("Python"; "Java")'
narrative = normalizer.normalize(technical)

print(narrative)
```

## Best Practices

1. **Reuse Parser Instances**: Create one parser and reuse it across requests
2. **Add Caching**: Use `lru_cache` or Redis for frequently parsed queries
3. **Validate Input**: Always validate user input before parsing
4. **Handle Errors Gracefully**: Catch `ValueError` for invalid queries
5. **Enable Logging in Development**: Use `enable_logging=True` for debugging
6. **Test Edge Cases**: Test with empty queries, special characters, nested operations
7. **Monitor Performance**: Track parsing times for complex queries
8. **Use Type Hints**: Leverage Python type hints for better IDE support

## Troubleshooting

### Common Issues

**Issue**: `ImportError: No module named 'lucene_query_parser'`
- Solution: Make sure the package is installed: `pip install lucene-query-parser`

**Issue**: `ValueError: Invalid Lucene query syntax`
- Solution: Check your query syntax. Common issues include unmatched parentheses or quotes

**Issue**: Performance degradation with many queries
- Solution: Implement caching using `lru_cache` or a database cache

**Issue**: Missing fields in result
- Solution: Make sure you're accessing the correct attributes of `QueryResult`

## Additional Resources

- [Lucene Query Syntax](https://lucene.apache.org/core/queryparser.html)
- [luqum Documentation](https://luqum.readthedocs.io/)
- [GitHub Repository](https://github.com/nikk-stagwellglobal/lucene-parser)

## Support

For issues or questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the API documentation
