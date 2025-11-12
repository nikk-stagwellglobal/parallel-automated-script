# Parallel AI Testing Script

Automated testing script for Parallel AI Deep Research across multiple models. This tool generates detailed prompts for multiple brands with structured widget components (Leaderboard, Sentiment Summary, Volume Alerts, Root Causes, Heatmap) and runs queries in parallel across different Parallel AI processors.



## Installation

### Prerequisites

- Python 3.12+
- Poetry package manager
- Google Cloud SDK (gcloud CLI)
- Access to the `plat-shared-art-shared` GCP project
- Parallel AI API key

**Quick start:**

1. Authenticate with Google Cloud:
```bash
gcloud auth login
gcloud auth application-default login
```

2. Configure Poetry for custom package repository:
```bash
cd parallel-ai-testing
poetry source add unicepta-pup https://us-central1-python.pkg.dev/plat-shared-art-shared/unicepta-pup/simple/
$ACCESS_TOKEN = gcloud auth print-access-token
poetry config http-basic.unicepta-pup oauth2accesstoken $ACCESS_TOKEN
```

3. Install dependencies:
```bash
poetry lock
poetry install
```

4. Set your Parallel AI API key:
```bash
export PARALLEL_API_KEY="NaFdoJEUqSfILMoEnElJn6vOEpBCye7QNDsHSG2L"
```

**Note:** Access tokens expire after 1 hour. If you encounter authentication errors, refresh your token and reconfigure Poetry. See [SETUP.md](SETUP.md) for troubleshooting.

## Usage

### Basic Usage

Run the script with default settings (all 10 brands, all available processors):

```bash
poetry run python -m parallel_ai_testing.main
```


```
parallel-ai-testing/
├── parallel_ai_testing/
│   ├── __init__.py
│   ├── main.py                 # Main orchestration script
│   ├── query_parser.py         # Boolean to natural language converter
│   ├── prompt_generator.py     # Prompt generation functions
│   ├── parallel_client.py      # Parallel AI API client
│   ├── result_saver.py         # Result saving utilities
│   └── logger_config.py        # Logging configuration
├── results/                    # Output directory for JSON results
├── logs/                       # Log files
├── pyproject.toml             # Poetry dependencies
└── README.md
```

