export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const headers = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Content-Type': 'application/json',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers });
    }

    const slug = url.pathname.replace('/counter/', '').replace(/\/$/, '');
    if (!slug) {
      return new Response(JSON.stringify({ error: 'Missing article ID' }), {
        status: 400, headers
      });
    }

    if (request.method === 'GET') {
      const count = await env.VIEW_COUNTS.get(slug) || '0';
      return new Response(JSON.stringify({ slug, views: parseInt(count) }), { headers });
    }

    if (request.method === 'POST') {
      const newCount = (parseInt(await env.VIEW_COUNTS.get(slug) || '0')) + 1;
      await env.VIEW_COUNTS.put(slug, newCount.toString());
      return new Response(JSON.stringify({ slug, views: newCount }), { headers });
    }

    return new Response(JSON.stringify({ error: 'Method not allowed' }), {
      status: 405, headers
    });
  },
};
