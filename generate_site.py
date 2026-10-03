#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, re, html as htmlmod, pathlib, datetime

SRC_JSON = pathlib.Path(r"d:\Users\MMCabo\Documents\Proyecto predeterminado\curso_redes_contenido.json")
OUT_DIR = pathlib.Path(r"d:\Users\MMCabo\Documents\Proyecto predeterminado\REDV")

raw = json.loads(SRC_JSON.read_text(encoding="utf-8"))
by_label = {}
for e in raw:
    lbl = e["label"]
    if lbl not in by_label or len(e.get("texts",[])) > len(by_label[lbl].get("texts",[])):
        by_label[lbl] = e

ORDER = [
    ("UNIDAD I", [
        ("1.1 Objetivos de Aprendizaje I", "U1 - Objetivos de Aprendizaje 1", "objetivos-aprendizaje-1"),
        ("1.2 Evolución Histórica de las Redes", "U1 - Evolucion Historica de las Redes", "evolucion-historica"),
        ("1.3 Capa 1: Física", "U1 - Modelo OSI/TCP-IP - Capa 1 Física", "capa-1-fisica"),
        ("1.4 Actividad — Capa 1", "U1 - A. Aprendizaje 1er Capa", "actividad-capa-1"),
        ("1.5 Capa 2: Enlace de Datos", "U1 - Capa 2 Enlace de Datos", "capa-2-enlace"),
        ("1.6 Actividad — Capa 2", "U1 - A. Aprendizaje 2da Capa", "actividad-capa-2"),
        ("1.7 Capa 3: Red", "U1 - Capa 3 Red", "capa-3-red"),
        ("1.8 Actividad — Capa 3", "U1 - A. Aprendizaje 3er Capa", "actividad-capa-3"),
        ("1.9 Capa 4: Transporte", "U1 - Capa 4 Transporte", "capa-4-transporte"),
        ("1.10 Actividad — Capa 4", "U1 - A. Aprendizaje 4ta Capa", "actividad-capa-4"),
        ("1.11 Capas 5–7: Sesión, Presentación y Aplicación", "U1 - Capas 5-7 Sesion/Presentacion/Aplicacion", "capas-5-7"),
        ("1.12 Actividad — Capas 5/6/7", "U1 - A. Aprendizaje 5,6,7 Capas", "actividad-capas-567"),
        ("1.13 Examen — Capa 1 Física", "U1 - Examen ISO Capa 1 Fisica", "examen-capa-1"),
        ("1.14 Examen — Capa 2 Enlace", "U1 - Examen ISO Capa 2 Enlace", "examen-capa-2"),
        ("1.15 Examen — Capa 3 Red", "U1 - Examen ISO Capa 3 Red", "examen-capa-3"),
    ]),
    ("UNIDAD II", [
        ("2.1 Punto a Punto", "U2 - Topologia Punto a Punto", "punto-a-punto"),
        ("2.2 Topología Bus", "U2 - Topologia Bus", "topologia-bus"),
        ("2.3 Topología Anillo", "U2 - Topologia Anillo", "topologia-anillo"),
        ("2.4 Topología Estrella", "U2 - Topologia Estrella", "topologia-estrella"),
        ("2.5 Topología Malla", "U2 - Topologia Malla", "topologia-malla"),
        ("2.6 Topología Híbrida", "U2 - Topologia Hibrida", "topologia-hibrida"),
        ("2.7 Física vs Lógica", "U2 - Topologia Fisica vs Logica", "fisica-vs-logica"),
        ("2.8 Evaluación — Topologías", "U2 - Evaluacion Topologias", "evaluacion-topologias"),
        ("2.9 Medios de Transmisión", "U2 - Medios de Transmision", "medios-transmision"),
        ("2.10 Tendencias Actuales", "U2 - Tendencias actuales en redes", "tendencias-actuales"),
        ("2.11 Componentes de Red LAN", "U2 - Componentes de una red LAN", "componentes-lan"),
    ]),
    ("UNIDAD III", [
        ("3.1 Cableado Ethernet RJ45", "U3 - Cableado Ethernet RJ45", "cableado-rj45"),
        ("3.2 Redes Virtuales (VLAN)", "U3 - Redes Virtuales", "redes-virtuales"),
        ("3.3 Presupuesto Red LAN", "U3 - Presupuesto para red LAN", "presupuesto-lan"),
        ("3.4 Wi-Fi 6 vs Wi-Fi 5", "U3 - Comparativas WiFi 6 vs WiFi 5", "wifi6-vs-wifi5"),
    ]),
    ("PROGRAMACIÓN LÓGICA", [
        ("4.1 Estructura Lógica", "PROG - Estructura Logica", "estructura-logica"),
        ("4.2 Ejercicios Secuencia Lógica", "PROG - Ejercicios Secuencia Logica", "ejercicios-secuencia"),
        ("4.3 Diagramas de Flujo", "PROG - Diagramas de Flujo", "diagramas-flujo"),
    ]),
]

def clean_texts(entry):
    texts = entry.get("texts",[]) if entry else []
    cleaned=[]
    seen=set()
    for t in texts:
        txt=re.sub(r"\s+"," ",t["text"]).strip()
        if not txt or len(txt)<3: continue
        if txt in ("Page updated","Google Sites","Report abuse","Skip to main content","Skip to navigation"): continue
        norm=txt.lower()
        if norm in seen: continue
        # skip spans that are substring of longer kept
        is_sub=False
        for c in cleaned:
            if txt.lower() in c.lower() and len(txt) < len(c)*0.9 and t["tag"] in ("span","a","div"):
                is_sub=True; break
        if is_sub: continue
        seen.add(norm); cleaned.append(txt)
    out=[]
    for t in texts:
        txt=re.sub(r"\s+"," ",t["text"]).strip()
        if txt not in cleaned: continue
        if any(x["text"]==txt for x in out): continue
        out.append({"tag":t["tag"],"text":txt})
    return out

# Build slug map
slug_to_info = {}  # slug -> (group, title, label, entry, texts)
all_slugs = []
for group, items in ORDER:
    for title, label, slug in items:
        entry = by_label.get(label)
        texts = clean_texts(entry) if entry else []
        url = entry.get("url","") if entry else ""
        # handle tinyurl-only pages
        if len(texts)==1 and "tinyurl.com/MODULO-REDES-IV" in texts[0]["text"]:
            texts = [
                {"tag":"p","text":"Esta sección corresponde a una actividad / evaluación interactiva del módulo externo."},
                {"tag":"p","text":"Recurso: https://tinyurl.com/MODULO-REDES-IV (Módulo REDES IV – guías, prácticas y evaluaciones)."},
            ]
        slug_to_info[slug] = {"group":group,"title":title,"label":label,"entry":entry,"texts":texts,"url":url}
        all_slugs.append(slug)

def esc(s): return htmlmod.escape(s, quote=False)

def render_article(texts):
    if not texts:
        return '<p class="muted">[Contenido no disponible]</p>'
    out=[]
    for blk in texts:
        tag=blk["tag"]; txt=blk["text"].strip()
        if not txt: continue
        # classify
        # emoji headings -> h2
        if any(e in txt for e in ["🌐","🧠","🚚","🧊"]) and len(txt)<140:
            out.append(f'<h2 class="article-h2">{esc(txt)}</h2>'); continue
        if any(e in txt for e in ["🔍","🧱","📐","✅","📦","🖼️","🧪","🌐","🔄","🎙️","🧷","🛣️","📬"]) and tag in ("h3","p") and len(txt)<170:
            # subheading
            out.append(f'<h3 class="article-h3">{esc(txt)}</h3>'); continue
        if re.match(r"^(A\.|B\.|C\.|D\.|E\.)\s", txt) and len(txt)<140:
            out.append(f'<h3 class="article-h3 accent">{esc(txt)}</h3>'); continue
        if len(txt)<80 and re.match(r".+:$", txt) and tag in ("p","span","div"):
            out.append(f'<h3 class="article-h3">{esc(txt)}</h3>'); continue
        if tag=="li":
            # will be grouped in ul
            out.append(f'<li>{esc(txt)}</li>')
        else:
            # paragraph; handle quote-like
            if txt.startswith("🛣") or txt.startswith("📬") or txt.startswith("✉") or txt.startswith("🏢") or txt.startswith("💬") or txt.startswith("💡") or txt.startswith("📌"):
                out.append(f'<blockquote>{esc(txt)}</blockquote>')
            else:
                # bold before colon
                if ":" in txt and len(txt.split(":")[0])<40:
                    a,b = txt.split(":",1)
                    out.append(f'<p><strong>{esc(a)}:</strong>{esc(b)}</p>')
                else:
                    out.append(f'<p>{esc(txt)}</p>')
    # Group consecutive <li> into <ul>
    grouped=[]
    buf=[]
    def flush():
        nonlocal buf
        if buf:
            grouped.append('<ul class="article-list">\n' + "\n".join(buf) + '\n</ul>')
            buf=[]
    for el in out:
        if el.startswith("<li>"):
            buf.append(el)
        else:
            flush(); grouped.append(el)
    flush()
    return "\n".join(grouped)

# Create nav HTML helper
def nav_html(active_slug=None):
    parts=[]
    parts.append('<nav class="sidebar" id="sidebar" aria-label="Navegación principal">')
    parts.append('<div class="sidebar-head"><div class="brand"><span class="brand-dot"></span> REDES V</div><div class="brand-sub">Fundamentos de Redes</div></div>')
    parts.append('<div class="nav-groups">')
    for group, items in ORDER:
        parts.append(f'<div class="nav-group"><div class="nav-group-title">{esc(group)}</div><ul>')
        for title, label, slug in items:
            active = ' class="active"' if slug==active_slug else ''
            parts.append(f'<li><a href="{slug}.html"{active}>{esc(title)}</a></li>')
        parts.append('</ul></div>')
    parts.append('</div>')
    parts.append('<div class="sidebar-foot"><a href="index.html" class="foot-link">⌂ Inicio</a><a href="mapa.html" class="foot-link">🗺 Mapa del sitio</a><a href="../REDES_V_Libro_Curso_Redes_IV.pdf" class="foot-link">📖 Libro PDF</a><div class="foot-meta">Curso REDES IV → REDES V<br>© REDES V · 2026</div></div>')
    parts.append('</nav>')
    return "\n".join(parts)

def page_template(title, slug, article_html, url_orig="", prev_slug=None, next_slug=None):
    # Build prev/next
    idx = all_slugs.index(slug) if slug in all_slugs else -1
    prev_link = ""
    next_link = ""
    if idx>0:
        ps = all_slugs[idx-1]; info=slug_to_info[ps]
        prev_link = f'<a class="pager-btn prev" href="{ps}.html"><span>← Anterior</span><strong>{esc(info["title"])}</strong></a>'
    else:
        prev_link = '<span class="pager-btn disabled"><span>Inicio</span><strong>Sin anterior</strong></span>'
    if idx>=0 and idx < len(all_slugs)-1:
        ns = all_slugs[idx+1]; info=slug_to_info[ns]
        next_link = f'<a class="pager-btn next" href="{ns}.html"><span>Siguiente →</span><strong>{esc(info["title"])}</strong></a>'
    else:
        next_link = '<span class="pager-btn disabled"><span>Final</span><strong>Sin siguiente</strong></span>'

    return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)} — REDES V</title>
<meta name="description" content="{esc(title)} — Curso Fundamentos de Redes de Computadoras, REDES V.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="assets/styles.css">
</head>
<body>
<div class="layout">
{nav_html(slug)}
<main class="main">
<header class="topbar">
<button class="menu-btn" id="menuBtn" aria-label="Abrir menú">☰</button>
<div class="topbar-title">{esc(title)}</div>
<div class="topbar-actions">
<div class="search-wrap"><input id="searchBox" type="search" placeholder="Buscar en REDES V… ( / )" autocomplete="off"><div id="searchResults" class="search-results hidden"></div></div>
<a class="btn btn-ghost" href="index.html">Inicio</a>
<a class="btn btn-primary" href="../REDES_V_Libro_Curso_Redes_IV.pdf">PDF</a>
</div>
</header>
<div class="content">
<nav class="breadcrumb"><a href="index.html">Inicio</a> <span>›</span> <span>{esc(slug_to_info[slug]["group"]) if slug in slug_to_info else ""}</span> <span>›</span> <strong>{esc(title)}</strong></nav>
<article class="article">
<div class="article-head">
<div class="kicker">{esc(slug_to_info[slug]["group"]) if slug in slug_to_info else ""} · PÁGINA DEL SITIO ORIGINAL</div>
<h1>{esc(title)}</h1>
</div>
<div class="article-body">
{article_html}
</div>
{"<div class='source-box'>Fuente: <a href='"+esc(url_orig)+"'>"+esc(url_orig)+"</a></div>" if url_orig else ""}
<div class="pager">
{prev_link}
{next_link}
</div>
</article>
<footer class="footer">Material académico — Curso REDES V · <a href="https://sites.google.com/view/curso-redes-iv/inicio">Sitio original</a> · Libro base ordenado y paginado con índice</footer>
</div>
</main>
</div>
<div class="overlay hidden" id="overlay"></div>
<script src="assets/app.js"></script>
</body>
</html>'''

# Generate assets
assets_dir = OUT_DIR / "assets"
assets_dir.mkdir(parents=True, exist_ok=True)

# Write styles.css - professional navy/teal system
css = r"""
:root{
  --navy:#0F2A44; --navy-2:#0B1E33; --teal:#0E7C7B; --teal-2:#0A5F5E; --sky:#2A7FFF;
  --grey-900:#1A2332; --grey-800:#2B3440; --grey-600:#5A6575; --grey-400:#9AA6B8; --grey-200:#E6EAF0; --grey-100:#F2F4F7; --grey-50:#F8F9FB;
  --radius:14px; --radius-sm:10px; --shadow:0 10px 30px rgba(15,42,68,.12); --shadow-sm:0 4px 14px rgba(15,42,68,.08);
  --sidebar-w:300px; --topbar-h:58px;
  --font: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
}
*{box-sizing:border-box} html{scroll-behavior:smooth}
body{margin:0;font-family:var(--font);background:var(--grey-50);color:var(--grey-900);line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:var(--teal);text-decoration:none} a:hover{color:var(--teal-2);text-decoration:underline}
.layout{display:flex;min-height:100vh}
/* Sidebar */
.sidebar{width:var(--sidebar-w);background:var(--navy);color:#D6E2EF;position:fixed;inset:0 auto 0 0;display:flex;flex-direction:column;overflow:hidden;z-index:30;border-right:1px solid rgba(255,255,255,.08)}
.sidebar-head{padding:22px 20px 16px;border-bottom:1px solid rgba(255,255,255,.08);background:linear-gradient(180deg, var(--navy) 0%, var(--navy-2) 100%)}
.brand{font-weight:800;letter-spacing:.08em;font-size:13px;color:#fff;display:flex;align-items:center;gap:8px}
.brand-dot{width:8px;height:8px;border-radius:50%;background:var(--teal);box-shadow:0 0 0 6px rgba(14,124,123,.18);display:inline-block}
.brand-sub{font-size:11px;color:#9AB8C8;margin-top:4px;letter-spacing:.04em}
.nav-groups{flex:1;overflow:auto;padding:14px 10px 10px;scrollbar-width:thin}
.nav-group{margin-bottom:18px}
.nav-group-title{font-size:10px;letter-spacing:.10em;color:#7FA0B6;font-weight:700;margin:0 8px 8px;text-transform:uppercase}
.nav-groups ul{list-style:none;margin:0;padding:0}
.nav-groups li a{display:block;padding:7px 10px;border-radius:8px;color:#C9D8E8;font-size:13px;line-height:1.3}
.nav-groups li a:hover{background:rgba(255,255,255,.07);color:#fff;text-decoration:none}
.nav-groups li a.active{background:rgba(14,124,123,.95);color:#fff;box-shadow:0 4px 12px rgba(0,0,0,.18)}
.sidebar-foot{padding:14px 16px 16px;border-top:1px solid rgba(255,255,255,.08);background:rgba(0,0,0,.14)}
.foot-link{display:block;padding:7px 10px;border-radius:8px;background:rgba(255,255,255,.06);color:#D6E2EF;font-size:12px;margin-bottom:6px}
.foot-link:hover{background:rgba(255,255,255,.10);color:#fff;text-decoration:none}
.foot-meta{margin-top:10px;font-size:10px;color:#7FA0B6;line-height:1.4}
/* Main */
.main{flex:1;margin-left:var(--sidebar-w);min-width:0}
.topbar{height:var(--topbar-h);background:#fff;border-bottom:1px solid var(--grey-200);display:flex;align-items:center;gap:14px;padding:0 20px;position:sticky;top:0;z-index:10}
.topbar-title{font-weight:700;color:var(--navy);font-size:14px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.topbar-actions{margin-left:auto;display:flex;align-items:center;gap:10px}
.menu-btn{display:none;border:1px solid var(--grey-200);background:#fff;border-radius:8px;padding:7px 10px;font-size:16px;cursor:pointer}
.btn{padding:8px 14px;border-radius:10px;font-size:12px;font-weight:700;border:1px solid transparent;cursor:pointer;display:inline-flex;align-items:center;gap:6px}
.btn-ghost{background:#fff;border-color:var(--grey-200);color:var(--grey-800)} .btn-ghost:hover{background:var(--grey-100)}
.btn-primary{background:var(--teal);color:#fff} .btn-primary:hover{background:var(--teal-2);color:#fff;text-decoration:none}
/* Search */
.search-wrap{position:relative}
.search-wrap input{width:300px;max-width:38vw;padding:8px 12px;border-radius:10px;border:1px solid var(--grey-200);font-size:13px;background:var(--grey-50)}
.search-wrap input:focus{outline:none;border-color:var(--teal);background:#fff;box-shadow:0 0 0 3px rgba(14,124,123,.14)}
.search-results{position:absolute;top:calc(100% + 8px);right:0;left:0;background:#fff;border:1px solid var(--grey-200);border-radius:12px;box-shadow:var(--shadow);overflow:hidden;max-height:420px;overflow:auto}
.search-results.hidden{display:none}
.search-item{display:block;padding:10px 12px;border-bottom:1px solid var(--grey-100);color:inherit}
.search-item:hover{background:var(--grey-50);text-decoration:none}
.search-item strong{color:var(--navy);font-size:13px}
.search-item span{color:var(--grey-600);font-size:11px;display:block}
/* Content */
.content{max-width:860px;margin:0 auto;padding:28px 24px 40px}
.breadcrumb{font-size:12px;color:var(--grey-600);display:flex;align-items:center;gap:6px;flex-wrap:wrap;margin-bottom:14px}
.breadcrumb a{color:var(--grey-600)} .breadcrumb strong{color:var(--navy)}
.article{background:#fff;border:1px solid var(--grey-200);border-radius:var(--radius);box-shadow:var(--shadow-sm);overflow:hidden}
.article-head{padding:22px 24px 14px;background:linear-gradient(180deg, #fff 0%, #F8FBFB 100%);border-bottom:1px solid var(--grey-100)}
.kicker{font-size:10px;letter-spacing:.10em;color:var(--teal);font-weight:800;text-transform:uppercase;margin-bottom:6px}
.article-head h1{margin:0;color:var(--navy);font-size:22px;line-height:1.25}
.article-body{padding:18px 24px 8px}
.article-body p{margin:10px 0;font-size:14.5px;color:#1F2A3A}
.article-h2{margin:22px 0 8px;color:var(--navy);font-size:17px;line-height:1.3;border-left:4px solid var(--teal);padding-left:10px}
.article-h3{margin:18px 0 6px;color:#143A5A;font-size:13.5px}
.article-h3.accent{background:#EAF2F8;border-radius:8px;padding:8px 10px}
.article-list{margin:8px 0 14px 18px;color:#1F2A3A;font-size:14px}
.article-list li{margin:6px 0}
blockquote{margin:14px 0;padding:12px 14px;background:#F6FAFA;border-left:4px solid var(--teal);border-radius:0 10px 10px 0;color:#2E4A62;font-style:italic}
.source-box{margin:18px 24px 0;padding:10px 12px;background:var(--grey-100);border:1px solid var(--grey-200);border-radius:10px;font-size:11px;color:var(--grey-600);word-break:break-all}
.source-box a{color:var(--teal)}
.pager{display:flex;gap:12px;padding:16px 24px 20px}
.pager-btn{flex:1;display:flex;flex-direction:column;padding:12px 14px;border-radius:12px;border:1px solid var(--grey-200);background:var(--grey-50);color:inherit}
.pager-btn:hover{border-color:var(--teal);background:#fff;text-decoration:none}
.pager-btn span{font-size:11px;letter-spacing:.06em;color:var(--grey-600);font-weight:700;text-transform:uppercase}
.pager-btn strong{font-size:13px;color:var(--navy);margin-top:2px}
.pager-btn.next{text-align:right;align-items:flex-end}
.pager-btn.disabled{opacity:.55;pointer-events:none}
.footer{margin-top:18px;text-align:center;color:var(--grey-600);font-size:11px;padding:10px}
/* Cards (index) */
.hero{background:var(--navy);color:#D6E2EF;border-radius:var(--radius);padding:26px 24px;box-shadow:var(--shadow);position:relative;overflow:hidden}
.hero::after{content:"";position:absolute;inset:0;background:radial-gradient(600px 220px at 20% 0%, rgba(42,127,255,.22), transparent 60%), radial-gradient(700px 260px at 90% 10%, rgba(14,124,123,.22), transparent 60%);pointer-events:none}
.hero > *{position:relative}
.hero-kicker{font-size:10px;letter-spacing:.12em;color:#7FB8C8;font-weight:800}
.hero h1{margin:8px 0 10px;color:#fff;font-size:30px;line-height:1.15}
.hero p{margin:0;color:#C9E8E8;max-width:680px;font-size:14.5px}
.hero-actions{margin-top:16px;display:flex;gap:10px;flex-wrap:wrap}
.hero-actions .btn{padding:10px 16px;font-size:13px}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:18px}
.card{background:#fff;border:1px solid var(--grey-200);border-radius:var(--radius);box-shadow:var(--shadow-sm);overflow:hidden;display:flex;flex-direction:column}
.card-head{padding:14px 16px;background:linear-gradient(135deg, #0F2A44 0%, #143A5A 100%);color:#fff}
.card-head h3{margin:0;font-size:13px}
.card-head p{margin:4px 0 0;color:#9AB8C8;font-size:11px}
.card-body{padding:12px 14px;flex:1}
.card-body ul{margin:0;padding:0;list-style:none}
.card-body li{padding:7px 0;border-bottom:1px solid var(--grey-100);font-size:13px}
.card-body li:last-child{border-bottom:0}
.card-body li a{color:var(--grey-900)} .card-body li a:hover{color:var(--teal)}
.pill{display:inline-block;padding:2px 7px;border-radius:999px;background:var(--grey-100);border:1px solid var(--grey-200);font-size:10px;color:var(--grey-600);font-weight:700;letter-spacing:.04em}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:16px}
.stat{background:#fff;border:1px solid var(--grey-200);border-radius:12px;padding:12px;text-align:center}
.stat strong{color:var(--navy);font-size:18px;display:block}
.stat span{font-size:11px;color:var(--grey-600)}
/* Overlay */
.overlay{position:fixed;inset:0;background:rgba(8,18,32,.45);backdrop-filter:blur(2px);z-index:20}
.overlay.hidden{display:none}
/* Responsive */
@media (max-width: 980px){
  .grid{grid-template-columns:1fr 1fr}
  .stats{grid-template-columns:1fr 1fr}
  .search-wrap input{width:200px}
}
@media (max-width: 760px){
  .sidebar{transform:translateX(-100%);transition:transform .22s ease}
  .sidebar.open{transform:translateX(0)}
  .main{margin-left:0}
  .menu-btn{display:inline-flex}
  .content{padding:18px 16px 24px}
  .grid{grid-template-columns:1fr}
  .hero h1{font-size:24px}
  .pager{flex-direction:column}
}
.muted{color:var(--grey-600)}
code{background:var(--grey-100);border:1px solid var(--grey-200);padding:1px 5px;border-radius:6px;font-size:12px}
"""
(assets_dir / "styles.css").write_text(css, encoding="utf-8")

# app.js
js = r"""
const btn = document.getElementById('menuBtn');
const sidebar = document.getElementById('sidebar');
const overlay = document.getElementById('overlay');
function openMenu(){ sidebar?.classList.add('open'); overlay?.classList.remove('hidden');}
function closeMenu(){ sidebar?.classList.remove('open'); overlay?.classList.add('hidden');}
btn?.addEventListener('click', ()=> sidebar.classList.contains('open') ? closeMenu() : openMenu());
overlay?.addEventListener('click', closeMenu);
// Search
const idx = [
  {slug:'index', title:'Inicio — REDES V', group:'Inicio'},
  {slug:'mapa', title:'Mapa del sitio', group:'Anexo'},
"""
# add entries
for slug, info in slug_to_info.items():
    js += f"  {{slug:'{slug}', title:{json.dumps(info['title'], ensure_ascii=False)}, group:{json.dumps(info['group'], ensure_ascii=False)}}},\n"
js += r"""];
const box = document.getElementById('searchBox');
const res = document.getElementById('searchResults');
function renderResults(q){
  if(!q || q.length<2){ res.classList.add('hidden'); res.innerHTML=''; return;}
  q=q.toLowerCase();
  const hits = idx.filter(x=> (x.title.toLowerCase().includes(q) || x.group.toLowerCase().includes(q) || x.slug.includes(q))).slice(0,8);
  if(!hits.length){ res.innerHTML=`<div class="search-item"><strong>Sin resultados</strong><span>Prueba con “capa”, “topología”, “VLAN”</span></div>`; res.classList.remove('hidden'); return;}
  res.innerHTML = hits.map(h=> `<a class="search-item" href="${h.slug}.html"><strong>${h.title}</strong><span>${h.group} · ${h.slug}.html</span></a>`).join('');
  res.classList.remove('hidden');
}
box?.addEventListener('input', e=> renderResults(e.target.value));
box?.addEventListener('focus', e=> renderResults(e.target.value));
document.addEventListener('click', e=>{ if(!e.target.closest('.search-wrap')){ res?.classList.add('hidden'); }});
document.addEventListener('keydown', e=>{ if(e.key==='/' && document.activeElement!==box){ e.preventDefault(); box?.focus(); } if(e.key==='Escape'){ res?.classList.add('hidden'); closeMenu(); }});
// Progress: mark visited links (optional localStorage)
try{
  const v = JSON.parse(localStorage.getItem('redv_visited')||'[]');
  const cur = location.pathname.split('/').pop();
  if(cur && !v.includes(cur)){ v.push(cur); localStorage.setItem('redv_visited', JSON.stringify(v)); }
}catch(e){}
"""
(assets_dir / "app.js").write_text(js, encoding="utf-8")

# Build index.html (landing professional)
# Stats
total_pages = len(all_slugs)
stats_html = f"""
<div class="stats">
  <div class="stat"><strong>{total_pages}</strong><span>Páginas migradas</span></div>
  <div class="stat"><strong>4</strong><span>Bloques temáticos</span></div>
  <div class="stat"><strong>7</strong><span>Capas OSI</span></div>
  <div class="stat"><strong>2026</strong><span>Edición REDES V</span></div>
</div>
"""

# Build index content cards
def card_for(group, items):
    lis = []
    for title,label,slug in items:
        lis.append(f'<li><a href="{slug}.html">{htmlmod.escape(title)}</a></li>')
    return f"""
<div class="card">
  <div class="card-head"><h3>{htmlmod.escape(group)}</h3><p>{len(items)} páginas</p></div>
  <div class="card-body"><ul>{''.join(lis)}</ul></div>
</div>
"""

index_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>REDES V — Fundamentos de Redes de Computadoras</title>
<meta name="description" content="REDES V — Plataforma profesional del curso Fundamentos de Redes. Todo el contenido del Curso REDES IV reorganizado, con buscador, navegación por unidades y libro PDF.">
<link rel="stylesheet" href="assets/styles.css">
</head>
<body>
<div class="layout">
{nav_html(None)}
<main class="main">
<header class="topbar">
<button class="menu-btn" id="menuBtn" aria-label="Abrir menú">☰</button>
<div class="topbar-title">REDES V — Fundamentos de Redes</div>
<div class="topbar-actions">
<div class="search-wrap"><input id="searchBox" type="search" placeholder="Buscar en REDES V… ( / )" autocomplete="off"><div id="searchResults" class="search-results hidden"></div></div>
<a class="btn btn-ghost" href="mapa.html">Mapa</a>
<a class="btn btn-primary" href="../REDES_V_Libro_Curso_Redes_IV.pdf">📖 Libro PDF</a>
</div>
</header>
<div class="content">
<div class="hero">
<div class="hero-kicker">CURSO REDES IV → REDES V · EDICIÓN PROFESIONAL</div>
<h1>Fundamentos de Redes<br>de Computadoras</h1>
<p>Plataforma académica con calidad profesional. Todo el contenido del sitio original reorganizado por unidades, con navegación rápida, buscador y libro base paginado. Lista para clases, evaluaciones y migración completa a la nueva web.</p>
<div class="hero-actions">
<a class="btn btn-primary" href="capa-1-fisica.html">Empezar por Capa 1 →</a>
<a class="btn btn-ghost" style="background:#fff" href="mapa.html">Ver mapa del sitio</a>
<a class="btn btn-ghost" style="background:rgba(255,255,255,.10);color:#fff;border-color:rgba(255,255,255,.18)" href="../REDES_V_Libro_Curso_Redes_IV.pdf">Descargar libro PDF</a>
</div>
</div>
{stats_html}
<div class="grid">
{card_for("UNIDAD I — Modelo OSI", ORDER[0][1])}
{card_for("UNIDAD II — Topologías y Medios", ORDER[1][1])}
{card_for("UNIDAD III + Programación Lógica", ORDER[2][1] + ORDER[3][1])}
</div>
<div class="article" style="margin-top:18px">
<div class="article-head"><div class="kicker">SOBRE ESTA EDICIÓN</div><h1 style="font-size:18px">De Google Sites a plataforma profesional</h1></div>
<div class="article-body">
<p>Esta web <strong>REDES V</strong> nace de la recopilación íntegra de <a href="https://sites.google.com/view/curso-redes-iv/inicio">sites.google.com/view/curso-redes-iv</a> (34 páginas). El contenido fue <strong>normalizado tipográficamente, deduplicado y reordenado</strong> en 4 bloques con índice navegable. Cada página conserva su <strong>URL origen</strong> al pie y puede convertirse 1:1 en una entrada de la nueva plataforma.</p>
<ul class="article-list">
  <li><strong>Navegación por unidades</strong> con menú lateral fijo, breadcrumbs y paginación anterior/siguiente.</li>
  <li><strong>Buscador instantáneo</strong> (pulsa <code>/</code>) y diseño responsive para móvil.</li>
  <li><strong>Libro PDF</strong> base con portada, créditos, índice clickeable y anexo de arquitectura.</li>
  <li><strong>Listo para GitHub Pages</strong>: esta carpeta <code>REDV/</code> se publica tal cual.</li>
</ul>
<blockquote>Recomendación: mantener los slugs actuales y redirigir <code>/curso-redes-iv/*</code> → <code>/redes-v/*</code>. Las páginas tipo <em>tinyurl</em> conviene migrarlas a cuestionarios nativos.</blockquote>
</div>
</div>
<footer class="footer">© REDES V · 2026 · Basado en Curso REDES IV · <a href="https://sites.google.com/view/curso-redes-iv/inicio">Sitio original</a> · <a href="../REDES_V_Libro_Curso_Redes_IV.pdf">Libro PDF</a></footer>
</div>
</main>
</div>
<div class="overlay hidden" id="overlay"></div>
<script src="assets/app.js"></script>
</body>
</html>
"""
(OUT_DIR / "index.html").write_text(index_html, encoding="utf-8")

# Build mapa.html
map_rows=[]
for group, items in ORDER:
    lis="".join([f'<li><a href="{slug}.html">{htmlmod.escape(title)}</a> <span class="pill">{htmlmod.escape(label)}</span></li>' for title,label,slug in items])
    map_rows.append(f'<div class="card"><div class="card-head"><h3>{htmlmod.escape(group)}</h3><p>{len(items)} páginas</p></div><div class="card-body"><ul>{lis}</ul></div></div>')

mapa_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Mapa del sitio — REDES V</title>
<link rel="stylesheet" href="assets/styles.css">
</head>
<body>
<div class="layout">
{nav_html("mapa")}
<main class="main">
<header class="topbar">
<button class="menu-btn" id="menuBtn">☰</button>
<div class="topbar-title">Mapa del sitio</div>
<div class="topbar-actions">
<div class="search-wrap"><input id="searchBox" type="search" placeholder="Buscar… ( / )"><div id="searchResults" class="search-results hidden"></div></div>
<a class="btn btn-ghost" href="index.html">Inicio</a>
<a class="btn btn-primary" href="../REDES_V_Libro_Curso_Redes_IV.pdf">PDF</a>
</div>
</header>
<div class="content">
<nav class="breadcrumb"><a href="index.html">Inicio</a> <span>›</span> <strong>Mapa del sitio</strong></nav>
<div class="article">
<div class="article-head"><div class="kicker">ANEXO</div><h1>Mapa del sitio original</h1></div>
<div class="article-body">
<p>Estructura de navegación tal como aparece en <strong>sites.google.com/view/curso-redes-iv</strong>. Útil para planificar menús, URLs y redirecciones de la nueva web REDES V.</p>
</div>
</div>
<div class="grid" style="margin-top:14px">
{"".join(map_rows)}
</div>
<div class="article" style="margin-top:16px">
<div class="article-head"><h1 style="font-size:16px">Próximos pasos</h1></div>
<div class="article-body">
<ul class="article-list">
<li>Definir paleta/logo definitivo (este tema navy/teal es la propuesta base).</li>
<li>Reemplazar enlaces <code>tinyurl.com/MODULO-REDES-IV</code> por formularios nativos.</li>
<li>Añadir banco de diagramas propios (OSI, topologías, cableado) y activar GitHub Pages.</li>
</ul>
</div>
</div>
<footer class="footer">REDES V · Mapa generado el {datetime.date.today().isoformat()}</footer>
</div>
</main>
</div>
<div class="overlay hidden" id="overlay"></div>
<script src="assets/app.js"></script>
</body>
</html>
"""
(OUT_DIR / "mapa.html").write_text(mapa_html, encoding="utf-8")

# Build all content pages
for slug, info in slug_to_info.items():
    article = render_article(info["texts"])
    html = page_template(info["title"], slug, article, info["url"])
    (OUT_DIR / f"{slug}.html").write_text(html, encoding="utf-8")

# Write README and .nojekyll
(OUT_DIR / ".nojekyll").write_text("", encoding="utf-8")
readme = f"""# REDES V — Fundamentos de Redes de Computadoras

Plataforma profesional generada a partir de **sites.google.com/view/curso-redes-iv** (Curso REDES IV).

- **{len(all_slugs)} páginas** migradas en 4 bloques: UNIDAD I (Modelo OSI), UNIDAD II (Topologías), UNIDAD III (Implementación) y PROGRAMACIÓN LÓGICA.
- Diseño **navy/teal** responsive, menú lateral, breadcrumbs, paginación, buscador (`/`) y libro PDF base.
- Cada página conserva su **URL origen** al pie.

## Publicar en GitHub Pages
1. Crear repo `mesaicecyt-max/REDV` en GitHub (público).
2. Subir esta carpeta `REDV/` tal cual (este README, `index.html`, `mapa.html`, `assets/` y los `*.html`).
3. En GitHub: Settings → Pages → Source: `Deploy from a branch` → Branch `main` / `root` → Save.

## Estructura
```
REDV/
  index.html, mapa.html, *.html (34 páginas)
  assets/styles.css, assets/app.js
  .nojekyll, README.md
../REDES_V_Libro_Curso_Redes_IV.pdf  (libro base paginado)
```

Generado: {datetime.date.today().isoformat()} · Origen: https://sites.google.com/view/curso-redes-iv/inicio
"""
(OUT_DIR / "README.md").write_text(readme, encoding="utf-8")

print(f"OK: {len(all_slugs)} páginas + index + mapa en {OUT_DIR}")
print("Archivos:", ", ".join([p.name for p in OUT_DIR.iterdir()][:20]))
