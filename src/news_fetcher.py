import os
import requests
from typing import List, Dict

def fetch_top_news(limit: int = 5) -> List[Dict[str, str]]:
    """Fetches global news based on specific keywords (AI, geopolitics, global events)."""
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        raise ValueError("NEWS_API_KEY environment variable is missing.")

    url = "https://newsapi.org/v2/everything"
    
    params = {
        "q": "(Artificial Intelligence OR AI) AND (war OR geopolitics OR global economy)",
        "language": "en",
        "sortBy": "relevancy",
        "apiKey": api_key
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        articles = data.get("articles", [])[:limit]
        return [{"title": a["title"], "url": a["url"], "source": a["source"]["name"]} for a in articles]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return []