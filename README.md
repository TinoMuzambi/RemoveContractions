# Remove Contractions

A focused Flask utility that expands common English contractions while preserving punctuation, whitespace, and possessives.

**Live app:** [remove-contractions.vercel.app](https://remove-contractions.vercel.app)

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app run --debug
```

## Test

```bash
pip install -r requirements-dev.txt
pytest
```

Text is processed in memory for one request and is not stored. Inputs are limited to 50,000 characters. Explicit mappings avoid treating possessive `'s` as “is”; ambiguous `'d` forms are expanded as “would.”
