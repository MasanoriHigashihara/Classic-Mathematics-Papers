# Cloudflare R2 セットアップガイド

このドキュメントでは、NotebookLM ClassicsプロジェクトでCloudflare R2を使用してPDFファイルをホストするための設定方法を説明します。

## 前提条件

- Cloudflareアカウント（無料プランで可）
- Wrangler CLI（Node.jsがインストールされている必要があります）

## 1. Cloudflare R2バケットの作成

### 1.1 Cloudflareダッシュボードにアクセス

1. [Cloudflare Dashboard](https://dash.cloudflare.com/)にログイン
2. 左サイドバーから **R2** を選択
3. **Create bucket** をクリック

### 1.2 バケット設定

- **Bucket name**: `notebooklm-classics-pdfs`（または任意の名前）
- **Location**: 自動選択（またはお好みのリージョン）
- **Create bucket** をクリック

## 2. パブリックアクセスの設定

### オプション A: R2.dev サブドメイン（推奨・簡単）

1. 作成したバケットを選択
2. **Settings** タブに移動
3. **Public access** セクションで **Allow Access** をクリック
4. **R2.dev subdomain** が表示されます（例: `https://pub-xxxxx.r2.dev`）
5. このURLをメモしておきます

### オプション B: カスタムドメイン

1. バケットの **Settings** タブ
2. **Custom Domains** セクションで **Connect Domain** をクリック
3. 所有しているドメインを入力（例: `cdn.example.com`）
4. DNS設定を完了

## 3. API認証情報の取得

### 3.1 R2 APIトークンの作成

1. Cloudflareダッシュボードで **R2** を選択
2. **Manage R2 API Tokens** をクリック
3. **Create API Token** をクリック
4. 以下の設定を行います：
   - **Token name**: `notebooklm-classics-upload`
   - **Permissions**: 
     - Object Read & Write
   - **Bucket**: 作成したバケットを選択
5. **Create API Token** をクリック

### 3.2 認証情報の保存

表示される以下の情報をメモします：

- **Access Key ID**: `xxxxxxxxxxxxxxxxxxxxx`
- **Secret Access Key**: `yyyyyyyyyyyyyyyyyyyyyy`
- **Account ID**: Cloudflareダッシュボードの右上に表示されています

⚠️ **重要**: Secret Access Keyは一度しか表示されないため、必ず安全な場所に保存してください。

## 4. Wrangler CLIのセットアップ

### 4.1 Wranglerのインストール（グローバル）

```bash
npm install -g wrangler
```

または、プロジェクトごとに使用する場合は `npx wrangler` を使用します。

### 4.2 Wranglerの認証

```bash
wrangler login
```

ブラウザが開き、Cloudflareアカウントへの認証を求められます。

## 5. 環境変数の設定

### 5.1 ローカル環境（オプション）

プロジェクトルートに `.env` ファイルを作成（Gitにコミットしないこと）：

```env
CLOUDFLARE_ACCOUNT_ID=your_account_id
CLOUDFLARE_R2_ACCESS_KEY_ID=your_access_key_id
CLOUDFLARE_R2_SECRET_ACCESS_KEY=your_secret_access_key
R2_PUBLIC_URL=https://pub-xxxxx.r2.dev
```

### 5.2 GitHub Secrets

GitHub リポジトリの設定でSecretsを追加：

1. GitHubリポジトリページで **Settings** > **Secrets and variables** > **Actions**
2. **New repository secret** をクリック
3. 以下のSecretsを追加：

| Name | Value |
|------|-------|
| `CLOUDFLARE_ACCOUNT_ID` | CloudflareアカウントID |
| `CLOUDFLARE_R2_ACCESS_KEY_ID` | R2 Access Key ID |
| `CLOUDFLARE_R2_SECRET_ACCESS_KEY` | R2 Secret Access Key |
| `R2_PUBLIC_URL` | R2のパブリックURL（例: `https://pub-xxxxx.r2.dev`） |

## 6. PDFファイルのアップロード

### 6.1 初回アップロード

**Windows (PowerShell):**
```powershell
.\scripts\upload-to-r2.ps1
```

**Linux/Mac (Bash):**
```bash
chmod +x scripts/upload-to-r2.sh
./scripts/upload-to-r2.sh
```

### 6.2 新しいPDFの追加

1. PDFファイルを `static/slides/` の適切なディレクトリに配置
2. アップロードスクリプトを実行
3. `hugo.toml` の `pdfBaseURL` パラメータにR2のURLを設定

## 7. Hugo設定の更新

`hugo.toml` を編集：

```toml
[params]
  # Cloudflare R2 PDF storage
  pdfBaseURL = "https://pub-xxxxx.r2.dev"  # 実際のR2 URLに置き換え
```

## 8. 動作確認

### 8.1 ローカルテスト

```bash
hugo server
```

ブラウザで `http://localhost:1313` を開き、PDFが正しく表示されることを確認します。

### 8.2 本番デプロイ

1. 変更をGitにコミット・プッシュ
2. GitHub Actionsが自動的にビルド・デプロイ
3. デプロイされたサイトでPDFが表示されることを確認

## トラブルシューティング

### PDFが表示されない

1. **R2のパブリックアクセスが有効か確認**
   - バケットの Settings > Public access が有効になっているか

2. **CORS設定の確認**
   - R2バケットの Settings > CORS policy で以下を設定：
   ```json
   [
     {
       "AllowedOrigins": ["*"],
       "AllowedMethods": ["GET", "HEAD"],
       "AllowedHeaders": ["*"],
       "MaxAgeSeconds": 3600
     }
   ]
   ```

3. **URLの確認**
   - ブラウザの開発者ツールでネットワークタブを確認
   - R2のURLが正しく生成されているか

### アップロードエラー

1. **Wrangler認証の確認**
   ```bash
   wrangler whoami
   ```

2. **APIトークンの権限確認**
   - R2 Object Read & Write権限があるか
   - 正しいバケットが選択されているか

3. **バケット名の確認**
   - スクリプト内のバケット名が正しいか

## メンテナンス

### PDFの更新

1. 新しいPDFファイルを `static/slides/` に配置
2. アップロードスクリプトを実行
3. 既存のファイルは自動的に上書きされます

### PDFの削除

```bash
# Wrangler CLIを使用
npx wrangler r2 object delete notebooklm-classics-pdfs/slides/path/to/file.pdf
```

### バケットの内容確認

```bash
# バケット内のファイル一覧
npx wrangler r2 object list notebooklm-classics-pdfs
```

## コスト見積もり

Cloudflare R2の料金（2024年12月時点）：

- **ストレージ**: $0.015/GB/月
- **Class A操作** (書き込み): $4.50/百万リクエスト
- **Class B操作** (読み取り): $0.36/百万リクエスト
- **エグレス**: 無料 ✨

**例**: 100MBのPDF、月間10,000ダウンロード
- ストレージ: $0.0015/月
- 読み取り: $0.0036/月
- **合計**: 約 $0.01/月（ほぼ無料）

## 参考リンク

- [Cloudflare R2 Documentation](https://developers.cloudflare.com/r2/)
- [Wrangler CLI Documentation](https://developers.cloudflare.com/workers/wrangler/)
- [R2 Pricing](https://developers.cloudflare.com/r2/pricing/)
