from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
from rich import print
from dotenv import load_dotenv
load_dotenv()
import os

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
@tool
def web_search(query: str) -> str:
    """
    Perform a web search using Tavily and return the top recent news with its title, URL, and snippet.
    """
    results = tavily.search(
        query=query,
        max_results=5,
        topic="general",
        time_range="week",
    )
    out = []
    for r in results['results']:
        out.append(f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n")
    return "\n---\n".join(out)

@tool
def scrape_webpage(url: str) -> str:
    """
    Scrape and return clean text content from a given URL for deeper reading.
    """
    try:
        response = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
            )
        soup = BeautifulSoup(response.content, 'html.parser')
        for tag in soup(['script', 'style',"nav","header","footer","aside"]):
            tag.decompose()
        return soup.get_text(separator=' ', strip=True)[:5000]  # Return first 5000 characters of text
    except Exception as e:
        return f"An error occurred while scraping the webpage: {str(e)}"