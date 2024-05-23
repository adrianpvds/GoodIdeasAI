
# Project Title: Good Ideas AI Scraper

## Description

This Python script is designed to automate the extraction and analysis of web content. It integrates several powerful tools and libraries, including OpenAI's language models, Spacy for natural language processing, and Apify for web scraping. The script corrects spelling, expands keywords for better search results, scrapes specified websites, and generates insights from the collected data using a language model.

## Features

- **Spelling Correction**: Corrects input spellings using the `SpellChecker` library to enhance the accuracy of keyword expansion.
- **Keyword Expansion**: Enhances keyword search capabilities using Spacy's NLP features, allowing for more effective data scraping.
- **Data Scraping**: Uses Apify to scrape data from specified websites, tailored to the needs specified by the expanded keywords.
- **Data Analysis**: Analyzes the scraped data to generate insights based on user queries, utilizing OpenAI's language models. It can handle multiple language models and configurations to tailor the analysis to specific requirements.

## Prerequisites

Before you run this script, you will need to install the following Python libraries:

```bash
pip install openai spacy apify-client langchain-community spellchecker
```

You will also need to download the English model for Spacy:

```bash
python -m spacy download en_core_web_sm
```

## Setup

1. **API Keys**: You need to have valid API keys for OpenAI and Apify services. Set these keys in your environment variables to keep them secure:

   ```bash
   export OPENAI_API_KEY='your_openai_api_key_here'
   export APIFY_API_KEY='your_apify_api_key_here'
   ```

2. **Configuration**: Replace placeholder API keys in the script with environment variables:

   ```python
   openai.api_key = os.getenv("OPENAI_API_KEY")
   apify_client = ApifyClient(os.getenv("APIFY_API_KEY"))
   ```

## Usage

To run this script, simply execute it from your command line:

```bash
python your_script_name.py
```

You will be prompted to enter the enterprise name, keywords, type of insight, and the specific websites you want to scrape. The script will correct the spelling of your inputs, expand the keywords, scrape the specified websites, and analyze the data to generate insights.

## Sample Output

After running the script, it outputs the insights extracted based on the analysis of the web content. These insights are printed directly to the console and include details on the content extracted and the analysis performed.

## Error Handling and Debugging

The script includes basic error handling for common issues such as API connectivity problems and scraping errors. In case of issues, check the console for error messages which can guide troubleshooting.
