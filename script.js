// Current year in footer
document.getElementById('year').textContent = new Date().getFullYear();

// Mobile nav toggle
const toggle = document.querySelector('.nav-toggle');
const links = document.querySelector('.nav-links');
toggle.addEventListener('click', () => links.classList.toggle('open'));
links.addEventListener('click', (e) => {
    if (e.target.tagName === 'A') links.classList.remove('open');
});

// Scroll reveal
const observer = new IntersectionObserver(
    (entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add('in');
                observer.unobserve(entry.target);
            }
        });
    },
    { threshold: 0.12 }
);
document.querySelectorAll('.reveal').forEach((el, i) => {
    el.style.transitionDelay = `${Math.min(i % 6, 5) * 0.06}s`;
    observer.observe(el);
});

// Live tech news feed (Hacker News front page via Algolia API)
(function loadNews() {
    const feed = document.getElementById('news-feed');
    if (!feed) return;

    function domainOf(url) {
        try { return new URL(url).hostname.replace(/^www\./, ''); }
        catch { return 'news.ycombinator.com'; }
    }
    function escapeHtml(s) {
        const d = document.createElement('div');
        d.textContent = s;
        return d.innerHTML;
    }

    fetch('https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=9')
        .then((r) => {
            if (!r.ok) throw new Error('Network error');
            return r.json();
        })
        .then((data) => {
            const hits = (data.hits || []).filter((h) => h.title).slice(0, 9);
            if (!hits.length) throw new Error('No stories');
            feed.classList.remove('reveal');
            feed.innerHTML = hits
                .map((h, i) => {
                    const link = h.url || `https://news.ycombinator.com/item?id=${h.objectID}`;
                    const rank = String(i + 1).padStart(2, '0');
                    return `
                        <a class="news-card" href="${link}" target="_blank" rel="noopener">
                            <span class="news-rank">#${rank}</span>
                            <span class="news-title">${escapeHtml(h.title)}</span>
                            <span class="news-meta">
                                <span class="news-domain">${escapeHtml(domainOf(h.url || ''))}</span>
                                <span>▲ ${h.points ?? 0}</span>
                                <span>💬 ${h.num_comments ?? 0}</span>
                            </span>
                        </a>`;
                })
                .join('');
        })
        .catch(() => {
            feed.innerHTML =
                '<p class="news-status">Couldn\'t load live news right now. ' +
                'Check out <a class="inline-link" href="https://news.ycombinator.com" target="_blank" rel="noopener">Hacker News</a> directly.</p>';
        });
})();
