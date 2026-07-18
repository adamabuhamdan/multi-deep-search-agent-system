# AI Research Pipeline

A lightweight Python research agent that searches the web, scrapes a selected resource, writes a structured research report, and then critiques its own output.

## Overview

This repository demonstrates a modular LLM-based research pipeline using:
- `langchain` for agent orchestration
- `langchain_google_genai` for Gemini model access
- `tavily-python` for web search
- `BeautifulSoup`, `trafilatura`, and `readability-lxml` for scraping

The pipeline includes:
1. A search agent that finds recent articles and summaries.
2. A reader agent that scrapes the most relevant URL from search results.
3. A writer prompt that generates a detailed report.
4. A critic prompt that evaluates the report.

## Features

- Query-driven exploration of any topic
- Web search results formatted with title, URL, and snippet
- Multi-strategy webpage scraping for robust extraction
- Structured report generation with introduction, key findings, conclusion, and sources
- Self-review feedback that includes a score and improvement recommendations

## Installation

### Requirements

- Python 3.10+
- A virtual environment (recommended)

### Install dependencies

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Configure environment variables

Create a `.env` file in the repository root containing:

```env
TAVILY_API_KEY=your_tavily_api_key
```

> Note: `langchain_google_genai` may also require Google Cloud credentials or configuration depending on your environment.

## Usage

Run the research pipeline with the repository entrypoint:

```powershell
python main.py
```

Run the frontend UI with Streamlit:

```powershell
streamlit run app.py
```

Or use the pipeline in Python code:

```python
from src.pipelines.pipeline import run_research_pipeline

result = run_research_pipeline(
    "The impact of artificial intelligence on the job market and employment trends in the next decade"
)
print(result["report"])
print(result["feedback"])
```

## Repository Structure

- `main.py` — entrypoint for executing the research pipeline
- `src/pipelines/pipeline.py` — orchestrates search, scrape, write, and critique steps
- `src/agents/agent.py` — builds LLM agents and prompt chains
- `src/tools/tools.py` — defines web search and URL scraping tools
- `requirements.txt` — Python dependency list
- `LICENSE` — project license

## Notes

- `app.py` is currently empty and not required to run the pipeline.
- Web scraping reliability depends on the target site and may return limited content for some pages.
- The project is designed for experimentation and can be extended with UI, more tools, or alternative search providers.

## Contributing

Contributions are welcome! Suggested improvements:
- add a Streamlit or web interface in `app.py`
- support additional search or scraping backends
- add caching for search results and scraped content
- improve report structure or prompt quality

## License

See the `LICENSE` file for license details.
