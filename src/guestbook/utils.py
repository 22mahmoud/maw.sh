from io import BytesIO
from urllib.parse import urlparse

import bleach
import markdown
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from PIL import Image


def allow_src(_, name, value):
    if name in ("alt", "height", "width"):
        return True
    if name == "src":
        p = urlparse(value)
        allowed_domains = (".giphy.com", ".tenor.com", ".imgur.com")
        return not p.netloc or any(
            p.netloc.endswith(domain) for domain in allowed_domains
        )

    return False


ALLOWED_ATTRS = {"a": ["href"], "img": allow_src}
ALLOWED_TAGS = [
    "p",
    "br",
    "strong",
    "em",
    "code",
    "pre",
    "ul",
    "ol",
    "li",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "img",
]


def render_guestbook_markdown(value):
    md = markdown.Markdown(extensions=["fenced_code"])
    html_output = md.convert(value)

    soup = BeautifulSoup(html_output, "html.parser")

    for img in soup.find_all("img"):
        if not isinstance(img, Tag):
            continue

        src_raw = img.get("src")

        if not isinstance(src_raw, str):
            continue

        src: str = src_raw

        try:
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/115.0.0.0 Safari/537.36 GuestbookBot/1.0"
                ),
                "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "identity",
            }
            response = requests.get(src, headers=headers, timeout=5)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))

            img["width"] = str(image.width)
            img["height"] = str(image.height)
        except Exception as e:
            print(f"[IMG ERROR] src={src} — {type(e).__name__}: {e}")
            pass

    html_with_dimensions = str(soup)

    clean_html = bleach.clean(
        html_with_dimensions,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRS,
        strip=True,
    )

    return clean_html
