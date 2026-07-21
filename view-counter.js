(async function () {
  const path = decodePath(window.location.pathname);
  if (!/^\/post\/.+\.html$/.test(path)) return;
  const title = document.querySelector('h1')?.textContent?.trim()
    || path.split('/').pop().replace(/\.html$/, '');
  const API = 'https://views.duckee.top/api/v1/views';

  const footer = document.querySelector('.post-footer p');
  if (footer && !footer.querySelector('[data-privacy-link]')) {
    const privacyLink = document.createElement('a');
    privacyLink.href = 'https://www.duckee.top/privacy.html';
    privacyLink.textContent = '访客数据说明';
    privacyLink.dataset.privacyLink = '';
    privacyLink.style.marginLeft = '.65em';
    footer.append(' · ', privacyLink);
  }

  try {
    const res = await fetch(API, {
      method: 'POST',
      cache: 'no-store',
      keepalive: true,
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({ site: 'blog', path, title, referrer: document.referrer }),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    const el = document.getElementById('view-count');
    if (el && Number.isFinite(Number(data.views))) {
      el.textContent = Number(data.views).toLocaleString('zh-CN');
    }
  } catch (e) {
    // Silently fail — don't break the page
  }

  function decodePath(value) {
    try { return decodeURI(value); } catch { return value; }
  }
})();
