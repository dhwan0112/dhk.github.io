// Theme toggle. The initial theme is set in <head> (saved choice, else the system setting).
const themeToggle = document.getElementById('theme-toggle');
const root = document.documentElement;

function labelThemeButton() {
    if (!themeToggle) return;
    themeToggle.textContent = root.getAttribute('data-theme') === 'dark' ? 'Light mode' : 'Dark mode';
}

if (themeToggle) {
    labelThemeButton();
    themeToggle.addEventListener('click', () => {
        const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        root.setAttribute('data-theme', next);
        try { localStorage.setItem('theme', next); } catch (e) {}
        labelThemeButton();
    });
}

// Sidebar on small screens
const menuToggle = document.querySelector('.mobile-menu-toggle');
const sidebar = document.querySelector('.sidebar');

function setMenu(open) {
    if (!menuToggle || !sidebar) return;
    sidebar.classList.toggle('active', open);
    menuToggle.setAttribute('aria-expanded', String(open));
    menuToggle.textContent = open ? 'Close' : 'Menu';
}

if (menuToggle) {
    menuToggle.addEventListener('click', () => setMenu(!sidebar.classList.contains('active')));
    document.querySelectorAll('.sidebar a').forEach(link => {
        link.addEventListener('click', () => setMenu(false));
    });
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') setMenu(false);
    });
}

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
