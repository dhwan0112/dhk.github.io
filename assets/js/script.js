// Theme Toggle
const themeToggle = document.getElementById('theme-toggle');
const html = document.documentElement;

// Check for saved theme preference or default to light mode
const currentTheme = localStorage.getItem('theme') || 'light';
html.setAttribute('data-theme', currentTheme);

// Update button text and icon based on current theme
function updateThemeButton(theme) {
    if (!themeToggle) return;
    const icon = themeToggle.querySelector('i');
    const text = themeToggle.querySelector('span');
    if (theme === 'dark') {
        icon.className = 'fas fa-sun';
        text.textContent = 'Light Mode';
    } else {
        icon.className = 'fas fa-moon';
        text.textContent = 'Dark Mode';
    }
}

// Theme toggle event listener
if (themeToggle) {
    // Initialize button state
    updateThemeButton(currentTheme);

    themeToggle.addEventListener('click', () => {
        const currentTheme = html.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';

        html.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeButton(newTheme);
    });
}

// Sidebar Toggle for Mobile
const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
const sidebar = document.querySelector('.sidebar');
const sidebarLinks = document.querySelectorAll('.sidebar-link');

if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener('click', () => {
        sidebar.classList.toggle('active');

        // Animate toggle button
        const spans = mobileMenuToggle.querySelectorAll('span');
        if (sidebar.classList.contains('active')) {
            spans[0].style.transform = 'rotate(-45deg) translate(-5px, 5px)';
            spans[1].style.opacity = '0';
            spans[2].style.transform = 'rotate(45deg) translate(-5px, -5px)';
        } else {
            spans[0].style.transform = 'none';
            spans[1].style.opacity = '1';
            spans[2].style.transform = 'none';
        }
    });
}

// Close sidebar when clicking on a link (mobile)
sidebarLinks.forEach(link => {
    link.addEventListener('click', () => {
        if (window.innerWidth <= 992) {
            sidebar.classList.remove('active');
            const spans = mobileMenuToggle.querySelectorAll('span');
            spans[0].style.transform = 'none';
            spans[1].style.opacity = '1';
            spans[2].style.transform = 'none';
        }
    });
});

// Update active sidebar link on scroll
window.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('section');
    const scrollPosition = window.pageYOffset + 200;

    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.offsetHeight;
        const sectionId = section.getAttribute('id');

        if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
            sidebarLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${sectionId}`) {
                    link.classList.add('active');
                }
            });
        }
    });
});

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const headerOffset = 80;
            const elementPosition = target.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });
        }
    });
});

// Intersection Observer for fade-in animation
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Animate elements on scroll
document.addEventListener('DOMContentLoaded', () => {
    const animateElements = document.querySelectorAll('.project-card, .skill-category, .info-item, .contact-item');

    animateElements.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(30px)';
        element.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
        observer.observe(element);
    });
});

// Subtle fade-in for sections (minimal animation)
const revealSections = document.querySelectorAll('section');
const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
        }
    });
}, {
    threshold: 0,
    rootMargin: '0px 0px -40px 0px'
});

revealSections.forEach(section => {
    if (!section.classList.contains('hero')) {
        section.style.opacity = '0';
        section.style.transition = 'opacity 0.4s ease-out';
        revealObserver.observe(section);
    }
});

// ---------- Blog: tag filter (?tag=...) ----------
(() => {
    const list = document.getElementById('post-list');
    if (!list) return;
    const items = Array.from(list.querySelectorAll('.post-item'));
    const links = Array.from(document.querySelectorAll('.blog-tag-link'));
    const empty = document.getElementById('post-list-empty');

    const apply = (tag) => {
        let shown = 0;
        items.forEach(item => {
            const tags = (item.dataset.tags || '').split('|').filter(Boolean);
            const show = !tag || tags.includes(tag);
            item.hidden = !show;
            if (show) shown++;
        });
        links.forEach(l => l.classList.toggle('is-active', (l.dataset.tag || '') === (tag || '')));
        if (empty) empty.hidden = shown !== 0;
    };

    const current = () => new URLSearchParams(location.search).get('tag') || '';
    apply(current());

    document.addEventListener('click', (e) => {
        const a = e.target.closest('a[data-tag]');
        if (!a || !(list.contains(a) || a.classList.contains("blog-tag-link"))) return;
        e.preventDefault();
        const tag = a.dataset.tag || '';
        const url = tag ? `?tag=${encodeURIComponent(tag)}` : location.pathname;
        history.pushState(null, '', url);
        apply(tag);
    });
    window.addEventListener('popstate', () => apply(current()));
})();

// ---------- Post: side table of contents ----------
(() => {
    const body = document.getElementById('post-body');
    const toc = document.getElementById('post-toc');
    if (!body || !toc) return;
    const headings = Array.from(body.querySelectorAll('h2, h3'));
    if (headings.length < 2) return;

    const nav = toc.querySelector('.post-toc-nav');
    const used = new Set();
    headings.forEach((h, i) => {
        if (!h.id) {
            let base = h.textContent.trim().toLowerCase().replace(/[^\p{L}\p{N}]+/gu, '-').replace(/^-+|-+$/g, '') || `section-${i}`;
            let id = base, n = 2;
            while (used.has(id) || document.getElementById(id)) id = `${base}-${n++}`;
            h.id = id;
        }
        used.add(h.id);
        const a = document.createElement('a');
        a.href = `#${h.id}`;
        a.textContent = h.textContent;
        a.className = h.tagName === 'H3' ? 'toc-h3' : 'toc-h2';
        nav.appendChild(a);
    });
    toc.hidden = false;

    const linkFor = new Map(headings.map((h, i) => [h, nav.children[i]]));
    let active = null;
    const setActive = (h) => {
        if (!h || h === active) return;
        if (active) linkFor.get(active).classList.remove('is-active');
        active = h;
        linkFor.get(h).classList.add('is-active');
    };

    const update = () => {
        const line = window.innerHeight * 0.25;
        let current = headings[0];
        for (const h of headings) {
            if (h.getBoundingClientRect().top <= line) current = h; else break;
        }
        setActive(current);
    };
    window.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    update();
})();
