# Cloudflare R2にPDFファイルをアップロード
# 使用方法: .\scripts\upload-to-r2.ps1

$BUCKET_NAME = "notebooklm-classics-pdfs"

Write-Host "Uploading PDFs to Cloudflare R2..." -ForegroundColor Green
Write-Host "Bucket: $BUCKET_NAME" -ForegroundColor Cyan
Write-Host ""

# static/slides 内の全PDFを検索してアップロード
$pdfFiles = Get-ChildItem -Path "static\slides" -Filter "*.pdf" -Recurse

if ($pdfFiles.Count -eq 0) {
    Write-Host "No PDF files found in static/slides" -ForegroundColor Yellow
    exit 0
}

Write-Host "Found $($pdfFiles.Count) PDF file(s)" -ForegroundColor Cyan
Write-Host ""

$uploadCount = 0
$errorCount = 0

foreach ($file in $pdfFiles) {
    # static\ を除いたパスを取得（Unixスタイルのパスに変換）
    $relativePath = $file.FullName.Substring($PWD.Path.Length + 1).Replace('\', '/').Replace('static/', '')
    
    Write-Host "[$($uploadCount + 1)/$($pdfFiles.Count)] Uploading: $relativePath" -ForegroundColor White
    
    try {
        # Wrangler CLIを使用してアップロード
        $output = npx wrangler r2 object put "$BUCKET_NAME/$relativePath" --file="$($file.FullName)" 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ Success" -ForegroundColor Green
            $uploadCount++
        } else {
            Write-Host "  ✗ Failed: $output" -ForegroundColor Red
            $errorCount++
        }
    } catch {
        Write-Host "  ✗ Error: $_" -ForegroundColor Red
        $errorCount++
    }
    
    Write-Host ""
}

Write-Host "Upload complete!" -ForegroundColor Green
Write-Host "Successfully uploaded: $uploadCount file(s)" -ForegroundColor Cyan
if ($errorCount -gt 0) {
    Write-Host "Failed: $errorCount file(s)" -ForegroundColor Red
}
