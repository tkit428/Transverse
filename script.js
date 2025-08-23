// DOM Elements
const navbar = document.getElementById('navbar');
const inputText = document.getElementById('inputText');
const outputText = document.getElementById('outputText');
const translateBtn = document.getElementById('translateBtn');
const loadingSpinner = document.getElementById('loadingSpinner');
const charCount = document.getElementById('charCount');
const sourceLanguage = document.getElementById('sourceLanguage');
const targetLanguage = document.getElementById('targetLanguage');
const switchLanguages = document.getElementById('switchLanguages');
const fileInput = document.getElementById('fileInput');
const copyBtn = document.getElementById('copyBtn');
const scrollProgress = document.getElementById('scrollProgress');
const backToTop = document.getElementById('backToTop');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeAnimations();
    initializeScrollObserver();
    initializeEventListeners();
    initializeNavigation();
    initializeFAQ();
    initializeScrollProgress();
    initializeBackToTop();
    initializeParallaxBackground();
});

// Scroll Observer for Navbar
function initializeScrollObserver() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('in-view');
            }
        });
    }, observerOptions);

    // Observe all animatable elements
    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });

    // Navbar scroll effect
    let lastScrollY = window.scrollY;

    window.addEventListener('scroll', () => {
        const currentScrollY = window.scrollY;

        if (currentScrollY > 100) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }

        lastScrollY = currentScrollY;
    });
}

// Initialize scroll progress bar
function initializeScrollProgress() {
    window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrollPercent = (scrollTop / scrollHeight) * 100;

        anime({
            targets: scrollProgress,
            width: `${scrollPercent}%`,
            duration: 100,
            easing: 'linear'
        });

        // Update active navigation based on scroll position
        updateActiveNavigation();
    });
}

// Update active navigation based on scroll position
function updateActiveNavigation() {
    const sections = ['home', 'features', 'pricing', 'faq'];
    const navLinks = document.querySelectorAll('.nav-link');
    const scrollPosition = window.scrollY + 100; // Offset for navbar height

    let currentSection = 'home';

    sections.forEach(sectionId => {
        const section = document.getElementById(sectionId);
        if (section) {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;

            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                currentSection = sectionId;
            }
        }
    });

    // Update active states
    navLinks.forEach(link => {
        link.classList.remove('active');
        const href = link.getAttribute('href');
        if (href === `#${currentSection}`) {
            link.classList.add('active');
        }
    });
}

// Initialize back to top button
function initializeBackToTop() {
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            backToTop.classList.add('visible');
        } else {
            backToTop.classList.remove('visible');
        }
    });

    backToTop.addEventListener('click', () => {
        anime({
            targets: document.documentElement,
            scrollTop: 0,
            duration: 800,
            easing: 'easeOutQuart'
        });
    });
}

// Initialize parallax background
function initializeParallaxBackground() {
    let ticking = false;

    function updateParallax() {
        const scrolled = window.pageYOffset;
        const parallaxElement = document.querySelector('body::before') || document.body;

        // Move background at 30% of scroll speed for subtle parallax effect
        const yPos = -(scrolled * 0.3);

        // Use CSS custom property for better performance
        document.documentElement.style.setProperty('--parallax-y', `${yPos}px`);

        ticking = false;
    }

    function requestTick() {
        if (!ticking) {
            requestAnimationFrame(updateParallax);
            ticking = true;
        }
    }

    window.addEventListener('scroll', requestTick);
}

// Initialize Anime.js animations
function initializeAnimations() {
    // Animate hero content on load
    anime.timeline({
        easing: 'easeOutExpo',
        duration: 1000
    })
        .add({
            targets: '.hero-title',
            opacity: [0, 1],
            translateY: [50, 0],
            delay: 300
        })
        .add({
            targets: '.hero-description',
            opacity: [0, 1],
            translateY: [30, 0],
            delay: 200
        }, '-=800')
        .add({
            targets: '.translator-container',
            opacity: [0, 1],
            translateY: [50, 0],
            scale: [0.9, 1],
            delay: 100
        }, '-=600');

    // Animate feature cards
    anime({
        targets: '.feature-card',
        translateY: [50, 0],
        opacity: [0, 1],
        delay: anime.stagger(100),
        duration: 800,
        easing: 'easeOutQuart'
    });

    // Animate pricing cards
    anime({
        targets: '.pricing-card',
        translateY: [50, 0],
        opacity: [0, 1],
        delay: anime.stagger(150),
        duration: 800,
        easing: 'easeOutQuart'
    });
}

// Helper function to update character count
function updateCharacterCount() {
    const count = inputText.value.length;
    charCount.textContent = count;

    if (count > 4500) {
        charCount.style.color = '#dc3545';
    } else {
        charCount.style.color = '#999';
    }
}

// Event Listeners
function initializeEventListeners() {
    // Character counter
    inputText.addEventListener('input', function() {
        updateCharacterCount();

        // Removed auto-translate on input
    });

    // Switch languages
    switchLanguages.addEventListener('click', function() {
        const sourceValue = sourceLanguage.value;
        const targetValue = targetLanguage.value;

            // Switch the language selections
            sourceLanguage.value = targetValue;
            targetLanguage.value = sourceValue;

            // Switch the text content
            const inputTextValue = inputText.value;
            const outputTextValue = outputText.value;

            inputText.value = outputTextValue;
            outputText.value = inputTextValue;

            // Update character count for the new input text
            updateCharacterCount();

            // Animate the switch
            anime({
                targets: this,
                rotate: '180deg',
                duration: 300,
                easing: 'easeOutQuart',
                complete: () => {
                    this.style.transform = 'rotate(0deg)';
                }
            });

            // Re-translate if there's content - removed auto-translate
    });

    // File upload
    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            handleFileUpload(file);
        }
    });

    // Translate button
    translateBtn.addEventListener('click', performTranslation);

    // Copy button
    copyBtn.addEventListener('click', function() {
        if (outputText.value) {
            navigator.clipboard.writeText(outputText.value).then(() => {
                showNotification('Translation copied to clipboard!', 'success');

                // Animate copy button
                anime({
                    targets: this,
                    scale: [1, 0.9, 1],
                    duration: 200,
                    easing: 'easeOutQuart'
                });
            });
        }
    });

    // Language dropdown changes
    sourceLanguage.addEventListener('change', () => {
        // Removed auto-translate on language change
    });

    targetLanguage.addEventListener('change', () => {
        // Removed auto-translate on language change
    });

    // Drag and Drop functionality
    const dragDropOverlay = document.getElementById('dragDropOverlay');

    // Show overlay on drag enter
    document.addEventListener('dragenter', function(e) {
        e.preventDefault();
        e.stopPropagation();
        dragDropOverlay.classList.add('active');
    });

    // Keep overlay active while dragging over
    document.addEventListener('dragover', function(e) {
        e.preventDefault();
        e.stopPropagation();
        if (!dragDropOverlay.classList.contains('active')) {
            dragDropOverlay.classList.add('active');
        }
    });

    // Hide overlay when dragging leaves the window
    document.addEventListener('dragleave', function(e) {
        e.preventDefault();
        e.stopPropagation();

        // Only hide if we're leaving the document itself (not child elements)
        if (e.clientX === 0 && e.clientY === 0) {
            dragDropOverlay.classList.remove('active');
        }
    });

    // Handle file drop
    document.addEventListener('drop', function(e) {
        e.preventDefault();
        e.stopPropagation();
        dragDropOverlay.classList.remove('active');

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            const file = files[0];
            handleFileUpload(file);
        }
    });

    // Click on overlay to dismiss
    dragDropOverlay.addEventListener('click', function(e) {
        if (e.target === dragDropOverlay) {
            dragDropOverlay.classList.remove('active');
        }
    });

    // File translation event listeners
    const translateFileBtn = document.getElementById('translateFileBtn');
    if (translateFileBtn) {
        translateFileBtn.addEventListener('click', translateFileContent);
    }

    const downloadTranslationBtn = document.getElementById('downloadTranslationBtn');
    if (downloadTranslationBtn) {
        downloadTranslationBtn.addEventListener('click', downloadTranslatedFile);
    }
}

// Navigation
function initializeNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        if (link.getAttribute('href').startsWith('#')) {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const targetId = this.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);

                if (targetElement) {
                    const offsetTop = targetElement.offsetTop - 80;

                    anime({
                        targets: document.documentElement,
                        scrollTop: offsetTop,
                        duration: 800,
                        easing: 'easeOutQuart'
                    });

                    // Update active link
                    navLinks.forEach(l => l.classList.remove('active'));
                    this.classList.add('active');
                }
            });
        }
    });
}

// FAQ
function initializeFAQ() {
    const faqQuestions = document.querySelectorAll('.faq-question');

    faqQuestions.forEach(question => {
        question.addEventListener('click', function() {
            const faqItem = this.parentElement;
            const isActive = faqItem.classList.contains('active');

            if (isActive) {
                // Close the current item
                faqItem.classList.remove('active');
                const answer = faqItem.querySelector('.faq-answer');
                answer.style.display = 'none';
            } else {
                // Close all other FAQ items first
                document.querySelectorAll('.faq-item').forEach(item => {
                    if (item !== faqItem) {
                        item.classList.remove('active');
                        const otherAnswer = item.querySelector('.faq-answer');
                        if (otherAnswer) {
                            otherAnswer.style.display = 'none';
                        }
                    }
                });

                // Open current item
                faqItem.classList.add('active');
                const answer = faqItem.querySelector('.faq-answer');
                answer.style.display = 'block';

                // Animate the answer
                anime({
                    targets: answer,
                    opacity: [0, 1],
                    translateY: [-10, 0],
                    duration: 300,
                    easing: 'easeOutQuart'
                });
            }
        });
    });
}

// Translation Logic
async function performTranslation() {
    const text = inputText.value.trim();

    console.log('performTranslation called with text:', text);

    if (!text) {
        showNotification('Please enter text to translate', 'error');
        return;
    }

    if (sourceLanguage.value === targetLanguage.value && sourceLanguage.value !== 'auto') {
        showNotification('Source and target languages cannot be the same', 'error');
        return;
    }

    // Show loading state
    setLoadingState(true);

    try {
        // Call Django backend API
        const apiUrl = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
            ? 'http://127.0.0.1:8000/api/translate/' 
            : '/api/translate/';
            
        console.log('Making API call to:', apiUrl);
        console.log('Request body:', {
            text: text,
            target_language: targetLanguage.options[targetLanguage.selectedIndex].text
        });

                const response = await fetch(apiUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
            body: JSON.stringify({
                text: text,
                target_language: targetLanguage.options[targetLanguage.selectedIndex].text
            })
                });

                console.log('Response status:', response.status);

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

        const data = await response.json();
                console.log('Response data:', data);

        if (data.error) {
            throw new Error(data.error);
        }

        outputText.value = data.translated_text;
        outputText.classList.add('success');

        // Animate the output
        anime({
            targets: '.output-section',
            scale: [0.98, 1],
            duration: 300,
            easing: 'easeOutQuart'
        });

        // Enable action buttons
        copyBtn.disabled = false;

        showNotification('Translation completed successfully!', 'success');

    } catch (error) {
        console.error('Translation error:', error);
        showNotification('Translation failed. Please try again.', 'error');
        outputText.classList.add('error');
    } finally {
        setLoadingState(false);
    }
}

// Helper function to get CSRF token
function getCsrfToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    return cookieValue || '';
}

// Simulate translation (legacy function - kept for fallback)
async function simulateTranslation(text, sourceLang, targetLang) {
    return new Promise((resolve) => {
        setTimeout(() => {
            // This is a mock translation - replace with actual translation service
            const translations = {
                'en': {
                    'es': 'Esta es una traducción simulada del texto en inglés al español.',
                    'fr': 'Ceci est une traduction simulée du texte anglais vers le français.',
                    'de': 'Dies ist eine simulierte Übersetzung von englischem Text ins Deutsche.',
                    'ja': 'これは英語のテキストから日本語への模擬翻訳です。',
                    'ko': '이것은 영어 텍스트에서 한국어로의 시뮬레이션된 번역입니다.',
                    'zh': '这是从英文文本到中文的模拟翻译。'
                }
            };

            const mockTranslation = translations[sourceLang]?.[targetLang] ||
                `[Translated from ${sourceLang} to ${targetLang}]: ${text}`;

            resolve(mockTranslation);
        }, 1500);
    });
}

// Simulate translation (replace with actual API)
async function simulateTranslation(text, sourceLang, targetLang) {
    return new Promise((resolve) => {
        setTimeout(() => {
            // This is a mock translation - replace with actual translation service
            const translations = {
                'en': {
                    'es': 'Esta es una traducción simulada del texto en inglés al español.',
                    'fr': 'Ceci est une traduction simulée du texte anglais vers le français.',
                    'de': 'Dies ist eine simulierte Übersetzung von englischem Text ins Deutsche.',
                    'ja': 'これは英語のテキストから日本語への模擬翻訳です。',
                    'ko': '이것은 영어 텍스트에서 한국어로의 시뮬레이션된 번역입니다.',
                    'zh': '这是从英文文本到中文的模拟翻译。'
                }
            };

            const mockTranslation = translations[sourceLang]?.[targetLang] ||
                `[Translated from ${sourceLang} to ${targetLang}]: ${text}`;

            resolve(mockTranslation);
        }, 1500);
    });
}

// Global variables for file upload
let extractedTextContent = '';
let currentFileInfo = null;
let translatedPdfDownloadUrl = '';

// Global variables for page selection
let selectedPages = [];
let currentFileData = null;
let originalUploadedFile = null; // Store original file for translation

// File upload handler
function handleFileUpload(file) {
    // Store the original file for later use during translation
    originalUploadedFile = file;
    console.log('File stored for translation:', file.name, file.type, file.size);

    // Update file reference in any existing translation UI
    if (currentFileInfo) {
        console.log('Updating file reference for existing translation session');
    }

    const allowedTypes = [
        // Document formats
        'text/plain',                                    // TXT
        'application/pdf',                              // PDF
        'application/vnd.ms-xpsdocument',               // XPS
        'application/oxps',                             // XPS (alternative)
        'application/epub+zip',                         // EPUB
        'application/x-mobipocket-ebook',               // MOBI
        'application/x-fictionbook+xml',                // FB2
        'text/xml',                                     // FB2 (alternative)
        'application/vnd.comicbook+zip',                // CBZ
        'application/zip',                              // CBZ (alternative)
        'image/svg+xml',                                // SVG

        // Image formats
        'image/jpeg',                                   // JPG/JPEG
        'image/png',                                    // PNG
        'image/bmp',                                    // BMP
        'image/gif',                                    // GIF
        'image/tiff',                                   // TIFF
        'image/x-portable-anymap',                      // PNM
        'image/x-portable-graymap',                     // PGM
        'image/x-portable-bitmap',                      // PBM
        'image/x-portable-pixmap',                      // PPM
        'image/x-portable-arbitrarymap',                // PAM
        'image/vnd.ms-photo',                           // JXR
        'image/jxr',                                    // JXR (alternative)
        'image/jp2',                                    // JPX/JP2
        'image/jpx',                                    // JPX/JP2 (alternative)
        'image/vnd.adobe.photoshop',                    // PSD
        'application/octet-stream'                      // PSD (alternative)
    ];

    if (!allowedTypes.includes(file.type)) {
        showNotification('Unsupported file type. Please upload supported document or image formats.', 'error');
        return;
    }

    // Show loading screen
    showFileUploadLoading();

    // Start actual file upload with progress tracking
    uploadFileToServer(file);
}

// Show file upload loading screen
function showFileUploadLoading() {
    const loadingScreen = document.getElementById('fileUploadLoading');
    loadingScreen.style.display = 'flex';
    setTimeout(() => {
        loadingScreen.classList.add('active');
    }, 10);
}

// Hide file upload loading screen
function hideFileUploadLoading() {
    const loadingScreen = document.getElementById('fileUploadLoading');
    loadingScreen.classList.remove('active');
    setTimeout(() => {
        loadingScreen.style.display = 'none';
        }, 300);
}

// Simulate upload progress
// Upload progress is now handled directly in uploadFileToServer function

// Upload file to Django server
function uploadFileToServer(file) {
    const progressFill = document.getElementById('uploadProgressFill');
    const progressText = document.getElementById('uploadProgressText');

    console.log('Starting file upload...');
    console.log('File details:', {
        name: file.name,
        size: file.size,
        type: file.type
    });

    const formData = new FormData();
    formData.append('file', file);

    // Use XMLHttpRequest for real progress tracking
    const xhr = new XMLHttpRequest();

    // Track upload progress
    xhr.upload.onprogress = function(event) {
        if (event.lengthComputable) {
            const percentComplete = (event.loaded / event.total) * 100;
            progressFill.style.width = percentComplete + '%';
            progressText.textContent = `Uploading... ${Math.round(percentComplete)}%`;
        }
    };

    // Handle upload completion
    xhr.onload = function() {
        if (xhr.status === 200) {
            try {
                const data = JSON.parse(xhr.responseText);
                console.log('Response data:', data);

                // Validate response structure
                if (typeof data !== 'object' || data === null) {
                    throw new Error('Invalid JSON response structure');
                }

                if (data.success) {
                    currentFileInfo = data.file_info;

                    // Show processing phase
                    progressFill.style.width = '95%';
                    progressText.textContent = 'Processing file...';

                    // Hide loading screen and show results
                    setTimeout(() => {
                        hideFileUploadLoading();
                        showFileTranslationResults(data);
                    }, 500);

                    if (data.extraction_error) {
                        showNotification(`Warning: ${data.extraction_error}`, 'warning');
                    }
                } else {
                    hideFileUploadLoading();
                    showNotification(`Upload failed: ${data.error}`, 'error');
                }
            } catch (error) {
                console.error('JSON parsing error:', error);
                hideFileUploadLoading();
                showNotification(`Upload failed: Invalid response format`, 'error');
            }
        } else {
            console.error('Upload failed with status:', xhr.status);
            console.error('Response:', xhr.responseText);
            hideFileUploadLoading();
            showNotification(`Upload failed: HTTP ${xhr.status} - ${xhr.responseText}`, 'error');
        }
    };

    // Handle upload errors
    xhr.onerror = function() {
        console.error('Network error during upload');
        hideFileUploadLoading();
        showNotification('Upload failed: Network error', 'error');
    };

    // Handle timeout
    xhr.timeout = 300000; // 5 minutes timeout
    xhr.ontimeout = function() {
        console.error('Upload timeout');
        hideFileUploadLoading();
        showNotification('Upload failed: Timeout - file too large or slow connection', 'error');
    };

    // Start the upload
    xhr.open('POST', 'http://127.0.0.1:8000/api/upload/', true);
    xhr.send(formData);
}

// Test server connectivity
function testServerConnection() {
    console.log('Testing server connection...');

    const xhr = new XMLHttpRequest();
    xhr.open('GET', 'http://127.0.0.1:8000/api/upload/', true);

    xhr.onload = function() {
        console.log('Test response status:', xhr.status);
        console.log('Test response headers:', xhr.getAllResponseHeaders());
        console.log('Test response text:', xhr.responseText);
    };

    xhr.onerror = function() {
        console.error('Test connection failed: Network error');
    };

    xhr.send();
}

// Uncomment the line below to test server connection on page load
// testServerConnection();

// Add a test button to the page for debugging
function addServerTestButton() {
    const testButton = document.createElement('button');
    testButton.textContent = '🧪 Test Server Connection';
    testButton.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        padding: 10px 15px;
        background: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-family: 'Anonymous Pro', monospace;
        font-size: 12px;
        z-index: 9999;
    `;
    testButton.onclick = testServerConnection;
    document.body.appendChild(testButton);
}

// Add test button on page load
document.addEventListener('DOMContentLoaded', addServerTestButton);

// Show file translation results
function showFileTranslationResults(data) {
    // Store the current file data globally
    currentFileData = data;

    // Initialize selected pages as empty
    selectedPages = [];

    // Generate page previews
    generatePagePreviews(data);

    // Update time estimate
    updateTimeEstimate(selectedPages);

    // Add event listeners for page controls
    setupPageControls();

    // Show results screen
    const resultsScreen = document.getElementById('fileTranslationResults');
    resultsScreen.style.display = 'block';
    setTimeout(() => {
        resultsScreen.classList.add('active');
    }, 10);

    console.log('File translation page shown, original file available:', !!originalUploadedFile);
}

// Generate page previews based on file content
function generatePagePreviews(data) {
    const previewContainer = document.getElementById('pagesPreviewContainer');
    const totalPages = data.file_info.pages || 1;

    let pagePreviews = [];

    // Create page previews for all actual pages in the file
    for (let i = 1; i <= totalPages; i++) {
        const isImageFile = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'].includes(data.file_info.extension.toLowerCase());

        pagePreviews.push({
            pageNumber: i,
            isImage: isImageFile,
            isPdf: data.file_info.extension.toLowerCase() === '.pdf'
        });
    }

    // Generate HTML for page previews as icons in a grid
    previewContainer.innerHTML = pagePreviews.map(preview => `
        <div class="page-icon ${selectedPages.includes(preview.pageNumber) ? 'selected' : ''}" data-page="${preview.pageNumber}">
            <div class="page-icon-content">
                ${preview.isImage ?
                    '<div class="page-icon-image">🖼️</div>' :
                    '<div class="page-icon-document">📄</div>'
                }
                <div class="page-number">${preview.pageNumber}</div>
            </div>
            <div class="page-checkmark ${selectedPages.includes(preview.pageNumber) ? 'visible' : ''}">✓</div>
        </div>
    `).join('');

    // Update total pages info
    updateSelectedPagesInfo();
}

// Setup page control event listeners
function setupPageControls() {
    // Select all button
    const selectAllBtn = document.getElementById('selectAllPages');
    if (selectAllBtn) {
        selectAllBtn.addEventListener('click', selectAllPages);
    }

    // Deselect all button
    const deselectAllBtn = document.getElementById('deselectAllPages');
    if (deselectAllBtn) {
        deselectAllBtn.addEventListener('click', deselectAllPages);
    }

    // Page input field
    const pageInput = document.getElementById('selectedPagesInput');
    if (pageInput) {
        pageInput.addEventListener('input', parsePageInput);
    }

    // Page preview clicks
    const previewContainer = document.getElementById('pagesPreviewContainer');
    if (previewContainer) {
        previewContainer.addEventListener('click', handlePagePreviewClick);
    }
}

// Handle individual page icon clicks
function handlePagePreviewClick(event) {
    const pageItem = event.target.closest('.page-icon');
    if (!pageItem) return;

    const pageNumber = parseInt(pageItem.dataset.page);
    if (isNaN(pageNumber)) return;

    togglePageSelection(pageNumber);
}

// Toggle page selection
function togglePageSelection(pageNumber) {
    const index = selectedPages.indexOf(pageNumber);
    if (index > -1) {
        selectedPages.splice(index, 1);
    } else {
        selectedPages.push(pageNumber);
    }

    // Sort selected pages
    selectedPages.sort((a, b) => a - b);

    // Update UI
    updatePageSelectionUI();
    updateTimeEstimate(selectedPages);
}

// Update page selection UI
function updatePageSelectionUI() {
    const pageItems = document.querySelectorAll('.page-icon');

    pageItems.forEach(item => {
        const pageNumber = parseInt(item.dataset.page);
        if (selectedPages.includes(pageNumber)) {
            item.classList.add('selected');
        } else {
            item.classList.remove('selected');
        }
    });

    updateSelectedPagesInfo();
}

// Select all pages
function selectAllPages() {
    const pageItems = document.querySelectorAll('.page-icon');
    selectedPages = [];

    pageItems.forEach(item => {
        const pageNumber = parseInt(item.dataset.page);
        if (!isNaN(pageNumber)) {
            selectedPages.push(pageNumber);
        }
    });

    selectedPages.sort((a, b) => a - b);
    updatePageSelectionUI();
    updateTimeEstimate(selectedPages);
}

// Deselect all pages
function deselectAllPages() {
    selectedPages = [];
    updatePageSelectionUI();
    updateTimeEstimate(selectedPages);
}

// Parse page input (e.g., "1,3,5-8")
function parsePageInput(event) {
    const input = event.target.value.trim();
    if (!input) {
        deselectAllPages();
        return;
    }

    const newSelectedPages = [];
    const parts = input.split(',');

    parts.forEach(part => {
        const trimmed = part.trim();
        if (trimmed.includes('-')) {
            // Handle ranges like "5-8"
            const rangeParts = trimmed.split('-');
            if (rangeParts.length === 2) {
                const start = parseInt(rangeParts[0].trim());
                const end = parseInt(rangeParts[1].trim());
                if (!isNaN(start) && !isNaN(end) && start <= end) {
                    for (let i = start; i <= end; i++) {
                        if (!newSelectedPages.includes(i)) {
                            newSelectedPages.push(i);
                        }
                    }
                }
            }
        } else {
            // Handle individual numbers
            const pageNum = parseInt(trimmed);
            if (!isNaN(pageNum) && !newSelectedPages.includes(pageNum)) {
                newSelectedPages.push(pageNum);
            }
        }
    });

    // Filter to only existing pages
    const maxPages = currentFileData ? (currentFileData.file_info.pages || 1) : 1000;
    selectedPages = newSelectedPages.filter(page => page >= 1 && page <= maxPages).sort((a, b) => a - b);

    updatePageSelectionUI();
    updateTimeEstimate(selectedPages);
}

// Update selected pages info
function updateSelectedPagesInfo() {
    const infoElement = document.getElementById('selectedPagesInfo');
    const totalElement = document.getElementById('totalPagesInfo');

    if (infoElement) {
        if (selectedPages.length === 0) {
            infoElement.textContent = 'No pages selected';
        } else if (selectedPages.length === 1) {
            infoElement.textContent = '1 page selected';
    } else {
            infoElement.textContent = `${selectedPages.length} pages selected`;
        }
    }

    if (totalElement) {
        const totalPages = currentFileData ? (currentFileData.file_info.pages || 1) : 0;
        totalElement.textContent = `Total: ${totalPages} pages`;
    }
}

// Update time estimate based on selected pages
function updateTimeEstimate(selectedPages) {
    const estimateElement = document.getElementById('timeEstimate');
    if (!estimateElement) return;

    if (selectedPages.length === 0) {
        estimateElement.textContent = '--';
        return;
    }

    // Calculate estimated time (4-5 seconds per page)
    const avgSecondsPerPage = 4.5;
    const totalSeconds = selectedPages.length * avgSecondsPerPage;

    if (totalSeconds < 60) {
        estimateElement.textContent = `${Math.round(totalSeconds)}s`;
                } else {
        const minutes = Math.floor(totalSeconds / 60);
        const seconds = Math.round(totalSeconds % 60);
        estimateElement.textContent = `${minutes}m ${seconds}s`;
    }
}

// Hide file translation results and go back to main
function hideFileTranslation() {
    const resultsScreen = document.getElementById('fileTranslationResults');
    const translationOutput = document.getElementById('fileTranslationOutput');

    // Hide translation output if visible
    if (translationOutput) {
        translationOutput.style.display = 'none';
    }

    // Hide results screen
    resultsScreen.classList.remove('active');
    setTimeout(() => {
        resultsScreen.style.display = 'none';
    }, 300);

    // Reset variables
selectedPages = [];
extractedTextContent = '';
currentFileInfo = null;
translatedPdfDownloadUrl = '';
currentFileData = null;
originalUploadedFile = null;
}

// Hide translation output
function hideFileTranslationOutput() {
    const translationOutput = document.getElementById('fileTranslationOutput');
    if (translationOutput) {
        translationOutput.style.display = 'none';
    }
}

// Translate file content
function translateFileContent() {
    if (!currentFileData) {
        showNotification('No file data available', 'error');
        return;
    }

    if (selectedPages.length === 0) {
        showNotification('Please select at least one page to translate', 'error');
        return;
    }

    const translateBtn = document.getElementById('translateFileBtn');
    const targetLanguage = document.getElementById('fileTargetLanguage').value;

    // Show loading state
    translateBtn.classList.add('loading');

    // Start timer
    const startTime = performance.now();

        // Use the stored original file from upload
    console.log('Original uploaded file:', originalUploadedFile);

    // Also check if there's a file in the file input (fallback)
    if (!originalUploadedFile) {
        const fileInput = document.getElementById('fileInput');
        if (fileInput && fileInput.files.length > 0) {
            originalUploadedFile = fileInput.files[0];
            console.log('Using file from file input as fallback:', originalUploadedFile.name);
        }
    }

    if (!originalUploadedFile) {
        showNotification('Please upload a file first', 'error');
        translateBtn.classList.remove('loading');
        return;
    }

    const formData = new FormData();
    formData.append('file', originalUploadedFile);  // Use original file like test_upload.html
    formData.append('target_language', targetLanguage);
    formData.append('service_name', 'gemini');

    // Add selected pages if any are selected
    if (selectedPages.length > 0 && selectedPages.length !== currentFileInfo.pages) {
        formData.append('pages', selectedPages.join(','));
    }

    showNotification(`Starting file translation with Google Gemini 2.5 Flash... This may take a few minutes depending on the number of pages.`, 'success');

    // Use XMLHttpRequest for translation (like test_upload.html)
    const xhr = new XMLHttpRequest();

    // Handle translation completion
    xhr.onload = function() {
        translateBtn.classList.remove('loading');

        // Calculate translation time
        const endTime = performance.now();
        const translationTime = ((endTime - startTime) / 1000).toFixed(2);

        if (xhr.status === 200) {
            try {
                const data = JSON.parse(xhr.responseText);
                console.log('Translation response:', data);

                if (data && data.success) {
                    translatedPdfDownloadUrl = data.download_url; // Match test_upload.html exactly
                    console.log('Translation successful:', {
                        downloadUrl: translatedPdfDownloadUrl,
                        translatedPages: data.translated_pages,
                        selectedPages: selectedPages.length,
                        fullResponse: data
                    });

                    // Show download section with success message
                    showFileTranslationSuccess(targetLanguage, 'Google Gemini 2.5 Flash', translationTime);
                    showNotification(`Successfully translated ${data.translated_pages || selectedPages.length} pages using Google Gemini 2.5 Flash in ${translationTime}s!`, 'success');
                } else if (data) {
                    console.error('Translation failed with response:', data);
                    showNotification(`Translation failed: ${data.error}`, 'error');
                } else {
                    console.error('Translation failed with empty response');
                    showNotification('Translation failed: Empty response from server', 'error');
                }
    } catch (error) {
                console.error('JSON parsing error:', error);
                console.error('Response text:', xhr.responseText);
                showNotification(`Translation failed: Invalid response format - ${xhr.responseText}`, 'error');
            }
        } else {
            console.error('Translation failed with status:', xhr.status);
            console.error('Response:', xhr.responseText);
            showNotification(`Translation failed: HTTP ${xhr.status} - ${xhr.responseText}`, 'error');
        }
    };

    // Handle translation errors
    xhr.onerror = function() {
        translateBtn.classList.remove('loading');
        console.error('Network error during translation');
        showNotification('Translation failed: Network error', 'error');
    };

    // Handle timeout
    xhr.timeout = 300000; // 5 minutes timeout
    xhr.ontimeout = function() {
        translateBtn.classList.remove('loading');
        console.error('Translation timeout');
        showNotification('Translation failed: Timeout - translation taking too long', 'error');
    };

    // Start the translation - use the correct endpoint like test_upload.html
    xhr.open('POST', 'http://127.0.0.1:8000/api/translate-pdf/', true);
    xhr.send(formData);
}

// Get text content for selected pages
function getSelectedPagesText() {
    if (!currentFileData || selectedPages.length === 0) {
        return '';
    }

    const text = currentFileData.extracted_text || '';
    const words = text.split(/\s+/);
    const avgWordsPerPage = 250; // Same as used in generatePagePreviews
    const selectedTextParts = [];

    selectedPages.forEach(pageNum => {
        const startWord = (pageNum - 1) * avgWordsPerPage;
        const endWord = pageNum * avgWordsPerPage;
        const pageText = words.slice(startWord, endWord).join(' ');
        if (pageText.trim()) {
            selectedTextParts.push(`--- Page ${pageNum} ---\n${pageText}`);
        }
    });

    return selectedTextParts.join('\n\n');
}

// Show file translation success message
function showFileTranslationSuccess(targetLanguage, service, time) {
    const translationOutput = document.getElementById('fileTranslationOutput');

    if (translationOutput) {
                        // Create success message HTML
        const successHTML = `
            <div class="download-success">
                <div class="success-icon-small">✅</div>
                <div class="success-message">
                    <strong>Translation Complete!</strong><br>
                    Translated to ${targetLanguage} using Google Gemini 2.5 Flash in ${time} seconds<br>
                    Click the download button below to get your translated file.
                </div>
            </div>
            <div class="download-actions">
                <button id="downloadTranslationBtn" class="download-btn">
                    <span class="download-icon">📥</span>
                    Download Translated File
                </button>
            </div>
        `;

        translationOutput.innerHTML = successHTML;
        translationOutput.style.display = 'flex';
        translationOutput.classList.add('show');

        // Re-attach download event listener
        const downloadBtn = document.getElementById('downloadTranslationBtn');
        if (downloadBtn) {
            downloadBtn.addEventListener('click', downloadTranslatedFile);
        }
    }
}

// Show file translation output (legacy function)
function showFileTranslationOutput(translatedText, targetLanguage, service, time) {
    const translationOutput = document.getElementById('fileTranslationOutput');
    const translationResult = document.getElementById('translationResultContent');

    if (translationOutput && translationResult) {
        translationResult.textContent = translatedText;
        translationOutput.style.display = 'flex';
        translationOutput.classList.add('show');
    }
}

// Download translated file
function downloadTranslatedFile() {
    if (!translatedPdfDownloadUrl) {
        showNotification('No translated file available for download', 'error');
        return;
    }

    console.log('Download URL:', translatedPdfDownloadUrl);
    console.log('Current file info:', currentFileInfo);

    // Validate download URL
    if (!translatedPdfDownloadUrl || translatedPdfDownloadUrl.trim() === '') {
        console.error('Invalid download URL:', translatedPdfDownloadUrl);
        showNotification('Invalid download URL received from server', 'error');
        return;
    }

    // Ensure URL has proper protocol
    if (!translatedPdfDownloadUrl.startsWith('http://') && !translatedPdfDownloadUrl.startsWith('https://')) {
        translatedPdfDownloadUrl = 'http://127.0.0.1:8000' + translatedPdfDownloadUrl;
        console.log('Fixed download URL to:', translatedPdfDownloadUrl);
    }

    // Try to validate download URL (optional - skip if server doesn't support HEAD)
    console.log('Validating download URL:', translatedPdfDownloadUrl);

    // First, create the download link immediately (like test_upload.html does)
    const link = document.createElement('a');
    link.href = translatedPdfDownloadUrl;
    link.download = 'translated_document.pdf'; // Use fixed filename like test_upload.html
    link.target = '_blank'; // Open in new tab if direct download fails
    document.body.appendChild(link);

    // Optional validation - don't block download if it fails
    fetch(translatedPdfDownloadUrl, { method: 'HEAD' })
        .then(response => {
            console.log('Download URL validation response:', {
                status: response.status,
                statusText: response.statusText,
                contentType: response.headers.get('content-type'),
                contentLength: response.headers.get('content-length'),
                url: response.url
            });

            if (response.status === 405) {
                console.log('Server doesn\'t support HEAD requests, but download should still work');
            } else if (response.status !== 200) {
                console.warn(`Server returned ${response.status} for download URL, but proceeding with download anyway`);
            }
        })
        .catch(error => {
            console.log('Download URL validation failed, but proceeding with download anyway:', error.message);
        })
        .finally(() => {
            // Always trigger the download regardless of validation result
            link.click();
            document.body.removeChild(link);
            showNotification('Download started!', 'success');
        });
}

// Utility functions
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function countWords(text) {
    return text.trim().split(/\s+/).filter(word => word.length > 0).length;
}

// Loading state management
function setLoadingState(loading) {
    if (loading) {
        translateBtn.classList.add('loading');
        translateBtn.disabled = true;
        inputText.disabled = true;
        copyBtn.disabled = true;
    } else {
        translateBtn.classList.remove('loading');
        translateBtn.disabled = false;
        inputText.disabled = false;

        // Re-enable action buttons if there's output
        if (outputText.value) {
            copyBtn.disabled = false;
        }
    }
}

// Notification system
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notification => notification.remove());

    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;

    // Style the notification
    Object.assign(notification.style, {
        position: 'fixed',
        top: '100px',
        right: '20px',
        padding: '1rem 1.5rem',
        borderRadius: '14px',
        fontWeight: '500',
        zIndex: '9999',
        maxWidth: '300px',
        wordWrap: 'break-word',
        boxShadow: '0 10px 30px rgba(0, 0, 0, 0.2)',
        transform: 'translateX(100%)',
        transition: 'transform 0.3s ease'
    });

    // Set colors based on type
    if (type === 'success') {
        notification.style.background = '#d4edda';
        notification.style.color = '#155724';
        notification.style.border = '1px solid #c3e6cb';
    } else if (type === 'warning') {
        notification.style.background = '#fff3cd';
        notification.style.color = '#856404';
        notification.style.border = '1px solid #ffeaa7';
    } else if (type === 'error') {
        notification.style.background = '#f8d7da';
        notification.style.color = '#721c24';
        notification.style.border = '1px solid #f5c6cb';
    } else {
        notification.style.background = '#d1ecf1';
        notification.style.color = '#0c5460';
        notification.style.border = '1px solid #bee5eb';
    }

    document.body.appendChild(notification);

    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);

    // Animate out and remove
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 4000);
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to translate
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        if (!translateBtn.disabled) {
            performTranslation();
        }
    }

    // Ctrl/Cmd + K to focus input
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        inputText.focus();
    }

    // Escape to clear
    if (e.key === 'Escape') {
        inputText.value = '';
        outputText.value = '';
        charCount.textContent = '0';
        outputText.classList.remove('success', 'error');
        copyBtn.disabled = true;
    }
});

// Auto-resize textareas - removed to keep static size
// function autoResize(textarea) {
//     textarea.style.height = 'auto';
//     textarea.style.height = Math.min(textarea.scrollHeight, 300) + 'px';
// }

// inputText.addEventListener('input', function() {
//     autoResize(this);
// });

// Theme detection and adaptation
function detectTheme() {
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        // User prefers dark theme - could add dark mode support here
        console.log('Dark theme detected');
    }
}

// Initialize theme detection
detectTheme();

// Listen for theme changes
if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', detectTheme);
}

// Performance optimization: Intersection Observer for lazy loading
const lazyLoadObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const img = entry.target;
            if (img.dataset.src) {
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                lazyLoadObserver.unobserve(img);
            }
        }
    });
});

// Observe all images with data-src
document.querySelectorAll('img[data-src]').forEach(img => {
    lazyLoadObserver.observe(img);
});

// Service Worker registration for PWA (optional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}

// Export functions for testing (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        performTranslation,
        handleFileUpload,
        showNotification,
        setLoadingState
    };
}
