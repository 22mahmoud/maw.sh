from io import BytesIO
from urllib.parse import urlparse

import bleach
import markdown
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from PIL import Image

from src.base.blocks.codeblock import highlight_code_with_shiki


def allow_src(_, name, value):
    if name in ("alt", "height", "width"):
        return True
    if name == "src":
        p = urlparse(value)
        allowed_domains = (".giphy.com", ".tenor.com", ".imgur.com")
        return not p.netloc or any(p.netloc.endswith(domain) for domain in allowed_domains)

    return False


ALLOWED_ATTRS = {"a": ["href"], "img": allow_src, "code": ["class"]}
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

    sanitized_html = bleach.clean(
        html_output,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRS,
        strip=True,
    )

    soup = BeautifulSoup(sanitized_html, "html.parser")

    for pre in soup.find_all("pre"):
        if not isinstance(pre, Tag):
            continue

        code = pre.code
        if not isinstance(code, Tag):
            continue

        raw_code = code.get_text()
        lang_class = code.get("class") or []
        language = "plaintext"

        for cls in lang_class:
            if cls.startswith("language-"):
                language = cls.replace("language-", "")
                break

        try:
            highlighted_html = highlight_code_with_shiki(raw_code, language)
            highlighted_fragment = BeautifulSoup(highlighted_html, "html.parser")
            pre.replace_with(highlighted_fragment)
        except Exception as e:
            print(f"[CODE HIGHLIGHT ERROR] lang={language}: {e}")
            continue

    for img in soup.find_all("img"):
        if not isinstance(img, Tag):
            continue

        src_raw = img.get("src")
        if not isinstance(src_raw, str):
            continue

        src: str = src_raw
        user_width = img.get("width")
        user_height = img.get("height")

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

            if not user_width:
                img["width"] = str(image.width)
            if not user_height:
                img["height"] = str(image.height)

            img["loading"] = "lazy"
            img["decoding"] = "async"
        except Exception as e:
            print(f"[IMG ERROR] src={src} — {type(e).__name__}: {e}")
            pass

    return str(soup)
