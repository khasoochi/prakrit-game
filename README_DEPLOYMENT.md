# ⚠️ Important: Streamlit Apps Don't Run on Vercel

**The app is crashing on Vercel because Streamlit requires a persistent server, not serverless functions.**

---

## ✅ SOLUTION: Use Streamlit Cloud (Better & Easier!)

Streamlit Cloud is:
- ✅ **100% FREE** (forever)
- ✅ **Made for Streamlit** (no configuration)
- ✅ **Easier than Vercel** (2 clicks to deploy)
- ✅ **Auto-updates** (push to GitHub = instant deploy)

---

## 🚀 Deploy in 5 Minutes

### Step 1: Upload Data to Turso (One-Time)

```bash
pip install libsql-client python-dotenv
python3 utils/upload_to_turso.py
```

**Wait for:**
```
✅ UPLOAD COMPLETE!
```

---

### Step 2: Deploy to Streamlit Cloud

1. **Go to:** https://share.streamlit.io

2. **Sign in** with GitHub

3. **Click:** "New app"

4. **Fill in:**
   - Repository: `your-username/prakrit-game`
   - Branch: `main` (or your branch name)
   - Main file path: `streamlit_app.py`

5. **Click "Advanced settings"**

6. **In "Secrets" box, paste:**
   ```toml
   TURSO_DATABASE_URL = "libsql://prakrit-khasoochi.aws-ap-south-1.turso.io"
   TURSO_AUTH_TOKEN = "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3NjI4NzIyNTUsImlkIjoiNjg1ZTllODgtYTZlZS00OWQ3LTg1MWQtNDVlNjczODYxZDlkIiwicmlkIjoiOGJiYWQzY2UtYzA2Mi00ZDYxLWE4OWYtYzM2MDJlMzk5MDI0In0.XO1aX7KG1AvzJtzF2uv6mBfxy20FQOBWlPAzwdQHrUhOpV-AwvW2v0pqhA2K3RFtyb7MaclTHdekWQ7LWhNtBg"
   ```

7. **Click "Deploy"**

8. **Wait 2-3 minutes** ☕

9. **Your app is LIVE!** 🎉

---

## 🎯 Your App URL

After deployment:
```
https://your-app-name.streamlit.app
```

Share this link with learners!

---

## 🧪 Test Locally First

```bash
pip install -r requirements_web.txt
python3 utils/upload_to_turso.py  # Upload data (one-time)
streamlit run streamlit_app.py     # Test locally
```

Open: http://localhost:8501

---

## 📝 Summary

❌ **Don't use Vercel** for Streamlit apps (causes crashes)
✅ **Use Streamlit Cloud** instead (designed for this!)

**It's actually easier:**
- No vercel.json needed
- No build configuration
- Just works!

---

## 💡 Alternative: Deploy Anywhere Else

If you really want to avoid Streamlit Cloud:

**Other platforms that support Streamlit:**
- Railway (free tier)
- Render (free tier)  
- Heroku (free tier ended, paid only)
- Google Cloud Run (small cost)

**But Streamlit Cloud is the easiest and free!**

---

## 🆘 Need Help?

**Common issues:**

1. **"Module not found"**
   - Check `requirements_web.txt` is committed
   - Redeploy from Streamlit dashboard

2. **"Database connection failed"**
   - Verify secrets are pasted correctly
   - No extra spaces or quotes

3. **"Upload to Turso failed"**
   ```bash
   pip install --upgrade libsql-client
   python3 utils/upload_to_turso.py
   ```

---

## ✅ Deployment Checklist

Before deploying:
- [ ] Run `python3 utils/upload_to_turso.py` (uploads data)
- [ ] Code pushed to GitHub
- [ ] Streamlit Cloud account created

During deployment:
- [ ] App created on Streamlit Cloud
- [ ] Secrets added (both TURSO variables)
- [ ] Click "Deploy"

After deployment:
- [ ] App loads successfully
- [ ] Test all 5 games
- [ ] Share the URL! 📱

---

**Your app will be at:** `https://prakrit-games.streamlit.app`

**Support:** https://docs.streamlit.io/streamlit-community-cloud
