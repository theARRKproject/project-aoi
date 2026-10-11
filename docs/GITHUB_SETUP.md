# Publishing Project Aoi on GitHub

## Suggested repository details

**Repository name:** `project-aoi`  
**Description:** `An experimental local AI assistant built with Python, Qwen, SQLite and semantic memory retrieval.`  
**Topics:** `python`, `local-ai`, `sqlite`, `pytorch`, `transformers`, `sentence-transformers`, `personal-assistant`, `machine-learning`, `portfolio-project`

## Publish with the website

1. Create a new **public** GitHub repository called `project-aoi`. Do not add an automatic README because this ZIP already has one.
2. Upload the **contents** of the `project-aoi` folder to the root of your repository. You can use GitHub's **Add file > Upload files**, or the git commands below.
3. For the optional project website, open **Settings > Pages** and choose **Deploy from a branch**. Choose branch `main`, folder `/docs`, then save.
4. GitHub will publish `docs/index.html`. The URL commonly looks like `https://YOUR-USERNAME.github.io/project-aoi/`.
5. Change `YOUR-USERNAME` in `docs/index.html` to your actual GitHub username, so the source links work.
6. Add the website URL to the repository's **About** panel. Pin the repository on your GitHub profile if you use it as a portfolio piece.

### Git commands

```bash
cd project-aoi
git init
git add .
git commit -m "Publish Project Aoi prototype showcase"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/project-aoi.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your account name. If your GitHub repository already exists, adapt the remote/push commands instead of overwriting work.

## Before publishing real work

- Do not upload your old `*.db` files or personal conversation transcripts. `.gitignore` excludes the default local data files.
- Review all code, comments and any media for secrets, tokens, personal data or files you do not have permission to publish.
- This repository includes a reconstruction, not the historical source. You can replace the reconstruction with your original code when you recover it and update the status page.
- This template does not include a software license. Add one only after choosing how you want others to reuse your code.
