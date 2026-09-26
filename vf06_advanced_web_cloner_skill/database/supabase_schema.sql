-- ========================================================
-- MA JI YOUNG EDITION & ATELIER
-- Supabase PostgreSQL Schema Definition (v1.0)
-- ========================================================

-- 1. EXTENSIONS
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 2. TABLE: site_settings (전역 설정 & 브랜드 메타)
CREATE TABLE IF NOT EXISTS site_settings (
    id VARCHAR(50) PRIMARY KEY DEFAULT 'default',
    brand_name_kr VARCHAR(100) NOT NULL DEFAULT '마지영 에디션',
    brand_name_en VARCHAR(100) NOT NULL DEFAULT 'MA JI YOUNG EDITION',
    sub_title VARCHAR(200) DEFAULT 'Atelier & Contemporary Art Archive',
    description TEXT,
    contact_email VARCHAR(100) DEFAULT 'contact@majiyoung-edition.art',
    contact_phone VARCHAR(50) DEFAULT '063-228-8422',
    address_kr TEXT DEFAULT '전북특별자치도 전주시 완산구 유연로 87 청목빌딩',
    banner_active BOOLEAN DEFAULT TRUE,
    banner_text_kr TEXT DEFAULT '마지영 개인전 《Moments》 청목미술관 2026.10.13 - 10.18 개최',
    banner_text_en TEXT DEFAULT 'MA JI YOUNG Solo Exhibition 《Moments》 at Cheongmok Museum of Art',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. TABLE: artist_profiles (작가 프로필 & 작가노트)
CREATE TABLE IF NOT EXISTS artist_profiles (
    id VARCHAR(50) PRIMARY KEY DEFAULT 'ma-ji-young',
    name_kr VARCHAR(50) NOT NULL DEFAULT '마지영',
    name_en VARCHAR(50) NOT NULL DEFAULT 'MA JI YOUNG',
    photo_url TEXT DEFAULT 'assets/images/artist_ma_ji_young.png',
    studio_photo_url TEXT DEFAULT 'assets/images/artist_ma_ji_young_studio.png',
    category VARCHAR(100) DEFAULT 'Contemporary / Relief Monochrome',
    statement_title_kr TEXT,
    statement_title_en TEXT,
    statement_kr JSONB DEFAULT '[]'::jsonb, -- 문단 배열
    statement_en JSONB DEFAULT '[]'::jsonb,
    connect_links JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. TABLE: exhibitions (전시 정보)
CREATE TABLE IF NOT EXISTS exhibitions (
    id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    venue VARCHAR(255) NOT NULL,
    venue_url TEXT,
    period_date VARCHAR(100) NOT NULL,
    image_url TEXT,
    badge VARCHAR(50) DEFAULT 'EXHIBITION',
    description TEXT,
    display_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. TABLE: artworks (42점 전 작품 및 신규 작품)
CREATE TABLE IF NOT EXISTS artworks (
    id VARCHAR(50) PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    title_kr VARCHAR(255) NOT NULL,
    title_en VARCHAR(255),
    series VARCHAR(100) NOT NULL DEFAULT 'Solo Works',
    medium VARCHAR(150) DEFAULT 'Mixed media on canvas & wood relief',
    year INT DEFAULT 2026,
    size_spec VARCHAR(100),
    dimensions JSONB DEFAULT '{}'::jsonb, -- { "w": 67.5, "h": 40.0, "unit": "cm" }
    price NUMERIC(12, 0) DEFAULT 0,
    status VARCHAR(50) DEFAULT 'available', -- 'available' (소장가능), 'reserved' (예약중), 'sold' (소장완료), 'private' (비공개)
    description_kr TEXT,
    description_en TEXT,
    image_url TEXT NOT NULL,
    tags TEXT[] DEFAULT ARRAY[]::TEXT[],
    is_featured BOOLEAN DEFAULT FALSE,
    display_order INT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. TABLE: inquiries (고객 소장 문의 및 프라이빗 뷰잉 신청)
CREATE TABLE IF NOT EXISTS inquiries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    artwork_id VARCHAR(50) REFERENCES artworks(id) ON DELETE SET NULL,
    artwork_code VARCHAR(50),
    artwork_title VARCHAR(255),
    client_name VARCHAR(100) NOT NULL,
    client_email VARCHAR(100) NOT NULL,
    client_phone VARCHAR(50),
    message TEXT NOT NULL,
    preferred_date DATE,
    status VARCHAR(50) DEFAULT 'pending', -- 'pending' (접수), 'reviewing' (검토중), 'contacted' (연락완료), 'closed' (완료)
    admin_notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 7. INDEXES FOR PERFORMANCE
CREATE INDEX IF NOT EXISTS idx_artworks_series ON artworks(series);
CREATE INDEX IF NOT EXISTS idx_artworks_order ON artworks(display_order);
CREATE INDEX IF NOT EXISTS idx_artworks_status ON artworks(status);
CREATE INDEX IF NOT EXISTS idx_exhibitions_order ON exhibitions(display_order);
CREATE INDEX IF NOT EXISTS idx_inquiries_created ON inquiries(created_at DESC);

-- 8. ROW LEVEL SECURITY (RLS) POLICIES
ALTER TABLE site_settings ENABLE ROW LEVEL SECURITY;
ALTER TABLE artist_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE exhibitions ENABLE ROW LEVEL SECURITY;
ALTER TABLE artworks ENABLE ROW LEVEL SECURITY;
ALTER TABLE inquiries ENABLE ROW LEVEL SECURITY;

-- Anonymous (Public) Read Access
CREATE POLICY "Allow public read access on site_settings" ON site_settings FOR SELECT USING (true);
CREATE POLICY "Allow public read access on artist_profiles" ON artist_profiles FOR SELECT USING (true);
CREATE POLICY "Allow public read access on exhibitions" ON exhibitions FOR SELECT USING (is_active = true);
CREATE POLICY "Allow public read access on artworks" ON artworks FOR SELECT USING (status != 'private');

-- Anonymous (Public) Inquiry Submission
CREATE POLICY "Allow public to submit inquiries" ON inquiries FOR INSERT WITH CHECK (true);

-- Authenticated Admin Full Access (Insert/Update/Delete)
CREATE POLICY "Allow authenticated admin full access on site_settings" ON site_settings FOR ALL TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "Allow authenticated admin full access on artist_profiles" ON artist_profiles FOR ALL TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "Allow authenticated admin full access on exhibitions" ON exhibitions FOR ALL TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "Allow authenticated admin full access on artworks" ON artworks FOR ALL TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "Allow authenticated admin full access on inquiries" ON inquiries FOR ALL TO authenticated USING (true) WITH CHECK (true);
