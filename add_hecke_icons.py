import re

# ファイルを読み込む
with open('content/papers/hecke/algebraic-numbers/_index.md', 'r', encoding='utf-8') as f:
    content = f.read()

# §の後にアイコンを追加するパターン
# 例: **§1.** 可除性。最大公約数。法（モジュロ）。素数。整数論の基本定理。
# を
# **§1.** 可除性。最大公約数。法（モジュロ）。素数。整数論の基本定理。 <span style="margin-left: 10px;"><a href="#" title="スライド" style="text-decoration: none; font-size: 1.1em;">📊</a> <a href="#" title="音声解説" style="text-decoration: none; font-size: 1.1em; margin-left: 8px;">🎧</a></span>
# に変換

# 日本語の§行を見つけて、その行末にアイコンを追加
pattern = r'(\*\*§\d+\.\*\* .+?)  \n'
replacement = r'\1 <span style="margin-left: 10px;"><a href="#" title="スライド" style="text-decoration: none; font-size: 1.1em;">📊</a> <a href="#" title="音声解説" style="text-decoration: none; font-size: 1.1em; margin-left: 8px;">🎧</a></span>  \n'

content = re.sub(pattern, replacement, content)

# ファイルに書き戻す
with open('content/papers/hecke/algebraic-numbers/_index.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("アイコンを追加しました！")
