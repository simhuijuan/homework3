---
sdk: gradio
app_file: app.py
---

# Live Sentiment Demo (Track C)

This Gradio app analyzes typed text with a small Hugging Face transformer and shows a label + confidence score in real time. It includes an event log and CSV export.

Live Space URL: (create a Hugging Face Space and paste the URL here)

How to run locally

1. Create a virtual environment and activate it.

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
python app.py
```

Model used

- `distilbert-base-uncased-finetuned-sst-2-english` via `transformers` pipeline (sentiment-analysis).

Notes

- The app lazily loads the model on first request so CI verify can import the files without downloading model weights.
- For deployment to Hugging Face Spaces: create a Space under your account, create an access token (write scope), and add a `HF_TOKEN` GitHub secret to enable automated deploy from GitHub Actions.
