import os
import requests


SEMRANK_URL = "https://api-semrank.cuik.io/api/premium/brief"
SEMRANK_STATUS_URL = "https://api-semrank.cuik.io/api/premium/status"


def get_seo_brief(keyword: str, lang: str = "fr", country: str = "fr") -> dict:
    """
    Récupère le brief SEO depuis l'API SEMRANK.
    Retourne un dict avec le brief ou un message d'erreur.
    """
    api_key = os.getenv("SEMRANK_KEY")

    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": api_key,
    }

    payload = {
        "keyword": keyword,
        "language": lang,
        "location": country,
    }

    try:
        response = requests.post(
            SEMRANK_URL,
            json=payload,
            headers=headers,
            timeout=60,
        )
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        elif response.status_code == 401:
            return {"success": False, "error": "Clé API SEMRANK invalide (401)", "data": {}}
        elif response.status_code == 429:
            return {"success": False, "error": "Crédits SEMRANK épuisés (429)", "data": {}}
        else:
            return {"success": False, "error": f"Erreur SEMRANK {response.status_code} : {response.text[:200]}", "data": {}}
    except Exception as e:
        return {"success": False, "error": str(e), "data": {}}


def format_brief_for_prompt(brief_result: dict) -> str:
    """Convertit le résultat SEMRANK en texte pour les prompts."""
    if not brief_result.get("success"):
        return f"Brief SEMRANK non disponible : {brief_result.get('error', 'Erreur inconnue')}"

    data = brief_result.get("data", {})
    lines = ["=== BRIEF SEMRANK ==="]

    # Mots-clés principaux
    top_kw = data.get("Top_Keywords", [])
    if top_kw:
        lines.append("Mots-clés principaux :")
        for kw in top_kw[:20]:
            if isinstance(kw, dict):
                lines.append(f"  - {kw.get('keyword', kw)}")
            else:
                lines.append(f"  - {kw}")

    # Brief de contenu
    content_brief = data.get("content_brief", "")
    if content_brief:
        lines.append("\nBrief de contenu :")
        lines.append(str(content_brief)[:3000])

    return "\n".join(lines)
