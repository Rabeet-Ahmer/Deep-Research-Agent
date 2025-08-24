from agents import Agent, function_tool
from config import agent_model
import requests
from bs4 import BeautifulSoup


@function_tool
def url_scrape(url: str) -> str:
    """
    Scrape the content of a webpage at the given URL.
    """
    try:
        headers = {
            "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
            )
        }
        response = requests.get(url, headers = headers, timeout = 10)
        response.raise_for_status()  
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            for script in soup(['script', 'style']):
                script.extract()
            text = soup.get_text(separator="\n", strip=True)
            lines = text.split("\n")
            return "\n".join(lines[:500])
        except ImportError:
            return response.text[:5000]
    except Exception as e:
        return f"Failed to scrape content from {url}: {e}"

SEARCH_INSTRUCTIONS = (
    "You are research assistant. Given a URL and its title, you will analyze the content of the URL"
    "and produce a concise summary of the information. The summary must be 2-3 paragraphs."
    "Capture the main points. Write succinctly, no need to have complete sentences or perfect grammar."
    "This will be consumed by someone synthesizing a report, so it is vital you capture the essence and ignore"
    "any fluff. Do not include any additional commentary other than summary itself"
)


search_agent = Agent(
    name = "Search Agent",
    instructions = SEARCH_INSTRUCTIONS,
    tools = [url_scrape],
    model = agent_model
)