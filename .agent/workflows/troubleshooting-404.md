---
description: ページが404になる問題のトラブルシューティング
---

# 404エラーのトラブルシューティング

## 問題の概要

新しいスライドページを追加したが、デプロイ後に404エラーが発生する。

---

## よくある原因と解決方法

### 1. 日付が未来になっている（最も多い原因）

**症状**: ローカルでは正常に表示されるが、GitHub Pagesで404

**原因**: 
- `hugo.toml` に `buildFuture = false` が設定されている
- GitHub ActionsはUTC（協定世界時）で動作する
- JSTで今日の日付（例: 2026-01-10）でも、UTCではまだ前日の場合がある
- その場合、Hugoは「未来の日付」と判断してページをビルドしない

**解決方法**:
```markdown
# NG: 日本時間で今日の日付
date: 2026-01-10

# OK: 確実に過去の日付を使う
date: 2025-01-10
```

**推奨**: 新しいページを作成する際は、**1年前の日付**を使用する

---

### 2. draft: true になっている

**症状**: ページが生成されない

**解決方法**:
```markdown
# NG
draft: true

# OK
draft: false
```

---

### 3. ファイル名やパスの誤り

**症状**: リンクをクリックしても404

**確認事項**:
- ファイル名のスペルミス
- パスの大文字/小文字（Linuxでは区別される）
- `_index.md` 内のリンクが正しいか

---

## 確認手順

1. **ローカルで確認**
   ```powershell
   hugo server -D
   ```
   ブラウザで http://localhost:1313/Classic-Mathematics-Papers/ を確認

2. **Gitステータス確認**
   ```powershell
   git status
   git diff
   ```

3. **コミット・プッシュ**
   ```powershell
   git add .
   git commit -m "Fix: description"
   git push
   ```

4. **GitHub Actions の完了を待つ**（1〜2分）

5. **ブラウザのキャッシュをクリア**してページを再読み込み（Ctrl+Shift+R）

---

## 2026-01-10 発生事例

**問題**: ヒルベルト数論報告第1章のスライドページが404

**原因**: frontmatterの日付が `2026-01-10`（JST）だったため、UTCで動作するGitHub Actionsでは「未来の日付」として判定され、`buildFuture = false` によりビルドから除外された

**解決**: 日付を `2025-01-10` に変更してプッシュ
