import requests
from bs4 import BeautifulSoup

BASE_URL = "https://jreda.com/"

def fetch_website_content():
    try:
        response = requests.get(BASE_URL, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unwanted elements
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)

        # Limit text size to prevent token overflow
        return text[:6000]

    except Exception as e:
        return "Website content unavailable."
