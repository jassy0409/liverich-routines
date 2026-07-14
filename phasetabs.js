/* Phasebar tabs: swap module content in place instead of navigating. */
(function () {
  function qs(s, d) { return (d || document).querySelector(s); }

  async function load(url, push) {
    try {
      const r = await fetch(url, { cache: 'no-cache' });
      if (!r.ok) throw new Error(r.status);
      const doc = new DOMParser().parseFromString(await r.text(), 'text/html');

      /* carry over the target page's own inline styles (e.g. Module 1) */
      document.querySelectorAll('style[data-swap]').forEach(e => e.remove());
      doc.querySelectorAll('style').forEach(st => {
        const c = st.cloneNode(true);
        c.setAttribute('data-swap', '');
        document.head.appendChild(c);
      });

      [['header.hero'], ['main'], ['footer']].forEach(([sel]) => {
        const src = doc.querySelector(sel), dst = qs(sel);
        if (src && dst) dst.innerHTML = src.innerHTML;
      });
      const p1 = qs('.topbar .pill'), p2 = doc.querySelector('.topbar .pill');
      if (p1 && p2) p1.textContent = p2.textContent;
      document.title = doc.title;

      if (push !== false) history.pushState({ tab: url }, '', url);
      window.scrollTo({ top: 0 });
    } catch (e) {
      location.href = url; /* graceful fallback to normal navigation */
    }
  }

  document.addEventListener('click', function (e) {
    const a = e.target.closest('a.ph');
    if (!a) return;
    e.preventDefault();
    if (!a.classList.contains('on')) load(a.getAttribute('href'));
  });

  window.addEventListener('popstate', function () {
    load(location.pathname.split('/').pop() || 'index.html', false);
  });
})();
