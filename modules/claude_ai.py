import os
import anthropic


def _get_client() -> anthropic.Anthropic:
    return anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_KEY"))


def write_introduction(
    keyword: str,
    semantic_context: str,
    pain_points_context: str,
    serp_context: str,
    kb_context: str = "",
    custom_instructions: str = "",
) -> str:
    """
    Étape 5 — Rédige l'introduction avec le framework PAS.
    Claude est utilisé uniquement pour la rédaction.
    """
    from .prompts import INTRODUCTION_PROMPT
    prompt = INTRODUCTION_PROMPT.format(
        keyword=keyword,
        semantic_context=semantic_context,
        pain_points_context=pain_points_context,
        serp_context=serp_context,
        kb_context=kb_context,
        custom_instructions=custom_instructions,
    )
    return _call_claude(prompt)


def write_seo_brief(
    keyword: str,
    textfocus_context: str,
    pain_points_context: str,
    semrank_context: str = "",
    kb_context: str = "",
    custom_instructions: str = "",
) -> str:
    """
    Étape 4 — Génère le brief SEO structuré + tableau sémantique enrichi.
    """
    from .prompts import SEMANTIC_BRIEF_PROMPT
    prompt = SEMANTIC_BRIEF_PROMPT.format(
        keyword=keyword,
        textfocus_context=textfocus_context,
        pain_points_context=pain_points_context,
        semrank_context=semrank_context,
        kb_context=kb_context,
        custom_instructions=custom_instructions,
    )
    return _call_claude(prompt, max_tokens=8000)


def write_article(
    keyword: str,
    seo_brief: str,
    textfocus_context: str,
    semantic_context: str,
    pain_points_context: str,
    introduction: str,
    semrank_context: str = "",
    kb_context: str = "",
    custom_instructions: str = "",
) -> str:
    """
    Étape 6 — Rédige l'article complet section par section selon le brief.
    Claude est utilisé uniquement pour la rédaction.
    """
    from .prompts import ARTICLE_PROMPT
    prompt = ARTICLE_PROMPT.format(
        keyword=keyword,
        seo_brief=seo_brief,
        textfocus_context=textfocus_context,
        semantic_context=semantic_context,
        pain_points_context=pain_points_context,
        introduction=introduction,
        semrank_context=semrank_context,
        kb_context=kb_context,
        custom_instructions=custom_instructions,
    )
    return _call_claude(prompt, max_tokens=16000)


def _call_claude(prompt: str, max_tokens: int = 4096) -> str:
    """Appel générique à Claude Sonnet pour la rédaction."""
    client = _get_client()
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=max_tokens,
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    return message.content[0].text
