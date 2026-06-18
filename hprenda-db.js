/**
 * hprenda-db.js  — Camada de persistência: Firebase Realtime DB + IndexedDB
 * Hospital do Prenda — Consulta Externa
 *
 * Expõe:
 *   window._fb        { ref, set, get, onValue, db }
 *   window._fbReady   boolean
 *   window._idb       { idbGet, idbSet, idbDel, idbKeys }
 *   window.configureFirebase(config)   → inicialização em runtime
 *
 * Emite o evento personalizado "firebaseReady" em window quando o Firebase
 * estiver conectado.
 *
 * Se não houver config do Firebase, o sistema funciona em modo offline
 * com o mock já presente no HTML + IndexedDB local.
 */

(function (global) {
  'use strict';

  var LOG = '[hprenda-db]';

  /* ─────────────────────────────────────────────────────────────
     0.  Garantir mock padrão (o HTML já tem um fallback, mas
         este ficheiro é carregado antes do inline-script do HTML)
  ───────────────────────────────────────────────────────────── */
  if (!global._fbReady) global._fbReady = false;
  if (!global._fb) {
    global._fb = {
      db: null,
      ref: function () { return {}; },
      set: function () { return Promise.resolve(); },
      get: function () {
        return Promise.resolve({
          exists: function () { return false; },
          val: function () { return null; }
        });
      },
      onValue: function () { return function () {}; }
    };
  }

  /* ─────────────────────────────────────────────────────────────
     1.  IndexedDB  —  sempre disponível, independente do Firebase
  ───────────────────────────────────────────────────────────── */
  var IDB_NAME    = 'prenda-hospital';
  var IDB_STORE   = 'records';
  var IDB_VERSION = 1;
  var _idbInstance = null;

  function _openIDB() {
    if (_idbInstance) return Promise.resolve(_idbInstance);
    return new Promise(function (resolve, reject) {
      if (!global.indexedDB) {
        console.warn(LOG, 'IndexedDB não suportado neste ambiente.');
        return reject(new Error('IndexedDB não disponível'));
      }
      var req = global.indexedDB.open(IDB_NAME, IDB_VERSION);
      req.onupgradeneeded = function (e) {
        var db = e.target.result;
        if (!db.objectStoreNames.contains(IDB_STORE)) {
          db.createObjectStore(IDB_STORE);
          console.log(LOG, 'Object store "' + IDB_STORE + '" criada.');
        }
      };
      req.onsuccess = function (e) {
        _idbInstance = e.target.result;
        console.log(LOG, 'IndexedDB pronta:', IDB_NAME);
        resolve(_idbInstance);
      };
      req.onerror = function (e) {
        console.error(LOG, 'Erro ao abrir IndexedDB:', e.target.error);
        reject(e.target.error);
      };
    });
  }

  function _idbTx(mode, fn) {
    return _openIDB().then(function (db) {
      return new Promise(function (resolve, reject) {
        var tx    = db.transaction(IDB_STORE, mode);
        var store = tx.objectStore(IDB_STORE);
        var req   = fn(store);
        tx.oncomplete = function () { resolve(req ? req.result : undefined); };
        tx.onerror    = function (e) { reject(e.target.error); };
        tx.onabort    = function (e) { reject(e.target.error || new Error('IDB tx aborted')); };
      });
    });
  }

  var _idb = {
    /** Lê um valor pelo key */
    idbGet: function (key) {
      return _idbTx('readonly', function (store) { return store.get(key); });
    },
    /** Grava (upsert) um valor */
    idbSet: function (key, value) {
      return _idbTx('readwrite', function (store) { return store.put(value, key); });
    },
    /** Remove uma entrada */
    idbDel: function (key) {
      return _idbTx('readwrite', function (store) { return store.delete(key); });
    },
    /** Devolve lista de todas as chaves */
    idbKeys: function () {
      return _openIDB().then(function (db) {
        return new Promise(function (resolve, reject) {
          var tx    = db.transaction(IDB_STORE, 'readonly');
          var store = tx.objectStore(IDB_STORE);
          var req   = store.getAllKeys();
          req.onsuccess = function () { resolve(req.result); };
          req.onerror   = function (e) { reject(e.target.error); };
        });
      });
    }
  };

  global._idb = _idb;

  // Iniciar IndexedDB de imediato (em background, sem bloquear)
  _openIDB().catch(function (err) {
    console.warn(LOG, 'IndexedDB indisponível — dados locais desactivados.', err);
  });

  /* ─────────────────────────────────────────────────────────────
     2.  Carregamento dinâmico do Firebase SDK (CDN)
  ───────────────────────────────────────────────────────────── */
  var FB_CDN_BASE = 'https://www.gstatic.com/firebasejs/10.12.2/';

  function _loadScript(src) {
    return new Promise(function (resolve, reject) {
      var s    = document.createElement('script');
      s.type   = 'module'; // SDK v10 é ESM; ver _initFirebaseModular
      s.src    = src;
      s.onload  = function () { resolve(); };
      s.onerror = function () { reject(new Error('Falha ao carregar: ' + src)); };
      document.head.appendChild(s);
    });
  }

  /* Carrega o Firebase usando import() dinâmico (ESM modular v10) */
  function _initFirebaseModular(config) {
    console.log(LOG, 'A carregar Firebase SDK modular (v10)…');

    return Promise.all([
      import(FB_CDN_BASE + 'firebase-app.js'),
      import(FB_CDN_BASE + 'firebase-database.js')
    ]).then(function (mods) {
      var appMod = mods[0];
      var dbMod  = mods[1];

      var initializeApp   = appMod.initializeApp;
      var getDatabase     = dbMod.getDatabase;
      var fbRef           = dbMod.ref;
      var fbSet           = dbMod.set;
      var fbGet           = dbMod.get;
      var fbOnValue       = dbMod.onValue;

      var app = initializeApp(config, 'hprenda-' + Date.now());
      var db  = getDatabase(app);

      global._fb = {
        db      : db,
        ref     : function (database, path) { return fbRef(database || db, path); },
        set     : fbSet,
        get     : fbGet,
        onValue : fbOnValue
      };

      global._fbReady = true;
      console.log(LOG, 'Firebase conectado com sucesso. Projecto:', config.projectId);
      global.dispatchEvent(new CustomEvent('firebaseReady', { detail: { db: db } }));
    });
  }

  /* ─────────────────────────────────────────────────────────────
     3.  Ler config: window.FIREBASE_CONFIG  ou  localStorage
  ───────────────────────────────────────────────────────────── */
  function _resolveConfig() {
    // Prioridade 1: variável global
    if (global.FIREBASE_CONFIG && global.FIREBASE_CONFIG.projectId) {
      return global.FIREBASE_CONFIG;
    }
    // Prioridade 2: localStorage
    try {
      var raw = localStorage.getItem('prenda_fb_config');
      if (raw) {
        var cfg = JSON.parse(raw);
        if (cfg && cfg.projectId) return cfg;
      }
    } catch (e) {
      console.warn(LOG, 'Erro ao ler localStorage:', e);
    }
    return null;
  }

  /* ─────────────────────────────────────────────────────────────
     4.  Inicialização principal
  ───────────────────────────────────────────────────────────── */
  function _boot() {
    var config = _resolveConfig();
    if (!config) {
      console.info(
        LOG,
        'Nenhuma config Firebase encontrada.',
        'Modo offline activo (IndexedDB disponível).',
        'Use window.configureFirebase(config) para activar sincronização.'
      );
      return;
    }
    _initFirebaseModular(config).catch(function (err) {
      console.error(LOG, 'Falha ao iniciar Firebase:', err);
      console.info(LOG, 'A continuar em modo offline.');
    });
  }

  /* ─────────────────────────────────────────────────────────────
     5.  API pública: configuração em runtime
  ───────────────────────────────────────────────────────────── */
  /**
   * Configura (ou reconfigura) o Firebase em runtime.
   * @param {object} config  — objecto de configuração Firebase
   * @param {boolean} [persist=true] — guardar em localStorage para sessões futuras
   */
  global.configureFirebase = function (config, persist) {
    if (!config || !config.projectId || !config.databaseURL) {
      console.error(LOG, 'configureFirebase: config inválida. Necessário projectId e databaseURL.');
      return;
    }
    if (persist !== false) {
      try {
        localStorage.setItem('prenda_fb_config', JSON.stringify(config));
        console.log(LOG, 'Config guardada em localStorage (chave: prenda_fb_config).');
      } catch (e) {
        console.warn(LOG, 'Não foi possível guardar config em localStorage:', e);
      }
    }
    _initFirebaseModular(config).catch(function (err) {
      console.error(LOG, 'configureFirebase: Falha ao conectar:', err);
    });
  };

  /* ─────────────────────────────────────────────────────────────
     6.  Arranque
  ───────────────────────────────────────────────────────────── */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', _boot);
  } else {
    // DOM já pronto (script carregado a meio ou fim do parse)
    _boot();
  }

  console.log(LOG, 'hprenda-db.js carregado. IndexedDB + Firebase prontos para inicializar.');

}(window));
