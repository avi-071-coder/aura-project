from newspaper import Article
from bs4 import BeautifulSoup


def scrape_text(url: str) -> dict:
    try:
        article = Article(url)
        article.download()
        article.parse()

        text = article.text
        html = article.html

        # Fallback cleaning if needed
        if not text or len(text) < 200:
            soup = BeautifulSoup(article.html, "html.parser")

            for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
                tag.decompose()

            text = soup.get_text(separator=" ", strip=True)

        return {
            "text": text[:6000],
            "html": html
        }

    except Exception as e:
        return {
            "text": f"Error: {e}",
            "html": ""
        }