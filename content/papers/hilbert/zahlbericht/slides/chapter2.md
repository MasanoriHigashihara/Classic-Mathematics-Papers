---
title: "Capitel II - スライド"
date: 2025-11-29
draft: false
bookHidden: true
---

# Capitel II - Die Ideale des Zahlkörpers
## 第2章 - 数体のイデアル

### スライド資料

<div id="pdf-viewer" style="text-align: center;">
  <canvas id="pdf-canvas" style="border: 1px solid #ccc; max-width: 100%;"></canvas>
  <div style="margin-top: 20px;">
    <button id="prev-page" style="padding: 10px 20px; margin: 5px; font-size: 16px;">◀ 前のページ</button>
    <span style="margin: 0 20px; font-size: 18px;">
      ページ <span id="page-num"></span> / <span id="page-count"></span>
    </span>
    <button id="next-page" style="padding: 10px 20px; margin: 5px; font-size: 16px;">次のページ ▶</button>
  </div>
  <div style="margin-top: 10px;">
    <a href="/slides/hilbert/zahlbericht/chapter2.pdf" target="_blank" style="font-size: 14px;">📥 PDFをダウンロード</a>
  </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
<script>
  const url = '/slides/hilbert/zahlbericht/chapter2.pdf';
  let pdfDoc = null;
  let pageNum = 1;
  let pageRendering = false;
  let pageNumPending = null;
  const scale = 1.5;
  const canvas = document.getElementById('pdf-canvas');
  const ctx = canvas.getContext('2d');

  pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';

  function renderPage(num) {
    pageRendering = true;
    pdfDoc.getPage(num).then(function(page) {
      const viewport = page.getViewport({scale: scale});
      canvas.height = viewport.height;
      canvas.width = viewport.width;

      const renderContext = {
        canvasContext: ctx,
        viewport: viewport
      };
      const renderTask = page.render(renderContext);

      renderTask.promise.then(function() {
        pageRendering = false;
        if (pageNumPending !== null) {
          renderPage(pageNumPending);
          pageNumPending = null;
        }
      });
    });

    document.getElementById('page-num').textContent = num;
  }

  function queueRenderPage(num) {
    if (pageRendering) {
      pageNumPending = num;
    } else {
      renderPage(num);
    }
  }

  function onPrevPage() {
    if (pageNum <= 1) {
      return;
    }
    pageNum--;
    queueRenderPage(pageNum);
  }

  function onNextPage() {
    if (pageNum >= pdfDoc.numPages) {
      return;
    }
    pageNum++;
    queueRenderPage(pageNum);
  }

  document.getElementById('prev-page').addEventListener('click', onPrevPage);
  document.getElementById('next-page').addEventListener('click', onNextPage);

  document.addEventListener('keydown', function(e) {
    if (e.key === 'ArrowLeft') onPrevPage();
    if (e.key === 'ArrowRight') onNextPage();
  });

  pdfjsLib.getDocument(url).promise.then(function(pdfDoc_) {
    pdfDoc = pdfDoc_;
    document.getElementById('page-count').textContent = pdfDoc.numPages;
    renderPage(pageNum);
  });
</script>

---

**内容:**
- §4 Die Multiplication der Ideale und ihre Teilbarkeit; Das Primideal（イデアルの乗法と可除性・素イデアル）
- §5 Die eindeutige Zerlegbarkeit eines Ideals in Primideale（イデアルの素イデアルへの一意分解）
- §6 Die Formen des Zahlkörpers und ihre Inhalte（数体の形式と内容）

**操作方法:**
- ボタンをクリックするか、キーボードの左右矢印キー（← →）でページを移動できます

[目次に戻る](../)
