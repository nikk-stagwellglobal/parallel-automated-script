"""Lucene Query Parser - A Python library for parsing and analyzing Lucene queries.

This library provides a simple, efficient way to parse Lucene queries and convert
them into multiple representations: deterministic text, natural language narratives,
and Abstract Syntax Tree (AST) JSON.

Example:
    >>> from lucene_query_parser import LuceneQueryParser
    >>> 
    >>> parser = LuceneQueryParser()
    >>> result = parser.parse('("Python" OR "Java") NOT "JavaScript"')
    >>> 
    >>> print(result.narrative_text)
    Search for documents containing any of the following: "Python", "Java" but exclude documents where "JavaScript".
    >>> 
    >>> print(result.deterministic_text)
    Include items that match ANY of: ("Python"; "Java") EXCLUDE items where: ("JavaScript")
    >>> 
    >>> print(result.ast_json)
    {'type': 'UnknownOperation', 'value': None, 'children': [...]}
"""

from .parser import LuceneQueryParser
from .models import QueryResult
from .normalizer import TextNormalizer

__version__ = "1.0.0"
__all__ = ["LuceneQueryParser", "QueryResult", "TextNormalizer"]
