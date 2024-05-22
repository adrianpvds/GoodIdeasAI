import openai
import spacy
from apify_client import ApifyClient
from langchain_community.llms.openai import OpenAI  # Corrected import
from langchain.chains import LLMChain  # Corrected import
from langchain.prompts import PromptTemplate  # Corrected import
from spellchecker import SpellChecker

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Initialize Spacy and Apify
nlp = spacy.load("en_core_web_sm")
apify_client = ApifyClient("")
openai.api_key = ""

def correct_spelling(text):
    spell = SpellChecker()
    corrected_text = ' '.join(spell.correction(word) or word for word in text.split())
    return corrected_text

def get_expanded_keywords(keywords):
    doc = nlp(keywords)
    expanded_keywords = [keywords]
    for token in doc:
        if token.text.lower() not in expanded_keywords:
            expanded_keywords.append(token.text.lower())
        if token.lemma_ not in expanded_keywords:
            expanded_keywords.append(token.lemma_)
    return list(set(expanded_keywords))

def scrape_data(enterprise, keywords, sources):
    #print(f"\n\n{sources=}\n\n")
    data = []
    for source in sources:
        run_input = {
            "startUrls": [{"url": source}],
            "pageFunction": """async function pageFunction(context) {
                const $ = context.jQuery;
                const { request, log } = context;
                const title = $('title').text();
                const bodyText = $('body').text();
                const metaDescription = $('meta[name="description"]').attr('content');
                return {
                    url: request.url,
                    title,
                    bodyText,
                    metaDescription,
                };
            }""",
            "maxCrawlingDepth": 1,
            "maxPagesPerCrawl": 1
        }
        run = []
        run1 = apify_client.actor("apify/web-scraper").call(run_input=run_input)
        for item in apify_client.dataset(run1["defaultDatasetId"]).iterate_items():
            run.append(item)
        if run1.get('status') == 'SUCCEEDED':
            data.extend(run)
        else:
            print(f"Failed to scrape {source}: {run1['statusMessage']}")
    return data

def analyze_data(data, insight_request):
    
    combined_text = " ".join([item["bodyText"] for item in data if "bodyText" in item])
    
    # Segmentation of the text into chunks under the maximum token limit
    max_length = 4000  # Adjust as per the model's limits
    text_chunks = [combined_text[i:i+max_length] for i in range(0, len(combined_text), max_length)]
    
    # could also add Huggingface, BERT, or other LLMs
    insights = []
    for chunk in text_chunks:
        llm = OpenAI(temperature=0.05, openai_api_key=openai.api_key)
        prompt_template = PromptTemplate(
            input_variables=["text", "insight_request"],
            template="Given the following text: {text}\n\n{insight_request}"
        )
        chain = LLMChain(llm=llm, prompt=prompt_template)
        response = chain.run({"text": chunk, "insight_request": insight_request})
        insights.append(response)
    return insights

def main():
    enterprise = input("Enterprise Name: ")
    keywords = input("Keyword(s): ")
    insight_request = input("Type of insight: ")
    sources = input("Specific websites to scrape (comma-separated): ").split(',')
    enterprise = correct_spelling(enterprise)
    keywords = correct_spelling(keywords)
    insight_request = correct_spelling(insight_request)
    expanded_keywords = get_expanded_keywords(keywords)
    all_data = []
    for keyword in expanded_keywords:
        data = scrape_data(enterprise, keyword, sources)
        all_data.extend(data)
    result = analyze_data(all_data, insight_request)
    for res in result:
        print(res)

if __name__ == "__main__":
    main()
