from datetime import datetime
import csv
import tempfile
import os
from typing import List, Dict, Optional

import gradio as gr
from textblob import TextBlob


# In-memory event log for this server process
EVENT_LOG: List[Dict] = []


def analyze_text(text: str, threshold: float):
    text = (text or "").strip()
    if not text:
        return {
            "label": "",
            "score": 0.0,
            "alert": False,
            "message": "Please enter some text to analyze.",
            "log": EVENT_LOG,
            "error": None,
        }

    try:
        # Use TextBlob for sentiment analysis
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity  # -1 (negative) to 1 (positive)
        
        # Convert to 0-1 scale
        score = (polarity + 1) / 2  # 0-1 scale
        
        # Determine label
        if polarity > 0.1:
            label = "POSITIVE"
        elif polarity < -0.1:
            label = "NEGATIVE"
        else:
            label = "NEUTRAL"
        
        ts = datetime.utcnow().isoformat() + "Z"
        entry = {"timestamp": ts, "text": text, "label": label, "score": score}
        EVENT_LOG.append(entry)

        alert = score >= threshold
        message = f"{label} ({score:.2f})"
        
        return {
            "label": label,
            "score": score,
            "alert": alert,
            "message": message,
            "log": EVENT_LOG,
            "error": None,
        }
    except Exception as e:
        error_msg = str(e)
        return {
            "label": "",
            "score": 0.0,
            "alert": False,
            "message": "",
            "log": EVENT_LOG,
            "error": error_msg,
        }


def export_log_csv() -> Optional[str]:
    if not EVENT_LOG:
        return None
    fd, path = tempfile.mkstemp(suffix=".csv")
    os.close(fd)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "text", "label", "score"])
        writer.writeheader()
        for row in EVENT_LOG:
            writer.writerow(row)
    return path


def create_app() -> gr.Blocks:
    with gr.Blocks() as demo:
        gr.Markdown("# Live Sentiment Demo\n\nType text and see sentiment label + confidence score.\nUses TextBlob for fast, lightweight sentiment analysis (no model downloads needed).")

        with gr.Row():
            with gr.Column(scale=2):
                txt = gr.Textbox(lines=4, placeholder="Type here...", label="Input text")
                threshold = gr.Slider(minimum=0.0, maximum=1.0, value=0.6, step=0.01, label="Alert threshold (score)")
                submit = gr.Button("Analyze")
                export_btn = gr.Button("Export Log (CSV)")
                download_file = gr.File(label="Download CSV")

            with gr.Column(scale=1):
                out_msg = gr.Markdown("---")
                log_table = gr.Dataframe(headers=["timestamp", "text", "label", "score"], label="Event Log")

        how_it_works = gr.Markdown(
            """
**How it works**

- Input text is analyzed using **TextBlob**, a lightweight sentiment analysis library.
- Analyzes polarity: negative (-1 to 0), neutral (~0), positive (0 to 1).
- Scores are normalized to 0-1 scale with labels: NEGATIVE, NEUTRAL, or POSITIVE.
- Entries are appended to a session event log with timestamps.
- If the score exceeds the alert threshold, the UI marks the result as an alert.

Benefits: Fast, no model downloads, no internet dependency, works offline.
"""
        )

        def _analyze(text, thr):
            res = analyze_text(text, thr)
            
            # If there's an error, display it prominently
            if res.get("error"):
                md = f"<span style='color:red;font-weight:700'>❌ ERROR</span><br/>{res['error']}"
                return md, []
            
            md = f"**Result:** {res['message']}"
            if res["alert"]:
                md = f"<span style='color:red;font-weight:700'>ALERT</span> — {md}"
            # show latest 100 events
            log = res["log"][-100:]
            table_rows = [[r["timestamp"], r["text"], r["label"], f"{r['score']:.3f}"] for r in log]
            return md, table_rows

        def _export():
            path = export_log_csv()
            return path

        submit.click(_analyze, inputs=[txt, threshold], outputs=[out_msg, log_table])
        export_btn.click(_export, inputs=None, outputs=download_file)

    return demo


if __name__ == "__main__":
    app = create_app()
    app.launch(server_name="0.0.0.0", server_port=7860)
