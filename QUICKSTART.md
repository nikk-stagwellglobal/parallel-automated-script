# Quick Start Guide

## Setup (10 minutes)

### Prerequisites
- Google Cloud SDK installed
- Access to `plat-shared-art-shared` GCP project
- Parallel AI API key

### Installation Steps

1. **Authenticate with Google Cloud:**
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```

2. **Configure Poetry for custom package repository:**
   ```bash
   cd parallel-ai-testing
   poetry source add unicepta-pup https://us-central1-python.pkg.dev/plat-shared-art-shared/unicepta-pup/simple/
   ACCESS_TOKEN=$(gcloud auth print-access-token)
   poetry config http-basic.unicepta-pup oauth2accesstoken $ACCESS_TOKEN
   ```

3. **Install dependencies:**
   ```bash
   poetry lock
   poetry install
   ```

4. **Set your API key:**
   ```bash
   export PARALLEL_API_KEY="your_api_key_here"
   ```

5. **Run the script:**
   ```bash
   poetry run python -m parallel_ai_testing.main
   ```

**Note:** For detailed setup instructions and troubleshooting, see [SETUP.md](SETUP.md).

## What It Does

The script will:
1. Process 10 automotive brands (Stellantis, BMW, Toyota, Ford, Honda, Tesla, Mercedes, Volkswagen, Audi, Hyundai)
2. Generate boolean queries for each brand
3. Convert queries to natural language prompts
4. Run each prompt against multiple Parallel AI models (pro, ultra) **in parallel**
5. Save results to `results/` directory as JSON files

## Output

You'll get:
- Individual JSON files per brand: `results/tesla_20251112_135400.json`
- Combined results file: `results/all_results.json`
- Logs in: `logs/parallel_testing.log`

## Custom Run

To test specific brands:

```bash
poetry run python example_custom_run.py
```

Edit `example_custom_run.py` to customize brands and processors.

