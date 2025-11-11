# 🚀 Deploy to Vercel with Turso (5 Minutes!)

Your Prakrit Games app is ready to deploy! Follow these simple steps.

---

## ✅ Prerequisites

You already have:
- ✅ Turso database credentials (provided)
- ✅ Web app code (ready)
- ✅ GitHub repository

You need:
- 📧 Vercel account (free - sign up at https://vercel.com)

---

## 📋 Step 1: Upload Data to Turso (One-Time, ~2 minutes)

```bash
# 1. Install dependencies
pip install libsql-client python-dotenv

# 2. Upload your databases to Turso
python3 utils/upload_to_turso.py

# This will:
# - Connect to your Turso database
# - Upload verb_forms.db (60MB)
# - Upload noun_forms.db (120MB)
# - Verify the upload

# Expected output:
# ✓ Connected to Turso!
# ✓ Successfully uploaded verb_forms.db!
# ✓ Successfully uploaded noun_forms.db!
# ✅ UPLOAD COMPLETE!
```

**That's it for database setup!** Your data is now on Turso's edge network. ⚡

---

## 🌐 Step 2: Deploy to Vercel (~3 minutes)

### Option A: One-Click Deploy (Easiest)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/YOUR_USERNAME/prakrit-game&env=TURSO_DATABASE_URL,TURSO_AUTH_TOKEN)

1. Click the button above
2. Connect your GitHub account
3. Add environment variables:
   - `TURSO_DATABASE_URL`: `libsql://prakrit-khasoochi.aws-ap-south-1.turso.io`
   - `TURSO_AUTH_TOKEN`: `eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3NjI4NzIyNTUsImlkIjoiNjg1ZTllODgtYTZlZS00OWQ3LTg1MWQtNDVlNjczODYxZDlkIiwicmlkIjoiOGJiYWQzY2UtYzA2Mi00ZDYxLWE4OWYtYzM2MDJlMzk5MDI0In0.XO1aX7KG1AvzJtzF2uv6mBfxy20FQOBWlPAzwdQHrUhOpV-AwvW2v0pqhA2K3RFtyb7MaclTHdekWQ7LWhNtBg`
4. Click "Deploy"
5. Wait 2-3 minutes ☕
6. Done! 🎉

### Option B: Manual Deploy

1. **Push your code to GitHub:**
   ```bash
   git add -A
   git commit -m "Ready for Vercel deployment"
   git push origin main
   ```

2. **Go to Vercel:**
   - Visit https://vercel.com
   - Sign in with GitHub
   - Click "Add New Project"

3. **Import Repository:**
   - Find your `prakrit-game` repository
   - Click "Import"

4. **Configure Project:**
   - **Framework Preset:** Other
   - **Root Directory:** `./`
   - **Build Command:** Leave empty (or `streamlit run streamlit_app.py`)
   - **Output Directory:** Leave empty
   - **Install Command:** `pip install -r requirements_web.txt`

5. **Add Environment Variables:**
   Click "Environment Variables" and add:

   | Key | Value |
   |-----|-------|
   | `TURSO_DATABASE_URL` | `libsql://prakrit-khasoochi.aws-ap-south-1.turso.io` |
   | `TURSO_AUTH_TOKEN` | `eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3NjI4NzIyNTUsImlkIjoiNjg1ZTllODgtYTZlZS00OWQ3LTg1MWQtNDVlNjczODYxZDlkIiwicmlkIjoiOGJiYWQzY2UtYzA2Mi00ZDYxLWE4OWYtYzM2MDJlMzk5MDI0In0.XO1aX7KG1AvzJtzF2uv6mBfxy20FQOBWlPAzwdQHrUhOpV-AwvW2v0pqhA2K3RFtyb7MaclTHdekWQ7LWhNtBg` |

   Make sure to select **Production, Preview, and Development** for both.

6. **Deploy:**
   - Click "Deploy"
   - Wait 2-3 minutes for build
   - Your app is live! 🚀

---

## 🎉 Step 3: Access Your App

After deployment completes:

1. Vercel will show: **"Your project is ready!"**
2. Click "Visit" or copy the URL
3. Your app will be at: `https://prakrit-game-XXXXX.vercel.app`

**Try it out:**
- Switch between scripts (Devanagari, IAST, ISO, HK)
- Play all 5 games
- Track your score and streak
- Share the link with learners! 🎓

---

## 🧪 Test Locally First (Optional)

Want to test before deploying?

```bash
# 1. Install dependencies
pip install -r requirements_web.txt

# 2. Make sure .env has your Turso credentials
# (Already set up with your credentials)

# 3. Run locally
streamlit run streamlit_app.py

# 4. Open browser to http://localhost:8501

# 5. Test all games, then deploy!
```

---

## 📊 What You Get

### Free Tier Benefits:
| Service | What You Get | Cost |
|---------|-------------|------|
| **Turso** | 9GB database, unlimited reads | **FREE** |
| **Vercel** | Unlimited bandwidth, auto-scaling | **FREE** |
| **SSL** | HTTPS automatically | **FREE** |
| **CDN** | Global edge network | **FREE** |

**Total: $0/month** for unlimited learners! 🎉

---

## 🔧 Troubleshooting

### "Database connection failed"

**Check:**
1. Are TURSO_DATABASE_URL and TURSO_AUTH_TOKEN set in Vercel?
2. Did you upload data with `upload_to_turso.py`?
3. Is the Turso token still valid?

**Fix:**
```bash
# Re-run upload script
python3 utils/upload_to_turso.py

# Check Vercel env vars in dashboard
```

### "No data showing"

**Verify upload:**
```bash
# Test locally
streamlit run streamlit_app.py

# If local works but Vercel doesn't:
# - Check Vercel environment variables
# - Redeploy from Vercel dashboard
```

### "Module not found"

**Fix:**
```bash
# Update requirements
pip install -r requirements_web.txt

# Redeploy on Vercel
```

### Build fails on Vercel

**Check:**
1. `requirements_web.txt` is in root directory
2. All dependencies are listed
3. No syntax errors in Python files

**Common fix:**
- Trigger new deployment from Vercel dashboard
- Check build logs for specific error

---

## ⚙️ Advanced Configuration

### Custom Domain

**On Vercel:**
1. Go to Project Settings → Domains
2. Add your domain
3. Update DNS records as shown
4. Wait for propagation (~48 hours max)

### Performance Optimization

Already optimized! ✅
- Turso edge database (low latency globally)
- Streamlit caching enabled
- Vercel edge network

### Environment Variables

**Current setup:**
```
TURSO_DATABASE_URL=libsql://prakrit-khasoochi.aws-ap-south-1.turso.io
TURSO_AUTH_TOKEN=eyJhbGciOiJF...
```

**To update:**
1. Go to Vercel Project Settings
2. Navigate to Environment Variables
3. Edit values
4. Redeploy

---

## 📈 Monitoring

### Vercel Dashboard
- **Deployments:** See all deployments and logs
- **Analytics:** Track page views (free tier)
- **Logs:** Debug errors in real-time

### Turso Dashboard
- **Database Size:** Monitor storage usage
- **Queries:** See query performance
- **Connections:** Track active connections

---

## 🔒 Security

### Best Practices:
✅ **Never commit .env file** (already in .gitignore)
✅ **Use environment variables** for secrets
✅ **Turso tokens** are scoped to database
✅ **HTTPS** automatic on Vercel
✅ **Read-only access** for public users (games only read data)

### Update Tokens:
If you need to rotate your Turso token:
1. Generate new token in Turso dashboard
2. Update TURSO_AUTH_TOKEN in Vercel
3. Redeploy

---

## 🎯 Next Steps

After deployment:

1. **Share Your App:**
   - Copy the Vercel URL
   - Share with learners
   - Post on social media

2. **Collect Feedback:**
   - Monitor usage
   - Get user feedback
   - Iterate and improve

3. **Optional Enhancements:**
   - Add Google Analytics
   - Create custom domain
   - Add more games
   - Implement user accounts

---

## 💡 Pro Tips

### Fast Iteration:
```bash
# Make changes locally
# Test: streamlit run streamlit_app.py
# Commit and push
git add -A && git commit -m "Update" && git push

# Vercel auto-deploys! 🚀
```

### Preview Deployments:
- Every git push creates a preview URL
- Test before merging to main
- Share previews with testers

### Rollback:
- Vercel keeps all deployments
- Instant rollback to any previous version
- Zero downtime

---

## 📞 Support

**Issues?**
1. Check build logs in Vercel dashboard
2. Test locally first
3. Verify Turso connection
4. Check environment variables

**Resources:**
- Vercel Docs: https://vercel.com/docs
- Turso Docs: https://docs.turso.tech
- Streamlit Docs: https://docs.streamlit.io

---

## ✅ Deployment Checklist

Before you deploy:
- [ ] Databases uploaded to Turso
- [ ] Code pushed to GitHub
- [ ] Vercel account created
- [ ] Environment variables ready

During deployment:
- [ ] Project imported to Vercel
- [ ] Environment variables set
- [ ] Build successful
- [ ] Deployment complete

After deployment:
- [ ] App loads correctly
- [ ] All 5 games work
- [ ] Script switching works
- [ ] Data displays correctly
- [ ] Share with learners! 🎓

---

## 🎉 Success!

Your Prakrit Games web app is now:
- ✅ **Live on the internet**
- ✅ **Fast globally** (Turso edge + Vercel CDN)
- ✅ **Free to host** (unlimited usage)
- ✅ **Auto-updating** (push to deploy)
- ✅ **Secure** (HTTPS, environment variables)

**Congratulations!** 🎊

Now go share your app and help people learn Prakrit! शुभं भवतु! ✨

---

**Your live app will be at:**
`https://prakrit-game-XXXXX.vercel.app`

**Upload data:** `python3 utils/upload_to_turso.py`
**Deploy:** Push to GitHub, Vercel auto-deploys!
