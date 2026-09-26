// ========================================================
// MA JI YOUNG EDITION & ATELIER
// Universal Supabase Client & Local DB Hybrid Adapter
// ========================================================

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.ArtDatabase = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {

  // Configuration (Can be injected or retrieved from localStorage)
  const STORAGE_KEY_CONFIG = 'mjy_supabase_config';
  const STORAGE_KEY_LOCAL_DB = 'mjy_local_database_v1';

  let config = {
    url: '',
    anonKey: '',
    useCloud: false
  };

  // Load stored config in browser
  if (typeof window !== 'undefined' && window.localStorage) {
    try {
      const savedConfig = localStorage.getItem(STORAGE_KEY_CONFIG);
      if (savedConfig) {
        config = Object.assign(config, JSON.parse(savedConfig));
      }
    } catch (e) {
      console.warn('Failed to load Supabase config from localStorage:', e);
    }
  }

  // Supabase Client instance
  let supabaseInstance = null;

  function initSupabase() {
    if (config.url && config.anonKey && typeof window !== 'undefined') {
      if (window.supabase && typeof window.supabase.createClient === 'function') {
        supabaseInstance = window.supabase.createClient(config.url, config.anonKey);
        config.useCloud = true;
        console.log('✅ Connected to Supabase Cloud:', config.url);
        return supabaseInstance;
      }
    }
    supabaseInstance = null;
    config.useCloud = false;
    return null;
  }

  // Local Storage DB Engine (Graceful Fallback & Offline Mode)
  function getLocalDB() {
    if (typeof window === 'undefined' || !window.localStorage) {
      return typeof GALLERY_DATA !== 'undefined' ? GALLERY_DATA : null;
    }
    try {
      const stored = localStorage.getItem(STORAGE_KEY_LOCAL_DB);
      if (stored) {
        return JSON.parse(stored);
      }
    } catch (e) {
      console.warn('Error reading local DB:', e);
    }

    // Default Seed from GALLERY_DATA
    if (typeof GALLERY_DATA !== 'undefined') {
      const initial = JSON.parse(JSON.stringify(GALLERY_DATA));
      // Add inquiries list if missing
      if (!initial.inquiries) initial.inquiries = [];
      saveLocalDB(initial);
      return initial;
    }
    return null;
  }

  function saveLocalDB(data) {
    if (typeof window !== 'undefined' && window.localStorage) {
      try {
        localStorage.setItem(STORAGE_KEY_LOCAL_DB, JSON.stringify(data));
      } catch (e) {
        console.error('Failed to save local DB:', e);
      }
    }
  }

  // Core API Service
  const ArtDatabase = {
    // Configuration Management
    getConfig() {
      return { ...config };
    },

    setConfig(newUrl, newAnonKey) {
      config.url = (newUrl || '').trim();
      config.anonKey = (newAnonKey || '').trim();
      if (typeof window !== 'undefined' && window.localStorage) {
        localStorage.setItem(STORAGE_KEY_CONFIG, JSON.stringify(config));
      }
      return initSupabase();
    },

    isCloudActive() {
      return config.useCloud && supabaseInstance !== null;
    },

    // Reset local database back to original data.js seed
    resetToDefaultSeed() {
      if (typeof GALLERY_DATA !== 'undefined') {
        const initial = JSON.parse(JSON.stringify(GALLERY_DATA));
        initial.inquiries = [];
        saveLocalDB(initial);
        return initial;
      }
      return null;
    },

    // 1. Artworks API
    async getArtworks(options = {}) {
      if (this.isCloudActive()) {
        try {
          let query = supabaseInstance.from('artworks').select('*').order('display_order', { ascending: true });
          if (options.series) {
            query = query.eq('series', options.series);
          }
          if (options.status) {
            query = query.eq('status', options.status);
          }
          const { data, error } = await query;
          if (error) throw error;
          return data;
        } catch (err) {
          console.warn('Supabase fetch failed, falling back to local DB:', err);
        }
      }

      // Local Fallback
      const db = getLocalDB();
      if (!db || !db.artist || !db.artist.artworks) return [];
      let list = db.artist.artworks;
      if (options.category) {
        list = list.filter(item => item.category === options.category);
      }
      return list;
    },

    async getArtworkById(id) {
      if (this.isCloudActive()) {
        try {
          const { data, error } = await supabaseInstance.from('artworks').select('*').eq('id', id).single();
          if (error) throw error;
          return data;
        } catch (err) {
          console.warn('Cloud getArtworkById failed:', err);
        }
      }
      const db = getLocalDB();
      return (db?.artist?.artworks || []).find(w => w.id === id) || null;
    },

    async saveArtwork(artwork) {
      if (!artwork.id) {
        artwork.id = 'MJY-' + Date.now().toString(36).toUpperCase();
      }

      if (this.isCloudActive()) {
        try {
          const { data, error } = await supabaseInstance
            .from('artworks')
            .upsert(artwork)
            .select()
            .single();
          if (error) throw error;
          return data;
        } catch (err) {
          console.error('Supabase saveArtwork failed:', err);
          throw err;
        }
      }

      // Local DB Update
      const db = getLocalDB();
      if (!db.artist) db.artist = { artworks: [] };
      if (!db.artist.artworks) db.artist.artworks = [];

      const idx = db.artist.artworks.findIndex(w => w.id === artwork.id);
      if (idx >= 0) {
        db.artist.artworks[idx] = { ...db.artist.artworks[idx], ...artwork };
      } else {
        db.artist.artworks.unshift(artwork);
      }
      saveLocalDB(db);
      return artwork;
    },

    async deleteArtwork(id) {
      if (this.isCloudActive()) {
        try {
          const { error } = await supabaseInstance.from('artworks').delete().eq('id', id);
          if (error) throw error;
          return true;
        } catch (err) {
          console.error('Supabase deleteArtwork failed:', err);
          throw err;
        }
      }

      const db = getLocalDB();
      if (db?.artist?.artworks) {
        db.artist.artworks = db.artist.artworks.filter(w => w.id !== id);
        saveLocalDB(db);
      }
      return true;
    },

    // 2. Exhibitions API
    async getExhibitions() {
      if (this.isCloudActive()) {
        try {
          const { data, error } = await supabaseInstance
            .from('exhibitions')
            .select('*')
            .order('display_order', { ascending: true });
          if (error) throw error;
          return data;
        } catch (err) {
          console.warn('Cloud getExhibitions failed:', err);
        }
      }
      const db = getLocalDB();
      return db?.artist?.exhibitions || [];
    },

    async saveExhibition(exhibition) {
      if (!exhibition.id) exhibition.id = 'exb-mjy-' + Date.now();
      if (this.isCloudActive()) {
        const { data, error } = await supabaseInstance.from('exhibitions').upsert(exhibition).select().single();
        if (error) throw error;
        return data;
      }
      const db = getLocalDB();
      if (!db.artist.exhibitions) db.artist.exhibitions = [];
      const idx = db.artist.exhibitions.findIndex(e => e.id === exhibition.id);
      if (idx >= 0) db.artist.exhibitions[idx] = { ...db.artist.exhibitions[idx], ...exhibition };
      else db.artist.exhibitions.push(exhibition);
      saveLocalDB(db);
      return exhibition;
    },

    // 3. Artist Profile & Statements API
    async getArtistProfile() {
      if (this.isCloudActive()) {
        try {
          const { data, error } = await supabaseInstance.from('artist_profiles').select('*').limit(1).single();
          if (error) throw error;
          return data;
        } catch (err) {
          console.warn('Cloud getArtistProfile failed:', err);
        }
      }
      const db = getLocalDB();
      return db?.artist || {};
    },

    async saveArtistProfile(profile) {
      if (this.isCloudActive()) {
        const { data, error } = await supabaseInstance.from('artist_profiles').upsert(profile).select().single();
        if (error) throw error;
        return data;
      }
      const db = getLocalDB();
      db.artist = { ...db.artist, ...profile };
      saveLocalDB(db);
      return db.artist;
    },

    // 4. Inquiries API
    async getInquiries() {
      if (this.isCloudActive()) {
        try {
          const { data, error } = await supabaseInstance
            .from('inquiries')
            .select('*')
            .order('created_at', { ascending: false });
          if (error) throw error;
          return data;
        } catch (err) {
          console.warn('Cloud getInquiries failed:', err);
        }
      }
      const db = getLocalDB();
      return db?.inquiries || [];
    },

    async submitInquiry(inquiry) {
      inquiry.id = 'INQ-' + Date.now();
      inquiry.created_at = new Date().toISOString();
      inquiry.status = 'pending';

      if (this.isCloudActive()) {
        try {
          const { data, error } = await supabaseInstance.from('inquiries').insert([inquiry]).select().single();
          if (error) throw error;
          return data;
        } catch (err) {
          console.warn('Supabase inquiry submit failed, saving locally:', err);
        }
      }
      const db = getLocalDB();
      if (!db.inquiries) db.inquiries = [];
      db.inquiries.unshift(inquiry);
      saveLocalDB(db);
      return inquiry;
    },

    async updateInquiryStatus(id, status, notes = '') {
      if (this.isCloudActive()) {
        const { data, error } = await supabaseInstance
          .from('inquiries')
          .update({ status, admin_notes: notes, updated_at: new Date().toISOString() })
          .eq('id', id)
          .select()
          .single();
        if (error) throw error;
        return data;
      }
      const db = getLocalDB();
      const item = (db.inquiries || []).find(i => i.id === id);
      if (item) {
        item.status = status;
        item.admin_notes = notes;
        saveLocalDB(db);
      }
      return item;
    },

    // 5. Site Settings API
    async getSettings() {
      if (this.isCloudActive()) {
        try {
          const { data, error } = await supabaseInstance.from('site_settings').select('*').limit(1).single();
          if (error) throw error;
          return data;
        } catch (err) {
          console.warn('Cloud getSettings failed:', err);
        }
      }
      const db = getLocalDB();
      return db?.brand || {};
    },

    async saveSettings(settings) {
      if (this.isCloudActive()) {
        const { data, error } = await supabaseInstance.from('site_settings').upsert(settings).select().single();
        if (error) throw error;
        return data;
      }
      const db = getLocalDB();
      db.brand = { ...db.brand, ...settings };
      saveLocalDB(db);
      return db.brand;
    }
  };

  // Auto-init on load if keys exist
  initSupabase();

  return ArtDatabase;
}));
