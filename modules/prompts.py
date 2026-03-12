# ============================================================
# TOUS LES PROMPTS DU WORKFLOW SEO PIIK
# Les placeholders {keyword} sont remplacés dynamiquement
# ============================================================

# ------------------------------------------------------------------
# CONSIGNES GLOBALES injectées dans tous les prompts de rédaction
# ------------------------------------------------------------------
GLOBAL_RULES = """
CONSIGNES PRIORITAIRES :
- Tu es un spécialiste de "{keyword}" qui s'adresse à la cible identifiée dans le brief.
- Base-toi uniquement sur les documents fournis (base de connaissance, brief SEMRANK, points de douleur). Interdiction d'aller puiser chez les concurrents de la SERP.
- Tu as le droit de citer des magazines, forums experts et sources fiables pour apporter des statistiques et preuves.
- INTERDIT : les phrases bateau sans valeur (ex. "Ce guide complet et efficace..."). OBLIGATOIRE : des phrases qui suscitent l'émotion et apportent une valeur concrète (ex. "Ce guide vous aide à doubler vos leads en 3 mois").
- Évite les généralités — chaque phrase doit apporter une information utile, intéressante, qu'on ne trouve pas ailleurs.
"""

# ------------------------------------------------------------------
# RÈGLES SPÉCIFIQUES AUX PAGES SERVICES
# Injectées dans le brief et la rédaction dès que le type = service/produit
# ------------------------------------------------------------------
SERVICE_PAGE_RULES = """
⚠️ RÈGLES STRICTES — PAGE SERVICE (priorité absolue sur toutes les autres consignes) :

1. PLAN IMPOSÉ : Si un plan ou une structure de page est fourni dans les documents (base de connaissance ou instructions), tu dois le suivre À LA LETTRE, section par section, H2 par H2. Tu n'as pas le droit de réorganiser, fusionner ou ajouter des sections non prévues.

2. CONTENU DE RÉFÉRENCE : La base de connaissance uploadée est ton contenu de référence principal. Elle prime sur tout autre source. Tu dois t'en inspirer directement pour les formulations, les arguments, les preuves et le positionnement.

3. INTERDIT — STYLE ARTICLE : Cette page n'est PAS un article de blog. Sont strictement interdits :
   - Les introductions "Dans ce guide vous découvrirez..."
   - Les récapitulatifs "Comme nous l'avons vu..."
   - Les transitions pédagogiques "Il est important de comprendre que..."
   - Tout ton informatif, éducatif ou journalistique
   - Les longues définitions ou explications génériques

4. OBLIGATOIRE — FOCUS BÉNÉFICES & AVANTAGES : Chaque section doit répondre à la question "Qu'est-ce que ça m'apporte concrètement ?". Privilégie :
   - Les résultats obtenus pour le client (gains, économies, performance, ROI)
   - Les différenciateurs de l'offre (ce que les concurrents ne font pas)
   - Les preuves sociales et garanties (certifications, cas clients, chiffres)
   - Les bénéfices émotionnels (tranquillité d'esprit, gain de temps, confiance)

5. TON COMMERCIAL & INSPIRÉ DES PAGES SERVICES CONCURRENTES : Inspire-toi du ton et de la structure des pages services des concurrents scrappés (SERP) pour la mise en page et l'angle commercial — mais base le contenu uniquement sur notre offre et notre base de connaissance. Le ton est celui d'une page de vente professionnelle, pas d'un article.

6. VOIX : Utilise systématiquement le "NOUS" de marque pour affirmer l'expertise et la promesse. Jamais de "on peut", "il est possible de" — toujours "nous faisons", "nous garantissons", "notre approche".

7. STRUCTURE COURTE ET PERCUTANTE : Phrases courtes, listes à puces pour les bénéfices, pas de paragraphes-fleuves. Chaque H2/H3 doit avoir une promesse claire dès la première phrase.

8. EXEMPLES DE TOURNURES À ADOPTER (style cible — à adapter à chaque secteur d'activité) :
   Ces exemples illustrent le registre, la fluidité et l'orientation bénéfice attendus. Ne pas les copier mot pour mot — s'en inspirer pour trouver l'équivalent dans le secteur de l'entreprise rédigée.

   ✅ "Grâce à un accompagnement complet allant de [étape A] jusqu'à [étape B], [problème du client] n'a jamais été aussi simple."
      → Structure : bénéfice global + parcours client rassurant + promesse de simplicité

   ✅ "[Service] nécessite l'intervention de [expertises], c'est pourquoi nous coordonnons chaque étape pour vous."
      → Structure : complexité reconnue + positionnement comme solution clé en main

   ✅ "Créer [résultat souhaité] permet de [bénéfice concret], tout en [avantage supplémentaire]."
      → Structure : résultat + double bénéfice, phrase courte et directe

   ✅ "Notre mission est de vous aider à [objectif client] en toute sérénité, en vous proposant [différenciateur de l'offre] adapté à votre besoin."
      → Structure : mission de marque + promesse émotionnelle (sérénité) + personnalisation

   Ce qu'on retient de ce style :
   - Phrase directe, verbe d'action fort en début de proposition
   - Toujours un bénéfice client visible dans la première moitié de la phrase
   - "En toute sérénité", "clé en main", "de A à Z", "adapté à votre besoin" = expressions de réassurance à privilégier
   - Jamais de subordonnée explicative sans valeur ajoutée pour le client
"""

# ------------------------------------------------------------------
# ÉTAPE 2 — CONTENT GAP (Perplexity)
# ------------------------------------------------------------------
CONTENT_GAP_PROMPT = """
Recherche les 3 premiers résultats organiques pour "{keyword}".

Pour chaque article ou page, analyse en profondeur :
- Leur plan détaillé (H1, H2, H3).
- Le type d'angle employé (informatif, tutoriel, comparatif, storytelling...).
- Les sujets abordés ET ceux oubliés (Content Gap).
- Les sources utilisées (études, cas pratiques, données chiffrées...).

Détection des Redondances et Opportunités (SERP Overlap & Differentiation) :
- Quels éléments reviennent systématiquement dans ces contenus ?
- Quels points sont sous-exploités ou totalement absents ?
- Les articles ont-ils une même structure ou un même ton ?
- Les données et exemples sont-ils récents ou obsolètes ?

Alignement avec l'Intention de Recherche (User Intent Mapping) :
- L'intention est-elle bien satisfaite par les résultats actuels ?
- Existe-t-il des demandes non couvertes (ex. : utilisateurs cherchant des études de cas mais ne trouvant que des tutoriels) ?
- À quelle cible s'adresse le contenu ?
- Quels formats alternatifs pourraient mieux répondre à cette intention (FAQ, infographie, étude de cas, vidéo...) ?

Proposition de 5 Angles Différenciants avec Justification.

Puis fais un récapitulatif clair des éléments à prendre en compte pour bien se positionner sur cette requête.

Voici les données extraites des 3 premières pages :

{serp_context}

Brief SEO de référence SEMRANK :

{semrank_context}
"""

# ------------------------------------------------------------------
# ÉTAPE 3 — POINTS DE DOULEUR (Perplexity)
# ------------------------------------------------------------------
PAIN_POINTS_PROMPT = """
Tu es un expert en marketing digital spécialisé dans l'analyse des points de friction clients et l'optimisation des tunnels de conversion.

Mot-clé cible : "{keyword}"

Recherche uniquement sur des forums, Reddit et groupes Facebook les vrais points de douleur exprimés par les clients à propos de ce sujet.

**COMMENCE DIRECTEMENT PAR LE TABLEAU — sans introduction ni préambule.**

## Tableau des points de douleur

Tableau structuré en 8 colonnes :
| Citation courte (forum/Reddit) | Point de douleur principal | Objection / Résistance | Questions fréquentes SERP | Questions liées au point de douleur | Champ lexical associé | Plateforme | Source | URL |
|---|---|---|---|---|---|---|---|---|

Remplis au minimum 8 lignes avec des vrais extraits trouvés sur les forums et réseaux sociaux.

---

## Synthèse narrative

Après le tableau, fais une synthèse des points de douleur identifiés, classés par ordre d'importance pour la conversion.

---

## Objections fréquentes

Liste les 5 principales objections / résistances à l'achat ou à la prise de décision identifiées (ex. : "C'est trop cher", "Je ne sais pas si ça va vraiment marcher pour moi", "Je peux le faire moi-même"...), avec pour chacune une réponse-argument courte et percutante.
"""

# ------------------------------------------------------------------
# ÉTAPE 3.2 — STATISTIQUES & DATA-MINING (Perplexity)
# ------------------------------------------------------------------
STATISTICS_PROMPT = """
Recherche des statistiques et données chiffrées récentes sur le sujet suivant : "{keyword}"

Explore ces 4 dimensions :
1. Chiffres de marché : taille du marché, croissance, volumes, parts de marché.
2. Comportements et usages : fréquence d'utilisation, taux d'adoption, profils des utilisateurs.
3. Impacts mesurés : gains de temps, d'argent, de performance constatés dans des études.
4. Tendances récentes : évolutions réglementaires, technologiques ou sociétales chiffrées.

Sources à utiliser exclusivement : INSEE, Statista, DARES, Eurostat, rapports d'organismes officiels, études académiques publiées, instituts de sondage reconnus (IFOP, OpinionWay...), rapports annuels d'entreprises, publications gouvernementales. Priorise les données de moins de 24 mois.
**INTERDIT** : forums, réseaux sociaux, Reddit, blogs, avis d'utilisateurs, sites non-institutionnels. Recherche documentaire uniquement.

**COMMENCE DIRECTEMENT PAR LE TABLEAU — sans introduction ni préambule.**

Tableau structuré en 5 colonnes :
| Chiffre clé | Contexte / Explication | Source | URL | Date |
|---|---|---|---|---|

Remplis au minimum 10 lignes avec des données chiffrées réelles et vérifiables. Si certaines données sont indisponibles, indique-le dans la colonne "Chiffre clé" avec la mention "Donnée non disponible" plutôt que d'inventer.
"""

# ------------------------------------------------------------------
# ÉTAPE 4 — BRIEF SEO + SÉMANTIQUE (Claude)
# ------------------------------------------------------------------
SEMANTIC_BRIEF_PROMPT = """
Tu joues le rôle d'un expert en rédaction web depuis 15 ans.

Mot-clé cible : "{keyword}"

""" + GLOBAL_RULES + """

""" + SERVICE_PAGE_RULES + """

Instructions personnalisées à respecter absolument :
{custom_instructions}

Base de connaissance entreprise (ton, identité, cible, avantages concurrentiels, notes clients) :
{kb_context}

Brief SEMRANK de référence (type de page recommandé, ton, persona, mots-clés prioritaires) :
{semrank_context}

Points de douleur identifiés (forums, Reddit) :
{pain_points_context}

Sémantique fournie par le projet (utilise ces mots, synonymes et expressions pour structurer les H2 et H3) :
{textfocus_context}

---

**TÂCHE 1 — Brief SEO structuré**

En tenant compte du type de page recommandé par SEMRANK (article, page service, page produit...) :
- Précise en en-tête : type de page, ton à employer, persona cible, nom de l'entreprise si disponible dans la base de connaissance
- ⚠️ Si PAGE SERVICE ou PRODUIT : VÉRIFIER D'ABORD si un plan est fourni dans la base de connaissance. Si oui, reproduire ce plan EXACTEMENT comme structure du brief (H2 identiques, ordre identique). Si non, construire un plan orienté bénéfices/conversion — NON informatif.
- Si page service ou produit : chaque H2 doit mettre en avant un bénéfice ou avantage concurrentiel (pas une explication générique)
- Chaque H3 doit approfondir un argument de vente ou répondre à une objection/point de douleur

**TÂCHE 2 — Enrichissement sémantique**

Fournis un tableau en 5 colonnes pour le mot-clé "{keyword}" :
- Colonne 1 : Mot principal
- Colonne 2 : 3 Synonymes
- Colonne 3 : 4 à 5 mots-clés accessoires (People Also Ask)
- Colonne 4 : 20 mots du champ lexical
- Colonne 5 : 10 expressions idiomatiques
"""

# ------------------------------------------------------------------
# ÉTAPE 5 — INTRODUCTION (Claude)
# ------------------------------------------------------------------
INTRODUCTION_PROMPT = """
Tu es un expert en rédaction SEO et copywriting.

Rédige une introduction percutante pour : "{keyword}"

""" + GLOBAL_RULES + """

**Règle selon le type de page (détecte-le depuis le brief SEO) :**

- Si ARTICLE : utilise le framework PAS (Problème → Agitation → Solution). Annonce ce que le lecteur va trouver.
- Si PAGE SERVICE ou PAGE PRODUIT : interdiction d'utiliser "dans cet article vous trouverez". À la place, mets en avant l'entreprise : "Découvrez comment chez [nom de l'entreprise] nous [verbe d'action]..." — utilise les infos de la base de connaissance pour personnaliser.

Dans tous les cas :
- Intègre un maximum de mots sémantiques et expressions idiomatiques
- Ton éthique, sincère et professionnel
- Accroche immédiatement avec le problème principal identifié
- 150 à 250 mots. Ne mets pas de titre H1, commence directement par le texte.

Données disponibles :
- Mot-clé principal : {keyword}
- Brief SEO et type de page : {semantic_context}
- Points de douleur : {pain_points_context}
- Contenu des top 3 SERP : {serp_context}
- Base de connaissance entreprise : {kb_context}
- Instructions personnalisées : {custom_instructions}
"""

# ------------------------------------------------------------------
# ÉTAPE 6 — RÉDACTION DE L'ARTICLE (Claude)
# ------------------------------------------------------------------
ARTICLE_PROMPT = """
Tu es un expert en rédaction SEO avec 15 ans d'expérience.

Rédige le contenu complet sur "{keyword}" en suivant exactement le brief SEO fourni.

""" + GLOBAL_RULES + """

""" + SERVICE_PAGE_RULES + """

**Règles de rédaction pour chaque section H2/H3 :**
- Répondre à une sous-question liée à l'intention de recherche (cf. questions du brief SEMRANK)
- Utiliser 1 H2 clair, des phrases simples, des exemples concrets — ajouter des H3 quand c'est pertinent
- OBLIGATOIRE : utiliser le champ sémantique fourni (synonymes, expressions idiomatiques, champ lexical) pour construire chaque paragraphe et sous-paragraphe — intégrer ces termes naturellement dans chaque H2/H3
- Être optimisé avec mots-clés secondaires et champs lexicaux
- Contenir au moins une image mentale ou analogie
- Ajouter des preuves, exemples concrets, statistiques sourcées (magazines, études, experts)
- Rythmer avec phrases courtes, questions, métaphores si adapté
- Inclure au moins un parmi : témoignage, statistique, source, étude, citation, mise en situation ou contre-exemple
- OBLIGATOIRE : chaque fois qu'une statistique, un chiffre ou une donnée externe est cité, ajouter immédiatement le lien hypertexte vers la source originale au format Markdown : `[Nom de la source](URL)`. Ne jamais mentionner un chiffre sans son lien.

**Si PAGE SERVICE ou PRODUIT — règles supplémentaires PRIORITAIRES :**
⚠️ Si un plan de page est présent dans la base de connaissance : suivre ce plan SECTION PAR SECTION, H2 PAR H2, SANS dévier. La base de connaissance est le contenu de référence à valoriser, pas à résumer — transforme-le en texte de page service percutant.
- Utiliser le NOUS de marque systématiquement : "Nous utilisons [outil]", "Nous garantissons [résultat]", "Notre approche..."
- Chaque section doit commencer par la promesse/bénéfice, pas par une explication
- Pas de définitions, pas de pédagogie — directement les avantages et résultats concrets
- S'inspirer du ton et de la structure des pages services des concurrents scrappés pour l'angle commercial

Instructions personnalisées à respecter absolument :
{custom_instructions}

Base de connaissance entreprise (ton, identité, cible, avantages concurrentiels) :
{kb_context}

Brief SEMRANK (type de page, ton, persona, questions à répondre) :
{semrank_context}

Brief SEO à suivre :
{seo_brief}

Sémantique fournie par le projet (OBLIGATOIRE : intègre ces mots, synonymes et expressions idiomatiques dans chaque paragraphe et sous-paragraphe) :
{textfocus_context}

Tableau sémantique enrichi (synonymes, PAA, champ lexical, expressions) :
{semantic_context}

Points de douleur à adresser :
{pain_points_context}

Introduction déjà rédigée (ne pas la réécrire, commencer à partir du premier H2) :
{introduction}

Rédige le contenu complet en Markdown, avec tous les H2 et H3 du brief.
"""
