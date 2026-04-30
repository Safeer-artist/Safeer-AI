# 🪶 Safeer AI — शायरी का उस्ताद

> *"Jo likhta hai dil se, Safeer use pehchanta hai."*

An AI poetry critic and curator — trained in the soul of Urdu-Hindi literature. Built for **Vikas Prajapati** for his collection *"सोलहवीं शायरी के सफर पर"*.

---

## ✦ Kya Karta Hai Safeer?

- **Categorize** karta hai — Ghazal, Nazm, Kavita, Rap, Sher, Thought
- **Quality Score** deta hai out of 10
- **Themes & Mood** identify karta hai
- **PDF mein daalna chahiye ya nahi** — clear verdict deta hai
- **Strengths & Suggestions** bhi — honest, dil se
- **Safeer ki apni baat** — ek sher ya line, har analysis ke baad

---

## 🚀 GitHub + Streamlit Cloud pe Deploy Karo (FREE)

### Step 1 — GitHub pe daalo

```bash
# GitHub pe naya repo banao: safeer-ai
# Phir ye commands chalao apne PC/laptop pe:

git init
git add .
git commit -m "🪶 Safeer AI - first commit"
git branch -M main
git remote add origin https://github.com/TERA_USERNAME/safeer-ai.git
git push -u origin main
```

### Step 2 — Streamlit Cloud pe deploy karo

1. Jao: **https://share.streamlit.io**
2. GitHub se login karo
3. **"New app"** click karo
4. Repository: `safeer-ai` select karo
5. Branch: `main`
6. Main file: `app.py`
7. **"Deploy!"** dabao

### Step 3 — API Key safely daalo

Streamlit Cloud pe **Settings → Secrets** mein jao aur yeh daalo:

```toml
ANTHROPIC_API_KEY = "sk-ant-api03-TERI_KEY_YAHAN"
```

> API key lene ke liye: https://console.anthropic.com

**Done! 🎉** Tera URL kuch aisa hoga:
`https://safeer-ai-TERA_USERNAME.streamlit.app`

Mobile pe bhi perfectly chalega! 📱

---

## 💻 Locally Chalana Chahte Ho?

```bash
# Install karo
pip install -r requirements.txt

# API key set karo (ek baar)
mkdir .streamlit
echo 'ANTHROPIC_API_KEY = "sk-ant-..."' > .streamlit/secrets.toml

# Run karo
streamlit run app.py
```

Browser mein khulega: `http://localhost:8501`

---

## 📁 Files

```
safeer-ai/
├── app.py              ← Main app
├── requirements.txt    ← Dependencies
└── README.md           ← Yahi file
```

---

*Made with ♡ — सोलहवीं शायरी के सफर पर*
