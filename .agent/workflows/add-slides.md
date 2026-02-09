---
description: 新しいスライドと音声解説を追加する手順
---

# 新しいスライドと音声解説を追加する手順

新しい章やセクションのスライドと音声解説を追加する際の標準手順です。

## 必要な情報

追加前に以下の情報を確認してください：

1. **スライドのURL** (例: `https://pub-b7de6127921a4952aac9bd48e1710bcb.r2.dev/slides/hilbert/zahlbericht/zchapter3-7.pdf`)
2. **音声解説のURL** (例: `https://youtu.be/Eycw7-evvwg`)
3. **対象の著者/論文** (例: Hilbert / Zahlbericht)
4. **章・節の情報** (例: 第3章 §7)
5. **ドイツ語タイトル** (例: Die Norm eines Ideals und ihre Eigenschaften)
6. **日本語タイトル** (例: イデアルのノルムとその性質)

---

## 手順

### 1. スライドページの作成

`content/papers/{author}/{work}/slides/` に新しいマークダウンファイルを作成

**例**: `content/papers/hilbert/zahlbericht/slides/chapter3-7.md`

```markdown
---
title: "Capitel III §7 - スライド"
date: 2026-02-09
draft: false
type: docs
bookHidden: true
---

# Capitel III §7 - Die Norm eines Ideals und ihre Eigenschaften
## 第3章 §7 - イデアルのノルムとその性質

<div style="text-align:center; margin: 1.5rem 0;">
  <iframe 
    width="280" 
    height="158" 
    src="https://www.youtube.com/embed/{YOUTUBE_ID}" 
    style="border:none; border-radius:8px;"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
    allowfullscreen>
  </iframe>
  <p style="font-size:0.85rem; color:#666; margin-top:0.5rem;">🎧 音声解説（NotebookLM）</p>
</div>

### スライド資料

{{< pdf-embed "slides/hilbert/zahlbericht/{PDF_FILENAME}" >}}

<div class="pdf-hint">
  <p><strong>💡 ヒント:</strong></p>
  <ul>
    <li>PDFが表示されない場合は、上のダウンロードボタンからPDFをダウンロードしてご覧ください</li>
    <li>ブラウザによっては、PDFビューアーが自動的に表示されます</li>
  </ul>
</div>

---

**内容:**
- §7 イデアルのノルムとその性質
```

---

### 2. 新着セクションに追加（_index.md）

`content/_index.md` の `## 🆕 新着` セクションの **先頭** にエントリを追加

```html
<div style="padding: 15px; border-left: 4px solid #9C27B0; background-color: #f9f9f9;">
  <strong>📊 <a href="papers/hilbert/zahlbericht/slides/chapter3-7/">ヒルベルト『数論報告』第3章 §7</a></strong>
  <span style="margin-left: 10px;">
    <a href="{SLIDE_URL}" title="スライド" style="text-decoration: none; font-size: 1.1em;">📊</a>
    <a href="{YOUTUBE_URL}" title="音声解説" style="text-decoration: none; font-size: 1.1em; margin-left: 8px;">🎧</a>
  </span><br>
  <span style="color: #666; font-size: 0.9em;">{日本語タイトル} - スライドと音声解説</span>
</div>
```

**注意**: 色コードはランダムに選択可能（例: `#9C27B0`, `#4CAF50`, `#2196F3`など）

---

### 3. メニューバーに追加（hugo.toml）

`hugo.toml` の `[[menu.before]]` セクションに追加

**⚠️ 重要: メニューの順序は `_index.md` の新着セクションの順序と一致させる**

新しいエントリは **weight = 1** で追加し、**既存のエントリのweightをすべて+1する**

```toml
[[menu.before]]
name = "数論報告 第3章 §7"
url = "/papers/hilbert/zahlbericht/slides/chapter3-7/"
parent = "新着"
weight = 1
```

**weightの規則:**
- `weight` の値が小さいほどメニューの上に表示される
- 新しいエントリは `weight = 1` で追加
- 既存エントリのweightを順番に+1してずらす（2, 3, 4, ...）
- `_index.md` の順序とメニューの順序を常に一致させる

---

### 4. 論文インデックスのリンク修正

該当論文の `_index.md` ファイル（例: `content/papers/hilbert/zahlbericht/_index.md`）で、
対応する節のリンクを `#` から正しいURLに変更

**変更前**:
```html
<a href="#" title="スライド">📊</a> <a href="#" title="音声解説">🎧</a>
```

**変更後**:
```html
<a href="slides/chapter3-7/" title="スライド">📊</a> <a href="https://youtu.be/{YOUTUBE_ID}" title="音声解説">🎧</a>
```

---

### 5. Git コミット & プッシュ

// turbo
```bash
git add -A && git commit -m "Add {Author} {Work} Chapter X Section Y" && git push
```

---

## チェックリスト

- [ ] スライドページ (`slides/chapterX-Y.md`) を作成
- [ ] `content/_index.md` の新着セクションの**先頭**に追加
- [ ] `hugo.toml` のメニューに追加（weight=1、既存を+1）
- [ ] **メニュー順序と新着順序が一致していることを確認**
- [ ] 論文 `_index.md` のリンクを修正
- [ ] Git push
- [ ] デプロイ後、リンクが正しく動作するか確認

---

## 順序の確認方法

メニューと新着の順序が一致しているか確認するには：

1. `content/_index.md` の新着セクションのエントリ順序を確認
2. `hugo.toml` のメニューエントリの `weight` 順序を確認
3. 両方が同じ順序になっていることを確認

**順序が異なる場合の修正方法:**
- `hugo.toml` の各エントリの `weight` を `_index.md` の順序に合わせて連番で設定
- 例: 1番目 → weight=1, 2番目 → weight=2, ...
