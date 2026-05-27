# Publish Dasun Welianga's GitHub profile package

This package is prepared for GitHub username **`IT24103496`**. GitHub displays a profile README only when a **public** repository is named exactly `IT24103496` and contains a root `README.md`.

## Create and publish the profile repository

1. Sign in to Dasun's GitHub account and create a **public** repository named `IT24103496` if it does not already exist.
2. Extract this ZIP, open the extracted folder, and push its **contents** to that repository.

```bash
git init
git branch -M main
git add .
git commit -m "Create automated network engineering profile README"
git remote add origin https://github.com/IT24103496/IT24103496.git
git push -u origin main
```

Uploading via GitHub's web interface also works: upload `README.md`, `assets/`, `.github/`, `docs/`, `tests/`, and `profile.config.json` at repository root.

## First run checklist

1. Open the repository **Actions** tab and enable workflows when prompted.
2. Run **Profile Bot** once. It refreshes live repository and activity blocks from public GitHub data.
3. Run **Contribution Snake** once. After the workflow creates the `output` branch, the animation appears in the README.
4. Confirm the **Quality Gate** and **CodeQL** workflow results.

## Safe personalization

`README.md` uses Dasun's public GitHub biography, public repositories and public LinkedIn link. The portrait shown in the README uses Dasun's existing public GitHub avatar URL; no private photo is packaged.

Edit `profile.config.json` to add verified technologies or future projects. Keep the `LIVE_OVERVIEW`, `PUBLIC_REPOS`, and `ACTIVITY_FEED` marker comments in `README.md`, because Profile Bot replaces only those sections.
