import re

# ファイルを読み込む
with open('content/papers/hilbert/zahlbericht/_index.md', 'r', encoding='utf-8') as f:
    content = f.read()

# §の行にアイコンを追加するパターン
# 例: **§1** Der Zahlkörper und die conjugierten Zahlkörper  
# を
# **§1** Der Zahlkörper und die conjugierten Zahlkörper <span style="margin-left: 10px;"><a href="#" title="スライド" style="text-decoration: none; font-size: 1.1em;">📊</a> <a href="#" title="音声解説" style="text-decoration: none; font-size: 1.1em; margin-left: 8px;">🎧</a></span>  
# に変換

# ドイツ語の§行を見つけて、行末にアイコンを追加
# パターン: **§数字** ドイツ語テキスト  (改行)
pattern = r'(\*\*§(\d+)\*\* .+?)  \n'

def add_icons(match):
    original_line = match.group(1)
    section_num = match.group(2)
    icons = f'<span style="margin-left: 10px;"><a href="#" title="スライド" style="text-decoration: none; font-size: 1.1em;">📊</a> <a href="#" title="音声解説" style="text-decoration: none; font-size: 1.1em; margin-left: 8px;">🎧</a></span>'
    return f'{original_line} {icons}  \n'

content = re.sub(pattern, add_icons, content)

# ファイルに書き戻す
with open('content/papers/hilbert/zahlbericht/_index.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("ヒルベルト数論報告の各節にアイコンを追加しました！")
