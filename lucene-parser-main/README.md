# Lucene Query Parser

A comprehensive Lucene query parsing solution available both as a **standalone Python library** and as a **FastAPI REST API service**. Parse complex Lucene queries, generate Abstract Syntax Trees (AST), and convert queries into human-readable narrative text.

## 🎯 Two Ways to Use

### 1. 📦 As a Python Library (Recommended for Internal Use)
Direct import and use in your Python applications - no HTTP overhead!

```python
from lucene_query_parser import LuceneQueryParser

parser = LuceneQueryParser()
result = parser.parse('("Python" OR "Java") NOT "JavaScript"')

print(result.narrative_text)
# Output: Search for documents containing any of the following: "Python", "Java" 
#         but exclude documents where "JavaScript".
```

**Benefits:**
- ⚡ No HTTP overhead - direct function calls
- 🔧 Framework-agnostic - works with any Python project
- 📦 Minimal dependencies - only requires `luqum`
- 🐍 Supports Python 3.13+

### 2. 🌐 As a REST API Service
HTTP API with FastAPI for external integrations and microservices.

```bash
# Start the API server
cd lucene-api
poetry run fastapi dev app/main.py

# Parse a query
curl -X POST "http://localhost:8000/api/v1/parse" \
  -H "Content-Type: application/json" \
  -d '{"query": "(\"Python\" OR \"Java\")"}'
```

**Benefits:**
- 🌍 Language-agnostic - use from any programming language
- 📝 Interactive documentation - Swagger UI at `/docs`
- 🔄 Multiple input methods - JSON payload or file upload
- ✅ Production-ready - clean architecture, logging, validation

### 3. 🖥️ Web Interface (Streamlit)
User-friendly web interface for testing and demonstrations.

### Installation & Running
```bash
cd lucene-query-parser/lucene-api
poetry install
poetry run fastapi dev app/main.py
```
Wait for the message: "Application startup complete"

**Step 2: Start the Streamlit App** (Terminal 2)
```bash
cd lucene-api
poetry run streamlit run ../streamlit_app.py
```

Access at `http://localhost:8501` for an interactive query parsing experience.

## 🚀 Quick Start

### Installation

**As a Library:**
```bash
pip install -e .
```

**For API Development:**
```bash
cd lucene-api
poetry install
```

## 📋 Features

### Core Capabilities
- ✨ Parse complex Lucene query syntax
- 🌳 Generate Abstract Syntax Tree (AST) in JSON format
- 📝 Convert to technical deterministic text
- 💬 Generate human-friendly narrative explanations
- ❌ Comprehensive error handling with meaningful messages

### Supported Query Types
- **Simple terms**: `test`, `python`
- **Phrases**: `"Machine Learning"`, `"data science"`
- **Boolean operators**: `AND`, `OR`, `NOT`
- **Field searches**: `title:"AI"`, `status:published`
- **Grouping**: `(A OR B) AND C`
- **Complex combinations**: `(title:"Python" OR title:"Java") AND status:published NOT archived`

### Library Features
- 🎯 Simple API with two main classes: `LuceneQueryParser` and `QueryResult`
- 🔧 Framework-agnostic design
- 📦 Minimal dependencies (only `luqum>=1.0.0`)
- 🐍 Python 3.9+ support for broad compatibility
- 🪵 Optional logging with standard Python logging module
- 💪 Type-safe with dataclasses and type hints

### API Features
- 🏗️ Clean architecture with separated layers (routes → controllers → services)
- ✅ Pydantic validation for request/response
- 🔌 Dependency injection with cached services
- 📤 Dual input methods (JSON and file upload)
- 📊 Structured logging to console and file
- 📚 Interactive API documentation (Swagger UI)
- ❤️ Health check endpoint

## 📚 Documentation
- **[examples/](examples/)** - Runnable code examples for various use cases

## 🧪 Testing

### Test the Library
```bash
# Run library tests
python test_library.py

# Run basic usage example
python examples/basic_usage.py

# Run error handling example
python examples/error_handling.py
```

### Test the API
```bash
# Start the API server
cd lucene-api
poetry run fastapi dev app/main.py

# In another terminal, run comprehensive tests
cd ..
bash test_api.sh
```

## 🏗️ Project Structure

```
lucene-query-parser/
├── lucene_query_parser/          # Standalone Python library
│   ├── __init__.py               # Public API exports
│   ├── models.py                 # QueryResult dataclass
│   ├── parser.py                 # LuceneQueryParser class
│   └── normalizer.py             # TextNormalizer class
├── lucene-api/                   # FastAPI service (uses library internally)
│   ├── app/
│   │   ├── api/routes/           # HTTP endpoints
│   │   ├── controllers/          # Request orchestration
│   │   ├── services/             # Business logic (wraps library)
│   │   ├── schemas/              # Pydantic models
│   │   ├── core/                 # Configuration & logging
│   │   └── dependencies/         # Dependency injection
│   └── pyproject.toml
├── examples/                     # Usage examples
│   ├── basic_usage.py
│   ├── error_handling.py
│   ├── integration_flask.py
│   ├── integration_django.py
│   └── batch_processing.py
├── streamlit_app.py              # Web interface
├── setup.py                      # Package installation
├── test_library.py               # Library test suite
├── test_api.sh                   # API test script
└── README.md                     # This file
```

## 💡 Use Cases

### Direct Library Integration
Perfect for:
- Backend services that need query parsing
- Data processing pipelines
- Search applications
- ETL workflows
- Any Python application needing Lucene query parsing

### API Service
Ideal for:
- Microservices architecture
- Language-agnostic integrations
- External client applications
- Centralized query parsing service
- Multi-tenant environments

### Web Interface
Great for:
- User testing and demonstrations
- Query development and debugging
- Training and education
- Non-technical user access

## 🔧 Technology Stack

- **Core Library**: Pure Python with `luqum` for Lucene parsing
- **API Framework**: FastAPI with Pydantic validation
- **Web Interface**: Streamlit for interactive UI
- **Python Version**: 3.13 (library supports 3.13+)
- **Dependency Management**: Poetry
- **Architecture**: Clean architecture with dependency injection

## 📖 Example Output

**Input Query:**
```
("H.B. Fuller" OR "Arkema") NOT "Albemarle County"
```

**Narrative Text:**
```
Search for documents containing any of the following: "H.B. Fuller", "Arkema" 
but exclude documents where "Albemarle County".
```

**Deterministic Text:**
```
Include items that match ANY of: ("H.B. Fuller"; "Arkema") 
EXCLUDE items where: ("Albemarle County")
```

**AST JSON:**
```json
{
  "type": "UnknownOperation",
  "value": null,
  "children": [
    {
      "type": "Group",
      "children": [
        {
          "type": "OrOperation",
          "children": [
            {"type": "Phrase", "value": "\"H.B. Fuller\""},
            {"type": "Phrase", "value": "\"Arkema\""}
          ]
        }
      ]
    },
    {
      "type": "Not",
      "children": [
        {"type": "Phrase", "value": "\"Albemarle County\""}
      ]
    }
  ]
}
```

## 🤝 Contributing

This project follows clean architecture principles and best practices:
- Separation of concerns across layers
- Dependency injection for testability
- Comprehensive error handling
- Type safety with type hints
- Detailed logging for debugging

