// PDF Page-by-Page Viewer using PDF.js

class PDFPageViewer {
    constructor(pdfUrl, canvasId) {
        this.pdfUrl = pdfUrl;
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.pdfDoc = null;
        this.currentPage = 1;
        this.totalPages = 0;
        this.scale = 1.5;

        this.init();
    }

    async init() {
        try {
            // Load PDF.js library
            const pdfjsLib = window['pdfjs-dist/build/pdf'];
            pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';

            // Load PDF document
            const loadingTask = pdfjsLib.getDocument(this.pdfUrl);
            this.pdfDoc = await loadingTask.promise;
            this.totalPages = this.pdfDoc.numPages;

            // Update page info
            this.updatePageInfo();

            // Render first page
            await this.renderPage(this.currentPage);

            // Setup event listeners
            this.setupControls();

            // Enable swipe gestures on mobile
            this.setupSwipeGestures();

        } catch (error) {
            console.error('Error loading PDF:', error);
            this.showError('PDFの読み込みに失敗しました');
        }
    }

    async renderPage(pageNum) {
        try {
            const page = await this.pdfDoc.getPage(pageNum);
            const viewport = page.getViewport({ scale: this.scale });

            // Set canvas dimensions
            this.canvas.width = viewport.width;
            this.canvas.height = viewport.height;

            // Render page
            const renderContext = {
                canvasContext: this.ctx,
                viewport: viewport
            };

            await page.render(renderContext).promise;

            // Update controls
            this.updateControls();

        } catch (error) {
            console.error('Error rendering page:', error);
        }
    }

    setupControls() {
        const prevBtn = document.getElementById('pdf-prev');
        const nextBtn = document.getElementById('pdf-next');

        if (prevBtn) {
            prevBtn.addEventListener('click', () => this.previousPage());
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', () => this.nextPage());
        }

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') this.previousPage();
            if (e.key === 'ArrowRight') this.nextPage();
        });
    }

    setupSwipeGestures() {
        let touchStartX = 0;
        let touchEndX = 0;

        this.canvas.addEventListener('touchstart', (e) => {
            touchStartX = e.changedTouches[0].screenX;
        });

        this.canvas.addEventListener('touchend', (e) => {
            touchEndX = e.changedTouches[0].screenX;
            this.handleSwipe();
        });

        const handleSwipe = () => {
            const swipeThreshold = 50;
            const diff = touchStartX - touchEndX;

            if (Math.abs(diff) > swipeThreshold) {
                if (diff > 0) {
                    // Swipe left - next page
                    this.nextPage();
                } else {
                    // Swipe right - previous page
                    this.previousPage();
                }
            }
        };

        this.handleSwipe = handleSwipe;
    }

    previousPage() {
        if (this.currentPage > 1) {
            this.currentPage--;
            this.renderPage(this.currentPage);
            this.updatePageInfo();
        }
    }

    nextPage() {
        if (this.currentPage < this.totalPages) {
            this.currentPage++;
            this.renderPage(this.currentPage);
            this.updatePageInfo();
        }
    }

    updatePageInfo() {
        const pageInfo = document.getElementById('pdf-page-info');
        if (pageInfo) {
            pageInfo.textContent = `${this.currentPage} / ${this.totalPages}`;
        }
    }

    updateControls() {
        const prevBtn = document.getElementById('pdf-prev');
        const nextBtn = document.getElementById('pdf-next');

        if (prevBtn) {
            prevBtn.disabled = this.currentPage === 1;
        }

        if (nextBtn) {
            nextBtn.disabled = this.currentPage === this.totalPages;
        }
    }

    showError(message) {
        const container = this.canvas.parentElement;
        container.innerHTML = `<div class="pdf-error">${message}</div>`;
    }
}

// Initialize PDF viewer when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const pdfViewerElement = document.querySelector('[data-pdf-url]');
    if (pdfViewerElement) {
        const pdfUrl = pdfViewerElement.getAttribute('data-pdf-url');
        new PDFPageViewer(pdfUrl, 'pdf-canvas');
    }
});
