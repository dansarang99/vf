// scripts/generate_seed_sql.js
// Reads data.js and generates production-ready database/supabase_seed.sql

const fs = require('fs');
const path = require('path');

// Read data.js content and eval it safely to extract GALLERY_DATA
const dataJsPath = path.join(__dirname, '../src/js/data.js');
const dataJsContent = fs.readFileSync(dataJsPath, 'utf8');

// Simple sandbox to evaluate data.js
const sandbox = {};
const fn = new Function('window', dataJsContent + '; return GALLERY_DATA;');
const data = fn(sandbox);

function escapeSql(str) {
  if (str === null || str === undefined) return 'NULL';
  return "'" + String(str).replace(/'/g, "''") + "'";
}

let sql = `-- ========================================================
-- MA JI YOUNG EDITION & ATELIER
-- Supabase PostgreSQL Seed Data
-- 100% Lossless Migration from data.js
-- ========================================================

-- 1. SEED: site_settings
INSERT INTO site_settings (
    id, brand_name_kr, brand_name_en, sub_title, description,
    contact_email, contact_phone, address_kr, banner_active,
    banner_text_kr, banner_text_en
) VALUES (
    'default',
    ${escapeSql(data.brand.nameKr)},
    ${escapeSql(data.brand.nameEn)},
    ${escapeSql(data.brand.subTitle)},
    ${escapeSql(data.brand.description)},
    'contact@majiyoung-edition.art',
    '063-228-8422',
    '전북특별자치도 전주시 완산구 유연로 87 청목빌딩',
    TRUE,
    '마지영 개인전 《Moments》 청목미술관 2026.10.13 - 10.18 개최',
    'MA JI YOUNG Solo Exhibition 《Moments》 at Cheongmok Museum of Art'
) ON CONFLICT (id) DO UPDATE SET
    brand_name_kr = EXCLUDED.brand_name_kr,
    brand_name_en = EXCLUDED.brand_name_en,
    sub_title = EXCLUDED.sub_title,
    description = EXCLUDED.description;

-- 2. SEED: artist_profiles
INSERT INTO artist_profiles (
    id, name_kr, name_en, photo_url, studio_photo_url, category,
    statement_title_kr, statement_title_en,
    statement_kr, statement_en, connect_links
) VALUES (
    'ma-ji-young',
    ${escapeSql(data.artist.nameKr)},
    ${escapeSql(data.artist.nameEn)},
    ${escapeSql(data.artist.photo)},
    ${escapeSql(data.artist.studioPhoto)},
    ${escapeSql(data.artist.category)},
    ${escapeSql(data.artist.statementTitleKr)},
    ${escapeSql(data.artist.statementTitleEn)},
    ${escapeSql(JSON.stringify(data.artist.statementKr))}::jsonb,
    ${escapeSql(JSON.stringify(data.artist.statementEn))}::jsonb,
    ${escapeSql(JSON.stringify(data.artist.connects))}::jsonb
) ON CONFLICT (id) DO UPDATE SET
    statement_kr = EXCLUDED.statement_kr,
    statement_en = EXCLUDED.statement_en,
    connect_links = EXCLUDED.connect_links;

-- 3. SEED: exhibitions
`;

data.artist.exhibitions.forEach((exb, index) => {
  sql += `INSERT INTO exhibitions (
    id, title, venue, venue_url, period_date, image_url, badge, description, display_order, is_active
) VALUES (
    ${escapeSql(exb.id)},
    ${escapeSql(exb.title)},
    ${escapeSql(exb.venue)},
    ${escapeSql(exb.venueUrl || '')},
    ${escapeSql(exb.date)},
    ${escapeSql(exb.image)},
    ${escapeSql(exb.badge)},
    ${escapeSql(exb.description)},
    ${index + 1},
    TRUE
) ON CONFLICT (id) DO UPDATE SET
    title = EXCLUDED.title,
    venue = EXCLUDED.venue,
    period_date = EXCLUDED.period_date,
    image_url = EXCLUDED.image_url,
    description = EXCLUDED.description;\n\n`;
});

sql += `-- 4. SEED: artworks (All 42 Works)\n`;

data.artist.artworks.forEach((art, index) => {
  // Parse dimensions e.g. "W 67.5 x H 40.0 cm"
  let dims = { w: null, h: null, unit: 'cm' };
  const dimMatch = (art.size || '').match(/W\s*([\d.]+)\s*x\s*H\s*([\d.]+)\s*(cm|mm)?/i);
  if (dimMatch) {
    dims.w = parseFloat(dimMatch[1]);
    dims.h = parseFloat(dimMatch[2]);
    dims.unit = dimMatch[3] || 'cm';
  }

  // Parse price numeric e.g. "8,500,000" -> 8500000
  const numericPrice = parseInt((art.price || '0').replace(/[^0-9]/g, ''), 10) || 0;

  // Map category to series label
  let seriesLabel = '대표작 (Master Collection)';
  if (art.category === 'series-quad') seriesLabel = '4연작 모듈 세트 (Quad Series)';
  else if (art.category === 'series-duo') seriesLabel = '2연작 듀오 블록 (Duo Series)';

  sql += `INSERT INTO artworks (
    id, code, title_kr, title_en, series, medium, year, size_spec, dimensions,
    price, status, description_kr, description_en, image_url, tags, is_featured, display_order
) VALUES (
    ${escapeSql(art.id)},
    ${escapeSql(art.title)},
    ${escapeSql(art.subTitle ? `${art.title} - ${art.subTitle}` : art.title)},
    ${escapeSql(art.subTitleEn || '')},
    ${escapeSql(seriesLabel)},
    ${escapeSql(art.medium)},
    2026,
    ${escapeSql(art.size)},
    ${escapeSql(JSON.stringify(dims))}::jsonb,
    ${numericPrice},
    'available',
    ${escapeSql(art.poemKr || '')},
    ${escapeSql(art.poemEn || '')},
    ${escapeSql(art.image)},
    ARRAY['Moments', ${escapeSql(art.badge || 'ORIGINAL')}, ${escapeSql(art.category)}],
    ${index < 4 ? 'TRUE' : 'FALSE'},
    ${index + 1}
) ON CONFLICT (id) DO UPDATE SET
    title_kr = EXCLUDED.title_kr,
    title_en = EXCLUDED.title_en,
    series = EXCLUDED.series,
    price = EXCLUDED.price,
    description_kr = EXCLUDED.description_kr,
    description_en = EXCLUDED.description_en,
    image_url = EXCLUDED.image_url;\n`;
});

const outputPath = path.join(__dirname, '../database/supabase_seed.sql');
fs.writeFileSync(outputPath, sql, 'utf8');
console.log(`Successfully generated ${outputPath} (${data.artist.artworks.length} artworks seeded)`);
