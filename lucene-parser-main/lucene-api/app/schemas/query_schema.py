from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any


class QueryRequest(BaseModel):
    """Request schema for query parsing"""
    query: str = Field(..., min_length=1, description="Lucene query string to parse")
    
    @field_validator('query')
    @classmethod
    def validate_query_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Query cannot be empty or whitespace only")
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": '("H.B. Fuller" OR "Arkema") NOT "Albemarle County"'
            }
        }


class ASTNode(BaseModel):
    """AST node representation"""
    type: str
    value: Optional[str] = None
    children: Optional[list] = None
    expr: Optional[Dict[str, Any]] = None


class QueryResponse(BaseModel):
    """Response schema for parsed query"""
    deterministic_text: str = Field(..., description="Human-readable query interpretation")
    narrative_text: str = Field(..., description="Normalized narrative explanation")
    ast_json: Dict[str, Any] = Field(..., description="Abstract Syntax Tree representation")
    
    class Config:
        json_schema_extra = {
            "example": {
                "deterministic_text": 'Include items that match ANY of: ("H.B. Fuller"; "Arkema") EXCLUDE items where: ("Albemarle County")',
                "narrative_text": "Search for documents containing either 'H.B. Fuller' or 'Arkema', but exclude any documents that mention 'Albemarle County'.",
                "ast_json": {
                    "type": "AndOperation",
                    "value": None,
                    "children": []
                }
            }
        }


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
