// Święto Wina — Service Worker (PWA offline)
// Podbij wersję przy każdej aktualizacji, żeby wymusić odświeżenie cache.
const CACHE = 'swieto-wina-v8';
const SHELL = [
  './',
  'index.html',
  'manifest.json',
  'icon-192.png',
  'icon-512.png',
  'apple-touch-icon.png'
];

// Instalacja — wgraj „szkielet" aplikacji do cache
self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting())
  );
});

// Aktywacja — wyczyść stare cache
self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);

  // Supabase API (dane na żywo) — zawsze sieć, nigdy z cache
  if (url.hostname.endsWith('supabase.co')) return;

  // Nawigacja (otwarcie aplikacji) — najpierw sieć, w razie braku internetu z cache
  if (req.mode === 'navigate') {
    e.respondWith(
      fetch(req).then((res) => {
        const copy = res.clone();
        caches.open(CACHE).then((c) => c.put('index.html', copy));
        return res;
      }).catch(() => caches.match('index.html'))
    );
    return;
  }

  // Reszta (skrypty, ikony, CDN Supabase JS) — najpierw cache, potem sieć i dopisz do cache
  e.respondWith(
    caches.match(req).then((cached) => {
      if (cached) return cached;
      return fetch(req).then((res) => {
        if (res && res.status === 200 && (url.origin === location.origin || url.hostname.includes('jsdelivr'))) {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(req, copy));
        }
        return res;
      }).catch(() => cached);
    })
  );
});
