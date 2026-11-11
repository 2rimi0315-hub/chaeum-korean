# -*- coding: utf-8 -*-
"""채움 국어 교실 활동지 공통 부품 (4-1 1단원 차시와 같은 마크업)."""
import html as H, os, json

TOOLS = os.path.dirname(os.path.abspath(__file__))
HEAD = open(os.path.join(TOOLS, 'head.html'), encoding='utf-8').read()
SCRIPT = open(os.path.join(TOOLS, 'script.html'), encoding='utf-8').read()
VHEAD = open(os.path.join(TOOLS, 'vocab_head.html'), encoding='utf-8').read()

def e(s): return H.escape(s, quote=True)

def say(t, plain=False, top=0):
    st = []
    if top: st.append(f'margin-top:{top}px;')
    if plain: st.append('background:#FBFAF5; color:#5F5E5A;')
    s = f' style="{" ".join(st)}"' if st else ''
    return f'<div class="say"{s}>{t}</div>'

def task(no, t, small='', top=22):
    sm = f' <small>{small}</small>' if small else ''
    st = f' style="margin-top:{top}px;"' if top else ''
    return f'<div class="task"{st}><span class="no">{no}</span><p>{t}{sm}</p></div>'

def _cell(c, center=False):
    if isinstance(c, tuple):
        return f'<td><input type="text" placeholder="{e(c[1])}"></td>'
    if center:
        return f'<td style="text-align:center; font-weight:700; background:#FBFAF5;">{c}</td>'
    return f'<td style="background:#FBF3DC;">{c}</td>'

def IN(ph=''): return ('in', ph)

def table(heads, rows, widths=None, center_cols=()):
    th = ''.join(f'<th style="width:{widths[i]}px;">{h}</th>' if widths and widths[i] else f'<th>{h}</th>' for i, h in enumerate(heads))
    trs = []
    for r in rows:
        tds = []
        for i, c in enumerate(r):
            if i == 0 and not isinstance(c, tuple):
                tds.append(f'<td class="word">{c}</td>')
            else:
                tds.append(_cell(c, center=i in center_cols))
        trs.append('<tr>' + ''.join(tds) + '</tr>')
    return f'<table><thead><tr>{th}</tr></thead><tbody>{"".join(trs)}</tbody></table>'

def vocab_table(words):
    rows = ''.join(f'<tr><td class="word">{w}</td><td><input type="text"></td><td><input type="text"></td></tr>' for w in words)
    return ('<table><thead><tr><th>낱말</th><th>내가 생각한 뜻</th><th>사전에서 찾은 뜻</th></tr></thead>'
            f'<tbody>{rows}</tbody></table>')

def flow(items):
    out = []
    for i, it in enumerate(items, 1):
        body = (f'<textarea class="writeline" rows="1" placeholder="{e(it[1])}"></textarea>' if isinstance(it, tuple)
                else f'<div class="fixed">{it}</div>')
        out.append(f'<div class="flowrow"><span class="fno">{i}</span>{body}</div>')
    return '<div class="flowlist">' + '\n<p class="flowarrow">▼</p>\n'.join(out) + '</div>'

def rv(q, ans, *wrong, order=None, col=None):
    opts = [ans] + list(wrong)
    if order: opts = [opts[i] for i in order]
    long_ = col if col is not None else max(len(o) for o in opts) > 8
    st = ' style="flex-direction:column; align-items:flex-start;"' if long_ else ''
    btns = ''.join(f'<button data-v="{e(o)}">{e(o)}</button>' for o in opts)
    return f'<div class="rv"><p class="q">{q}</p><div class="rvgroup"{st} data-ranswer="{e(ans)}">{btns}</div></div>'

def ox(q, ans):
    a = 'O' if ans else 'X'
    return (f'<div class="rv"><p class="q">{q}</p><div class="rvgroup" data-ranswer="{a}">'
            '<button data-v="O">⭕ 맞아요</button><button data-v="X">❌ 아니에요</button></div></div>')

def mapw(center, branches):
    bs = ''.join(
        f'<div class="branch"><div class="bcard b{i}"><h3>{h}</h3><p class="lab">{lab}</p><textarea placeholder="{e(ph)}"></textarea></div></div>'
        for i, (h, lab, ph) in enumerate(branches, 1))
    return (f'<div class="mapwrap"><div class="center-node">{center}</div><div class="stem"></div>'
            f'<div class="branches">{bs}</div></div>')

def chips(items):
    return '<div class="combine">' + ''.join(
        f'<div class="chip"><small>{s}</small><b>{b}</b><input type="text" placeholder="{e(ph)}"></div>' for s, b, ph in items) + '</div>'

def boki(t): return f'<div class="boki">{t}</div>'
def wl(ph): return f'<textarea class="writeline" rows="1" placeholder="{e(ph)}"></textarea>'

def box(*parts, style=''):
    st = f' style="{style}"' if style else ''
    return f'<div class="box"{st}>\n      ' + '\n      '.join(parts) + '\n    </div>'

def section(cls, badge, title, *boxes):
    return (f'<section class="{cls}">\n    <div class="stage"><span class="badge">{badge}</span><h2>{title}</h2></div>\n    '
            + '\n    '.join(boxes) + '\n  </section>')

def key_concept(t):
    return ('<div class="box" style="background:var(--purple-bg); border-color:var(--purple);"><p style="font-size:13px; font-weight:800; color:var(--purple-dark); letter-spacing:0.08em;">🔑 오늘의 핵심 개념 <small style="font-weight:600; color:#8A8271; letter-spacing:0;">— 한 문장으로 기억해요</small></p>'
            f'<p style="font-size:17px; font-weight:800; margin-top:8px; line-height:1.6; color:var(--ink);">{t}</p></div>')

def comic(lid):
    return (f'<div class="comic"><p class="clabel">🖼️ 그림으로 생각 열기 <small>그림을 보고, 오늘 무엇을 배울지 이야기해 보세요.</small></p><div class="cowrap"><img src="comics/{lid}.png" alt="생각 열기 그림" style="width:100%; display:block;" '
            "onerror=\"if(!this.dataset.j){this.dataset.j=1;this.src=this.src.replace('.png','.jpg');}else{this.parentElement.innerHTML='<div style=&quot;padding:48px 20px; text-align:center; color:#B4AE9D; font-size:14.5px; background:#FBFAF5; line-height:1.8;&quot;>🖼️ 여기에 그림이 들어가요<br>"
            f"(comics/{lid}.png 파일을 넣어 주세요)</div>';}}\"></div></div>")

def unit_check(unit, sub):
    return ('<label style="display:flex; align-items:center; gap:10px; font-size:17px; font-weight:700; background:#FBFAF5; border-radius:12px; padding:12px 16px;">\n'
            '        <input type="checkbox" style="width:22px; height:22px;">\n'
            f'        <span style="line-height:1.5;"><small style="display:block; font-size:13px; font-weight:600; color:#8A8271;">{unit}</small>{sub}</span>\n      </label>')

def marktools(env, imp, unk='🩷 모르는 낱말'):
    return ('<div class="marktools">\n'
            f'        <button id="btn-env" onclick="setMode(\'env\')">{env}</button>\n'
            f'        <button id="btn-important" onclick="setMode(\'important\')">{imp}</button>\n'
            f'        <button id="btn-unknown" onclick="setMode(\'unknown\')">{unk}</button>\n'
            '        <button id="btn-erase" class="erase" onclick="setMode(\'erase\')">지우개</button>\n      </div>')

def passage(kind, title, src, paras):
    ps = '\n'.join(f'        <p class="{c}">{t}</p>' if c else f'        <p>{t}</p>' for c, t in paras)
    return (f'<p class="ptitle"><small>{kind}</small>{title}<span style="display:block; font-size:12.5px; font-weight:600; color:#9A937F; margin-top:4px;">{src}</span></p>\n'
            f'      <div class="passage" id="passage">\n{ps}\n      </div>')

def legend(env, imp):
    return ('<div class="legendline">\n'
            f'        <span><i style="background:var(--mark-env)"></i>{env}</span>\n'
            f'        <span><i style="background:var(--mark-important)"></i>{imp}</span>\n'
            '        <span><i style="background:var(--mark-unknown)"></i>모르는 낱말</span>\n'
            '        <span>💡 인쇄해서 쓸 때는 ○, 밑줄, △로 직접 표시해요.</span>\n      </div>')

def wordhelp(pairs):
    return say('📖 낱말 도움: ' + ' · '.join(f'<b>{w}</b> {m}' for w, m in pairs), plain=True, top=14)

def textbook_note(t):
    return ('<div class="say" style="background:#FFF6D6; color:#6B5A1E;">📕 ' + t + '</div>')

TAGS = {'낱말': '#5F5E5A', '추론': '#E8762C', '서술형': '#7F77DD', '내용': '#1D9E75', '맞춤법': '#C2477A'}
def tag(t): return f'<span style="font-size:11.5px; font-weight:800; color:#fff; background:{TAGS[t]}; border-radius:999px; padding:3px 10px; margin-left:6px; vertical-align:2px;">{t}</span>'

_qn = [0]
def mc(n, q, t, opts, ans, boki_t=None, fix=False):
    _qn[0] += 1
    b = boki(boki_t) if boki_t else ''
    btns = ''.join(f'<button>{"①②③④"[i]} {o}</button>' for i, o in enumerate(opts))
    fx = ('<div class="fixline"><p>✏️ 고른 문장을 <b>바르게 고쳐</b> 써 보세요.</p><textarea class="writeline" rows="1" placeholder="바르게 고치면: "></textarea></div>' if fix else '')
    return f'<div class="quiz"><p class="qtitle">{n}. {q}{tag(t)}</p>{b}<div class="mc" data-q="q{_qn[0]}" data-answer="{ans}">{btns}</div>{fx}</div>'

def essay(n, q, prompt, ph):
    return f'<div class="quiz"><p class="qtitle">{n}. {q}{tag("서술형")}</p><p style="font-size:15px;">{prompt}</p>{wl(ph)}</div>'

FACES = '<div class="faces"><button onclick="pickFace(this)">⭕<small>잘해요</small></button><button onclick="pickFace(this)">🔺<small>조금 자신 없어요</small></button><button onclick="pickFace(this)">❌<small>어려워요</small></button></div>'

def wrap_section(checks, quizzes, homework, title='스스로 확인해요'):
    sc = ''.join(f'<div class="selfcheck"><p>💪 {c}</p>{FACES}</div>' for c in checks)
    qs = '\n      '.join(quizzes)
    return ('<section class="s-wrap">\n    <div class="stage"><span class="badge">정리</span><h2>' + title + '</h2></div>\n'
            f'    <div class="box">\n      {sc}\n    </div>\n'
            '    <div class="box">\n      <div class="task"><span class="no">🏆</span><p>문제를 풀어 봐요. <small>헷갈리면 △, 모르면 ☆ — 문제 옆의 ◻ 버튼을 눌러 표시해요.</small></p></div>\n'
            f'      {qs}\n      <button class="checkbtn" onclick="grade()">정답 확인하기</button>\n      <p id="result"></p>\n    </div>\n'
            '    <div class="box" style="background:var(--tangerine-bg); border-style:dashed;">\n'
            '      <p style="font-size:15px; font-weight:700; color:var(--tangerine-dark);">🏠 오늘의 숙제</p>\n'
            f'      <p style="font-size:15px; margin-top:4px;">{homework[0]}</p>\n      {wl(homework[1])}\n    </div>\n  </section>')

def page(lid, title_tag, eyebrow, h1, sections):
    _qn[0] = 0
    head = HEAD
    import re
    head = re.sub(r'<title>.*?</title>', f'<title>{e(title_tag)}</title>', head, flags=re.S)
    body = ('<body>\n<div class="wrap">\n\n  <header class="top">\n'
            '    <img src="logo.png" alt="채움언어학습연구소" style="height:36px; width:auto; display:block; margin-bottom:14px;" onerror="this.style.display=\'none\'">\n'
            f'    <p class="eyebrow">{eyebrow}</p>\n    <h1>{h1}</h1>\n'
            '    <div class="idrow"><span>이름 <input type="text"></span><span>날짜 <input type="text" placeholder="    월    일"></span></div>\n  </header>\n\n  '
            + '\n\n  '.join(sections) + '\n</div>\n</body>\n')
    return head + body + SCRIPT

def vocab_page(eyebrow, h1, words):
    body = ('<body>\n<div class="wrap">\n  <header>\n'
            '    <img src="logo.png" alt="채움언어학습연구소" style="height:36px; width:auto; display:block; margin-bottom:14px;" onerror="this.style.display=\'none\'">\n'
            f'    <p class="eyebrow">{eyebrow} · 어휘 카드 8장</p>\n    <h1>{h1}</h1>\n'
            '    <p class="sub">카드를 눌러 낱말의 뜻을 확인해요 · 소리 내어 따라 읽으면 더 좋아요!</p>\n  </header>\n'
            '  <div class="toolbar">\n    <button class="primary" onclick="window.print()">🖨 인쇄하기 (카드 + 뜻 정리표)</button>\n'
            '    <button onclick="revealAll(true)">뜻 모두 보기</button>\n    <button onclick="revealAll(false)">뜻 모두 숨기기</button>\n  </div>\n'
            '  <p class="hint">💡 화면에서는 카드를 누르면 뜻이 나타나요. 인쇄하면 카드에는 낱말만 나오고, 두 번째 장에 뜻 정리표가 나옵니다.</p>\n'
            '  <div class="grid" id="grid"></div>\n  <section class="answers">\n    <h2>낱말 뜻 정리표</h2>\n    <table>\n'
            '      <thead><tr><th style="width:90px">낱말</th><th>뜻</th><th>이렇게 써요</th></tr></thead>\n      <tbody id="tbody"></tbody>\n    </table>\n  </section>\n'
            '  <a class="back" href="index.html">‹ 첫 화면으로 돌아가기</a>\n</div>\n<script>\nconst WORDS = [\n'
            + ',\n'.join('  ' + json.dumps({'e': a, 'w': b, 'm': c, 'x': d}, ensure_ascii=False) for a, b, c, d in words) + '\n];\n')
    tail = r"""const grid = document.getElementById('grid');
const tbody = document.getElementById('tbody');
WORDS.forEach(w=>{
  const el = document.createElement('div');
  el.className = 'card';
  const base = 'cards/' + encodeURIComponent(w.w);
  el.innerHTML = '<div class="pic"><img src="'+base+'.png" alt="'+w.w+'" loading="lazy" onerror="if(!this.dataset.j){this.dataset.j=1;this.src=this.src.replace(\'.png\',\'.jpg\');}else{this.style.display=\'none\';this.nextElementSibling.style.display=\'flex\';}">'
    + '<span class="emoji" style="display:none">'+w.e+'</span></div>'
    + '<div class="word">'+w.w+'</div>'
    + '<div class="mean">'+w.m+'</div><div class="ex">예) '+w.x+'</div>';
  el.onclick = ()=> el.classList.toggle('open');
  grid.appendChild(el);
  const tr = document.createElement('tr');
  tr.innerHTML = '<td class="w">'+w.e+' '+w.w+'</td><td>'+w.m+'</td><td>'+w.x+'</td>';
  tbody.appendChild(tr);
});
function revealAll(on){ document.querySelectorAll('.card').forEach(c=>c.classList.toggle('open', on)); }
</script>
</body>
</html>
"""
    import re
    vh = re.sub(r'<title>.*?</title>', f'<title>{e(h1)} — 낱말 카드</title>', VHEAD, flags=re.S)
    return vh + body + tail

def pick(q, opts):
    """정답 없는 고르기(내 선택·자기 점검)."""
    btns = ''.join(f'<button onclick="pickFace(this)" style="padding:8px 14px; font-size:15px;">{o}</button>' for o in opts)
    return f'<div class="rv"><p class="q">{q}</p><div class="faces" style="flex-wrap:wrap;">{btns}</div></div>'
