# Deploying to GitHub Pages

Your site is already committed to a local git repository. Follow these steps to put it online.

## 1. Create a GitHub account (skip if you have one)
Go to https://github.com/signup and sign up (free).

## 2. Create a new empty repository
1. Go to https://github.com/new
2. **Repository name:** `aastha-portfolio` (or anything you like)
3. Set it to **Public**
4. Do **NOT** check "Add a README" / .gitignore / license (the repo already has files)
5. Click **Create repository**

## 3. Push your code
GitHub will show a URL like `https://github.com/<your-username>/aastha-portfolio.git`.
Run these commands in this folder (replace the URL with yours):

```powershell
git remote add origin https://github.com/<your-username>/aastha-portfolio.git
git branch -M main
git push -u origin main
```

The first push will ask you to sign in to GitHub in your browser — approve it.

## 4. Turn on GitHub Pages
1. On your repo page, click **Settings**
2. Left sidebar → **Pages**
3. Under **Build and deployment** → **Source**, choose **Deploy from a branch**
4. **Branch:** `main`, folder: `/ (root)` → **Save**
5. Wait ~1 minute, then refresh. Your live link appears at the top:
   `https://<your-username>.github.io/aastha-portfolio/`

Share that link anywhere. 🎉

## Updating the site later
Edit the files, then:
```powershell
git add .
git commit -m "Update content"
git push
```
The live site updates automatically in under a minute.
