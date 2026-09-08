"""Extraction du texte d'œuvres depuis fr.wikisource.org.

Wikisource balise son propre chrome avec la classe `ws-noexport` : on s'appuie
dessus plutôt que sur des heuristiques. Les numéros de page (`ws-pagenum`) sont
CONSERVÉS comme ancres [[p.N]] — ce sont eux qui rendent solubles les questions
à référence exacte, et les jeter est l'erreur d'ingestion classique.
"""
from __future__ import annotations
import html as _html, json, re, subprocess, time, urllib.parse
from html.parser import HTMLParser

API = "https://fr.wikisource.org/w/api.php"
UA = "pocllm-research/0.1 (personal RAG evaluation; anthonygosme@gmail.com)"
DELAY = 1.0                      # sérialisé et throttlé, étiquette API Wikimedia
SKIP_TAGS = {"script", "style", "sup", "table"}


class WSExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self._skip = 0
        self._skip_tag: str | None = None
        self._depth = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get("class", "")
        if self._skip:
            if tag == self._skip_tag:
                self._depth += 1
            return
        if tag in SKIP_TAGS or "ws-noexport" in cls or "Z3988" in cls:
            self._skip, self._skip_tag, self._depth = 1, tag, 1
            return
        if "ws-pagenum" in cls:                      # ancre de pagination
            # `id` porte le numéro IMPRIMÉ ; `title` ne porte que la page de scan
            # ("...1762a.djvu/13"), qu'on ne garde qu'en repli.
            n = str(a.get("id") or "").strip()
            if not n.isdigit():
                m = re.search(r"/(\d+)\s*$", str(a.get("title") or ""))
                n = m.group(1) if m else ""
            if n:
                self.out.append(f" [[p.{n}]] ")
            return
        if tag in ("p", "div", "br", "li", "dd", "blockquote") or re.fullmatch(r"h[1-6]", tag or ""):
            self.out.append("\n")
        if re.fullmatch(r"h[1-6]", tag or ""):
            self.out.append("\n" + "#" * int(tag[1]) + " ")

    def handle_endtag(self, tag):
        if self._skip:
            if tag == self._skip_tag:
                self._depth -= 1
                if self._depth <= 0:
                    self._skip, self._skip_tag = 0, None
            return
        if tag in ("p", "div", "li", "blockquote") or re.fullmatch(r"h[1-6]", tag or ""):
            self.out.append("\n")

    def handle_data(self, data):
        if not self._skip:
            self.out.append(data)

    def text(self) -> str:
        t = _html.unescape("".join(self.out))
        t = re.sub(r"[ \t]+", " ", t)
        t = re.sub(r" *\n *", "\n", t)
        return re.sub(r"\n{3,}", "\n\n", t).strip()


def _api(params: dict) -> dict:
    url = API + "?" + urllib.parse.urlencode({**params, "format": "json", "formatversion": "2"})
    r = subprocess.run(["curl", "-sS", "-m", "45", "-A", UA, url],
                       capture_output=True, text=True)
    time.sleep(DELAY)
    try:
        return json.loads(r.stdout or "{}")
    except json.JSONDecodeError:
        return {}


def resolve(title: str) -> str:
    """Suit les redirections. Beaucoup d'œuvres pointent vers une édition datée
    (« Fondements... » -> « Fondements... (trad. Delbos) ») : sans cette étape,
    l'œuvre paraît vide alors qu'elle est intégralement présente."""
    d = _api({"action": "query", "titles": title, "redirects": "1"})
    q = d.get("query", {})
    for r in q.get("redirects", []) or []:
        if r.get("from") == title:
            return r.get("to", title)
    pages = q.get("pages", []) or []
    return pages[0].get("title", title) if pages else title


def page_text(title: str) -> str:
    d = _api({"action": "parse", "page": title, "prop": "text", "redirects": "1"})
    h = d.get("parse", {}).get("text")
    if not h:
        return ""
    p = WSExtractor()
    p.feed(h)
    return p.text()


def subpages(work: str, limit: int = 500) -> list[str]:
    """Sous-pages d'une œuvre = ses unités canoniques (chapitre, livre, section)."""
    work = resolve(work)
    out, cont = [], None
    while True:
        params = {"action": "query", "list": "allpages", "apprefix": work + "/",
                  "apnamespace": "0", "aplimit": str(min(limit, 500))}
        if cont:
            params["apcontinue"] = cont
        d = _api(params)
        out += [p["title"] for p in d.get("query", {}).get("allpages", [])]
        cont = d.get("continue", {}).get("apcontinue")
        if not cont or len(out) >= limit:
            break
    return out


def category_members(cat: str, limit: int = 500) -> list[str]:
    d = _api({"action": "query", "list": "categorymembers", "cmtitle": f"Catégorie:{cat}",
              "cmnamespace": "0", "cmlimit": str(limit)})
    return [p["title"] for p in d.get("query", {}).get("categorymembers", [])]
