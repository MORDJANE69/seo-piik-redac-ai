import io
from pypdf import PdfReader
from docx import Document


def extract_text(file) -> str:
    """
    Extrait le texte d'un fichier uploadé via Streamlit.
    Supporte PDF, DOCX, TXT, MD.
    """
    name = file.name.lower()
    content = file.read()

    if name.endswith(".pdf"):
        reader = PdfReader(io.BytesIO(content))
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    elif name.endswith(".docx"):
        doc = Document(io.BytesIO(content))
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

    elif name.endswith((".txt", ".md")):
        return content.decode("utf-8", errors="ignore")

    return ""


def build_context(files) -> str:
    """
    Compile tous les documents en un seul bloc de contexte pour les prompts.
    """
    if not files:
        return ""

    sections = []
    for file in files:
        file.seek(0)
        text = extract_text(file).strip()
        if text:
            sections.append(f"--- Document : {file.name} ---\n{text[:3000]}")

    if not sections:
        return ""

    return "=== BASE DE CONNAISSANCE ENTREPRISE ===\n\n" + "\n\n".join(sections)
