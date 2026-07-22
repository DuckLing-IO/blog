(async function () {
  const counter = document.getElementById('view-count');
  if (!counter) return;

  const path = decodePath(window.location.pathname);
  if (!/^\/post\/.+\.html$/.test(path)) return;

  const title = document.querySelector('h1')?.textContent?.trim()
    || path.split('/').pop().replace(/\.html$/, '');
  const api = 'https://views.duckee.top/api/v1/views';

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
    const response = await fetch(api, {
      method: 'POST',
      cache: 'no-store',
      keepalive: true,
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({ site: 'blog', path, title, referrer: document.referrer }),
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);

    const data = await response.json();
    const views = Number(data.views);
    if (!Number.isFinite(views)) throw new Error('Invalid view count');

    counter.textContent = `${views.toLocaleString('zh-CN')} 次浏览`;
  } catch (error) {
    counter.textContent = '浏览量暂不可用';
    console.warn('Unable to load the article view count.', error);
  }

  function decodePath(value) {
    try { return decodeURI(value); } catch { return value; }
  }
})();
