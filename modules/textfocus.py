import os
import requests


PERPLEXITY_URL = "https://api.perplexity.ai/chat/completions"

SEMANTIC_PROMPT = """Tu es spécialiste {keyword}, Je veux tous les mots sémantiques autour {keyword} pour mon SEO

Tu vas créer une grille sémantique pour le mot-clé {keyword}

Tu dois te baser sur les critères des outils SEO de sémantique pour construire la grille complète :
1. Analyse Lexicale et Lemmatisation
Les outils commencent par découper le texte en mots (tokenisation).
Ils identifient ensuite la forme de base des mots (lemmatisation) : par exemple, "manger", "mange", "mangeait" sont ramenés à "manger".
2. Reconnaissance des Entités Nommées (NER - Named Entity Recognition)
Certains outils détectent les entités spécifiques (lieux, personnes, entreprises, concepts…).
Exemple : "Apple" → Entreprise, "Paris" → Ville.
3. Analyse des Cooccurrences
Les outils cherchent quels mots apparaissent souvent ensemble dans un corpus donné.
Ex. : "vélo électrique" est souvent associé à "batterie lithium", "assistance électrique", "autonomie".
4. Modèles de Word Embedding (Word2Vec, FastText, BERT)
Ces modèles analysent comment les mots sont liés en fonction de leur contexte.
Exemple :
Word2Vec → Transforme les mots en vecteurs numériques et trouve les plus proches.
BERT → Comprend le contexte grâce à une analyse bi-directionnelle du texte.
5. Construction de Graphe Sémantique
Certains outils construisent un graphe des relations entre les mots-clés pour montrer leurs liens hiérarchiques et conceptuels.
Ex. : "mobilité douce" peut être relié à "vélo", "trottinette", "marche à pied", etc.
6. Recherche des Intentions de Recherche
Les outils classent les mots-clés selon l'intention de l'utilisateur (transactionnelle, informationnelle, navigationnelle).
Exemple : "acheter vélo électrique" → transactionnel, "comment fonctionne un vélo électrique ?" → informationnel.
"""


def get_semantic_grid(keyword: str, lang: str = "fr") -> dict:
    """
    Génère une grille sémantique via Perplexity (remplace TextFocus).
    """
    api_key = os.getenv("PERPLEXITY_KEY")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "sonar-deep-research",
        "messages": [
            {"role": "system", "content": "Tu es un expert SEO. Réponds toujours en français."},
            {"role": "user", "content": SEMANTIC_PROMPT.format(keyword=keyword)},
        ],
        "max_tokens": 4000,
        "temperature": 0.2,
    }
    try:
        response = requests.post(PERPLEXITY_URL, headers=headers, json=payload, timeout=300)
        response.raise_for_status()
        text = response.json()["choices"][0]["message"]["content"]
        return {"success": True, "data": text}
    except Exception as e:
        return {"success": False, "error": str(e), "data": ""}


def format_semantic_for_prompt(semantic_result: dict, max_words: int = 50) -> str:
    """Retourne directement le texte généré par Perplexity."""
    if not semantic_result.get("success"):
        return f"Grille sémantique non disponible : {semantic_result.get('error', 'Erreur')}"
    return semantic_result.get("data", "")
