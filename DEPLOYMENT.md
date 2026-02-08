# Deployment Guide

## ⚠️ Important: Vercel Limitation

**Vercel does NOT natively support Streamlit apps.** Streamlit requires a persistent server process, while Vercel uses serverless functions with time limits.

## ✅ Recommended: Streamlit Cloud

**Streamlit Cloud is the best platform for deploying Streamlit apps.**

### Quick Deploy Steps:

1. **Your code is already on GitHub** ✅
   - Repository: `MuhammadAsadIshfaq/Gemini-Hackathon-project`

2. **Go to Streamlit Cloud**
   - Visit: https://share.streamlit.io
   - Sign in with your GitHub account

3. **Deploy**
   - Click "New app"
   - Repository: `MuhammadAsadIshfaq/Gemini-Hackathon-project`
   - Branch: `main`
   - Main file: `app.py`
   - Click "Deploy"

4. **Your app will be live at:**
   - `https://gemini-hackathon-project.streamlit.app` (or similar)

### Benefits:
- ✅ Free hosting
- ✅ Automatic deployments on git push
- ✅ Built for Streamlit
- ✅ No configuration needed
- ✅ Custom subdomain
- ✅ HTTPS by default

---

## Alternative: Vercel (Not Recommended)

If you still want to try Vercel, the configuration files are included, but it may not work properly due to Streamlit's architecture.

### Vercel Setup:
1. Connect your GitHub repo to Vercel
2. Vercel will detect the `vercel.json` configuration
3. Deploy

**Note:** You may still encounter issues because Streamlit needs a persistent server.

---

## Other Options:

### Railway
- Visit: https://railway.app
- Connect GitHub repo
- Add Python buildpack
- Set start command: `streamlit run app.py --server.port $PORT`

### Render
- Visit: https://render.com
- Create new Web Service
- Connect GitHub repo
- Build command: `pip install -r requirements.txt`
- Start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

### Heroku
- Visit: https://heroku.com
- Create new app
- Connect GitHub repo
- Add `Procfile` with: `web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

---

## Recommendation

**Use Streamlit Cloud** - it's the easiest and most reliable option for Streamlit apps.

