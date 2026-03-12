import os
from serpapi import GoogleSearch


def get_top_results(keyword: str, num: int = 3, lang: str = "fr", country: str = "fr") -> list:
    """
    Récupère les top résultats organiques Google via SerpAPI.
    Retourne une liste de dicts avec position, titre, url, snippet.
    """
    params = {
        "engine": "google",
        "q": keyword,
        "api_key": os.getenv("SERPAPI_KEY"),
        "gl": country,
        "hl": lang,
        "num": 10,
    }

    search = GoogleSearch(params)
    data = search.get_dict()

    organic = data.get("organic_results", [])

    results = []
    for r in organic[:num]:
        results.append({
            "position": r.get("position", 0),
            "title": r.get("title", ""),
            "url": r.get("link", ""),
            "snippet": r.get("snippet", ""),
            "displayed_link": r.get("displayed_link", ""),
        })

    return results
