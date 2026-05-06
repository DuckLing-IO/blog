(async function () {
  const path = window.location.pathname;
  const match = path.match(/\/post\/(.+)\.html/);
  if (!match) return;
  const slug = match[1];

  const API = 'https://views.duckee.top/counter/';

  try {
    const res = await fetch(API + slug, { method: 'POST' });
    const data = await res.json();
    const el = document.getElementById('view-count');
    if (el) el.textContent = data.views;
  } catch (e) {
    // Silently fail — don't break the page
  }
})();
