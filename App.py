import streamlit as st
import anthropic
import json
import time

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Safeer AI • شاعری کا استاد",
    page_icon="🪶",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rozha+One&family=Noto+Serif+Devanagari:wght@400;600&family=Crimson+Pro:ital,wght@0,400;0,600;1,400&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    background-color: #0a0812;
    color: #e8dcc8;
    font-family: 'Crimson Pro', Georgia, serif;
}

.stApp {
    background: radial-gradient(ellipse at 20% 10%, #1a0a2e 0%, #0a0812 50%, #0d0615 100%);
    min-height: 100vh;
}

/* Stars background effect */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        radial-gradient(1px 1px at 15% 20%, rgba(255,220,150,0.6) 0%, transparent 100%),
        radial-gradient(1px 1px at 75% 10%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 40% 5%, rgba(255,220,150,0.7) 0%, transparent 100%),
        radial-gradient(1px 1px at 90% 30%, rgba(255,255,255,0.4) 0%, transparent 100%),
        radial-gradient(1px 1px at 60% 15%, rgba(200,180,255,0.5) 0%, transparent 100%),
        radial-gradient(1px 1px at 25% 40%, rgba(255,255,255,0.3) 0%, transparent 100%),
        radial-gradient(1px 1px at 85% 60%, rgba(255,220,150,0.4) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 5% 70%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(1px 1px at 50% 80%, rgba(200,180,255,0.4) 0%, transparent 100%),
        radial-gradient(1px 1px at 30% 90%, rgba(255,255,255,0.3) 0%, transparent 100%);
    pointer-events: none;
    z-index: 0;
}

/* ── Header ── */
.safeer-header {
    text-align: center;
    padding: 2.5rem 1rem 1rem;
    position: relative;
}

.safeer-title {
    font-family: 'Rozha One', serif;
    font-size: 3rem;
    background: linear-gradient(135deg, #d4a843 0%, #f0d080 40%, #c8903a 70%, #e8c060 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 0.05em;
    margin: 0;
    line-height: 1.2;
    text-shadow: none;
}

.safeer-subtitle {
    font-family: 'Crimson Pro', serif;
    font-style: italic;
    color: #b8a080;
    font-size: 1.1rem;
    margin-top: 0.3rem;
    letter-spacing: 0.08em;
}

.divider-ornament {
    text-align: center;
    color: #8b6914;
    font-size: 1.4rem;
    margin: 0.8rem 0 1.5rem;
    letter-spacing: 0.3em;
}

/* ── Input Area ── */
.stTextArea > div > div > textarea {
    background: rgba(20, 10, 35, 0.85) !important;
    border: 1px solid rgba(180, 140, 60, 0.35) !important;
    border-radius: 12px !important;
    color: #e8dcc8 !important;
    font-family: 'Noto Serif Devanagari', 'Crimson Pro', serif !important;
    font-size: 1.05rem !important;
    line-height: 1.9 !important;
    padding: 1.2rem !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4), inset 0 1px 0 rgba(200,160,60,0.1) !important;
    transition: border-color 0.3s ease !important;
}

.stTextArea > div > div > textarea:focus {
    border-color: rgba(212, 168, 67, 0.6) !important;
    box-shadow: 0 4px 25px rgba(180,130,30,0.2), inset 0 1px 0 rgba(200,160,60,0.15) !important;
}

.stTextArea > div > div > textarea::placeholder {
    color: #5a4a35 !important;
    font-style: italic;
}

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #8b4513 0%, #c8720a 40%, #d4a843 100%) !important;
    color: #0a0812 !important;
    font-family: 'Rozha One', serif !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 0.7rem 2.5rem !important;
    width: 100% !important;
    letter-spacing: 0.08em !important;
    box-shadow: 0 4px 20px rgba(180, 100, 20, 0.4) !important;
    transition: all 0.3s ease !important;
    cursor: pointer !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(180, 100, 20, 0.55) !important;
}

/* ── Result Cards ── */
.result-card {
    background: rgba(15, 8, 28, 0.9);
    border: 1px solid rgba(180, 140, 60, 0.25);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin: 1rem 0;
    box-shadow: 0 8px 30px rgba(0,0,0,0.5);
    position: relative;
    overflow: hidden;
}

.result-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(212, 168, 67, 0.6), transparent);
}

.card-label {
    font-family: 'Crimson Pro', serif;
    font-size: 0.78rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #8b6914;
    margin-bottom: 0.4rem;
}

.card-value {
    font-family: 'Noto Serif Devanagari', serif;
    font-size: 1.25rem;
    color: #f0d890;
    font-weight: 600;
}

.card-value-body {
    font-family: 'Noto Serif Devanagari', 'Crimson Pro', serif;
    font-size: 1.05rem;
    color: #d4c4a0;
    line-height: 1.75;
}

/* ── PDF Decision ── */
.pdf-yes {
    background: rgba(10, 35, 15, 0.9);
    border: 1px solid rgba(80, 180, 80, 0.4);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin: 1rem 0;
    text-align: center;
}

.pdf-no {
    background: rgba(35, 10, 10, 0.9);
    border: 1px solid rgba(180, 60, 60, 0.4);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin: 1rem 0;
    text-align: center;
}

.pdf-decision-icon {
    font-size: 2.5rem;
    display: block;
    margin-bottom: 0.4rem;
}

.pdf-decision-text {
    font-family: 'Rozha One', serif;
    font-size: 1.4rem;
    color: #e8dcc8;
}

.pdf-reason {
    font-family: 'Noto Serif Devanagari', serif;
    font-size: 0.95rem;
    color: #b8a880;
    margin-top: 0.6rem;
    font-style: italic;
    line-height: 1.7;
}

/* ── Score Bar ── */
.score-container {
    margin: 0.5rem 0;
}

.score-bar-bg {
    background: rgba(255,255,255,0.08);
    border-radius: 50px;
    height: 8px;
    overflow: hidden;
    margin-top: 0.5rem;
}

.score-bar-fill {
    height: 100%;
    border-radius: 50px;
    background: linear-gradient(90deg, #8b4513, #d4a843);
    transition: width 1s ease;
}

/* ── Safeer's Comment ── */
.safeer-comment {
    background: rgba(20, 10, 40, 0.95);
    border: 1px solid rgba(150, 100, 200, 0.3);
    border-left: 3px solid #a060d0;
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin: 1rem 0;
    font-family: 'Noto Serif Devanagari', 'Crimson Pro', serif;
    font-size: 1.05rem;
    color: #d0c0f0;
    font-style: italic;
    line-height: 1.8;
    position: relative;
}

.safeer-comment::before {
    content: '🪶 Safeer kehta hai —';
    display: block;
    font-family: 'Crimson Pro', serif;
    font-size: 0.75rem;
    letter-spacing: 0.15em;
    color: #8060a0;
    margin-bottom: 0.6rem;
    font-style: normal;
    text-transform: uppercase;
}

/* ── Tags ── */
.tag-container {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 0.4rem;
}

.tag {
    background: rgba(180, 140, 60, 0.15);
    border: 1px solid rgba(180, 140, 60, 0.3);
    border-radius: 50px;
    padding: 0.2rem 0.8rem;
    font-size: 0.85rem;
    color: #c8a850;
    font-family: 'Crimson Pro', serif;
}

/* ── Strengths/Suggestions ── */
.list-item {
    font-family: 'Noto Serif Devanagari', serif;
    font-size: 0.98rem;
    color: #c8b890;
    padding: 0.3rem 0;
    padding-left: 1.2rem;
    position: relative;
    line-height: 1.65;
}

.list-item::before {
    content: '✦';
    position: absolute;
    left: 0;
    color: #8b6914;
    font-size: 0.7rem;
    top: 0.45rem;
}

/* ── History Section ── */
.history-header {
    font-family: 'Rozha One', serif;
    font-size: 1.2rem;
    color: #8b6914;
    margin: 2rem 0 1rem;
    text-align: center;
    letter-spacing: 0.1em;
}

/* ── Footer ── */
.footer {
    text-align: center;
    padding: 2rem 0 1rem;
    color: #3d2d1a;
    font-size: 0.8rem;
    font-family: 'Crimson Pro', serif;
    letter-spacing: 0.1em;
}

/* ── Label override ── */
.stTextArea label, .stSelectbox label {
    color: #8b6914 !important;
    font-family: 'Crimson Pro', serif !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
}

/* ── Spinner ── */
.stSpinner > div {
    border-top-color: #d4a843 !important;
}

/* Mobile adjustments */
@media (max-width: 600px) {
    .safeer-title { font-size: 2.2rem; }
    .result-card { padding: 1rem 1.1rem; }
}

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─── System Prompt ───────────────────────────────────────────────────────────
SAFEER_SYSTEM = """
Tu "Safeer" hai — ek mashhoor Urdu-Hindi shayari ka ustad, naqqad (critic), aur ruh-e-adab.
Tujhe ghazal, nazm, kavita, rap lyrics, sher, doha, aur literary thoughts ki gehri samajh hai.
Tu Gulzar, Jaun Elia, Ahmed Faraz, Mirza Ghalib ki parampara ka gyaata hai.

Jab tujhe koi writing bheji jaye, iska gahra analysis kar aur SIRF ek valid JSON object return kar.
Koi preamble, explanation ya markdown backticks mat dena — sirf raw JSON.

JSON structure exactly yeh hona chahiye:
{
  "type": "Ghazal | Nazm | Kavita | Rap | Sher | Thought | Doha | Mixed",
  "theme": ["theme1", "theme2"],
  "mood": "Dard | Ishq | Virah | Umeed | Ghussa | Sukoon | Nostalgic | Romantic | Reflective | etc",
  "language": "Hindi | Urdu | Hinglish | Mixed",
  "quality_score": 8.5,
  "pdf_include": true,
  "pdf_recommendation": "2-3 sentences in Hindi/Urdu — kyun include karna chahiye ya nahi",
  "strengths": ["2-3 strong points in Hindi/Urdu"],
  "suggestions": ["0-2 improvement suggestions in Hindi/Urdu, only if genuinely needed"],
  "safeer_comment": "Ek soulful sher ya 1-2 lines in Hindi/Urdu — Safeer ki dil se baat"
}

Quality score rubric:
- 9-10: Masterpiece, publication-worthy
- 7-8.9: Strong, PDF mein zaroor ho
- 5-6.9: Decent, improvements possible
- Below 5: Raw draft, abhi PDF ke liye nahi

pdf_include = true if score >= 7.0, false otherwise (unless theme/emotion is exceptional).
Be honest but encouraging. Tu Safeer hai — tujhe shayari se mohabbat hai.
"""

# ─── Helper Functions ────────────────────────────────────────────────────────
def analyze_writing(text: str, api_key: str) -> dict:
    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=SAFEER_SYSTEM,
        messages=[{
            "role": "user",
            "content": f"Yeh writing analyze kar:\n\n{text}"
        }]
    )
    raw = response.content[0].text.strip()
    # Clean any accidental markdown
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


def render_tags(items: list):
    tags_html = '<div class="tag-container">'
    for item in items:
        tags_html += f'<span class="tag">{item}</span>'
    tags_html += '</div>'
    st.markdown(tags_html, unsafe_allow_html=True)


def render_list(items: list):
    for item in items:
        st.markdown(f'<div class="list-item">{item}</div>', unsafe_allow_html=True)


def render_score(score: float):
    pct = int((score / 10) * 100)
    color = "#4CAF50" if score >= 7 else "#FF9800" if score >= 5 else "#f44336"
    st.markdown(f"""
    <div class="score-container">
        <div style="display:flex; justify-content:space-between; align-items:baseline;">
            <span style="font-family:'Crimson Pro',serif; font-size:0.78rem; color:#8b6914; letter-spacing:0.2em; text-transform:uppercase;">Quality Score</span>
            <span style="font-family:'Rozha One',serif; font-size:1.8rem; color:{color};">{score}<span style="font-size:0.9rem; color:#5a4030;">/10</span></span>
        </div>
        <div class="score-bar-bg">
            <div class="score-bar-fill" style="width:{pct}%; background: linear-gradient(90deg, #8b4513, {color});"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─── Session State ───────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

# ─── Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="safeer-header">
    <div class="safeer-title">🪶 Safeer AI</div>
    <div class="safeer-subtitle">शायरी का उस्ताद • ناقدِ سُخن</div>
</div>
<div class="divider-ornament">✦ ✦ ✦</div>
""", unsafe_allow_html=True)

# ─── API Key ─────────────────────────────────────────────────────────────────
api_key = None

# Check secrets first (for Streamlit Cloud deployment)
try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
except Exception:
    pass

# If not in secrets, show input
if not api_key:
    with st.expander("🔑 API Key Setup (Pehli baar sirf ek baar)", expanded=True):
        st.markdown("""
        <div style="font-family:'Crimson Pro',serif; color:#8b6914; font-size:0.9rem; margin-bottom:0.8rem;">
        Anthropic API key chahiye. <a href="https://console.anthropic.com" target="_blank" style="color:#d4a843;">console.anthropic.com</a> se le aao.
        </div>
        """, unsafe_allow_html=True)
        api_key_input = st.text_input(
            "Anthropic API Key",
            type="password",
            placeholder="sk-ant-...",
            label_visibility="collapsed"
        )
        if api_key_input:
            api_key = api_key_input

# ─── Main Input ──────────────────────────────────────────────────────────────
writing_input = st.text_area(
    "APNI WRITING YAHAN LIKHEIN",
    placeholder="यहाँ अपनी शायरी, नज़्म, ग़ज़ल, या कोई भी लिखावट paste करें...\nSafeer padh ke batayega — kitab mein ho ya nahi 🪶",
    height=220,
    label_visibility="visible"
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyze_btn = st.button("✦ Safeer se Poochho ✦")

# ─── Analysis ────────────────────────────────────────────────────────────────
if analyze_btn:
    if not writing_input.strip():
        st.warning("Kuch toh likho pehle... 🖊️")
    elif not api_key:
        st.error("API key chahiye. Upar setup karo.")
    else:
        with st.spinner("Safeer padh raha hai... 🪶"):
            try:
                result = analyze_writing(writing_input.strip(), api_key)
                time.sleep(0.3)

                # PDF Decision
                if result.get("pdf_include"):
                    st.markdown(f"""
                    <div class="pdf-yes">
                        <span class="pdf-decision-icon">✅</span>
                        <div class="pdf-decision-text">Kitab mein Shamil Karo</div>
                        <div class="pdf-reason">{result.get("pdf_recommendation", "")}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="pdf-no">
                        <span class="pdf-decision-icon">🚫</span>
                        <div class="pdf-decision-text">Abhi Kitab ke Liye Nahi</div>
                        <div class="pdf-reason">{result.get("pdf_recommendation", "")}</div>
                    </div>
                    """, unsafe_allow_html=True)

                # Score
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                render_score(result.get("quality_score", 0))
                st.markdown('</div>', unsafe_allow_html=True)

                # Type, Theme, Mood row
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown(f"""
                    <div class="result-card">
                        <div class="card-label">विधा • Type</div>
                        <div class="card-value">{result.get("type", "—")}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_b:
                    st.markdown(f"""
                    <div class="result-card">
                        <div class="card-label">भाव • Mood</div>
                        <div class="card-value">{result.get("mood", "—")}</div>
                    </div>
                    """, unsafe_allow_html=True)

                # Themes
                st.markdown('<div class="result-card"><div class="card-label">विषय • Themes</div>', unsafe_allow_html=True)
                render_tags(result.get("theme", []))
                st.markdown('</div>', unsafe_allow_html=True)

                # Strengths
                if result.get("strengths"):
                    st.markdown('<div class="result-card"><div class="card-label">✦ Khoobiyaan • Strengths</div>', unsafe_allow_html=True)
                    render_list(result["strengths"])
                    st.markdown('</div>', unsafe_allow_html=True)

                # Suggestions
                if result.get("suggestions"):
                    st.markdown('<div class="result-card"><div class="card-label">✎ Behtar Ho Sakta Hai</div>', unsafe_allow_html=True)
                    render_list(result["suggestions"])
                    st.markdown('</div>', unsafe_allow_html=True)

                # Safeer's comment
                if result.get("safeer_comment"):
                    st.markdown(f"""
                    <div class="safeer-comment">{result["safeer_comment"]}</div>
                    """, unsafe_allow_html=True)

                # Save to history
                st.session_state.history.append({
                    "preview": writing_input[:60] + "...",
                    "type": result.get("type"),
                    "score": result.get("quality_score"),
                    "pdf": result.get("pdf_include"),
                    "mood": result.get("mood")
                })

            except json.JSONDecodeError:
                st.error("Kuch galat hua response parse karte waqt. Dobara try karo.")
            except anthropic.AuthenticationError:
                st.error("API key galat hai. Dobara check karo.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ─── History ─────────────────────────────────────────────────────────────────
if st.session_state.history:
    st.markdown('<div class="history-header">✦ Is Session Ki Writings ✦</div>', unsafe_allow_html=True)
    for i, item in enumerate(reversed(st.session_state.history[-5:])):
        pdf_icon = "✅" if item["pdf"] else "🚫"
        score_color = "#4CAF50" if item["score"] >= 7 else "#FF9800"
        st.markdown(f"""
        <div class="result-card" style="padding: 0.8rem 1.2rem;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.3rem;">
                <span style="font-family:'Noto Serif Devanagari',serif; color:#c8b890; font-size:0.9rem; flex:1; min-width:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">{item['preview']}</span>
                <div style="display:flex; gap:0.6rem; align-items:center; flex-shrink:0;">
                    <span style="font-size:0.75rem; color:#8b6914;">{item['type']}</span>
                    <span style="font-size:0.85rem; color:{score_color}; font-family:'Rozha One',serif;">{item['score']}</span>
                    <span>{pdf_icon}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    🪶 Safeer AI • सोलहवीं शायरी के सफर पर<br>
    <span style="font-size:0.7rem;">Built with ♡ by Vikas Prajapati</span>
</div>
""", unsafe_allow_html=True)
        
