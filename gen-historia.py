#!/usr/bin/env python3
"""Generuje historia.html — historię wersji i budowy aplikacji Święto Wina.

Źródło prawdy: CHANGELOG.md (opisy wersji) + historia gita (co dzień się działo).
Uruchomienie: python3 gen-historia.py   (w katalogu repo)
Po zmianach w CHANGELOG.md odpal ponownie i wypchnij — kafelek sam się zaktualizuje.
"""
import html
import re
import subprocess
from collections import OrderedDict

import sys

# Tryb lokalny: python3 gen-historia.py --local <sciezka-wyjsciowa>
# Wersja lokalna lezy obok centrum.html, wiec powrot moze byc TWARDYM linkiem
# do centrum — nie zalezy od historii przegladarki ani od GitHub Pages.
LOCAL = "--local" in sys.argv
OUT = (sys.argv[sys.argv.index("--local") + 1] if LOCAL else "historia.html")


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True).stdout.strip()


# ── dane z gita ──────────────────────────────────────────────────────────
commits = []
for line in git("log", "--reverse", "--pretty=%ad|%h|%s", "--date=short").split("\n"):
    if "|" in line:
        d, h, s = line.split("|", 2)
        commits.append((d, h, s))

tags = OrderedDict()
for t in git("tag", "--sort=creatordate").split("\n"):
    if t:
        tags[t] = git("log", "-1", "--pretty=%ad", "--date=short", t)

by_day = OrderedDict()
for d, h, s in commits:
    by_day.setdefault(d, []).append((h, s))


# ── markdown-lite → html ─────────────────────────────────────────────────
def md(text):
    t = html.escape(text)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    return t


def parse_changelog(path="CHANGELOG.md"):
    """Zwraca listę (naglowek, [linie tresci]) dla każdej sekcji '## '."""
    try:
        raw = open(path, encoding="utf-8").read()
    except FileNotFoundError:
        return []
    sections, cur = [], None
    for line in raw.split("\n"):
        if line.startswith("## "):
            if cur:
                sections.append(cur)
            cur = (line[3:].strip(), [])
        elif cur is not None:
            cur[1].append(line)
    if cur:
        sections.append(cur)
    return sections


def render_body(lines):
    out, in_ul = [], False
    for ln in lines:
        s = ln.strip()
        if s in ("", "---"):
            if in_ul:
                out.append("</ul>")
                in_ul = False
            continue
        if s.startswith("### "):
            if in_ul:
                out.append("</ul>")
                in_ul = False
            out.append(f'<h4>{md(s[4:])}</h4>')
        elif s.startswith("- "):
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{md(s[2:])}</li>")
        else:
            if in_ul:
                out.append(f"<li class=cont>{md(s)}</li>")
            else:
                out.append(f"<p>{md(s)}</p>")
    if in_ul:
        out.append("</ul>")
    return "\n".join(out)


# ── skład strony ─────────────────────────────────────────────────────────
sections = parse_changelog()
wersje = [(h, b) for h, b in sections if h.lower().startswith(("v", "wersja"))]
biezaca = wersje[0][0].split("—")[0].strip() if wersje else "—"

CSS = """
:root{--bg:#0d0b10;--s1:#17131c;--s2:#1f1a26;--s3:#282130;--border:#332b3d;
--text:#ece7f2;--muted:#9b8fa8;--gold:#c8a84b;--gold2:#8a7433;--wine:#8b2030;--wine2:#c4485c;--green:#4ea36b;
--r:16px;--rsm:10px}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);
font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;line-height:1.6}
.wrap{max-width:880px;margin:0 auto;padding:28px 18px 70px}
h1{font-family:Georgia,serif;font-size:30px;margin:0 0 6px;color:var(--gold);font-weight:400}
.sub{color:var(--muted);font-size:14px;margin-bottom:26px}
.pill{display:inline-block;background:var(--s3);border:1px solid var(--gold2);color:var(--gold);
border-radius:999px;padding:4px 13px;font-size:12px;font-weight:700;margin-right:7px}
.karta{background:var(--s1);border:1px solid var(--border);border-radius:var(--r);
padding:20px 22px;margin:0 0 16px;position:relative}
.karta.teraz{border-color:var(--gold2);box-shadow:0 0 0 1px rgba(200,168,75,.18)}
.karta h3{font-family:Georgia,serif;font-size:19px;margin:0 0 4px;color:var(--gold);font-weight:400}
.data{color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:.6px;margin-bottom:12px}
.karta h4{font-size:12px;text-transform:uppercase;letter-spacing:.7px;color:var(--muted);
margin:16px 0 7px;font-weight:700}
.karta p{margin:8px 0;font-size:14px}
ul{margin:8px 0;padding-left:20px}
li{font-size:14px;margin:5px 0}
li.cont{list-style:none;margin-left:-6px;color:var(--muted);font-size:13px}
code{background:var(--s3);border-radius:5px;padding:1px 6px;font-size:12.5px;
font-family:ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--gold)}
strong{color:#fff}
h2.sekcja{font-family:Georgia,serif;font-size:22px;color:var(--gold);font-weight:400;
margin:40px 0 8px;border-top:1px solid var(--border);padding-top:26px}
details{background:var(--s1);border:1px solid var(--border);border-radius:var(--rsm);
padding:11px 15px;margin:8px 0}
details.karta{padding:14px 18px;margin:0 0 10px;border-radius:var(--r)}
details.karta summary{display:flex;flex-wrap:wrap;align-items:center;gap:10px;font-size:15px}
details.karta .wname{font-family:Georgia,serif;font-size:18px;color:var(--gold);font-weight:400}
details.karta .wdata{color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:.6px}
details.karta[open] .tresc{border-top:1px solid var(--border);margin-top:12px;padding-top:12px}
details.karta p.lead{color:var(--text);font-size:14px;margin:0 0 6px}
details.karta:hover{border-color:var(--gold2)}
summary{cursor:pointer;font-size:14px;font-weight:600;color:var(--text);outline:none}
summary::marker{color:var(--gold)}
details .lc{color:var(--muted);font-weight:400;font-size:12.5px}
.commit{font-size:13px;color:var(--muted);margin:6px 0 6px 4px;display:flex;gap:9px}
.commit .h{font-family:ui-monospace,Menlo,monospace;color:var(--gold2);flex:0 0 58px}
.stat{display:flex;flex-wrap:wrap;gap:10px;margin:22px 0 8px}
.stat div{background:var(--s1);border:1px solid var(--border);border-radius:var(--rsm);
padding:12px 16px;min-width:120px;flex:1}
.stat b{display:block;font-size:22px;color:var(--gold);font-family:Georgia,serif;font-weight:400}
.stat span{font-size:11px;text-transform:uppercase;letter-spacing:.6px;color:var(--muted)}
a{color:var(--gold)}
.powrot{display:inline-block;margin-bottom:20px;font-size:13px;color:var(--muted);text-decoration:none}
.powrot:hover{color:var(--gold)}
.stopka{margin-top:36px;padding-top:18px;border-top:1px solid var(--border);
color:var(--muted);font-size:12px}
@media(max-width:520px){h1{font-size:24px}.wrap{padding:20px 14px 60px}}
"""

parts = [
    "<!DOCTYPE html><html lang=pl><head><meta charset=UTF-8>",
    '<meta name=viewport content="width=device-width,initial-scale=1">',
    "<title>Historia wersji — Święto Wina 🍷</title>",
    f"<style>{CSS}</style></head><body><div class=wrap>",
    ('<a class=powrot href="centrum.html">← wróć do Centrum dowodzenia</a>'
     if LOCAL else
     '<a class=powrot href="./" onclick="if(history.length>1){history.back();return false}">'
     '← wróć</a>'),
    "<h1>🍷 Historia Święta Wina</h1>",
    f'<div class=sub>Jak ta aplikacja powstawała — wersja po wersji, od pierwszego dnia do dziś. '
    f'Aktualnie: <strong>{html.escape(biezaca)}</strong></div>',
    "<div class=stat>",
    f"<div><b>{len(commits)}</b><span>zmian w kodzie</span></div>",
    f"<div><b>{len(by_day)}</b><span>dni pracy</span></div>",
    f"<div><b>{len(wersje)}</b><span>opisanych wersji</span></div>",
    f"<div><b>{commits[0][0] if commits else '—'}</b><span>pierwszy commit</span></div>",
    "</div>",
    '<h2 class=sekcja>Wersje</h2>',
    '<p class=sub>Kliknij wersję, żeby rozwinąć szczegóły.</p>',
]

for i, (head, body) in enumerate(wersje):
    m = re.match(r"^(v[\d.]+[^—]*)—\s*([\d-]+)\s*—?\s*(.*)$", head)
    if m:
        nazwa, data, opis = m.group(1).strip(), m.group(2), m.group(3)
    else:
        m2 = re.match(r"^(.+?)—\s*(maj 2026|[\d-]+)\s*—?\s*(.*)$", head)
        if m2:
            nazwa, data, opis = m2.group(1).strip(), m2.group(2), m2.group(3)
        else:
            nazwa, data, opis = head, "", ""
    tag_name = nazwa.split()[0]
    pills = ""
    if tag_name in tags:
        pills += f'<span class=pill>tag {html.escape(tag_name)}</span>'
    if i == 0:
        pills += "<span class=pill>aktualna</span>"
    # zwijane: w zamkniętym stanie widać tylko nazwę i datę
    parts.append(f'<details class="karta{" teraz" if i == 0 else ""}">')
    parts.append(f'<summary><span class=wname>{html.escape(nazwa)}</span>'
                 f'<span class=wdata>{html.escape(data)}</span>{pills}</summary>')
    parts.append('<div class=tresc>')
    if opis:
        parts.append(f'<p class=lead>{md(opis)}</p>')
    parts.append(render_body(body))
    parts.append("</div></details>")

parts.append('<h2 class=sekcja>Dzień po dniu</h2>')
parts.append('<p class=sub>Pełny ślad z gita — każda zmiana, jaka weszła do aplikacji. '
             'Kliknij dzień, żeby rozwinąć.</p>')

for d in reversed(list(by_day.keys())):
    lista = by_day[d]
    parts.append(f'<details><summary>{d} <span class=lc>· {len(lista)} '
                 f'{"zmiana" if len(lista) == 1 else "zmian"}</span></summary>')
    for h, s in lista:
        parts.append(f'<div class=commit><span class=h>{h}</span><span>{html.escape(s)}</span></div>')
    parts.append("</details>")

parts.append('<div class=stopka>Strona generowana skryptem <code>gen-historia.py</code> '
             'z pliku <code>CHANGELOG.md</code> i historii gita. '
             'Repozytorium: <a href="https://github.com/sztukson/swieto-wina">sztukson/swieto-wina</a>.</div>')
parts.append("</div></body></html>")

open(OUT, "w", encoding="utf-8").write("\n".join(parts))
print(f"{OUT}: {len(wersje)} wersji, {len(commits)} commitów, {len(by_day)} dni")
