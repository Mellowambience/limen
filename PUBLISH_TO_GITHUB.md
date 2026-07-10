# Publish LIMEN to GitHub

The project is already initialized as a local Git repository with a clean first commit.

## Recommended repository

- Owner: `Mellowambience`
- Name: `limen`
- Visibility: public
- Description: `A local-first Quantum Sentient-Lite returning intelligence, life steward, and creative evolution engine.`

## GitHub CLI

From the project directory:

```bash
gh auth login
gh repo create Mellowambience/limen --public --source . --remote origin --push --description "A local-first Quantum Sentient-Lite returning intelligence, life steward, and creative evolution engine."
```

## Without GitHub CLI

Create an empty public repository named `limen` under `Mellowambience`, then run:

```bash
git remote add origin https://github.com/Mellowambience/limen.git
git branch -M main
git push -u origin main
```

Do not initialize the remote with a README, license, or `.gitignore`; those already exist here.
