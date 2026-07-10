$ErrorActionPreference = "Stop"
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw "GitHub CLI (gh) is required. Install it, then run gh auth login."
}
gh repo create Mellowambience/limen --public --source . --remote origin --push --description "A local-first Quantum Sentient-Lite returning intelligence, life steward, and creative evolution engine."
