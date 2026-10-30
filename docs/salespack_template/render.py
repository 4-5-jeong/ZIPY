"""
Sales Pack 렌더러 예시 — slots.json → HTML(8장) → PDF
사용: python render.py slots_filled.json out.pdf [--theme light|dark]
의존: pip install jinja2 playwright && playwright install chromium
핵심 아이디어: 페이지 컴포넌트 1개(page) + 본문 변형 3종(cards3 / vs2 / table)
"""
import json, sys
from jinja2 import Template
from playwright.sync_api import sync_playwright

PAGE = Template("""
<section class="page">
  <div class="label">{{ p.label }}</div>
  <div class="chapter">{{ meta.customer }} 제안 · {{ meta.date }}</div>
  <h1 class="title">{{ p.title }}</h1>
  {% if p.subtitle %}<p class="subtitle">{{ p.subtitle }}</p>{% endif %}

  {% if p.body == "cards3" %}
  <div class="cards3">
    {% for c in p.cards %}
    <div class="card"><div class="no">{{ "%02d"|format(loop.index) }}</div>
      <h3>{{ c.title }}</h3><p>{{ c.body }}{% for r in c.ref %}<span class="ref">[{{ r }}]</span>{% endfor %}</p>
      {% if c.meta %}<div class="meta">{{ c.meta }}</div>{% endif %}</div>
    {% endfor %}
  </div>

  {% elif p.body == "vs2" %}
  <div class="vs2">
    <div class="side"><h3>{{ p.vs.left.heading }}</h3><ul>{% for i in p.vs.left.items %}<li>{{ i.text }}</li>{% endfor %}</ul></div>
    <div class="mid">VS</div>
    <div class="side right"><h3>{{ p.vs.right.heading }}</h3><ul>{% for i in p.vs.right.items %}<li>{{ i.text }}{% for r in i.ref %}<span class="ref">[{{ r }}]</span>{% endfor %}</li>{% endfor %}</ul></div>
  </div>

  {% elif p.body == "table" %}
  <table><thead><tr>{% for h in p.table.header %}<th>{{ h }}</th>{% endfor %}</tr></thead>
  <tbody>{% for row in p.table.rows %}<tr>{% for cell in row %}<td>{{ cell }}</td>{% endfor %}</tr>{% endfor %}</tbody></table>
  {% endif %}

  <div class="conclusion">{{ p.conclusion or "" }}</div>
  <div class="pageno">{{ p.no }} / {{ total }}</div>
</section>
""")

def render_html(slots: dict, css: str, theme: str = "light") -> str:
    pages = slots["pages"]
    body = "\n".join(PAGE.render(p=p, meta=slots["meta"], total=len(pages)) for p in pages)
    return f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>{css}</style></head><body data-theme="{theme}">{body}</body></html>'

def to_pdf(html: str, out: str):
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page()
        pg.set_content(html, wait_until="networkidle")
        pg.pdf(path=out, width="297mm", height="210mm", print_background=True)
        b.close()

if __name__ == "__main__":
    slots = json.load(open(sys.argv[1], encoding="utf-8"))
    theme = "dark" if "--theme" in sys.argv and "dark" in sys.argv else "light"
    css = open("template.css", encoding="utf-8").read()   # template.html의 <style> 내용을 분리해둔 파일
    html = render_html(slots, css, theme)
    open("preview.html", "w", encoding="utf-8").write(html)   # 화면③ 미리보기도 이 HTML을 그대로 씀
    to_pdf(html, sys.argv[2])
    print("ok →", sys.argv[2])
