/* Service Worker — Grupo 30 Gestão de Stock
   App offline-first: a aplicação (HTML/CSS/JS) fica em cache para funcionar
   sem internet; os dados do utilizador vivem no IndexedDB.
   - Navegação/HTML: network-first (recebe atualizações quando há rede,
     usa a cópia em cache quando está offline).
   - Restantes (fontes, etc.): cache-first com cache em tempo de execução.
*/
const CACHE = 'grupo30-v2';
const CORE = ['grupo30_gestao_stock.html', 'index.html', 'manifest.json',
  'icon-192.png', 'icon-512.png', 'icon-maskable-512.png'];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE)
      .then((c) => Promise.allSettled(CORE.map((u) => c.add(u))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  let url;
  try { url = new URL(req.url); } catch (_) { return; }

  const isHTML = req.mode === 'navigate' ||
    (url.origin === location.origin && url.pathname.endsWith('.html'));

  if (isHTML) {
    // network-first, cai para a cache quando offline
    e.respondWith(
      fetch(req)
        .then((r) => {
          const copy = r.clone();
          caches.open(CACHE).then((c) => c.put(req, copy)).catch(() => {});
          return r;
        })
        .catch(() => caches.match(req).then((m) => m || caches.match('grupo30_gestao_stock.html')))
    );
    return;
  }

  // outros recursos: cache-first
  e.respondWith(
    caches.match(req).then((m) => m || fetch(req).then((r) => {
      const copy = r.clone();
      caches.open(CACHE).then((c) => c.put(req, copy)).catch(() => {});
      return r;
    }).catch(() => m))
  );
});
