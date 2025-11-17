"""Core Lucene query parser implementation."""

import logging
from typing import Dict, Any, Optional
from luqum.parser import parser
from luqum.tree import (
    Phrase, Word, SearchField, OrOperation, AndOperation,
    Not, Group, FieldGroup, UnknownOperation
)

from .models import QueryResult
from .normalizer import TextNormalizer


logger = logging.getLogger(__name__)


class LuceneQueryParser:
    """Main parser class for parsing Lucene queries.
    
    This class provides a simple interface to parse Lucene queries and
    generate multiple representations: deterministic text, narrative text,
    and Abstract Syntax Tree (AST) JSON.
    
    Example:
        >>> parser = LuceneQueryParser()
        >>> result = parser.parse('("Python" OR "Java") NOT "JavaScript"')
        >>> print(result.narrative_text)
        Search for documents containing any of the following: "Python", "Java" but exclude documents where "JavaScript".
    """
    
    def __init__(self, enable_logging: bool = False):
        """Initialize the parser.
        
        Args:
            enable_logging: Whether to enable logging output (default: False)
        """
        self.normalizer = TextNormalizer(enable_logging=enable_logging)
        if enable_logging:
            logging.basicConfig(level=logging.INFO)
    
    def parse(self, query: str) -> QueryResult:
        """Parse a Lucene query and return comprehensive results.
        
        Args:
            query: The Lucene query string to parse
            
        Returns:
            QueryResult object containing deterministic text, narrative text,
            and AST JSON representation
            
        Raises:
            ValueError: If the query has invalid Lucene syntax
            
        Example:
            >>> parser = LuceneQueryParser()
            >>> result = parser.parse('title:"Python Programming"')
            >>> print(result.deterministic_text)
            title: contains the EXACT PHRASE "Python Programming"
        """
        logger.info(f"Parsing query: {query[:100]}...")
        
        try:
            ast_tree = parser.parse(query)
            logger.debug(f"Successfully parsed query into AST: {type(ast_tree).__name__}")
        except Exception as e:
            logger.error(f"Failed to parse query: {str(e)}")
            raise ValueError(f"Invalid Lucene query syntax: {str(e)}")
        
        deterministic_text = self._node_to_deterministic_text(ast_tree)
        logger.debug(f"Generated deterministic text: {deterministic_text[:100]}...")
        
        narrative_text = self.normalizer.normalize(deterministic_text)
        logger.debug(f"Generated narrative text: {narrative_text[:100]}...")
        
        ast_json = self._ast_to_json(ast_tree)
        
        return QueryResult(
            deterministic_text=deterministic_text,
            narrative_text=narrative_text,
            ast_json=ast_json,
            query=query
        )
    
    def _ast_to_json(self, node: Any) -> Dict[str, Any]:
        """Convert AST node to JSON representation.
        
        Args:
            node: The AST node to convert
            
        Returns:
            Dictionary representation of the AST node
        """
        result = {
            "type": type(node).__name__,
            "value": getattr(node, 'value', None) or getattr(node, 'name', None)
        }
        
        if hasattr(node, 'children'):
            result["children"] = [self._ast_to_json(child) for child in node.children]
        elif hasattr(node, 'expr'):
            result["expr"] = self._ast_to_json(node.expr)
        
        return result
    
    def _node_to_deterministic_text(self, node: Any, parent_op: Optional[str] = None) -> str:
        """Convert AST node to deterministic text representation.
        
        Args:
            node: The AST node to convert
            parent_op: The parent operation type (for context)
            
        Returns:
            Deterministic text representation of the node
        """
        if isinstance(node, Phrase):
            return node.value
        
        elif isinstance(node, Word):
            return f'contains "{node.value}"'
        
        elif isinstance(node, SearchField):
            field_name = node.name
            field_expr = node.expr
            
            if isinstance(field_expr, FieldGroup):
                inner = field_expr.expr
                if isinstance(inner, Phrase):
                    phrase_value = inner.value.strip('"')
                    return f'{field_name}: contains the EXACT PHRASE "{phrase_value}"'
                elif isinstance(inner, OrOperation):
                    items = []
                    for child in inner.children:
                        if isinstance(child, Phrase):
                            items.append(child.value)
                        elif isinstance(child, Word):
                            items.append(f'"{child.value}"')
                        else:
                            items.append(self._node_to_deterministic_text(child))
                    items_str = "; ".join(items)
                    return f'{field_name}: contains ANY of [{items_str}]'
                elif isinstance(inner, AndOperation):
                    items = []
                    for child in inner.children:
                        if isinstance(child, Phrase):
                            items.append(child.value)
                        elif isinstance(child, Word):
                            items.append(f'"{child.value}"')
                        else:
                            items.append(self._node_to_deterministic_text(child))
                    items_str = "; ".join(items)
                    return f'{field_name}: contains ALL of [{items_str}]'
                else:
                    inner_text = self._node_to_deterministic_text(inner)
                    return f'{field_name}: {inner_text}'
            else:
                inner_text = self._node_to_deterministic_text(field_expr)
                return f'{field_name}: {inner_text}'
        
        elif isinstance(node, OrOperation):
            children_texts = [self._node_to_deterministic_text(child) for child in node.children]
            items = "; ".join(children_texts)
            return f'Include items that match ANY of: ({items})'
        
        elif isinstance(node, AndOperation):
            children_texts = [self._node_to_deterministic_text(child) for child in node.children]
            items = "; ".join(children_texts)
            return f'Include items that match ALL of: ({items})'
        
        elif isinstance(node, Not):
            child = node.children[0]
            child_text = self._node_to_deterministic_text(child)
            return f'EXCLUDE items where: ({child_text})'
        
        elif isinstance(node, Group):
            inner = node.children[0]
            return self._node_to_deterministic_text(inner)
        
        elif isinstance(node, FieldGroup):
            inner = node.expr
            return self._node_to_deterministic_text(inner)
        
        elif isinstance(node, UnknownOperation):
            parts = []
            for child in node.children:
                parts.append(self._node_to_deterministic_text(child))
            return " ".join(parts)
        
        else:
            return str(node)
