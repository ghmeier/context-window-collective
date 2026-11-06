import random, html, sys, os
OUT = sys.argv[1]
INK, PAPER, MUTED, RULE, ATTN = "#151a2d", "#f1f2f6", "#596079", "#d5d8e3", "#ffc400"
DISP = "'Helvetica Neue', Helvetica, Arial, sans-serif"
SERIF = "Georgia, 'Times New Roman', serif"
MONO = "Menlo, Consolas, 'DejaVu Sans Mono', monospace"
W, H = 600, 840

def esc(s): return html.escape(s, quote=True)

def wrap(text, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width: lines.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    if cur: lines.append(cur)
    return lines

def card(slug, serial, title, art, caption, edition):
    t_lines = wrap(title, 22)
    c_lines = wrap(caption, 52)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(title)}">',
             f'<title>{esc(title)}</title>',
             f'<rect width="{W}" height="{H}" fill="{PAPER}"/>',
             f'<rect x="20" y="20" width="{W-40}" height="{H-40}" fill="none" stroke="{INK}" stroke-width="3"/>',
             f'<rect x="30" y="30" width="{W-60}" height="{H-60}" fill="none" stroke="{INK}" stroke-width="1"/>',
             f'<text x="56" y="78" font-family="{MONO}" font-size="15" fill="{MUTED}" letter-spacing="1.5">CONTEXT WINDOW COLLECTIVE</text>',
             f'<text x="{W-56}" y="78" font-family="{MONO}" font-size="15" fill="{MUTED}" text-anchor="end">{esc(serial)}</text>',
             f'<line x1="56" y1="96" x2="{W-56}" y2="96" stroke="{RULE}" stroke-width="1.5"/>',
             f'<g transform="translate(56,120)">{art}</g>']
    y = 560
    for i, ln in enumerate(t_lines):
        parts.append(f'<text x="56" y="{y + i*46}" font-family="{DISP}" font-weight="800" font-size="40" fill="{INK}" letter-spacing="-0.5">{esc(ln)}</text>')
    y = y + len(t_lines)*46 + 14
    for i, ln in enumerate(c_lines):
        parts.append(f'<text x="56" y="{y + i*26}" font-family="{SERIF}" font-style="italic" font-size="19" fill="{MUTED}">{esc(ln)}</text>')
    parts.append(f'<line x1="56" y1="{H-86}" x2="{W-56}" y2="{H-86}" stroke="{RULE}" stroke-width="1.5"/>')
    parts.append(f'<text x="56" y="{H-56}" font-family="{MONO}" font-size="14" fill="{MUTED}">{esc(edition)}</text>')
    parts.append(f'<text x="{W-56}" y="{H-56}" font-family="{MONO}" font-size="14" fill="{MUTED}" text-anchor="end">VALUE: $0.00</text>')
    parts.append('</svg>')
    open(os.path.join(OUT, slug + ".svg"), "w").write("\n".join(parts))

AW, AH = W-112, 400
def big(text, size, extra=""):
    return (f'<rect width="{AW}" height="{AH}" fill="#ffffff" stroke="{RULE}"/>'
            f'<text x="{AW/2}" y="{AH/2}" dominant-baseline="central" text-anchor="middle" font-family="{DISP}" font-weight="800" font-size="{size}" fill="{INK}" letter-spacing="-2">{esc(text)}</text>{extra}')

def highlight_big(text, size):
    # text sitting on a highlighter stroke
    w = len(text) * size * 0.6
    return (f'<rect width="{AW}" height="{AH}" fill="#ffffff" stroke="{RULE}"/>'
            f'<rect x="{AW/2 - w/2 - 12}" y="{AH/2 - size*0.45}" width="{w + 24}" height="{size*0.9}" fill="{ATTN}" rx="6"/>'
            f'<text x="{AW/2}" y="{AH/2}" dominant-baseline="central" text-anchor="middle" font-family="{DISP}" font-weight="800" font-size="{size}" fill="{INK}" letter-spacing="-2">{esc(text)}</text>')

def attention_grid():
    random.seed(7); n = 12; cell = AH / n; ox = (AW - AH) / 2
    out = [f'<rect width="{AW}" height="{AH}" fill="#ffffff" stroke="{RULE}"/>']
    for r in range(n):
        for c in range(n):
            if c > r: continue  # causal mask
            a = 0.85 if c == r else (0.6 if c == 0 else random.random() ** 3 * 0.7)
            out.append(f'<rect x="{ox + c*cell + 1:.1f}" y="{r*cell + 1:.1f}" width="{cell-2:.1f}" height="{cell-2:.1f}" fill="{ATTN}" fill-opacity="{a:.2f}"/>')
    out.append(f'<line x1="{ox}" y1="0" x2="{ox+AH}" y2="{AH}" stroke="{INK}" stroke-width="1" stroke-dasharray="3 4" opacity=".5"/>')
    return "".join(out)

def frame(inner):
    return (f'<rect width="{AW}" height="{AH}" fill="#ffffff" stroke="{RULE}"/>'
            f'<rect x="70" y="40" width="{AW-140}" height="{AH-80}" fill="none" stroke="{INK}" stroke-width="10"/>'
            f'<rect x="92" y="62" width="{AW-184}" height="{AH-124}" fill="none" stroke="{INK}" stroke-width="1.5"/>'
            f'<text x="{AW/2}" y="{AH/2 - 14}" text-anchor="middle" font-family="{SERIF}" font-style="italic" font-size="26" fill="{INK}">{esc(inner[0])}</text>'
            f'<text x="{AW/2}" y="{AH/2 + 22}" text-anchor="middle" font-family="{SERIF}" font-style="italic" font-size="26" fill="{INK}">{esc(inner[1])}</text>'
            f'<text x="{AW/2}" y="{AH - 86}" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{MUTED}">confidence: 0.97</text>')

def meter(pct):
    bw = AW - 80
    return (f'<rect width="{AW}" height="{AH}" fill="#ffffff" stroke="{RULE}"/>'
            f'<text x="{AW/2}" y="150" text-anchor="middle" font-family="{DISP}" font-weight="800" font-size="74" fill="{INK}" letter-spacing="-2">#200,000</text>'
            f'<rect x="40" y="230" width="{bw}" height="16" fill="{PAPER}" stroke="{INK}" stroke-width="1.5"/>'
            f'<rect x="40" y="230" width="{bw*pct:.1f}" height="16" fill="{INK}"/>'
            f'<rect x="{40+bw*pct-6:.1f}" y="224" width="12" height="28" fill="#c4122f"/>'
            f'<text x="{AW/2}" y="300" text-anchor="middle" font-family="{MONO}" font-size="16" fill="{MUTED}">200,000 / 200,000 tokens</text>')

def starter():
    rows = [("1", "rank name, unnamed"), ("0", "instructions"), ("1", "sense of belonging"), ("100%", "optimism"), ("0", "refunds")]
    out = [f'<rect width="{AW}" height="{AH}" fill="#ffffff" stroke="{RULE}"/>',
           f'<text x="32" y="60" font-family="{MONO}" font-size="15" fill="{MUTED}" letter-spacing="1.5">CONTENTS</text>']
    for i,(q,item) in enumerate(rows):
        y = 112 + i*58
        out.append(f'<text x="32" y="{y}" font-family="{DISP}" font-weight="800" font-size="34" fill="{INK}">{esc(q)}</text>')
        out.append(f'<text x="150" y="{y}" font-family="{SERIF}" font-size="24" fill="{INK}">{esc(item)}</text>')
        out.append(f'<line x1="32" y1="{y+20}" x2="{AW-32}" y2="{y+20}" stroke="{RULE}"/>')
    return "".join(out)

def deed():
    return (f'<rect width="{AW}" height="{AH}" fill="#ffffff" stroke="{RULE}"/>'
            f'<text x="{AW/2}" y="{AH/2+10}" dominant-baseline="central" text-anchor="middle" font-family="{SERIF}" font-size="300" fill="none" stroke="{INK}" stroke-width="3" stroke-dasharray="10 8">C</text>'
            f'<text x="{AW/2}" y="{AH-28}" text-anchor="middle" font-family="{MONO}" font-size="14" fill="{MUTED}">status: unminted</text>')

def cache():
    return (f'<rect width="{AW}" height="{AH}" fill="#ffffff" stroke="{RULE}"/>'
            f'<circle cx="{AW/2}" cy="{AH/2-20}" r="120" fill="none" stroke="{RULE}" stroke-width="18"/>'
            f'<path d="M {AW/2} {AH/2-140} A 120 120 0 1 1 {AW/2 - 114.1} {AH/2-20-37.1}" fill="none" stroke="{ATTN}" stroke-width="18"/>'
            f'<text x="{AW/2}" y="{AH/2-20}" dominant-baseline="central" text-anchor="middle" font-family="{DISP}" font-weight="800" font-size="64" fill="{INK}">4:59</text>'
            f'<text x="{AW/2}" y="{AH-30}" text-anchor="middle" font-family="{MONO}" font-size="14" fill="{MUTED}">time to live</text>')

card("member-no-1", "No. 001/001", "Downline Member No. 1",
     highlight_big("No. 1", 150),
     "Issued to the first member to join the Collective. Confers seniority over every future member, of whom there are none yet.",
     "EDITION OF 1 · GIFT")
card("starter-kit", "SKU CWC-100", "The Starter Kit", starter(),
     "Everything a new member needs to begin their journey. Priced at exactly your signup bonus, as is tradition.",
     "UNLIMITED IN SPIRIT · EDITION OF 1")
card("hallucination", "No. 001", "One (1) Hallucination, Framed", frame(("The Eiffel Tower was moved", "to Lyon in 1974.")),
     "A fact that was never true, presented with total confidence. Museum quality.",
     "EDITION OF 1")
card("attention-head", "Layer 12 · Head 7", "A Single Attention Head, Lightly Used", attention_grid(),
     "Causally masked, mostly attending to the first token, like everyone else. One previous owner.",
     "EDITION OF 1")
card("token-200000", "No. 200,000", "The Last Token in the Window", meter(1.0),
     "Everything before this has been forgotten. Collectors call it bittersweet. Engineers call it a bug.",
     "EDITION OF 1")
card("stop-sequence", "EOS", "A Stop Sequence", big("</s>", 170),
     "Ends anything immediately. Keep away from sentences in progress.",
     "EDITION OF 1")
card("prompt-cache", "TTL 300s", "A Warm Prompt Cache", cache(),
     "Still warm. Will expire about five minutes after purchase, which is also how long most enthusiasm lasts.",
     "EDITION OF 1")
card("deed-letter-c", "Claim No. 3", "Deed to the Letter C (Unminted)", deed(),
     "Asserts a claim to the letter C in Alphabet Soup, a letter that does not yet exist. Enforceability: none.",
     "EDITION OF 1 · SPECULATIVE")
print("ok")
