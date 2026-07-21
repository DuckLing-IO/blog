(function () {
  const input = document.getElementById('post-search');
  const posts = [...document.querySelectorAll('[data-post]')];
  const groups = [...document.querySelectorAll('[data-post-group]')];
  const status = document.getElementById('search-status');
  const empty = document.getElementById('empty-search');

  if (!input || !posts.length) return;

  function applyFilter(updateUrl) {
    const rawQuery = input.value.trim();
    const query = rawQuery.toLocaleLowerCase('zh-CN');
    let visibleCount = 0;

    posts.forEach((post) => {
      const matches = !query || post.dataset.search.includes(query);
      post.hidden = !matches;
      if (matches) visibleCount += 1;
    });

    groups.forEach((group) => {
      group.hidden = !group.querySelector('[data-post]:not([hidden])');
    });

    empty.hidden = visibleCount !== 0;
    status.textContent = query ? `找到 ${visibleCount} 篇文章` : '';
    if (updateUrl) {
      const url = new URL(window.location.href);
      if (rawQuery) url.searchParams.set('q', rawQuery);
      else url.searchParams.delete('q');
      window.history.replaceState({}, '', url);
    }
  }

  const initialQuery = new URL(window.location.href).searchParams.get('q');
  if (initialQuery) {
    input.value = initialQuery;
    applyFilter(false);
  }

  input.addEventListener('input', () => applyFilter(true));
})();
