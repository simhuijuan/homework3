---
sdk: gradio
app_file: app.py
---

# Live Sentiment Demo (Track C)

This Gradio app analyzes typed text with **TextBlob** for fast, lightweight sentiment analysis. Shows label + confidence score in real time with event logging and CSV export. No model downloads or internet dependency required.

Live Space URL: https://huggingface.co/spaces/simhuijuan/homework3

## How to run locally

1. Create a virtual environment and activate it.

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
python app.py
```

2. Open browser to `http://localhost:7860`

## Features

- ✅ Fast lightweight sentiment analysis using TextBlob
- ✅ Works offline - no internet dependency for model downloads
- ✅ Real-time analysis with POSITIVE/NEUTRAL/NEGATIVE labels
- ✅ Event log with timestamps
- ✅ CSV export functionality
- ✅ Alert threshold customization

## Technology

- **Framework**: Gradio (web UI)
- **Sentiment Analysis**: TextBlob (lexicon-based, no ML model download)
- **Python**: 3.8+

## Deployment to Hugging Face Spaces

1. Create a Hugging Face access token:
   - Visit https://huggingface.co/settings/tokens and click "New token"
   - Give it a descriptive name, select the `write` scope
   - Copy the token value

2. Add the token to your GitHub repo as a secret:
   - Go to your repository on GitHub → Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Set **Name** to `HF_TOKEN` and **Value** to your token
   - Click Save

3. The GitHub Actions workflow (`.github/workflows/verify-and-deploy.yml`) will automatically:
   - Verify the app on every push to `main`
   - Deploy to Hugging Face Space at: https://huggingface.co/spaces/simhuijuan/homework3

4. Check the Actions tab on GitHub to monitor deployment progress

## Notes

- TextBlob uses a pre-built sentiment lexicon, so startup is instant
- Results are normalized to 0-1 scale for consistency
- Event log stores analysis history during the session

