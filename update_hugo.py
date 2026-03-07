import re

with open('c:/Users/natsu/.gemini/antigravity/scratch/notebooklm-classics/hugo.toml', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
out_lines = []
in_menu = False
for line in lines:
    if line.startswith('[[menu.before]]'):
        in_menu = True
    if line.startswith('weight = ') and in_menu:
        w = int(line.split('=')[1].strip())
        if w >= 2:
            out_lines.append(f'weight = {w + 1}')
            continue
    out_lines.append(line)

# Now insert the new item
insert_idx = None
for i, line in enumerate(out_lines):
    if line.startswith('weight = 1'):
        insert_idx = i + 1
        break

new_item = """
[[menu.before]]
name = "博士論文 第I部 第2章第5節"
url = "/papers/gentzen/doctoral-thesis/slides/part1-chapter2-5/"
parent = "新着"
weight = 2"""

if insert_idx:
    out_lines.insert(insert_idx, new_item)

with open('c:/Users/natsu/.gemini/antigravity/scratch/notebooklm-classics/hugo.toml', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out_lines))
