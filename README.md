# Aura: Smart Webpage Summarizer

## Overview

Aura is a browser-based tool designed to simplify how users consume long-form web content. It consists of a Chrome Extension connected to a FastAPI backend that analyzes any webpage and generates a structured summary.

The system extracts the main content of a webpage, processes it using AI and text analysis techniques, and presents the result in a concise and interactive format. Instead of manually scanning large blocks of text, users can quickly understand the core ideas and navigate directly to relevant sections.

---

## Purpose

Modern webpages often contain excessive information, advertisements, and distractions, making it difficult to identify key insights quickly.

Aura is built to:
- Reduce time spent reading lengthy content  
- Improve information accessibility  
- Provide structured summaries for faster understanding  
- Enable direct navigation to important parts of a webpage 

This project demonstrates how AI and web technologies can be combined to improve content consumption efficiency.

---

## Features

- Automatic extraction of main webpage content  
- AI-assisted summarization  
- Key bullet point generation  
- Estimated reading time calculation  
- Community-based metrics (average time spent and visit count)  
- Click-to-scroll navigation to relevant sections of the page  

---

## Tech Stack

### Backend
- FastAPI (Python) — API framework  
- Transformers (HuggingFace) — summarization model  
- BeautifulSoup — HTML parsing and cleaning  
- Newspaper3k — article content extraction  
- Uvicorn — ASGI server  

### Frontend (Extension)
- JavaScript  
- Chrome Extension APIs  

---

## How to Run

### Backend Setup
cd aura-backend
pip install -r requirements.txt
uvicorn main:app --reload


---

### Chrome Extension Setup

1. Open Chrome  
2. Navigate to chrome://extensions/
3. Enable Developer Mode  
4. Click "Load unpacked"  
5. Select the `aura-extension` folder  

---

## Usage

1. Open any webpage in Chrome  
2. Click on the Aura AI extension icon  
3. Click "Summarize Page"  
4. View the generated summary and bullet points  
5. Click on any bullet point to navigate to the corresponding section of the page  

---

## Limitations

- The backend must be running locally for the extension to function  
- Some websites may not be fully supported due to dynamic content or anti-scraping mechanisms  
  


---

## Environment Configuration

The `.env` file is not included in this repository for security reasons. Any sensitive configuration such as API keys should be stored in this file locally.

---

## Conclusion

Aura AI is a full-stack project that integrates backend development, AI-based text processing, web scraping, and browser extension development. It provides a practical solution for improving how users interact with and understand online content while demonstrating real-world application of modern technologies.
