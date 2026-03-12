import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def extract_content(url: str) -> dict:
    """
    Extrait les titres (H1-H4), les paragraphes et le nombre de mots d'une URL.
    Retourne un dict structuré pour l'analyse.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")

        # Supprimer les éléments inutiles
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        # Extraire les titres
        headings = []
        for tag in soup.find_all(["h1", "h2", "h3", "h4"]):
            text = tag.get_text(strip=True)
            if text:
                headings.append({
                    "level": tag.name.upper(),
                    "text": text,
                })

        # Extraire les paragraphes (min 40 chars pour filtrer les boutons/menus)
        paragraphs = [
            p.get_text(strip=True)
            for p in soup.find_all("p")
            if len(p.get_text(strip=True)) > 40
        ]

        full_text = " ".join(paragraphs)
        word_count = len(full_text.split())

        # Meta description
        meta_desc = ""
        meta = soup.find("meta", attrs={"name": "description"})
        if meta:
            meta_desc = meta.get("content", "")

        return {
            "url": url,
            "headings": headings,
            "paragraphs": paragraphs[:15],
            "word_count": word_count,
            "meta_description": meta_desc,
            "full_text": full_text[:4000],
            "error": None,
        }

    except Exception as e:
        return {
            "url": url,
            "headings": [],
            "paragraphs": [],
            "word_count": 0,
            "meta_description": "",
            "full_text": "",
            "error": str(e),
        }


def format_headings_for_prompt(scraped: dict) -> str:
    """Formate les titres d'une page pour l'insertion dans un prompt."""
    if scraped.get("error"):
        return f"Erreur lors de l'extraction : {scraped['error']}"

    lines = [f"URL : {scraped['url']}", f"Nombre de mots : {scraped['word_count']}"]
    if scraped.get("meta_description"):
        lines.append(f"Meta description : {scraped['meta_description']}")
    lines.append("\nStructure des titres :")
    for h in scraped["headings"]:
        indent = "  " * (int(h["level"][1]) - 1)
        lines.append(f"{indent}{h['level']} : {h['text']}")
    lines.append("\nExtrait du contenu :")
    lines.append(scraped["full_text"][:2000])
    return "\n".join(lines)
