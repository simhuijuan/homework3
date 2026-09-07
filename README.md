---
sdk: gradio
app_file: app.py
---

# Live Sentiment Demo (Track C)

This Gradio app analyzes typed text with a small Hugging Face transformer and shows a label + confidence score in real time. It includes an event log and CSV export.

Live Space URL: https://huggingface.co/spaces/simhuijuan/homework3

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
- For deployment to Hugging Face Spaces: create a Space under your account and add a Hugging Face access token to GitHub as a repository secret named `HF_TOKEN` (write scope). The provided GitHub Actions workflow will use this secret to push updates to the Space on `main`.

How to create and add `HF_TOKEN` (write scope)

1. Create a Hugging Face access token:

	- Visit https://huggingface.co/settings/tokens and click "New token".
	- Give it a descriptive name, select the `write` scope, and create the token. Copy the token value — you will not be able to view it again.

2. Add the token to your GitHub repo as a secret:

	- Go to your repository on GitHub → Settings → Secrets and variables → Actions → New repository secret.
	- Set **Name** to `HF_TOKEN` and **Value** to the token you copied. Click Save.

3. Confirm the workflow is configured to deploy to your Space: the workflow pushes to `https://huggingface.co/spaces/simhuijuan/homework3`.

Triggering deploy

- Push a commit to `main` (or re-run the workflow) to trigger the verify + deploy jobs. Check the Actions tab on GitHub to follow progress and inspect logs. If the verify job fails, copy the logs and I can help fix the issue.

