# 🚀 Deploy in 5 Minutes - Streamlit Cloud + Turso

**The easiest way to deploy your Prakrit Games web app!**

---

## ✅ What You Need

1. ✅ Turso credentials (you have these!)
2. ✅ GitHub account
3. ✅ Streamlit Cloud account (free - uses GitHub login)

---

## 📋 Step 1: Upload Data to Turso (~2 min)

```bash
# Install dependencies
pip install libsql-client python-dotenv

# Upload your databases
python3 utils/upload_to_turso.py
```

**Expected output:**
```
✓ Connected to Turso!
📋 Creating tables...
📦 Inserting data...
✓ Successfully uploaded verb_forms.db!
✓ Successfully uploaded noun_forms.db!
✅ UPLOAD COMPLETE!
```

---

## 🌐 Step 2: Deploy to Streamlit Cloud (~3 min)

### A. Push to GitHub

```bash
git add -A
git commit -m "Ready for deployment"
git push origin main  # or your branch name
```

### B. Deploy on Streamlit Cloud

1. **Go to:** https://streamlit.io/cloud
2. **Sign in** with your GitHub account
3. **Click:** "New app"
4. **Select:**
   - Repository: `your-username/prakrit-game`
   - Branch: `main` (or your branch)
   - Main file path: `streamlit_app.py`

5. **Click "Advanced settings"**

6. **Add secrets** (copy-paste this):
   ```toml
   TURSO_DATABASE_URL = "libsql://prakrit-khasoochi.aws-ap-south-1.turso.io"
   TURSO_AUTH_TOKEN = "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3NjI4NzIyNTUsImlkIjoiNjg1ZTllODgtYTZlZS00OWQ3LTg1MWQtNDVlNjczODYxZDlkIiwicmlkIjoiOGJiYWQzY2UtYzA2Mi00ZDYxLWE4OWYtYzM2MDJlMzk5MDI0In0.XO1aX7KG1AvzJtzF2uv6mBfxy20FQOBWlPAzwdQHrUhOpV-AwvW2v0pqhA2K3RFtyb7MaclTHdekWQ7LWhNtBg"
   ```

7. **Click "Deploy"**

8. **Wait 2-3 minutes** ☕

9. **Done!** 🎉

---

## 🎉 Your App is Live!

Your app will be at:
```
https://prakrit-games.streamlit.app
```
(or similar URL shown by Streamlit)

**Try it:**
- Open the URL
- Play all 5 games
- Switch between scripts
- Share with learners! 📚

---

## 🧪 Test Locally First (Optional)

```bash
# Install dependencies
pip install -r requirements_web.txt

# Run locally
streamlit run streamlit_app.py

# Test at http://localhost:8501
```

---

## 📊 What You Get (FREE!)

| Feature | Details |
|---------|---------|
| **Hosting** | Free forever on Streamlit Cloud |
| **Database** | 9GB free on Turso |
| **SSL** | HTTPS automatic |
| **Updates** | Auto-deploy on git push |
| **Custom URL** | prakrit-games.streamlit.app |

**Total Cost: $0/month** 💰

---

## 🔧 Troubleshooting

### "Database connection failed"

1. Check secrets in Streamlit Cloud:
   - Go to app settings
   - Verify TURSO_DATABASE_URL and TURSO_AUTH_TOKEN
   - Make sure there are no extra spaces

2. Verify data upload:
   ```bash
   python3 utils/upload_to_turso.py
   ```

### "App won't start"

1. Check app logs in Streamlit Cloud dashboard
2. Verify `requirements_web.txt` has all dependencies
3. Reboot app from Streamlit Cloud dashboard

### "No data in games"

1. Run upload script again:
   ```bash
   python3 utils/upload_to_turso.py
   ```

2. Check Turso dashboard to verify data exists

---

## ⚙️ Update Your App

```bash
# Make changes locally
# Test
streamlit run streamlit_app.py

# Commit and push
git add -A
git commit -m "Update games"
git push

# Streamlit Cloud auto-deploys! 🚀
```

---

## 🎯 Next Steps

### Share Your App:
- Copy your Streamlit Cloud URL
- Share on social media
- Send to learners

### Monitor Usage:
- Check Streamlit Cloud dashboard
- View app metrics
- Track visitors

### Optional Enhancements:
- Add more games
- Customize UI theme
- Add user feedback form

---

## 📞 Need Help?

**Common Issues:**

1. **Build fails:**
   - Check `requirements_web.txt` syntax
   - Verify all files committed to GitHub

2. **Games not loading:**
   - Check browser console for errors
   - Verify Turso credentials in secrets

3. **Slow loading:**
   - Clear Streamlit cache
   - Reboot app from dashboard

**Resources:**
- Streamlit Docs: https://docs.streamlit.io
- Turso Docs: https://docs.turso.tech
- Community: https://discuss.streamlit.io

---

## ✅ Checklist

Setup (one-time):
- [ ] Data uploaded to Turso
- [ ] Code pushed to GitHub
- [ ] Streamlit Cloud account created

Deployment:
- [ ] App created on Streamlit Cloud
- [ ] Secrets added (TURSO_DATABASE_URL, TURSO_AUTH_TOKEN)
- [ ] App deployed successfully

Verification:
- [ ] App loads in browser
- [ ] All 5 games work
- [ ] Script switching works
- [ ] Data displays correctly

---

## 🎊 Success!

Your Prakrit Games app is now:
- ✅ **Live on the internet**
- ✅ **Free to host forever**
- ✅ **Auto-updates on git push**
- ✅ **Fast globally (Turso edge network)**
- ✅ **Ready to share**

**Start teaching Prakrit today!** शुभं भवतु! ✨

---

**Quick Links:**
- 📱 Your app: https://prakrit-games.streamlit.app
- 🔧 Upload data: `python3 utils/upload_to_turso.py`
- 🚀 Deploy: Push to GitHub → Auto-deploys!
