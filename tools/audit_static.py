#!/usr/bin/env python3
"""AI 슬롭 정적 감사 (docs/goals/prototype-final-deslop-actions-desktop.md 6-1).

사용: python3 tools/audit_static.py prototype-final.html
출력: 항목마다 AUDIT_LINE:<항목> PASS|FAIL <세부>, 마지막 줄 AUDIT_RESULT:ALL_PASS 또는 AUDIT_RESULT:FAIL n
기준값은 goal 파일과 같게 유지한다. 느슨하게 바꾸지 않는다.
"""
import re
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "prototype-final.html"
src = open(path, encoding="utf-8").read()

styles = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", src, re.S))
inline_styles = re.findall(r'style="([^"]*)"', src)
results = []


def line(item, ok, detail=""):
    results.append(ok)
    print(f"AUDIT_LINE:{item} {'PASS' if ok else 'FAIL'} {detail}".rstrip())


def rules(css):
    """(selector, body) 목록. @media 안쪽 규칙도 펼친다."""
    out = []
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    i = 0
    while i < len(css):
        m = re.compile(r"([^{}]+)\{").search(css, i)
        if not m:
            break
        sel = m.group(1).strip()
        depth, j = 1, m.end()
        while j < len(css) and depth:
            if css[j] == "{":
                depth += 1
            elif css[j] == "}":
                depth -= 1
            j += 1
        body = css[m.end():j - 1]
        if sel.startswith("@media") or sel.startswith("@supports"):
            out.extend(rules(body))
        else:
            out.append((sel, body))
        i = j
    return out


R = rules(styles)

# GRADIENT
grad_pat = re.compile(r"linear-gradient|radial-gradient|background-clip\s*:\s*text", re.I)
total = len(grad_pat.findall(src))
allowed = sum(len(grad_pat.findall(b)) for s, b in R if s.strip() == ".sk")
allowed = min(allowed, 1)
line("GRADIENT", total - allowed == 0, f"count={total} allowed_sk={allowed}")

# EMOJI
emoji_pat = re.compile("[\U0001F000-\U0001FAFF☀-⛿✀-✒✔-➿⬀-⯿️]")
em = emoji_pat.findall(src)
line("EMOJI", not em, f"count={len(em)} {''.join(em[:5])}")

# TYPE
fs_decls = re.findall(r"font-size\s*:\s*([^;}\"]+)", src)
fs_attr = re.findall(r'font-size="[^"]*"', src)
non_token = [v.strip() for v in fs_decls if not v.strip().startswith("var(--fs-")]
tokens = dict((k, v.strip()) for k, v in re.findall(r"(--fs-[\w-]+)\s*:\s*([^;]+);", styles))
def px(v):
    m = re.match(r"([\d.]+)px", v)
    return float(m.group(1)) if m else None
sizes = [px(v) for v in tokens.values() if px(v)]
body = px(tokens.get("--fs-body", "")) if "--fs-body" in tokens else None
ratio = (max(sizes) / body) if sizes and body else 0
type_ok = not non_token and not fs_attr and 0 < len(tokens) <= 7 and ratio >= 2.0
line("TYPE", type_ok, f"tokens={len(tokens)} ratio={ratio:.2f} non_token={len(non_token)} attr={len(fs_attr)} {non_token[:3]}")

# LEFTBAR
lb = re.findall(r"border-left(?:-[a-z]+)?\s*:", src)
line("LEFTBAR", not lb, f"count={len(lb)}")

# GLASS
bf = re.findall(r"backdrop-filter", src)
bad_rgba = []
def scan_rgba(sel, body):
    for a in re.findall(r"background(?:-color)?\s*:\s*rgba\(\s*[\d.]+\s*,\s*[\d.]+\s*,\s*[\d.]+\s*,\s*([\d.]+)\s*\)", body):
        if float(a) < 0.95 and sel.strip() != ".dim" and not sel.strip().startswith(".dim"):
            bad_rgba.append(f"{sel.strip()[:30]}:{a}")
for s, b in R:
    scan_rgba(s, b)
for b in inline_styles:
    scan_rgba("inline", b)
line("GLASS", not bf and not bad_rgba, f"backdrop={len(bf)} rgba<0.95={bad_rgba[:4]}")

# ICON
allowed_icons = {"home", "note", "chart", "person", "back", "chev", "check", "play"}
used = set(re.findall(r'href="#i-([\w-]+)"', src)) | set(re.findall(r"\bic\('([\w-]+)'\)", src)) | set(re.findall(r"icon\s*:\s*'([\w-]+)'", src))
bad_icons = sorted(used - allowed_icons)
line("ICON", not bad_icons, f"not_allowed={bad_icons}")

# BUTTON
has_active = bool(re.search(r"\.btn[^{,]*:active", styles))
has_focus = ":focus-visible" in styles
op_only = [s for s, b in R if ":hover" in s and [p.split(":")[0].strip() for p in b.split(";") if p.strip()] == ["opacity"]]
line("BUTTON", has_active and has_focus and not op_only, f"active={has_active} focus_visible={has_focus} opacity_only_hover={op_only[:3]}")

# MOTION
mo = re.findall(r"IntersectionObserver|mousemove|pointermove", src)
kf = re.findall(r"@keyframes", src)
line("MOTION", not mo and len(kf) <= 1, f"observers={len(mo)} keyframes={len(kf)}")

# SPACING
scale = {0, 2, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64}
sp_prop = re.compile(r"(?<![\w-])(margin(?:-[a-z]+)?|padding(?:-[a-z]+)?|gap|row-gap|column-gap|inset|top|right|bottom|left)\s*:\s*([^;}\"]+)")
bad_sp = []
def scan_sp(body, where):
    for prop, val in sp_prop.findall(body):
        for n in re.findall(r"(-?[\d.]+)px", val):
            if abs(float(n)) not in scale:
                bad_sp.append(f"{where}:{prop}:{n}")
for s, b in R:
    scan_sp(b, s.strip()[:20])
for b in inline_styles:
    scan_sp(b, "inline")
line("SPACING", not bad_sp, f"off_scale={len(bad_sp)} {bad_sp[:5]}")

# DASH
dash = re.findall(r"—|&mdash;|–|&ndash;", src)
line("DASH", not dash, f"count={len(dash)}")

# BUZZ
buzz = re.findall(r"seamless|robust|elevate|empower|leverage|혁신|스마트한|완벽한|최적의|손쉽게|간편하게|원활", src, re.I)
line("BUZZ", not buzz, f"count={len(buzz)} {buzz[:5]}")

# SERIF
it = re.findall(r"font-style\s*:\s*italic", src)
serif = re.findall(r"(?<!sans-)\bserif\b", src)
line("SERIF", not it and not serif, f"italic={len(it)} serif={len(serif)}")

# GRAIN
gr = re.findall(r"feTurbulence|noise|grain", src, re.I)
line("GRAIN", not gr, f"count={len(gr)}")

# SELFCONTAINED
ext = re.findall(r"<script[^>]+src=|<link[^>]+href=\"https?:|<img[^>]+src=\"https?:", src)
line("SELFCONTAINED", not ext, f"count={len(ext)}")

fails = results.count(False)
print("AUDIT_RESULT:ALL_PASS" if fails == 0 else f"AUDIT_RESULT:FAIL {fails}")
