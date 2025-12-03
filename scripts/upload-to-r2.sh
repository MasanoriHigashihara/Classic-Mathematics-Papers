#!/bin/bash

# Cloudflare R2にPDFファイルをアップロード
# 使用方法: ./scripts/upload-to-r2.sh

BUCKET_NAME="notebooklm-classics-pdfs"

echo "Uploading PDFs to Cloudflare R2..."
echo "Bucket: $BUCKET_NAME"
echo ""

# static/slides 内の全PDFを検索
pdf_files=$(find static/slides -name "*.pdf" 2>/dev/null)

if [ -z "$pdf_files" ]; then
    echo "No PDF files found in static/slides"
    exit 0
fi

# ファイル数をカウント
file_count=$(echo "$pdf_files" | wc -l)
echo "Found $file_count PDF file(s)"
echo ""

upload_count=0
error_count=0
current=0

# 各PDFファイルをアップロード
echo "$pdf_files" | while read file; do
    current=$((current + 1))
    
    # static/ を除いたパスを取得
    relative_path="${file#static/}"
    
    echo "[$current/$file_count] Uploading: $relative_path"
    
    # Wrangler CLIを使用してアップロード
    if npx wrangler r2 object put "$BUCKET_NAME/$relative_path" --file="$file" 2>&1; then
        echo "  ✓ Success"
        upload_count=$((upload_count + 1))
    else
        echo "  ✗ Failed"
        error_count=$((error_count + 1))
    fi
    
    echo ""
done

echo "Upload complete!"
echo "Successfully uploaded: $upload_count file(s)"
if [ $error_count -gt 0 ]; then
    echo "Failed: $error_count file(s)"
fi
