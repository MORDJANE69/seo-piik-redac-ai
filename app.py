import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

# Compatibilité Streamlit Cloud : injecte les secrets comme variables d'env
for _k, _v in st.secrets.items():
    if isinstance(_v, str):
        os.environ.setdefault(_k, _v)

from modules import serp, scraper, semrank, perplexity, claude_ai, export, knowledge_base

# ─────────────────────────────────────────────
# Configuration de la page
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SEO PIIK — Générateur de contenu",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.step-header { font-size: 1.1rem; font-weight: 700; color: #1a1a2e; margin-bottom: 0.3rem; }
.step-done { color: #28a745; }
.step-running { color: #fd7e14; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Initialisation du session state
# ─────────────────────────────────────────────
for key in [
    "serp_results", "scraped_data", "semrank_brief",
    "content_gap", "pain_points", "statistics",
    "seo_brief", "introduction", "article", "done", "kb_context",
]:
    if key not in st.session_state:
        st.session_state[key] = None

# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.image("https://www.seo-piik.com/wp-content/uploads/2023/01/logo-seo-piik.png", width=160)
    st.title("SEO PIIK")
    st.markdown("**Générateur de contenu SEO automatisé**")
    st.divider()

    keyword = st.text_input(
        "Mot-clé principal",
        placeholder="ex : consultant SEO freelance",
        help="Le mot-clé sur lequel tu veux te positionner",
    )

    custom_instructions = st.text_area(
        "Instructions personnalisées (optionnel)",
        placeholder="Ex : Adopte un ton chaleureux et proche. Mets en avant l'expérience locale. Évite le jargon technique...",
        height=100,
        help="Ces instructions seront appliquées lors de la rédaction du brief et de l'article.",
    )

    st.divider()
    st.markdown("**🧠 Sémantique du projet**")
    st.caption("Colle ici la grille sémantique fournie pour ce projet (champ lexical, synonymes, expressions idiomatiques...). Elle sera utilisée pour construire les paragraphes et sous-paragraphes.")
    semantic_input = st.text_area(
        "Sémantique",
        placeholder="Ex : vélo électrique, e-bike, mobilité douce, assistance électrique, batterie lithium, autonomie, recharge...",
        height=120,
        label_visibility="collapsed",
        help="Fournis la sémantique ici — elle remplace l'appel Perplexity.",
    )

    col1, col2 = st.columns(2)
    with col1:
        lang = st.selectbox("Langue", ["fr", "en"], index=0)
    with col2:
        country = st.selectbox("Pays", ["fr", "be", "ch", "ca", "us"], index=0)

    st.divider()

    # ── Clés API : saisie manuelle si pas définies en secrets ──
    st.markdown("**🔑 Clés API**")

    def _get(env_key, label, session_key):
        env_val = os.getenv(env_key, "")
        if env_val:
            return env_val
        if session_key not in st.session_state:
            st.session_state[session_key] = ""
        val = st.text_input(label, value=st.session_state[session_key], type="password", key=session_key + "_input")
        st.session_state[session_key] = val
        if val:
            os.environ[env_key] = val
        return val

    _get("SERPAPI_KEY",   "SerpAPI Key",   "_serpapi")
    _get("SEMRANK_KEY",   "SEMRANK Key",   "_semrank")
    _get("PERPLEXITY_KEY","Perplexity Key","_perplexity")
    _get("ANTHROPIC_KEY", "Anthropic Key", "_anthropic")

    keys = {
        "SerpAPI":    os.getenv("SERPAPI_KEY"),
        "SEMRANK":    os.getenv("SEMRANK_KEY"),
        "Perplexity": os.getenv("PERPLEXITY_KEY"),
        "Anthropic":  os.getenv("ANTHROPIC_KEY"),
    }
    all_ok = all(keys.values())
    if all_ok:
        st.success("Toutes les clés API sont configurées ✅")
    else:
        st.caption("Entre tes clés API ci-dessus pour démarrer.")

    st.divider()
    st.markdown("**📚 Base de connaissance**")
    st.caption("Ajoute des documents sur ton entreprise : ton, identité, cible, avantages concurrentiels, notes clients, articles de référence...")
    uploaded_files = st.file_uploader(
        "Importer des documents",
        type=["pdf", "docx", "txt", "md"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )
    if uploaded_files:
        kb = knowledge_base.build_context(uploaded_files)
        st.session_state.kb_context = kb
        st.success(f"{len(uploaded_files)} document(s) chargé(s) ✅")
    elif st.session_state.kb_context is None:
        st.session_state.kb_context = ""

    st.divider()
    run = st.button(
        "🚀 Lancer l'analyse complète",
        type="primary",
        disabled=not (keyword and all_ok),
        use_container_width=True,
    )

    if st.session_state.done:
        st.success("✅ Analyse terminée !")

# ─────────────────────────────────────────────
# Titre principal
# ─────────────────────────────────────────────
st.title("🚀 SEO PIIK — Générateur de contenu automatisé")
if not keyword:
    st.info("👈 Renseigne ton mot-clé dans la barre latérale puis clique sur Lancer.")
    st.stop()

# ─────────────────────────────────────────────
# WORKFLOW PRINCIPAL
# ─────────────────────────────────────────────
if run:
    st.session_state.done = False

    # ── ÉTAPE 1 : SERP ──────────────────────────────────────────────
    with st.status("📊 Étape 1 — Récupération des 3 premiers résultats Google...", expanded=True) as status:
        try:
            results = serp.get_top_results(keyword, num=3, lang=lang, country=country)
            st.session_state.serp_results = results
            for r in results:
                st.markdown(f"**#{r['position']} — {r['title']}**  \n🔗 {r['url']}")
            status.update(label=f"✅ Étape 1 — {len(results)} résultats récupérés", state="complete")
        except Exception as e:
            status.update(label=f"❌ Étape 1 — Erreur SerpAPI : {e}", state="error")
            st.stop()

    # ── ÉTAPE 1b : Scraping des pages ───────────────────────────────
    with st.status("🔍 Extraction du contenu des 3 pages...", expanded=False) as status:
        scraped = []
        for r in st.session_state.serp_results:
            data = scraper.extract_content(r["url"])
            scraped.append(data)
        st.session_state.scraped_data = scraped
        status.update(label="✅ Contenu extrait des 3 pages", state="complete")

    # ── ÉTAPE 1c : SEMRANK ──────────────────────────────────────────
    with st.status("📋 Récupération du brief SEMRANK...", expanded=False) as status:
        brief = semrank.get_seo_brief(keyword, lang=lang)
        st.session_state.semrank_brief = brief
        if brief.get("success"):
            status.update(label="✅ Brief SEMRANK récupéré", state="complete")
        else:
            status.update(
                label=f"⚠️ SEMRANK : {brief.get('error', 'Endpoint inconnu')}",
                state="error",
            )

    # Préparer les contextes pour les prompts
    serp_context = ""
    for i, (r, s) in enumerate(zip(st.session_state.serp_results, st.session_state.scraped_data), 1):
        serp_context += f"\n=== Résultat {i} ===\n"
        serp_context += scraper.format_headings_for_prompt(s)

    semrank_context = semrank.format_brief_for_prompt(st.session_state.semrank_brief)
    tf_context = semantic_input or ""

    # ── ÉTAPE 2 : CONTENT GAP ───────────────────────────────────────
    with st.status("🔎 Étape 2 — Analyse Content Gap (Perplexity)...", expanded=True) as status:
        try:
            gap = perplexity.run_content_gap(keyword, serp_context, semrank_context)
            st.session_state.content_gap = gap
            status.update(label="✅ Étape 2 — Content Gap analysé", state="complete")
        except Exception as e:
            status.update(label=f"❌ Étape 2 — Erreur : {e}", state="error")
            st.stop()

    # ── ÉTAPE 3 : POINTS DE DOULEUR ─────────────────────────────────
    with st.status("💡 Étape 3 — Points de douleur (Perplexity)...", expanded=True) as status:
        try:
            pain = perplexity.run_pain_points(keyword)
            st.session_state.pain_points = pain
            status.update(label="✅ Étape 3 — Points de douleur identifiés", state="complete")
        except Exception as e:
            status.update(label=f"❌ Étape 3 — Erreur : {e}", state="error")
            st.stop()

    # ── ÉTAPE 3.2 : STATISTIQUES & DATA-MINING ──────────────────────
    with st.status("📈 Étape 3.2 — Statistiques & data-mining (Perplexity)...", expanded=True) as status:
        try:
            stats = perplexity.run_statistics(keyword)
            st.session_state.statistics = stats
            status.update(label="✅ Étape 3.2 — Statistiques collectées", state="complete")
        except Exception as e:
            status.update(label=f"❌ Étape 3.2 — Erreur : {e}", state="error")
            st.stop()

    # ── ÉTAPE 4 : BRIEF SEO + SÉMANTIQUE ────────────────────────────
    with st.status("📄 Étape 4 — Brief SEO + enrichissement sémantique (Claude)...", expanded=True) as status:
        try:
            brief_sem = claude_ai.write_seo_brief(
                keyword=keyword,
                textfocus_context=tf_context,
                pain_points_context=st.session_state.pain_points,
                semrank_context=semrank_context,
                kb_context=st.session_state.kb_context or "",
                custom_instructions=custom_instructions,
            )
            st.session_state.seo_brief = brief_sem
            status.update(label="✅ Étape 4 — Brief SEO et sémantique générés", state="complete")
        except Exception as e:
            status.update(label=f"❌ Étape 4 — Erreur Claude : {e}", state="error")
            st.stop()

    # ── ÉTAPE 5 : INTRODUCTION (CLAUDE) ─────────────────────────────
    with st.status("✍️ Étape 5 — Rédaction de l'introduction (Claude)...", expanded=True) as status:
        try:
            intro = claude_ai.write_introduction(
                keyword=keyword,
                semantic_context=st.session_state.seo_brief,
                pain_points_context=st.session_state.pain_points,
                serp_context=serp_context,
                kb_context=st.session_state.kb_context or "",
                custom_instructions=custom_instructions,
            )
            st.session_state.introduction = intro
            status.update(label="✅ Étape 5 — Introduction rédigée", state="complete")
        except Exception as e:
            status.update(label=f"❌ Étape 5 — Erreur Claude : {e}", state="error")
            st.stop()

    # ── ÉTAPE 6 : ARTICLE COMPLET (CLAUDE) ──────────────────────────
    with st.status("📝 Étape 6 — Rédaction de l'article complet (Claude)...", expanded=True) as status:
        try:
            article = claude_ai.write_article(
                keyword=keyword,
                seo_brief=st.session_state.seo_brief,
                textfocus_context=tf_context,
                semantic_context=st.session_state.seo_brief,
                pain_points_context=st.session_state.pain_points,
                introduction=st.session_state.introduction,
                semrank_context=semrank_context,
                kb_context=st.session_state.kb_context or "",
                custom_instructions=custom_instructions,
            )
            st.session_state.article = article
            status.update(label="✅ Étape 6 — Article complet rédigé", state="complete")
        except Exception as e:
            status.update(label=f"❌ Étape 6 — Erreur Claude : {e}", state="error")
            st.stop()

    st.session_state.done = True
    st.balloons()

# ─────────────────────────────────────────────
# AFFICHAGE DES RÉSULTATS (si analyse terminée)
# ─────────────────────────────────────────────
if st.session_state.done and st.session_state.article:

    st.divider()
    st.header("📊 Résultats de l'analyse")

    tab1, tab2, tab3, tab3b, tab4, tab5, tab6 = st.tabs([
        "🔍 SERP & Contenu",
        "🔎 Content Gap",
        "💡 Points de douleur",
        "📈 Statistiques",
        "🧠 Grille sémantique",
        "📄 Brief SEO + Sémantique",
        "✍️ Article complet",
    ])

    with tab1:
        st.subheader("Top 3 résultats Google")
        for i, (r, s) in enumerate(zip(
            st.session_state.serp_results,
            st.session_state.scraped_data
        ), 1):
            with st.expander(f"#{i} — {r['title']}", expanded=(i == 1)):
                st.markdown(f"**URL :** {r['url']}")
                st.markdown(f"**Snippet :** {r['snippet']}")
                st.markdown(f"**Mots :** {s.get('word_count', '?')}")
                st.markdown("**Structure :**")
                for h in s.get("headings", []):
                    indent = "&nbsp;" * (int(h["level"][1]) - 1) * 4
                    st.markdown(
                        f"{indent}**{h['level']}** — {h['text']}",
                        unsafe_allow_html=True,
                    )

    with tab2:
        st.subheader("Analyse Content Gap")
        st.markdown(st.session_state.content_gap)

    with tab3:
        st.subheader("Points de douleur clients")
        st.markdown(st.session_state.pain_points)

    with tab3b:
        st.subheader("Statistiques & Data-mining")
        st.caption("Données chiffrées collectées depuis des sources de haute autorité (INSEE, Statista, études académiques, rapports annuels).")
        st.markdown(st.session_state.statistics)

    with tab4:
        st.subheader("Sémantique du projet")
        if semantic_input:
            st.markdown(semantic_input)
        else:
            st.info("Aucune sémantique fournie. Colle ta grille sémantique dans la barre latérale pour l'utiliser.")

    with tab5:
        st.subheader("Brief SEO & enrichissement sémantique")
        st.markdown(st.session_state.seo_brief)

    with tab6:
        st.subheader("Article complet")
        st.markdown("### Introduction")
        st.markdown(st.session_state.introduction)
        st.divider()
        st.markdown(st.session_state.article)

    # ── EXPORT ──────────────────────────────────────────────────────
    st.divider()
    st.header("📤 Exporter")

    full_content = export.build_full_export(
        keyword=keyword,
        content_gap=st.session_state.content_gap,
        pain_points=st.session_state.pain_points,
        statistics=st.session_state.statistics,
        seo_brief=st.session_state.seo_brief,
        introduction=st.session_state.introduction,
        article=st.session_state.article,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.download_button(
            label="📥 Télécharger en Markdown",
            data=full_content.encode("utf-8"),
            file_name=f"seo_{keyword.replace(' ', '_')}.md",
            mime="text/markdown",
            use_container_width=True,
        )

    with col2:
        try:
            docx_path = export.export_word(full_content, keyword)
            with open(docx_path, "rb") as f:
                st.download_button(
                    label="📥 Télécharger en Word",
                    data=f.read(),
                    file_name=f"seo_{keyword.replace(' ', '_')}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True,
                )
        except Exception as e:
            st.error(f"Erreur export Word : {e}")

    with col3:
        # Sauvegarde locale dans outputs/
        try:
            md_path = export.export_markdown(full_content, keyword)
            st.success(f"Fichiers sauvegardés dans `/outputs/`")
        except Exception as e:
            st.warning(f"Sauvegarde locale : {e}")
