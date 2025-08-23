// Component Loader - Loads header and footer consistently across all pages
class ComponentLoader {
    constructor() {
        this.currentPage = this.getCurrentPage();
        this.init();
    }

    async init() {
        await this.loadHeader();
        await this.loadFooter();
        
        // Small delay to ensure DOM elements are available
        setTimeout(() => {
            this.initializeNavigation();
            this.initializeScrollProgress();
            this.initializeBackToTop();
            this.setActiveNavItem();
            this.initializeScrollSectionDetection();
            this.initializeLanguageSelector();
        }, 100);
    }

    getCurrentPage() {
        const path = window.location.pathname;
        const filename = path.split('/').pop().replace('.html', '') || 'index';
        return filename === 'index' ? 'home' : filename;
    }

    async loadHeader() {
        try {
            const response = await fetch('header.html');
            const headerHTML = await response.text();
            document.querySelector('#header-placeholder, .header-placeholder').innerHTML = headerHTML;
        } catch (error) {
            console.error('Failed to load header:', error);
        }
    }

    async loadFooter() {
        try {
            const response = await fetch('footer.html');
            const footerHTML = await response.text();
            document.querySelector('#footer-placeholder, .footer-placeholder').innerHTML = footerHTML;
        } catch (error) {
            console.error('Failed to load footer:', error);
        }
    }

    setActiveNavItem() {
        // Remove all active classes first
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });

        // Get current page and hash
        const currentPath = window.location.pathname;
        const currentHash = window.location.hash;
        const filename = currentPath.split('/').pop().replace('.html', '') || 'index';
        
        // Set active based on current page
        if (filename === 'index' || filename === '') {
            // On homepage, check for hash sections
            if (currentHash) {
                const sectionName = currentHash.replace('#', '');
                const sectionLink = document.querySelector(`[data-page="${sectionName}"]`);
                if (sectionLink) {
                    sectionLink.classList.add('active');
                } else {
                    // Default to home if hash doesn't match
                    const homeLink = document.querySelector('[data-page="home"]');
                    if (homeLink) homeLink.classList.add('active');
                }
            } else {
                // No hash, highlight home
                const homeLink = document.querySelector('[data-page="home"]');
                if (homeLink) homeLink.classList.add('active');
            }
        }
        // For other pages (login, privacy, terms, contact), don't highlight any nav items
    }

    initializeNavigation() {
        const navbar = document.querySelector('.navbar');
        let lastScrollY = window.scrollY;

        // Handle navigation clicks for single page sections
        document.querySelectorAll('.nav-link[href^="#"], .nav-link[href*="#"]').forEach(link => {
            link.addEventListener('click', (e) => {
                const href = link.getAttribute('href');
                if (href.includes('#')) {
                    const targetId = href.split('#')[1];
                    const targetElement = document.getElementById(targetId);
                    
                    if (targetElement) {
                        e.preventDefault();
                        targetElement.scrollIntoView({ 
                            behavior: 'smooth',
                            block: 'start'
                        });
                        
                        // Update URL without page reload
                        history.pushState(null, null, `#${targetId}`);
                        
                        // Update active nav item
                        document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
                        link.classList.add('active');
                    }
                }
            });
        });
    }

    initializeScrollProgress() {
        // Consolidated scroll handler with throttling for better performance
        this.initializeOptimizedScrollHandler();
    }

    initializeOptimizedScrollHandler() {
        const navbar = document.querySelector('.navbar');
        const scrollProgress = document.getElementById('scrollProgress');
        const backToTop = document.getElementById('backToTop');
        
        // Throttle function for better performance
        let ticking = false;
        
        const updateOnScroll = () => {
            const currentScrollY = window.scrollY;
            
            // Navbar scroll behavior
            if (navbar) {
                if (currentScrollY > 100) {
                    navbar.classList.add('scrolled');
                } else {
                    navbar.classList.remove('scrolled');
                }
            }
            
            // Scroll progress bar
            if (scrollProgress) {
                const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
                const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
                const scrolled = (winScroll / height) * 100;
                scrollProgress.style.width = scrolled + '%';
            }
            
            // Back to top button
            if (backToTop) {
                if (currentScrollY > 300) {
                    backToTop.classList.add('visible');
                } else {
                    backToTop.classList.remove('visible');
                }
            }
            
            ticking = false;
        };
        
        const requestTick = () => {
            if (!ticking) {
                requestAnimationFrame(updateOnScroll);
                ticking = true;
            }
        };
        
        // Single scroll event listener with throttling
        window.addEventListener('scroll', requestTick, { passive: true });
    }

    initializeBackToTop() {
        const backToTop = document.getElementById('backToTop');
        if (!backToTop) return;

        // Back to top functionality (scroll behavior handled in optimized handler)
        backToTop.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    initializeScrollSectionDetection() {
        // Only on homepage
        const currentPath = window.location.pathname;
        const filename = currentPath.split('/').pop().replace('.html', '') || 'index';
        
        console.log('Current path:', currentPath, 'Filename:', filename);
        
        if (filename !== 'index' && filename !== '') return;

        const sections = ['home', 'features', 'faq'];
        const sectionElements = sections.map(id => document.getElementById(id)).filter(Boolean);
        
        console.log('Found sections:', sectionElements.map(el => el.id));
        
        if (sectionElements.length === 0) return;

        // Check if nav links exist
        const navLinks = document.querySelectorAll('.nav-link[data-page]');
        console.log('Found nav links:', Array.from(navLinks).map(link => link.getAttribute('data-page')));

        // Function to update active navigation
        const updateActiveNav = (activeId) => {
            console.log('Updating active nav to:', activeId);
            
            // Remove all active classes
            document.querySelectorAll('.nav-link').forEach(link => {
                link.classList.remove('active');
            });
            
            // Add active class to current section
            const activeLink = document.querySelector(`[data-page="${activeId}"]`);
            if (activeLink) {
                activeLink.classList.add('active');
                console.log('Successfully activated:', activeId);
            } else {
                console.log('Could not find nav link for:', activeId);
            }
        };

        // Simplified scroll-based detection
        const detectActiveSection = () => {
            const scrollPosition = window.scrollY + window.innerHeight / 3; // Trigger when 1/3 down viewport
            
            let activeSection = 'home'; // Default to home
            
            sectionElements.forEach(section => {
                const rect = section.getBoundingClientRect();
                const sectionTop = window.scrollY + rect.top;
                
                if (scrollPosition >= sectionTop) {
                    activeSection = section.id;
                }
            });
            
            return activeSection;
        };

        // Throttled scroll handler
        let ticking = false;
        const handleScroll = () => {
            if (!ticking) {
                requestAnimationFrame(() => {
                    const activeSection = detectActiveSection();
                    updateActiveNav(activeSection);
                    ticking = false;
                });
                ticking = true;
            }
        };

        // Initial setup
        setTimeout(() => {
            const initialSection = detectActiveSection();
            updateActiveNav(initialSection);
            console.log('Initial active section set to:', initialSection);
        }, 200);

        // Add scroll listener
        window.addEventListener('scroll', handleScroll, { passive: true });
        
        // Store for cleanup
        this.scrollSectionHandler = handleScroll;
    }

    // Language selector functionality
    initializeLanguageSelector() {
        const languageSelector = document.getElementById('interfaceLanguage');
        if (!languageSelector) return;

        // Load saved language preference
        const savedLanguage = localStorage.getItem('transverse_language') || 'en';
        languageSelector.value = savedLanguage;

        // Handle language changes
        languageSelector.addEventListener('change', (e) => {
            const selectedLanguage = e.target.value;
            localStorage.setItem('transverse_language', selectedLanguage);
            
            // In a real app, this would trigger translation
            console.log(`Language changed to: ${selectedLanguage}`);
        });
    }
}

// Initialize component loader when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new ComponentLoader();
});

// Export for use in other scripts
window.ComponentLoader = ComponentLoader;
