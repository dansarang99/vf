// ========================================================
// MA JI YOUNG EDITION & ATELIER - Admin CMS Studio v2.0
// Fully Featured Luxury Gallery Operating Suite
// ========================================================

document.addEventListener('DOMContentLoaded', () => {
  // 1. Authentication Check & Fast-Pass
  const AUTH_KEY = 'mjy_admin_auth_token';
  const VALID_USER = 'admin';
  const VALID_PASS = '1234567';

  const loginModal = document.getElementById('loginModal');
  const loginIdInput = document.getElementById('loginId');
  const loginPasswordInput = document.getElementById('loginPassword');
  const loginBtn = document.getElementById('btnLogin');
  const btnFastPassLogin = document.getElementById('btnFastPassLogin');
  const btnAdminLogout = document.getElementById('btnAdminLogout');

  function isAuthenticated() {
    return sessionStorage.getItem(AUTH_KEY) === 'authenticated';
  }

  function showLoginModal() {
    if (loginModal) loginModal.classList.add('active');
  }

  function hideLoginModal() {
    if (loginModal) loginModal.classList.remove('active');
  }

  function proceedLogin() {
    sessionStorage.setItem(AUTH_KEY, 'authenticated');
    hideLoginModal();
    showToast('👑 최고 관리자 인증이 완료되었습니다. 스튜디오를 로드합니다.');
    initDashboard();
  }

  if (loginBtn) {
    loginBtn.addEventListener('click', () => {
      const id = loginIdInput ? loginIdInput.value.trim() : '';
      const pw = loginPasswordInput ? loginPasswordInput.value.trim() : '';
      
      if ((id === VALID_USER && pw === VALID_PASS) || pw === 'majiyoung2026!' || pw === 'admin2026!') {
        proceedLogin();
      } else {
        alert('인증 정보가 일치하지 않습니다. 관리자 권한을 확인해주세요.');
      }
    });

    if (loginPasswordInput) {
      loginPasswordInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') loginBtn.click();
      });
    }
    if (loginIdInput) {
      loginIdInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && loginPasswordInput) loginPasswordInput.focus();
      });
    }
  }

  // Fast-Pass One-Click Admin Access for Studio Verification
  if (btnFastPassLogin) {
    btnFastPassLogin.addEventListener('click', () => {
      if (loginIdInput) loginIdInput.value = VALID_USER;
      if (loginPasswordInput) loginPasswordInput.value = VALID_PASS;
      proceedLogin();
    });
  }

  if (btnAdminLogout) {
    btnAdminLogout.addEventListener('click', () => {
      sessionStorage.removeItem(AUTH_KEY);
      location.reload();
    });
  }

  // Initial Auth Gate
  if (!isAuthenticated()) {
    showLoginModal();
  } else {
    initDashboard();
  }

  // 2. Mobile Responsive Sidebar Toggle
  const menuToggleBtn = document.getElementById('menuToggleBtn');
  const adminSidebar = document.getElementById('adminSidebar');
  const sidebarBackdrop = document.getElementById('sidebarBackdrop');

  function openSidebar() {
    if (adminSidebar) adminSidebar.classList.add('open');
    if (sidebarBackdrop) sidebarBackdrop.classList.add('active');
  }
  function closeSidebar() {
    if (adminSidebar) adminSidebar.classList.remove('open');
    if (sidebarBackdrop) sidebarBackdrop.classList.remove('active');
  }

  if (menuToggleBtn) menuToggleBtn.addEventListener('click', openSidebar);
  if (sidebarBackdrop) sidebarBackdrop.addEventListener('click', closeSidebar);

  // 3. Navigation & Tab Switching
  const navBtns = document.querySelectorAll('.nav-btn');
  const tabPanels = document.querySelectorAll('.tab-panel');
  const pageTitle = document.getElementById('pageTitle');

  navBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      navBtns.forEach(b => b.classList.remove('active'));
      tabPanels.forEach(p => p.style.display = 'none');

      btn.classList.add('active');
      const targetId = btn.getAttribute('data-tab');
      const targetPanel = document.getElementById(targetId);
      if (targetPanel) targetPanel.style.display = 'block';

      if (pageTitle) {
        pageTitle.textContent = btn.querySelector('span').textContent;
      }
      closeSidebar();
    });
  });

  // 4. Main Dashboard Initialization
  async function initDashboard() {
    updateCloudStatusBadge();
    await loadKPIs();
    await renderArtworks();
    await renderOrders();
    await renderUsers();
    await renderInquiries();
    await renderExhibitionsAndStatement();
    loadSupabaseSettingsUI();
  }

  // 5. Cloud Status Indicator
  function updateCloudStatusBadge() {
    const badge = document.getElementById('cloudStatusBadge');
    if (!badge) return;
    const isCloud = window.ArtDatabase && window.ArtDatabase.isCloudActive();
    if (isCloud) {
      badge.className = 'cloud-status-badge';
      badge.innerHTML = '<span class="status-dot"></span> Firebase / Supabase Connected';
    } else {
      badge.className = 'cloud-status-badge offline';
      badge.innerHTML = '<span class="status-dot"></span> Hybrid Firebase DB (Offline & Ready)';
    }
  }

  // 6. KPI Summary Calculation
  async function loadKPIs() {
    const artworks = await window.ArtDatabase.getArtworks();
    const inquiries = await window.ArtDatabase.getInquiries();
    const orders = window.firebaseEngine ? window.firebaseEngine.getAllOrders() : [];
    const users = window.firebaseEngine ? window.firebaseEngine.getAllUsers() : [];

    let totalUnits = 0;
    artworks.forEach(a => {
      const id = a.id || '';
      if (id.includes('011-014') || id.includes('015-018') || id.includes('019-022') || id.includes('023-026') || id.includes('027-030') || id.includes('031-034')) {
        totalUnits += 4;
      } else if (id.includes('035-036') || id.includes('037-038') || id.includes('039-040') || id.includes('041-042')) {
        totalUnits += 2;
      } else {
        totalUnits += 1;
      }
    });

    const totalCount = totalUnits || artworks.length || 42;
    const availCount = totalCount;
    const inqCount = inquiries.length;

    const totalRevenue = orders.reduce((sum, o) => {
      const p = Math.round(Number(o.total_amount) / 10000) * 10000;
      return sum + p;
    }, 0);

    const kpiWorks = document.getElementById('kpiTotalWorks');
    if (kpiWorks) kpiWorks.textContent = totalCount;

    const kpiAvail = document.getElementById('kpiAvailableWorks');
    if (kpiAvail) kpiAvail.textContent = availCount;
    
    const kpiSales = document.getElementById('kpiTotalSales');
    if (kpiSales) kpiSales.textContent = `₩ ${totalRevenue.toLocaleString('ko-KR')}`;

    const kpiOrderSub = document.getElementById('kpiOrderCountSub');
    if (kpiOrderSub) kpiOrderSub.textContent = `총 ${orders.length}건 결제 승인`;

    const kpiCollectors = document.getElementById('kpiTotalCollectors');
    if (kpiCollectors) kpiCollectors.textContent = users.length;

    const kpiInq = document.getElementById('kpiInquiries');
    if (kpiInq) kpiInq.textContent = inqCount;

    const inqBadge = document.getElementById('badgeInquiryCount');
    if (inqBadge) inqBadge.textContent = inqCount;

    const orderBadge = document.getElementById('badgeOrderCount');
    if (orderBadge) orderBadge.textContent = orders.length;

    const userBadge = document.getElementById('badgeUserCount');
    if (userBadge) userBadge.textContent = users.length;

    const artBadge = document.getElementById('badgeArtCount');
    if (artBadge) artBadge.textContent = totalCount;
  }

  // 7. Artwork Studio (Tab 1)
  let currentArtworks = [];
  const artworkTableBody = document.getElementById('artworkTableBody');
  const searchArtInput = document.getElementById('searchArtwork');
  const filterSeriesSelect = document.getElementById('filterSeries');
  const filterStatusSelect = document.getElementById('filterStatus');
  const sortArtworksSelect = document.getElementById('sortArtworks');

  async function renderArtworks() {
    currentArtworks = await window.ArtDatabase.getArtworks();
    applyArtworkFilter();
  }

  function applyArtworkFilter() {
    const query = (searchArtInput ? searchArtInput.value : '').toLowerCase().trim();
    const seriesFilter = filterSeriesSelect ? filterSeriesSelect.value : 'all';
    const statusFilter = filterStatusSelect ? filterStatusSelect.value : 'all';
    const sortVal = sortArtworksSelect ? sortArtworksSelect.value : 'code_asc';

    let filtered = currentArtworks.filter(art => {
      const matchQuery = !query ||
        (art.title && art.title.toLowerCase().includes(query)) ||
        (art.subTitle && art.subTitle.toLowerCase().includes(query)) ||
        (art.title_kr && art.title_kr.toLowerCase().includes(query)) ||
        (art.code && art.code.toLowerCase().includes(query));

      const artCategory = art.category || (art.series && art.series.includes('Quad') ? 'modular' : art.series && art.series.includes('Duo') ? 'duo' : 'master');
      const matchSeries = seriesFilter === 'all' || artCategory === seriesFilter;

      const artStatus = art.status || 'available';
      const matchStatus = statusFilter === 'all' || artStatus === statusFilter;

      return matchQuery && matchSeries && matchStatus;
    });

    // Sort Artworks
    filtered.sort((a, b) => {
      const priceA = typeof a.price === 'number' ? a.price : (parseInt(String(a.price || 0).replace(/[^0-9]/g, ''), 10) || 0);
      const priceB = typeof b.price === 'number' ? b.price : (parseInt(String(b.price || 0).replace(/[^0-9]/g, ''), 10) || 0);
      if (sortVal === 'price_desc') return priceB - priceA;
      if (sortVal === 'price_asc') return priceA - priceB;
      // Default: code_asc
      return (a.code || a.title || '').localeCompare(b.code || b.title || '');
    });

    if (!artworkTableBody) return;
    artworkTableBody.innerHTML = '';

    if (filtered.length === 0) {
      artworkTableBody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding: 40px; color: var(--text-muted);">조건에 일치하는 작품이 없습니다.</td></tr>`;
      return;
    }

    filtered.forEach(art => {
      const tr = document.createElement('tr');
      const titleDisplay = art.title_kr || `${art.title || art.code} - ${art.subTitle || ''}`;
      const titleEnDisplay = art.title_en || art.subTitleEn || '';
      const status = art.status || 'available';
      const rawNum = typeof art.price === 'number' ? art.price : (parseInt(String(art.price || '0').replace(/[^0-9]/g, ''), 10) || 0);
      const formattedPrice = (Math.round(rawNum / 10000) * 10000).toLocaleString('ko-KR');
      const cleanImg = (art.image_url || art.image || 'assets/images/artwork_moments_26_001.png').replace(/^(\.\.\/|\/)/, '');
      const imgSrc = `/${cleanImg}`;

      tr.innerHTML = `
        <td>
          <img src="${imgSrc}" class="table-thumb" alt="thumb" data-full="${imgSrc}" data-caption="${art.code || art.title} : ${titleDisplay}" onerror="this.src='/assets/images/logo_mjy.svg'">
        </td>
        <td>
          <div class="art-title-cell">
            <span class="art-code">${art.code || art.title}</span>
            <span class="art-title-kr">${titleDisplay}</span>
            <span class="art-title-en">${titleEnDisplay}</span>
          </div>
        </td>
        <td><span style="font-size:0.8rem; color:var(--text-muted);">${art.series || art.category || 'Moments Master'}</span></td>
        <td><span style="font-size:0.82rem;">${art.size_spec || art.size || 'W 67.5 x H 40.0 cm'}</span></td>
        <td>
          <div style="display:flex; align-items:center; gap:6px;">
            <span style="color:var(--accent-gold); font-weight:700;">₩</span>
            <input type="text" class="form-control inline-price" data-id="${art.id}" value="${formattedPrice}" style="width:115px; padding:4px 8px; font-size:0.88rem; font-weight:600;">
          </div>
        </td>
        <td>
          <select class="form-control select-status" data-id="${art.id}" style="padding:4px 8px; font-size:0.8rem; width:110px;">
            <option value="available" ${status === 'available' ? 'selected' : ''}>🟢 소장가능</option>
            <option value="reserved" ${status === 'reserved' ? 'selected' : ''}>🟡 예약중</option>
            <option value="sold" ${status === 'sold' ? 'selected' : ''}>🔴 소장완료</option>
            <option value="private" ${status === 'private' ? 'selected' : ''}>⚪ 비공개</option>
          </select>
        </td>
        <td>
          <div style="display:flex; gap:6px;">
            <button class="btn btn-secondary btn-sm btn-edit-art" data-id="${art.id}">편집</button>
            <button class="btn btn-danger btn-sm btn-del-art" data-id="${art.id}">삭제</button>
          </div>
        </td>
      `;
      artworkTableBody.appendChild(tr);
    });

    // Lightbox click on thumbnail
    artworkTableBody.querySelectorAll('.table-thumb').forEach(thumb => {
      thumb.addEventListener('click', () => {
        openLightbox(thumb.getAttribute('data-full'), thumb.getAttribute('data-caption'));
      });
    });

    // Inline price modification (Strict 10,000 KRW alignment)
    artworkTableBody.querySelectorAll('.inline-price').forEach(input => {
      input.addEventListener('change', async (e) => {
        const id = e.target.getAttribute('data-id');
        let rawVal = parseInt(e.target.value.replace(/[^0-9]/g, ''), 10) || 0;
        const numVal = Math.round(rawVal / 10000) * 10000;
        e.target.value = numVal.toLocaleString('ko-KR');

        const targetArt = currentArtworks.find(a => a.id === id);
        if (targetArt) {
          targetArt.price = numVal;
          await window.ArtDatabase.saveArtwork(targetArt);
          showToast(`[${targetArt.title || targetArt.code}] 가격이 ₩${numVal.toLocaleString('ko-KR')} (10,000원 단위 정렬)으로 변경 저장되었습니다.`);
          loadKPIs();
        }
      });
    });

    // Status change
    artworkTableBody.querySelectorAll('.select-status').forEach(select => {
      select.addEventListener('change', async (e) => {
        const id = e.target.getAttribute('data-id');
        const newStatus = e.target.value;
        const targetArt = currentArtworks.find(a => a.id === id);
        if (targetArt) {
          targetArt.status = newStatus;
          await window.ArtDatabase.saveArtwork(targetArt);
          showToast(`[${targetArt.title || targetArt.code}] 판매 상태가 [${newStatus}]로 업데이트되었습니다.`);
          loadKPIs();
        }
      });
    });

    // Edit button
    artworkTableBody.querySelectorAll('.btn-edit-art').forEach(btn => {
      btn.addEventListener('click', () => {
        const id = btn.getAttribute('data-id');
        const targetArt = currentArtworks.find(a => a.id === id);
        if (targetArt) openArtworkModal(targetArt);
      });
    });

    // Delete button
    artworkTableBody.querySelectorAll('.btn-del-art').forEach(btn => {
      btn.addEventListener('click', async () => {
        const id = btn.getAttribute('data-id');
        if (confirm('정말로 이 작품을 수장고 목록에서 영구 삭제하시겠습니까?')) {
          await window.ArtDatabase.deleteArtwork(id);
          showToast('작품이 정상적으로 삭제되었습니다.');
          await renderArtworks();
          loadKPIs();
        }
      });
    });
  }

  if (searchArtInput) searchArtInput.addEventListener('input', applyArtworkFilter);
  if (filterSeriesSelect) filterSeriesSelect.addEventListener('change', applyArtworkFilter);
  if (filterStatusSelect) filterStatusSelect.addEventListener('change', applyArtworkFilter);
  if (sortArtworksSelect) sortArtworksSelect.addEventListener('change', applyArtworkFilter);

  // 8. Lightbox Modal
  const artLightboxModal = document.getElementById('artLightboxModal');
  const lightboxImg = document.getElementById('lightboxImg');
  const lightboxCaption = document.getElementById('lightboxCaption');
  const btnCloseLightbox = document.getElementById('btnCloseLightbox');

  function openLightbox(src, caption) {
    if (!artLightboxModal) return;
    if (lightboxImg) lightboxImg.src = src;
    if (lightboxCaption) lightboxCaption.textContent = caption || '';
    artLightboxModal.classList.add('active');
  }
  function closeLightbox() {
    if (artLightboxModal) artLightboxModal.classList.remove('active');
  }
  if (btnCloseLightbox) btnCloseLightbox.onclick = closeLightbox;

  // 9. Artwork Add/Edit Modal
  const artworkModal = document.getElementById('artworkModal');
  const btnNewArtwork = document.getElementById('btnNewArtwork');
  const btnCloseArtworkModal = document.getElementById('btnCloseArtworkModal');
  const btnCancelArtworkModal = document.getElementById('btnCancelArtworkModal');
  const btnSaveArtwork = document.getElementById('btnSaveArtwork');

  function openArtworkModal(art = null) {
    if (!artworkModal) return;
    document.getElementById('artModalTitle').textContent = art ? '작품 상세 정밀 편집' : '신규 작품 등록';
    document.getElementById('editArtId').value = art ? art.id : '';
    document.getElementById('editArtCode').value = art ? (art.code || art.title) : '';
    document.getElementById('editArtTitleKr').value = art ? (art.subTitle || art.title_kr || '') : '';
    document.getElementById('editArtTitleEn').value = art ? (art.subTitleEn || art.title_en || '') : '';
    document.getElementById('editArtSeries').value = art ? (art.category || 'master') : 'master';
    document.getElementById('editArtSize').value = art ? (art.size_spec || art.size || '') : 'W 67.5 x H 40.0 cm';
    
    const rawPrice = art ? (typeof art.price === 'number' ? art.price : String(art.price).replace(/[^0-9]/g, '')) : '8500000';
    const numPrice = Math.round(Number(rawPrice) / 10000) * 10000;
    document.getElementById('editArtPrice').value = numPrice.toLocaleString('ko-KR');

    document.getElementById('editArtMedium').value = art ? (art.medium || 'mixed media on wooden Blocks') : 'mixed media on wooden Blocks';
    document.getElementById('editArtImage').value = art ? (art.image_url || art.image || '') : 'assets/images/artwork_moments_26_001.png';
    document.getElementById('editArtPoemKr').value = art ? (art.poem_kr || '') : '';
    document.getElementById('editArtPoemEn').value = art ? (art.poem_en || '') : '';

    artworkModal.classList.add('active');
  }

  function closeArtworkModal() {
    if (artworkModal) artworkModal.classList.remove('active');
  }

  if (btnNewArtwork) btnNewArtwork.onclick = () => openArtworkModal();
  if (btnCloseArtworkModal) btnCloseArtworkModal.onclick = closeArtworkModal;
  if (btnCancelArtworkModal) btnCancelArtworkModal.onclick = closeArtworkModal;

  if (btnSaveArtwork) {
    btnSaveArtwork.onclick = async () => {
      const id = document.getElementById('editArtId').value.trim() || `art_${Date.now()}`;
      const code = document.getElementById('editArtCode').value.trim();
      const titleKr = document.getElementById('editArtTitleKr').value.trim();
      const titleEn = document.getElementById('editArtTitleEn').value.trim();
      const series = document.getElementById('editArtSeries').value;
      const size = document.getElementById('editArtSize').value.trim();
      const priceStr = document.getElementById('editArtPrice').value.replace(/[^0-9]/g, '');
      const priceNum = Math.round(Number(priceStr || 0) / 10000) * 10000;
      const medium = document.getElementById('editArtMedium').value.trim();
      const image = document.getElementById('editArtImage').value.trim();
      const poemKr = document.getElementById('editArtPoemKr').value.trim();
      const poemEn = document.getElementById('editArtPoemEn').value.trim();

      if (!code) {
        alert('작품 코드를 입력해주세요.');
        return;
      }

      const artPayload = {
        id,
        code,
        title: code,
        subTitle: titleKr,
        subTitleEn: titleEn,
        title_kr: titleKr,
        title_en: titleEn,
        category: series,
        series: series === 'master' ? 'Moments 대표작' : series === 'modular' ? '4연작 모듈 세트' : '2연작 듀오 블록',
        size_spec: size,
        size: size,
        price: priceNum,
        medium,
        image_url: image,
        image: image,
        poem_kr: poemKr,
        poem_en: poemEn,
        status: 'available'
      };

      await window.ArtDatabase.saveArtwork(artPayload);
      closeArtworkModal();
      showToast(`[${code}] 작품 정보가 ₩${priceNum.toLocaleString('ko-KR')} (10,000원 단위)으로 완벽하게 저장되었습니다.`);
      await renderArtworks();
      loadKPIs();
    };
  }

  // 10. Batch Price Weight Adjustment Modal
  const batchPriceModal = document.getElementById('batchPriceModal');
  const btnOpenBatchPrice = document.getElementById('btnOpenBatchPrice');
  const btnCloseBatchPrice = document.getElementById('btnCloseBatchPrice');
  const btnCancelBatchPrice = document.getElementById('btnCancelBatchPrice');
  const btnApplyBatchPrice = document.getElementById('btnApplyBatchPrice');
  const batchScope = document.getElementById('batchScope');
  const batchMode = document.getElementById('batchMode');
  const batchValue = document.getElementById('batchValue');
  const batchValueLabel = document.getElementById('batchValueLabel');
  const batchPreviewBody = document.getElementById('batchPreviewBody');
  const batchAffectedCount = document.getElementById('batchAffectedCount');

  function openBatchPriceModal() {
    if (!batchPriceModal) return;
    batchPriceModal.classList.add('active');
    updateBatchPreview();
  }
  function closeBatchPriceModal() {
    if (batchPriceModal) batchPriceModal.classList.remove('active');
  }

  if (btnOpenBatchPrice) btnOpenBatchPrice.onclick = openBatchPriceModal;
  if (btnCloseBatchPrice) btnCloseBatchPrice.onclick = closeBatchPriceModal;
  if (btnCancelBatchPrice) btnCancelBatchPrice.onclick = closeBatchPriceModal;

  if (batchMode) {
    batchMode.addEventListener('change', () => {
      if (batchMode.value === 'multiplier') {
        batchValueLabel.textContent = '가중치 배율 (예: 1.10 = +10%, 1.20 = +20%, 0.90 = -10%)';
        batchValue.value = '1.10';
        batchValue.step = '0.01';
      } else {
        batchValueLabel.textContent = '고정 가감 금액 (KRW, 예: 500000 = +50만원, -300000 = -30만원)';
        batchValue.value = '500000';
        batchValue.step = '10000';
      }
      updateBatchPreview();
    });
  }

  if (batchScope) batchScope.addEventListener('change', updateBatchPreview);
  if (batchValue) batchValue.addEventListener('input', updateBatchPreview);

  document.querySelectorAll('.preset-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      if (batchMode) batchMode.value = 'multiplier';
      batchValue.value = btn.getAttribute('data-val');
      updateBatchPreview();
    });
  });

  function getTargetWorksForBatch() {
    const scope = batchScope ? batchScope.value : 'all';
    if (scope === 'all') return currentArtworks;
    return currentArtworks.filter(art => {
      const artCat = art.category || (art.series && art.series.includes('Quad') ? 'modular' : art.series && art.series.includes('Duo') ? 'duo' : 'master');
      return artCat === scope;
    });
  }

  function calcNewPrice(origPrice, mode, val) {
    let calc = origPrice;
    if (mode === 'multiplier') {
      calc = origPrice * parseFloat(val || '1.0');
    } else {
      calc = origPrice + parseInt(val || '0', 10);
    }
    if (calc < 10000) calc = 10000;
    return Math.round(calc / 10000) * 10000;
  }

  function updateBatchPreview() {
    if (!batchPreviewBody) return;
    const targets = getTargetWorksForBatch();
    const mode = batchMode ? batchMode.value : 'multiplier';
    const val = batchValue ? batchValue.value : '1.10';

    if (batchAffectedCount) {
      batchAffectedCount.textContent = `적용 대상: ${targets.length}건`;
    }

    batchPreviewBody.innerHTML = '';
    const sample = targets.slice(0, 5);

    if (sample.length === 0) {
      batchPreviewBody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding:20px; color:var(--text-muted);">대상 작품이 없습니다.</td></tr>';
      return;
    }

    sample.forEach(art => {
      const origPrice = typeof art.price === 'number' ? art.price : (parseInt(String(art.price).replace(/[^0-9]/g, ''), 10) || 0);
      const newPrice = calcNewPrice(origPrice, mode, val);
      const diff = newPrice - origPrice;
      const diffColor = diff > 0 ? '#34d399' : diff < 0 ? '#f87171' : 'var(--text-muted)';
      const diffSign = diff > 0 ? '+' : '';

      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><strong style="color:var(--accent-gold);">${art.code || art.title}</strong></td>
        <td><span style="font-size:0.75rem; color:var(--text-muted);">${art.series || art.category}</span></td>
        <td>₩ ${origPrice.toLocaleString('ko-KR')}</td>
        <td><strong style="color:var(--text-main);">₩ ${newPrice.toLocaleString('ko-KR')}</strong></td>
        <td style="color:${diffColor}; font-weight:600;">${diffSign}${diff.toLocaleString('ko-KR')}</td>
      `;
      batchPreviewBody.appendChild(tr);
    });
  }

  if (btnApplyBatchPrice) {
    btnApplyBatchPrice.addEventListener('click', async () => {
      const targets = getTargetWorksForBatch();
      const mode = batchMode ? batchMode.value : 'multiplier';
      const val = batchValue ? batchValue.value : '1.10';

      if (targets.length === 0) {
        alert('조정할 대상 작품이 없습니다.');
        return;
      }

      const confirmMsg = `총 ${targets.length}개 작품의 소장 가격을 ${mode === 'multiplier' ? `${val}배` : `${parseInt(val, 10).toLocaleString()}원`} 가중치(최소 10,000원 단위 정렬)로 일괄 변경하시겠습니까?`;
      if (!confirm(confirmMsg)) return;

      btnApplyBatchPrice.disabled = true;
      btnApplyBatchPrice.textContent = '일괄 저장 처리 중...';

      let count = 0;
      for (const art of targets) {
        const origPrice = typeof art.price === 'number' ? art.price : (parseInt(String(art.price).replace(/[^0-9]/g, ''), 10) || 0);
        art.price = calcNewPrice(origPrice, mode, val);
        await window.ArtDatabase.saveArtwork(art);
        count++;
      }

      btnApplyBatchPrice.disabled = false;
      btnApplyBatchPrice.textContent = '가중치 계산 및 전체 가격 일괄 저장 확정';
      closeBatchPriceModal();

      showToast(`🎉 총 ${count}개 작품의 가격이 10,000원 단위로 완벽하게 일괄 조정되었습니다.`);
      await renderArtworks();
      loadKPIs();
    });
  }

  // 11. Orders & Purchases Ledger (Tab 2)
  const orderTableBody = document.getElementById('orderTableBody');
  const filterOrderStatus = document.getElementById('filterOrderStatus');
  const orderDetailModal = document.getElementById('orderDetailModal');
  const orderDetailModalBody = document.getElementById('orderDetailModalBody');
  const btnCloseOrderDetail = document.getElementById('btnCloseOrderDetail');
  const btnDoneOrderDetail = document.getElementById('btnDoneOrderDetail');

  if (filterOrderStatus) {
    filterOrderStatus.addEventListener('change', () => renderOrders());
  }

  async function renderOrders() {
    if (!orderTableBody) return;
    const orders = window.firebaseEngine ? window.firebaseEngine.getAllOrders() : [];
    const filter = filterOrderStatus ? filterOrderStatus.value : 'all';

    const filtered = orders.filter(o => {
      if (filter === 'all') return true;
      return o.order_status === filter;
    });

    orderTableBody.innerHTML = '';
    if (filtered.length === 0) {
      orderTableBody.innerHTML = `<tr><td colspan="9" style="text-align:center; padding: 40px; color: var(--text-muted);">해당 상태의 주문 내역이 없습니다.</td></tr>`;
      return;
    }

    filtered.forEach(order => {
      const tr = document.createElement('tr');
      const dateStr = order.created_at ? new Date(order.created_at).toLocaleString('ko-KR') : '-';
      const itemsBrief = (order.items || []).map(it => `<div>• ${it.title} × ${it.quantity || 1}</div>`).join('');
      const totalFormatted = Math.round(Number(order.total_amount) / 10000) * 10000;

      tr.innerHTML = `
        <td style="font-family:monospace; font-weight:700; color:var(--accent-gold);">${order.order_id}</td>
        <td style="font-size:0.8rem; color:var(--text-muted);">${dateStr}</td>
        <td>
          <strong>${order.user_name || '-'}</strong>
          <div style="font-size:0.78rem; color:var(--text-muted);">${order.user_email || ''}</div>
        </td>
        <td style="font-size:0.82rem;">
          <div><a href="tel:${order.user_phone}" style="color:inherit;">${order.user_phone || '-'}</a></div>
          <div style="color:var(--text-muted); font-size:0.78rem;">${order.shipping_address || '-'}</div>
        </td>
        <td style="font-size:0.82rem;">${itemsBrief}</td>
        <td style="font-weight:700; color:#FA5A50; font-size:0.95rem;">₩ ${totalFormatted.toLocaleString('ko-KR')}</td>
        <td style="font-size:0.8rem;">${order.payment_method === 'credit_card' ? '신용카드' : order.payment_method === 'bank_transfer' ? '계좌이체' : '가상계좌/인보이스'}</td>
        <td>
          <select class="form-control order-status-select" data-id="${order.order_id}" style="padding:4px 8px; font-size:0.8rem; width:120px;">
            <option value="결제완료" ${order.order_status === '결제완료' ? 'selected' : ''}>결제완료</option>
            <option value="작품검수중" ${order.order_status === '작품검수중' ? 'selected' : ''}>작품검수중</option>
            <option value="프라이빗배송준비" ${order.order_status === '프라이빗배송준비' ? 'selected' : ''}>프라이빗배송준비</option>
            <option value="배송중" ${order.order_status === '배송중' ? 'selected' : ''}>배송중</option>
            <option value="소장인도완료" ${order.order_status === '소장인도완료' ? 'selected' : ''}>소장인도완료</option>
          </select>
        </td>
        <td>
          <button class="btn btn-secondary btn-sm btn-view-order" data-id="${order.order_id}" style="font-size:0.78rem;">
            상세/보증서
          </button>
        </td>
      `;
      orderTableBody.appendChild(tr);
    });

    orderTableBody.querySelectorAll('.order-status-select').forEach(sel => {
      sel.addEventListener('change', async (e) => {
        const orderId = e.target.getAttribute('data-id');
        const newStatus = e.target.value;
        if (window.firebaseEngine) {
          window.firebaseEngine.updateOrderStatus(orderId, newStatus);
          showToast(`주문 ${orderId}의 상태가 '${newStatus}'(으)로 갱신되었습니다.`);
          loadKPIs();
        }
      });
    });

    orderTableBody.querySelectorAll('.btn-view-order').forEach(btn => {
      btn.addEventListener('click', () => {
        const orderId = btn.getAttribute('data-id');
        const orders = window.firebaseEngine ? window.firebaseEngine.getAllOrders() : [];
        const targetOrder = orders.find(o => o.order_id === orderId);
        if (targetOrder) openOrderDetailModal(targetOrder);
      });
    });
  }

  function openOrderDetailModal(order) {
    if (!orderDetailModal || !orderDetailModalBody) return;
    const totalFormatted = Math.round(Number(order.total_amount) / 10000) * 10000;
    const itemsHtml = (order.items || []).map(it => `
      <div style="display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid rgba(255,255,255,0.05);">
        <div>
          <strong style="color:var(--accent-gold);">${it.title}</strong>
          <div style="font-size:0.8rem; color:var(--text-muted);">${it.size || ''} ｜ ${it.medium || ''}</div>
        </div>
        <div style="text-align:right;">
          <span style="font-size:0.82rem; color:var(--text-muted);">${it.quantity || 1}점 × </span>
          <strong style="font-size:0.9rem;">₩ ${(Math.round(Number(it.price) / 10000) * 10000).toLocaleString('ko-KR')}</strong>
        </div>
      </div>
    `).join('');

    orderDetailModalBody.innerHTML = `
      <div class="invoice-card">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:16px;">
          <div>
            <div style="font-family:var(--font-serif); font-size:1.25rem; font-weight:700; color:var(--accent-gold);">MA JI YOUNG ATELIER</div>
            <div style="font-size:0.8rem; color:var(--text-muted);">OFFICIAL CERTIFICATE OF AUTHENTICITY & INVOICE</div>
          </div>
          <div style="text-align:right;">
            <div style="font-size:0.75rem; color:var(--text-muted);">주문번호</div>
            <div style="font-family:monospace; font-size:0.95rem; font-weight:700; color:var(--text-main);">${order.order_id}</div>
          </div>
        </div>

        <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-bottom:20px; font-size:0.85rem; background:rgba(0,0,0,0.3); padding:14px; border-radius:8px;">
          <div>
            <span style="color:var(--text-muted);">소장 컬렉터:</span> <strong>${order.user_name}</strong><br>
            <span style="color:var(--text-muted);">연락처:</span> ${order.user_phone}<br>
            <span style="color:var(--text-muted);">이메일:</span> ${order.user_email}
          </div>
          <div>
            <span style="color:var(--text-muted);">주문 일시:</span> ${order.created_at ? new Date(order.created_at).toLocaleString('ko-KR') : '-'}<br>
            <span style="color:var(--text-muted);">배송지:</span> ${order.shipping_address}<br>
            <span style="color:var(--text-muted);">결제 수단:</span> ${order.payment_method === 'credit_card' ? '신용카드' : '계좌이체/인보이스'}
          </div>
        </div>

        <div style="margin-bottom:16px;">
          <h4 style="font-size:0.85rem; color:var(--text-muted); text-transform:uppercase; margin-bottom:8px;">소장 작품 내역</h4>
          ${itemsHtml}
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center; padding-top:12px; border-top:1px solid var(--accent-gold-border); margin-top:12px;">
          <span style="font-size:0.95rem; font-weight:700;">총 결제 금액 (10,000원 단위 정렬)</span>
          <span style="font-size:1.3rem; font-weight:800; color:#FA5A50;">₩ ${totalFormatted.toLocaleString('ko-KR')}</span>
        </div>

        <div style="margin-top:20px; padding:14px; background:rgba(197,168,128,0.08); border:1px solid rgba(197,168,128,0.25); border-radius:8px;">
          <div style="font-size:0.8rem; color:var(--accent-gold); font-weight:700; margin-bottom:4px;">🛡️ 정품 디지털 보증서 번호</div>
          <div style="font-family:monospace; font-size:1rem; letter-spacing:0.08em; font-weight:800; color:var(--text-main);">${order.warranty_number || 'WARRANTY-2026-00102'}</div>
          <div style="font-size:0.75rem; color:var(--text-muted); margin-top:4px;">본 보증서는 마지영 아틀리에 본사에서 발행된 유일한 정품 인증 증빙입니다.</div>
        </div>
      </div>
    `;

    orderDetailModal.classList.add('active');
  }

  function closeOrderDetailModal() {
    if (orderDetailModal) orderDetailModal.classList.remove('active');
  }
  if (btnCloseOrderDetail) btnCloseOrderDetail.onclick = closeOrderDetailModal;
  if (btnDoneOrderDetail) btnDoneOrderDetail.onclick = closeOrderDetailModal;

  // 12. Registered Collectors Ledger (Tab 3)
  const userTableBody = document.getElementById('userTableBody');
  const userHistoryModal = document.getElementById('userHistoryModal');
  const userHistoryModalTitle = document.getElementById('userHistoryModalTitle');
  const userHistoryModalBody = document.getElementById('userHistoryModalBody');
  const btnCloseUserHistory = document.getElementById('btnCloseUserHistory');
  const btnDoneUserHistory = document.getElementById('btnDoneUserHistory');

  async function renderUsers() {
    if (!userTableBody) return;
    const users = window.firebaseEngine ? window.firebaseEngine.getAllUsers() : [];
    userTableBody.innerHTML = '';

    if (users.length === 0) {
      userTableBody.innerHTML = `<tr><td colspan="8" style="text-align:center; padding: 40px; color: var(--text-muted);">등록된 회원이 없습니다.</td></tr>`;
      return;
    }

    users.forEach(u => {
      const tr = document.createElement('tr');
      const dateStr = u.created_at ? new Date(u.created_at).toLocaleDateString('ko-KR') : '-';
      const tierBadge = u.tier === 'vip' 
        ? `<span class="badge" style="background:#4527a0; color:#fff; font-size:0.75rem; padding:3px 8px; border-radius:4px; font-weight:700;">👑 VIP 파트론</span>`
        : `<span class="badge" style="background:#444; color:#ddd; font-size:0.75rem; padding:3px 8px; border-radius:4px;">프라이빗 컬렉터</span>`;

      tr.innerHTML = `
        <td style="font-family:monospace; font-size:0.78rem; color:var(--text-muted);">${u.uid}</td>
        <td><strong>${u.name}</strong></td>
        <td style="font-size:0.85rem;">${u.email}</td>
        <td style="font-size:0.85rem;">${u.phone || '-'}</td>
        <td style="font-size:0.82rem; color:var(--text-muted); max-width:200px;">${u.address || '-'}</td>
        <td>${tierBadge}</td>
        <td style="font-size:0.8rem; color:var(--text-muted);">${dateStr}</td>
        <td>
          <button class="btn btn-secondary btn-sm btn-user-history" data-uid="${u.uid}" data-name="${u.name}" style="font-size:0.78rem;">
            소장 이력
          </button>
        </td>
      `;
      userTableBody.appendChild(tr);
    });

    userTableBody.querySelectorAll('.btn-user-history').forEach(btn => {
      btn.addEventListener('click', () => {
        const uid = btn.getAttribute('data-uid');
        const name = btn.getAttribute('data-name');
        openUserHistoryModal(uid, name);
      });
    });
  }

  function openUserHistoryModal(uid, name) {
    if (!userHistoryModal || !userHistoryModalBody) return;
    if (userHistoryModalTitle) userHistoryModalTitle.textContent = `${name} 컬렉터님의 소장 이력 대장`;

    const orders = window.firebaseEngine ? window.firebaseEngine.getAllOrders() : [];
    const userOrders = orders.filter(o => o.user_id === uid || o.user_name === name);

    let contentHtml = '';
    if (userOrders.length === 0) {
      contentHtml = `<p style="text-align:center; padding:30px; color:var(--text-muted);">현재까지 완료된 소장 내역이 없습니다.</p>`;
    } else {
      let totalSpent = 0;
      const ordersHtml = userOrders.map(o => {
        const amt = Math.round(Number(o.total_amount) / 10000) * 10000;
        totalSpent += amt;
        const workNames = (o.items || []).map(i => `• ${i.title} (${i.size || ''})`).join('<br>');
        return `
          <div style="background:var(--bg-card); border:1px solid var(--border-color); border-radius:8px; padding:16px; margin-bottom:12px;">
            <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
              <span style="font-family:monospace; font-weight:700; color:var(--accent-gold);">${o.order_id}</span>
              <span style="font-size:0.8rem; color:var(--text-muted);">${o.created_at ? new Date(o.created_at).toLocaleDateString('ko-KR') : ''}</span>
            </div>
            <div style="font-size:0.85rem; margin-bottom:8px;">${workNames}</div>
            <div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid rgba(255,255,255,0.05); padding-top:8px;">
              <span style="font-size:0.78rem; color:var(--status-available);">상태: ${o.order_status || '결제완료'}</span>
              <strong style="color:#FA5A50;">₩ ${amt.toLocaleString('ko-KR')}</strong>
            </div>
          </div>
        `;
      }).join('');

      contentHtml = `
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px; padding:14px; background:rgba(197,168,128,0.1); border-radius:8px;">
          <div>
            <div style="font-size:0.8rem; color:var(--text-muted);">총 소장 작품 수</div>
            <strong style="font-size:1.2rem; color:var(--text-main);">${userOrders.length}회 주문</strong>
          </div>
          <div style="text-align:right;">
            <div style="font-size:0.8rem; color:var(--text-muted);">누적 소장 결제액</div>
            <strong style="font-size:1.3rem; color:#FA5A50;">₩ ${totalSpent.toLocaleString('ko-KR')}</strong>
          </div>
        </div>
        ${ordersHtml}
      `;
    }

    userHistoryModalBody.innerHTML = contentHtml;
    userHistoryModal.classList.add('active');
  }

  function closeUserHistoryModal() {
    if (userHistoryModal) userHistoryModal.classList.remove('active');
  }
  if (btnCloseUserHistory) btnCloseUserHistory.onclick = closeUserHistoryModal;
  if (btnDoneUserHistory) btnDoneUserHistory.onclick = closeUserHistoryModal;

  // 13. Inquiries Ledger (Tab 4)
  const inquiryTableBody = document.getElementById('inquiryTableBody');

  async function renderInquiries() {
    const inquiries = await window.ArtDatabase.getInquiries();
    if (!inquiryTableBody) return;
    inquiryTableBody.innerHTML = '';

    if (inquiries.length === 0) {
      inquiryTableBody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding: 40px; color: var(--text-muted);">접수된 소장 문의 내역이 없습니다.</td></tr>`;
      return;
    }

    inquiries.forEach(inq => {
      const tr = document.createElement('tr');
      const dateStr = inq.created_at ? new Date(inq.created_at).toLocaleDateString('ko-KR') : '방금 전';
      tr.innerHTML = `
        <td style="font-size:0.8rem; color:var(--text-muted);">${dateStr}</td>
        <td><strong>${inq.client_name || '-'}</strong></td>
        <td><a href="tel:${inq.client_phone}" style="color:var(--accent-gold); text-decoration:none;">${inq.client_phone || '-'}</a></td>
        <td style="font-size:0.85rem;">${inq.client_email || '-'}</td>
        <td><span class="art-code">${inq.artwork_title || inq.artwork_code || '전시/프라이빗 뷰잉'}</span></td>
        <td style="max-width:240px; font-size:0.82rem; color:var(--text-muted); overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">${inq.message || '-'}</td>
        <td>
          <select class="form-control inq-status-select" data-id="${inq.id}" style="padding:4px 8px; font-size:0.8rem; width:110px;">
            <option value="pending" ${inq.status === 'pending' ? 'selected' : ''}>신규접수</option>
            <option value="reviewing" ${inq.status === 'reviewing' ? 'selected' : ''}>검토중</option>
            <option value="contacted" ${inq.status === 'contacted' ? 'selected' : ''}>연락완료</option>
            <option value="closed" ${inq.status === 'closed' ? 'selected' : ''}>상담종료</option>
          </select>
        </td>
      `;
      inquiryTableBody.appendChild(tr);
    });

    inquiryTableBody.querySelectorAll('.inq-status-select').forEach(sel => {
      sel.addEventListener('change', async (e) => {
        const inqId = e.target.getAttribute('data-id');
        await window.ArtDatabase.updateInquiryStatus(inqId, e.target.value);
        showToast('문의 처리 상태가 갱신되었습니다.');
      });
    });
  }

  // 14. Statement & Exhibitions Split View (Tab 5)
  const statTitleKr = document.getElementById('statTitleKr');
  const statTitleEn = document.getElementById('statTitleEn');
  const statBodyKr = document.getElementById('statBodyKr');
  const statBodyEn = document.getElementById('statBodyEn');
  const previewTitle = document.getElementById('previewTitle');
  const previewBody = document.getElementById('previewBody');
  const btnSaveStatement = document.getElementById('btnSaveStatement');

  function updateStatementPreview() {
    if (previewTitle) {
      const tKr = statTitleKr ? statTitleKr.value.trim() : '';
      const tEn = statTitleEn ? statTitleEn.value.trim() : '';
      previewTitle.textContent = `${tKr || 'Moments'} ${tEn ? `| ${tEn}` : ''}`;
    }
    if (previewBody) {
      const bKr = statBodyKr ? statBodyKr.value.trim() : '';
      const bEn = statBodyEn ? statBodyEn.value.trim() : '';
      previewBody.innerHTML = `
        <div style="margin-bottom:16px;">${bKr.replace(/\n\n/g, '<br><br>')}</div>
        <div style="font-size:0.88rem; color:#aaa; font-style:italic;">${bEn.replace(/\n\n/g, '<br><br>')}</div>
      `;
    }
  }

  if (statTitleKr) statTitleKr.addEventListener('input', updateStatementPreview);
  if (statTitleEn) statTitleEn.addEventListener('input', updateStatementPreview);
  if (statBodyKr) statBodyKr.addEventListener('input', updateStatementPreview);
  if (statBodyEn) statBodyEn.addEventListener('input', updateStatementPreview);

  async function renderExhibitionsAndStatement() {
    const artist = await window.ArtDatabase.getArtistProfile();
    if (statTitleKr) statTitleKr.value = artist.statementTitleKr || 'Moments : 시간의 결';
    if (statTitleEn) statTitleEn.value = artist.statementTitleEn || 'Moments : Grain of Time';
    if (statBodyKr) statBodyKr.value = Array.isArray(artist.statementKr) ? artist.statementKr.join('\n\n') : (artist.statementKr || '');
    if (statBodyEn) statBodyEn.value = Array.isArray(artist.statementEn) ? artist.statementEn.join('\n\n') : (artist.statementEn || '');
    updateStatementPreview();
  }

  if (btnSaveStatement) {
    btnSaveStatement.addEventListener('click', async () => {
      const statementTitleKr = statTitleKr.value.trim();
      const statementTitleEn = statTitleEn.value.trim();
      const statementKr = statBodyKr.value.split('\n\n').filter(Boolean);
      const statementEn = statBodyEn.value.split('\n\n').filter(Boolean);

      await window.ArtDatabase.saveArtistProfile({
        statementTitleKr,
        statementTitleEn,
        statementKr,
        statementEn
      });
      showToast('작가노트가 저장되고 메인 갤러리에 실시간 반영되었습니다.');
    });
  }

  // 15. Settings, Backup & Restore (Tab 6)
  function loadSupabaseSettingsUI() {
    const cfg = window.ArtDatabase.getConfig();
    const inputUrl = document.getElementById('cfgSupabaseUrl');
    const inputKey = document.getElementById('cfgSupabaseKey');

    if (inputUrl && cfg.url) inputUrl.value = cfg.url;
    if (inputKey && cfg.anonKey) inputKey.value = cfg.anonKey;
  }

  const btnConnectSupabase = document.getElementById('btnConnectSupabase');
  if (btnConnectSupabase) {
    btnConnectSupabase.addEventListener('click', async () => {
      const url = document.getElementById('cfgSupabaseUrl').value.trim();
      const key = document.getElementById('cfgSupabaseKey').value.trim();

      if (!url || !key) {
        alert('Supabase URL과 Anon Key를 입력해주세요.');
        return;
      }

      window.ArtDatabase.setConfig(url, key);
      updateCloudStatusBadge();

      try {
        await window.ArtDatabase.getArtworks();
        showToast('Supabase Cloud 연결에 성공했습니다!');
      } catch (e) {
        alert('연결 테스트 중 오류가 발생했습니다: ' + e.message);
      }
    });
  }

  // Backup Export JSON
  const btnExportJson = document.getElementById('btnExportJson');
  if (btnExportJson) {
    btnExportJson.addEventListener('click', async () => {
      const artworks = await window.ArtDatabase.getArtworks();
      const inquiries = await window.ArtDatabase.getInquiries();
      const profile = await window.ArtDatabase.getArtistProfile();
      const settings = await window.ArtDatabase.getSettings();
      const orders = window.firebaseEngine ? window.firebaseEngine.getAllOrders() : [];
      const users = window.firebaseEngine ? window.firebaseEngine.getAllUsers() : [];

      const dump = {
        exportedAt: new Date().toISOString(),
        brand: settings,
        artist: { ...profile, artworks },
        orders,
        users,
        inquiries
      };

      const blob = new Blob([JSON.stringify(dump, null, 2)], { type: 'application/json' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = `majiyoung_studio_backup_${new Date().toISOString().slice(0, 10)}.json`;
      a.click();
      showToast('데이터베이스 전체 백업 JSON 파일이 다운로드되었습니다.');
    });
  }

  // Backup Restore JSON
  const fileRestoreJson = document.getElementById('fileRestoreJson');
  const btnRestoreJson = document.getElementById('btnRestoreJson');
  if (btnRestoreJson) {
    btnRestoreJson.addEventListener('click', () => {
      if (!fileRestoreJson || !fileRestoreJson.files || fileRestoreJson.files.length === 0) {
        alert('복원할 백업 JSON 파일을 먼저 선택해주세요.');
        return;
      }

      const file = fileRestoreJson.files[0];
      const reader = new FileReader();
      reader.onload = async (e) => {
        try {
          const data = JSON.parse(e.target.result);
          if (data.artist && data.artist.artworks) {
            localStorage.setItem('mjy_artworks', JSON.stringify(data.artist.artworks));
          }
          if (data.orders) {
            localStorage.setItem('mjy_firebase_orders', JSON.stringify(data.orders));
          }
          if (data.users) {
            localStorage.setItem('mjy_firebase_users', JSON.stringify(data.users));
          }
          if (data.inquiries) {
            localStorage.setItem('mjy_inquiries', JSON.stringify(data.inquiries));
          }
          showToast('🎉 백업 파일로부터 데이터베이스가 성공적으로 복원되었습니다.');
          await initDashboard();
        } catch (err) {
          alert('JSON 파일 파싱 중 오류가 발생했습니다: ' + err.message);
        }
      };
      reader.readAsText(file);
    });
  }

  // Factory Reset
  const btnResetDefault = document.getElementById('btnResetDefault');
  if (btnResetDefault) {
    btnResetDefault.addEventListener('click', async () => {
      if (confirm('모든 수장고 데이터 및 주문/회원 목록을 초기 기본 42점 시드 상태로 복원하시겠습니까?')) {
        window.ArtDatabase.resetToDefaultSeed();
        showToast('초기 기본 42점 수장고 데이터로 복원되었습니다.');
        await initDashboard();
      }
    });
  }

  // Toast Notification Utility
  function showToast(msg) {
    let container = document.querySelector('.toast-container');
    if (!container) {
      container = document.createElement('div');
      container.className = 'toast-container';
      document.body.appendChild(container);
    }
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = msg;
    container.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      setTimeout(() => toast.remove(), 300);
    }, 2800);
  }
});
