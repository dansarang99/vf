// scripts/migrate_supabase.js
// Automatic database seeder for Supabase Cloud using @supabase/supabase-js

require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
const path = require('path');

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseKey) {
  console.log('⚠️ [Notice] SUPABASE_URL or SUPABASE_KEY is missing in .env file.');
  console.log('💡 You can still run the website and admin mode with our Built-in Hybrid Local Engine (localStorage).');
  console.log('👉 To connect to Supabase Cloud, add your credentials to .env and re-run: node scripts/migrate_supabase.js');
  process.exit(0);
}

const supabase = createClient(supabaseUrl, supabaseKey);

// Read data.js
const dataJsPath = path.join(__dirname, '../src/js/data.js');
const dataJsContent = fs.readFileSync(dataJsPath, 'utf8');
const fn = new Function('window', dataJsContent + '; return GALLERY_DATA;');
const data = fn({});

async function runMigration() {
  console.log(`🚀 Starting Migration to Supabase (${supabaseUrl})...`);

  // 1. Migrate Site Settings
  try {
    const { error: errSettings } = await supabase.from('site_settings').upsert({
      id: 'default',
      brand_name_kr: data.brand.nameKr,
      brand_name_en: data.brand.nameEn,
      sub_title: data.brand.subTitle,
      description: data.brand.description,
      contact_email: 'contact@majiyoung-edition.art',
      contact_phone: '063-228-8422',
      address_kr: '전북특별자치도 전주시 완산구 유연로 87 청목빌딩',
      banner_active: true,
      banner_text_kr: '마지영 개인전 《Moments》 청목미술관 2026.10.13 - 10.18 개최',
      banner_text_en: 'MA JI YOUNG Solo Exhibition 《Moments》 at Cheongmok Museum of Art'
    });
    if (errSettings) console.warn('⚠️ site_settings error:', errSettings.message);
    else console.log('✅ Site settings synced successfully.');
  } catch (e) {
    console.warn('⚠️ site_settings skipped:', e.message);
  }

  // 2. Migrate Artist Profile
  try {
    const { error: errArtist } = await supabase.from('artist_profiles').upsert({
      id: 'ma-ji-young',
      name_kr: data.artist.nameKr,
      name_en: data.artist.nameEn,
      photo_url: data.artist.photo,
      studio_photo_url: data.artist.studioPhoto,
      category: data.artist.category,
      statement_title_kr: data.artist.statementTitleKr,
      statement_title_en: data.artist.statementTitleEn,
      statement_kr: data.artist.statementKr,
      statement_en: data.artist.statementEn,
      connect_links: data.artist.connects
    });
    if (errArtist) console.warn('⚠️ artist_profiles error:', errArtist.message);
    else console.log('✅ Artist profile synced successfully.');
  } catch (e) {
    console.warn('⚠️ artist_profiles skipped:', e.message);
  }

  // 3. Migrate Exhibitions
  try {
    const exbPayload = data.artist.exhibitions.map((exb, idx) => ({
      id: exb.id,
      title: exb.title,
      venue: exb.venue,
      venue_url: exb.venueUrl || '',
      period_date: exb.date,
      image_url: exb.image,
      badge: exb.badge,
      description: exb.description,
      display_order: idx + 1,
      is_active: true
    }));
    const { error: errExb } = await supabase.from('exhibitions').upsert(exbPayload);
    if (errExb) console.warn('⚠️ exhibitions error:', errExb.message);
    else console.log(`✅ ${exbPayload.length} exhibitions synced successfully.`);
  } catch (e) {
    console.warn('⚠️ exhibitions skipped:', e.message);
  }

  // 4. Migrate Artworks
  try {
    const artPayload = data.artist.artworks.map((art, idx) => {
      let dims = { w: null, h: null, unit: 'cm' };
      const dimMatch = (art.size || '').match(/W\s*([\d.]+)\s*x\s*H\s*([\d.]+)\s*(cm|mm)?/i);
      if (dimMatch) {
        dims.w = parseFloat(dimMatch[1]);
        dims.h = parseFloat(dimMatch[2]);
        dims.unit = dimMatch[3] || 'cm';
      }
      const numericPrice = parseInt((art.price || '0').replace(/[^0-9]/g, ''), 10) || 0;
      let seriesLabel = '대표작 (Master Collection)';
      if (art.category === 'series-quad') seriesLabel = '4연작 모듈 세트 (Quad Series)';
      else if (art.category === 'series-duo') seriesLabel = '2연작 듀오 블록 (Duo Series)';

      return {
        id: art.id,
        code: art.title,
        title_kr: art.subTitle ? `${art.title} - ${art.subTitle}` : art.title,
        title_en: art.subTitleEn || '',
        series: seriesLabel,
        medium: art.medium,
        year: 2026,
        size_spec: art.size,
        dimensions: dims,
        price: numericPrice,
        status: 'available',
        description_kr: art.poemKr || '',
        description_en: art.poemEn || '',
        image_url: art.image,
        tags: ['Moments', art.badge || 'ORIGINAL', art.category],
        is_featured: idx < 4,
        display_order: idx + 1
      };
    });

    const { error: errArt } = await supabase.from('artworks').upsert(artPayload);
    if (errArt) console.warn('⚠️ artworks error:', errArt.message);
    else console.log(`✅ ${artPayload.length} artworks synced successfully.`);
  } catch (e) {
    console.warn('⚠️ artworks skipped:', e.message);
  }

  console.log('🎉 Migration completed!');
}

runMigration();
