# SEO PIIK — Installation locale

## Prérequis

- Python 3.10 ou supérieur → https://www.python.org/downloads/
- Un terminal (Terminal sur Mac, PowerShell ou CMD sur Windows)

---

## Étapes d'installation

### 1. Dézipper le dossier

Décompresse le fichier ZIP à l'endroit de ton choix.

### 2. Ouvrir un terminal dans le dossier

Sur Mac : clic droit sur le dossier → "Nouveau terminal au dossier"
Sur Windows : ouvre PowerShell, puis `cd "chemin/vers/le/dossier"`

### 3. Créer un environnement virtuel (recommandé)

```bash
python -m venv venv
```

Activer l'environnement :
- **Mac/Linux** : `source venv/bin/activate`
- **Windows** : `venv\Scripts\activate`

### 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 5. Configurer les clés API

Copie le fichier `.env.example` et renomme-le `.env` :

```bash
cp .env.example .env
```

Ouvre `.env` avec un éditeur de texte et renseigne tes clés API :

```
SERPAPI_KEY=ta_clé_serpapi
SEMRANK_KEY=ta_clé_semrank
PERPLEXITY_KEY=ta_clé_perplexity
ANTHROPIC_KEY=ta_clé_anthropic
```

**Où obtenir les clés :**
- SerpAPI → https://serpapi.com
- SEMRANK → https://semrank.io
- Perplexity → https://www.perplexity.ai/settings/api
- Anthropic → https://console.anthropic.com

### 6. Lancer l'application

```bash
streamlit run app.py
```

L'application s'ouvre automatiquement dans ton navigateur sur `http://localhost:8501`

---

## En cas de problème

- Vérifie que Python est bien installé : `python --version`
- Vérifie que toutes les clés API dans `.env` sont correctes
- Assure-toi que l'environnement virtuel est bien activé avant de lancer
