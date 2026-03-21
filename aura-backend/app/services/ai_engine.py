import re
from heapq import nlargest
from bs4 import BeautifulSoup

# OPTIONAL lightweight AI (only used for small text)
try:
    from transformers import pipeline
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
except:
    summarizer = None


def clean_sentences(text):
    sentences = re.split(r'\.\s+', text)
    return [s.strip() for s in sentences if len(s.strip()) > 40]


def extractive_summary(text):
    sentences = clean_sentences(text)

    # Score sentences by length + keyword density
    word_freq = {}
    words = re.findall(r'\w+', text.lower())

    for word in words:
        if len(word) > 3:
            word_freq[word] = word_freq.get(word, 0) + 1

    scores = []
    for s in sentences:
        score = sum(word_freq.get(w.lower(), 0) for w in s.split())
        scores.append((score, s))

    top_sentences = [s for _, s in nlargest(5, scores)]

    return top_sentences


def generate_summary(text: str, html: str) -> dict:
    if not text.strip():
        return {
            "summary": "No content",
            "bullets": [],
            "estimated_read_time": "0 min",
            "anchors": []
        }

    # 🔥 FAST extractive summary
    bullets = extractive_summary(text)

    # 🔥 OPTIONAL AI refinement (ONLY if short text)
    if summarizer and len(text.split()) < 800:
        try:
            ai_result = summarizer(text[:800], max_length=80, min_length=30, do_sample=False)
            summary = ai_result[0]["summary_text"]
        except:
            summary = " ".join(bullets[:3])
    else:
        summary = " ".join(bullets[:3])

    # Anchors (lightweight)
    anchors = []
    if html:
        soup = BeautifulSoup(html, "html.parser")
        for b in bullets:
            el = soup.find(lambda tag: tag.name in ['p','h1','h2'] and b[:20].lower() in tag.get_text().lower())
            if el:
                selector = f"#{el.get('id')}" if el.get('id') else el.name
                anchors.append({"text": b, "selector": selector})

    read_time = f"{max(1, len(text.split()) // 200)} min"

    return {
        "summary": summary,
        "bullets": bullets[:5],
        "estimated_read_time": read_time,
        "anchors": anchors
    }