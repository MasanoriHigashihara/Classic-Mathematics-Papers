import re

with open("hugo.toml", "r", encoding="utf-8", newline='') as f:
    text = f.read()

lines = text.split('\n')
out = []
for line in lines:
    m = re.match(r'^weight\s*=\s*(\d+)\r?$', line)
    if m:
        w = int(m.group(1))
        if w >= 2:
            r = '\r' if line.endswith('\r') else ''
            out.append(f"weight = {w + 1}{r}")
        else:
            out.append(line)
    else:
        out.append(line)

new_text = '\n'.join(out)
insert_idx = new_text.find("weight = 1") + 10
insert_idx = new_text.find("\n", insert_idx) + 1

new_entry = """
[[menu.before]]
name = "代数的整数論講義 第II章 §7"
url = "/papers/hecke/algebraic-numbers/slides/chapter2-7/"
parent = "新着"
weight = 2
"""
if '\r\n' in text:
    new_entry = new_entry.replace('\n', '\r\n')

new_text = new_text[:insert_idx] + new_entry + new_text[insert_idx:]

with open("hugo.toml", "w", encoding="utf-8", newline='') as f:
    f.write(new_text)
