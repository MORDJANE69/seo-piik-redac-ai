import os
import requests


PERPLEXITY_URL = "https://api.perplexity.ai/chat/completions"


def query(
    prompt: str,
    system: str = "Tu es un expert SEO et marketing digital. Réponds toujours en français.",
    model: str = "sonar-pro",
    max_tokens: int = 4000,
) -> str:
    """
    Envoie un prompt à l'API Perplexity et retourne la réponse texte.
    Utilise sonar-pro pour avoir accès à la recherche web en temps réel.
    """
    api_key = os.getenv("PERPLEXITY_KEY")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": max_tokens,
        "temperature": 0.2,
        "return_citations": True,
        "return_related_questions": False,
    }

    response = requests.post(PERPLEXITY_URL, headers=headers, json=payload, timeout=120)
    response.raise_for_status()

    data = response.json()
    return data["choices"][0]["message"]["content"]


def run_content_gap(keyword: str, serp_context: str, semrank_context: str) -> str:
    """Étape 2 — Analyse content gap et angles différenciants."""
    from .prompts import CONTENT_GAP_PROMPT
    prompt = CONTENT_GAP_PROMPT.format(
        keyword=keyword,
        serp_context=serp_context,
        semrank_context=semrank_context,
    )
    return query(prompt)


def run_pain_points(keyword: str) -> str:
    """Étape 3 — Recherche des points de douleur uniquement sur forums et réseaux sociaux."""
    from .prompts import PAIN_POINTS_PROMPT
    api_key = os.getenv("PERPLEXITY_KEY")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "sonar-pro",
        "messages": [
            {
                "role": "system",
                "content": "Tu es un expert en marketing digital. Recherche uniquement sur des forums et réseaux sociaux. Réponds toujours en français.",
            },
            {
                "role": "user",
                "content": PAIN_POINTS_PROMPT.format(keyword=keyword),
            },
        ],
        "max_tokens": 8000,
        "temperature": 0.2,
        "return_citations": True,
        "search_domain_filter": [
            "reddit.com",
            "quora.com",
            "forum.fr",
            "forums.fr",
            "commentcamarche.net",
            "clubic.com/forum",
            "hardware.fr",
            "developpez.net/forums",
            "jeuxvideo.com/forums",
            "aufeminin.com",
            "forum.wordreference.com",
        ],
    }

    response = requests.post(PERPLEXITY_URL, headers=headers, json=payload, timeout=180)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def run_statistics(keyword: str) -> str:
    """Étape 3.2 — Recherche de statistiques et data-mining."""
    from .prompts import STATISTICS_PROMPT
    prompt = STATISTICS_PROMPT.format(keyword=keyword)
    return query(
        prompt,
        system="Tu es un assistant de recherche factuelle. Fournis uniquement des données chiffrées vérifiables issues de sources officielles. Réponds toujours en français.",
        max_tokens=6000,
    )


def run_semantic_brief(
    keyword: str,
    textfocus_context: str,
    pain_points_context: str,
) -> str:
    """Étape 4 — Brief SEO structuré + tableau sémantique complet."""
    from .prompts import SEMANTIC_BRIEF_PROMPT
    prompt = SEMANTIC_BRIEF_PROMPT.format(
        keyword=keyword,
        textfocus_context=textfocus_context,
        pain_points_context=pain_points_context,
    )
    return query(prompt)
