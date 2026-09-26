// ========================================================
// MA JI YOUNG EDITION & ATELIER - Admin CMS Controller
// ========================================================

document.addEventListener('DOMContentLoaded', () => {
  // 1. Authentication Check (admin / 1234567)
  const AUTH_KEY = 'mjy_admin_auth_token';
  const VALID_USER = 'admin';
  const VALID_PASS = '1234567';

  const loginModal = document.getElementById('loginModal');
  const loginIdInput = document.getElementById('loginId');
  const loginPasswordInput = document.getElementById('loginPassword');
  const loginBtn = document.getElementById('btnLogin');

  function isAuthenticated() {
    return sessionStorage.getItem(AUTH_KEY) === 'authenticated';
  }

  function showLoginModal() {
    if (loginModal) loginModal.classList.add('active');
  }

  function hideLoginModal() {
    if (loginModal) loginModal.classList.remove('active');
  }

  if (loginBtn) {
    loginBtn.addEventListener('click', () => {
      const id = loginIdInput ? loginIdInput.value.trim() : '';
      const pw = loginPasswordInput ? loginPasswordInput.value.trim() : '';
      
      // Check admin / 1234567 or legacy passcode
      if ((id === VALID_USER && pw === VALID_PASS) || pw === 'majiyoung2026!' || pw === 'admin2026!') {
        sessionStorage.setItem(AUTH_KEY, 'authenticated');
        hideLoginModal();
        showToast('성공적으로 관리자 인증되었습니다. (ID: admin)');
        initDashboard();
      } else {
        alert('아이디 또는 비밀번호가 일치하지 않습니다.\n기본 인증 정보: admin / 1234567');
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

  if (!isAuthenticated()) {
    showLoginModal();
  } else {
    initDashboard();
  }

  // 2. Navigation & Tab Switching
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
    });
  });

  // 3. Main Dashboard Initialization
  async function initDashboard() {
    updateCloudStatusBadge();
    await loadKPIs();
    await renderArtworks();
    await renderInquiries();
    await renderExhibitionsAndStatement();
    loadSupabaseSettingsUI();
  }

  // 4. Cloud Status Indicator
  function updateCloudStatusBadge() {
    const badge = document.getElementById('cloudStatusBadge');
    if (!badge) return;
    const isCloud = window.ArtDatabase && window.ArtDatabase.isCloudActive();
    if (isCloud) {
      badge.className = 'cloud-status-badge';
      badge.innerHTML = '<span class="status-dot"></span> Supabase Cloud Connected';
    } else {
      badge.className = 'cloud-status-badge offline';
      badge.innerHTML = '<span class="status-dot"></span> Hybrid Local DB (Ready to Cloud)';
    }
  }

  // 5. KPI Summary Calculation
  async function loadKPIs() {
    const artworks = await window.ArtDatabase.getArtworks();
    const inquiries = await window.ArtDatabase.getInquiries();

    const totalCount = artworks.length;
    const availCount = artworks.filter(a => (a.status || 'available') === 'available').length;
    const soldCount = artworks.filter(a => a.status === 'sold').length;
    const inqCount = inquiries.length;

    document.getElementById('kpiTotalWorks').textContent = totalCount;
    document.getElementById('kpiAvailableWorks').textContent = availCount;
    document.getElementById('kpiSoldWorks').textContent = soldCount;
    document.getElementById('kpiInquiries').textContent = inqCount;

    const inqBadge = document.getElementById('badgeInquiryCount');
    if (inqBadge) inqBadge.textContent = inqCount;
  }

  // 6. Artwork Studio (Tab 1)
  let currentArtworks = [];
  const artworkTableBody = document.getElementById('artworkTableBody');
  const searchArtInput = document.getElementById('searchArtwork');
  const filterSeriesSelect = document.getElementById('filterSeries');

  async function renderArtworks() {
    currentArtworks = await window.ArtDatabase.getArtworks();
    applyArtworkFilter();
  }

  function applyArtworkFilter() {
    const query = (searchArtInput ? searchArtInput.value : '').toLowerCase().trim();
    const seriesFilter = filterSeriesSelect ? filterSeriesSelect.value : 'all';

    let filtered = currentArtworks.filter(art => {
      const matchQuery = !query ||
        (art.title && art.title.toLowerCase().includes(query)) ||
        (art.subTitle && art.subTitle.toLowerCase().includes(query)) ||
        (art.title_kr && art.title_kr.toLowerCase().includes(query)) ||
        (art.code && art.code.toLowerCase().includes(query));

      const artCategory = art.category || (art.series && art.series.includes('Quad') ? 'modular' : art.series && art.series.includes('Duo') ? 'duo' : 'master');
      const matchSeries = seriesFilter === 'all' || artCategory === seriesFilter;

      return matchQuery && matchSeries;
    });

    if (!artworkTableBody) return;
    artworkTableBody.innerHTML = '';

    if (filtered.length === 0) {
      artworkTableBody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding: 40px; color: var(--text-muted);">일치하는 작품이 없습니다.</td></tr>`;
      return;
    }

    filtered.forEach(art => {
      const tr = document.createElement('tr');
      const titleDisplay = art.title_kr || `${art.title || art.code} - ${art.subTitle || ''}`;
      const titleEnDisplay = art.title_en || art.subTitleEn || '';
      const status = art.status || 'available';
      const rawNum = typeof art.price === 'number' ? art.price : (parseInt(String(art.price || '0').replace(/[^0-9]/g, ''), 10) || 0);
      const formattedPrice = rawNum.toLocaleString('ko-KR');

      tr.innerHTML = `
        <td><img src="../${art.image_url || art.image}" class="table-thumb" alt="thumb" onerror="this.src='../assets/images/logo_mjy.svg'"></td>
        <td>
          <div class="art-title-cell">
            <span class="art-code">${art.code || art.title}</span>
            <span class="art-title-kr">${titleDisplay}</span>
            <span class="art-title-en">${titleEnDisplay}</span>
          </div>
        </td>
        <td><span style="font-size:0.8rem; color:var(--text-muted);">${art.series || art.category}</span></td>
        <td><span style="font-size:0.82rem;">${art.size_spec || art.size || '-'}</span></td>
        <td>
          <div style="display:flex; align-items:center; gap:6px;">
            <span>₩</span>
            <input type="text" class="form-control inline-price" data-id="${art.id}" value="${formattedPrice}" style="width:110px; padding:4px 8px; font-size:0.85rem;">
          </div>
        </td>
        <td>
          <select class="form-control select-status" data-id="${art.id}" style="padding:4px 8px; font-size:0.8rem; width:100px;">
            <option value="available" ${status === 'available' ? 'selected' : ''}>소장가능</option>
            <option value="reserved" ${status === 'reserved' ? 'selected' : ''}>예약중</option>
            <option value="sold" ${status === 'sold' ? 'selected' : ''}>소장완료</option>
            <option value="private" ${status === 'private' ? 'selected' : ''}>비공개</option>
          </select>
        </td>
        <td>
          <div style="display:flex; gap:8px;">
            <button class="btn btn-secondary btn-sm btn-edit-art" data-id="${art.id}">편집</button>
            <button class="btn btn-danger btn-sm btn-del-art" data-id="${art.id}">삭제</button>
          </div>
        </td>
      `;
      artworkTableBody.appendChild(tr);
    });

    // Event Bindings for Table elements
    artworkTableBody.querySelectorAll('.inline-price').forEach(input => {
      input.addEventListener('change', async (e) => {
        const id = e.target.getAttribute('data-id');
        let rawVal = parseInt(e.target.value.replace(/[^0-9]/g, ''), 10) || 0;
        // 최소 10,000원 단위 정렬 (Round to nearest 10,000 KRW)
        const numVal = Math.round(rawVal / 10000) * 10000;
        e.target.value = numVal.toLocaleString('ko-KR');

        const targetArt = currentArtworks.find(a => a.id === id);
        if (targetArt) {
          targetArt.price = numVal;
          await window.ArtDatabase.saveArtwork(targetArt);
          showToast(`[${targetArt.title || targetArt.code}] 가격이 ₩${numVal.toLocaleString('ko-KR')} (10,000원 단위)으로 변경되었습니다.`);
          loadKPIs();
        }
      });
    });

    artworkTableBody.querySelectorAll('.select-status').forEach(select => {
      select.addEventListener('change', async (e) => {
        const id = e.target.getAttribute('data-id');
        const newStatus = e.target.value;
        const targetArt = currentArtworks.find(a => a.id === id);
        if (targetArt) {
          targetArt.status = newStatus;
          await window.ArtDatabase.saveArtwork(targetArt);
          showToast(`[${targetArt.title || targetArt.code}] 상태가 [${newStatus}]로 업데이트되었습니다.`);
          loadKPIs();
        }
      });
    });

    artworkTableBody.querySelectorAll('.btn-edit-art').forEach(btn => {
      btn.addEventListener('click', () => {
        const id = btn.getAttribute('data-id');
        const targetArt = currentArtworks.find(a => a.id === id);
        if (targetArt) openArtworkModal(targetArt);
      });
    });

    artworkTableBody.querySelectorAll('.btn-del-art').forEach(btn => {
      btn.addEventListener('click', async () => {
        const id = btn.getAttribute('data-id');
        if (confirm('정말로 이 작품을 목록에서 삭제하시겠습니까?')) {
          await window.ArtDatabase.deleteArtwork(id);
          showToast('작품이 삭제되었습니다.');
          await renderArtworks();
          loadKPIs();
        }
      });
    });
  }

  if (searchArtInput) searchArtInput.addEventListener('input', applyArtworkFilter);
  if (filterSeriesSelect) filterSeriesSelect.addEventListener('change', applyArtworkFilter);

  // Artwork Add/Edit Modal
  const artworkModal = document.getElementById('artworkModal');
  const btnNewArtwork = document.getElementById('btnNewArtwork');
  const btnCloseArtworkModal = document.getElementById('btnCloseArtworkModal');
  const btnSaveArtwork = document.getElementById('btnSaveArtwork');

  function openArtworkModal(art = null) {
    document.getElementById('artModalTitle').textContent = art ? '작품 상세 정밀 편집' : '신규 작품 등록';
    document.getElementById('editArtId').value = art ? art.id : '';
    document.getElementById('editArtCode').value = art ? (art.code || art.title) : '';
    document.getElementById('editArtTitleKr').value = art ? (art.subTitle || art.title_kr || '') : '';
    document.getElementById('editArtTitleEn').value = art ? (art.subTitleEn || art.title_en || '') : '';
    document.getElementById('editArtSeries').value = art ? (art.category || 'master') : 'master';
    document.getElementById('editArtSize').value = art ? (art.size_spec || art.size || '') : '';
    const rawPrice = art ? (typeof art.price === 'number' ? art.price : String(art.price).replace(/[^0-9]/g, '')) : '0';
    document.getElementById('editArtPrice').value = rawPrice;
    document.getElementById('editArtImage').value = art ? (art.image_url || art.image || '') : 'assets/images/artwork_moments_26_001.png';
    document.getElementById('editArtMedium').value = art ? (art.medium || '') : 'mixed media on wooden Blocks';
    document.getElementById('editArtPoemKr').value = art ? (art.poemKr || art.description_kr || '') : '';
    document.getElementById('editArtPoemEn').value = art ? (art.poemEn || art.description_en || '') : '';

    if (artworkModal) artworkModal.classList.add('active');
  }

  if (btnNewArtwork) btnNewArtwork.addEventListener('click', () => openArtworkModal());
  if (btnCloseArtworkModal) btnCloseArtworkModal.addEventListener('click', () => artworkModal.classList.remove('active'));

  if (btnSaveArtwork) {
    btnSaveArtwork.addEventListener('click', async () => {
      const id = document.getElementById('editArtId').value;
      const code = document.getElementById('editArtCode').value.trim() || ('Moments 26-' + Date.now().toString().slice(-3));
      const subTitle = document.getElementById('editArtTitleKr').value.trim();
      const subTitleEn = document.getElementById('editArtTitleEn').value.trim();
      const category = document.getElementById('editArtSeries').value;
      const size = document.getElementById('editArtSize').value.trim();
      const price = parseInt(document.getElementById('editArtPrice').value.replace(/[^0-9]/g, ''), 10) || 0;
      const image = document.getElementById('editArtImage').value.trim();
      const medium = document.getElementById('editArtMedium').value.trim();
      const poemKr = document.getElementById('editArtPoemKr').value.trim();
      const poemEn = document.getElementById('editArtPoemEn').value.trim();

      let target = currentArtworks.find(a => a.id === id);
      if (!target) {
        target = { id: id || ('MJY-' + Date.now().toString(36).toUpperCase()), status: 'available' };
      }

      target.title = code;
      target.code = code;
      target.subTitle = subTitle;
      target.subTitleEn = subTitleEn;
      target.title_kr = `${code} - ${subTitle}`;
      target.title_en = subTitleEn;
      target.category = category;
      target.series = category === 'modular' ? '4연작 모듈 세트 (Quad Series)' : category === 'duo' ? '2연작 듀오 블록 (Duo Series)' : '대표작 (Master Collection)';
      target.size = size;
      target.size_spec = size;
      target.price = price;
      target.image = image;
      target.image_url = image;
      target.medium = medium;
      target.poemKr = poemKr;
      target.poemEn = poemEn;
      target.description_kr = poemKr;
      target.description_en = poemEn;

      await window.ArtDatabase.saveArtwork(target);
      artworkModal.classList.remove('active');
      showToast('작품 정보가 완벽히 저장되었습니다.');
      await renderArtworks();
      loadKPIs();
    });
  }

  // 6-2. Batch Price Weight Adjustment Studio (10,000 KRW Unit Policy)
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
    if (batchPriceModal) {
      batchPriceModal.classList.add('active');
      updateBatchPreview();
    }
  }

  function closeBatchPriceModal() {
    if (batchPriceModal) batchPriceModal.classList.remove('active');
  }

  if (btnOpenBatchPrice) btnOpenBatchPrice.addEventListener('click', openBatchPriceModal);
  if (btnCloseBatchPrice) btnCloseBatchPrice.addEventListener('click', closeBatchPriceModal);
  if (btnCancelBatchPrice) btnCancelBatchPrice.addEventListener('click', closeBatchPriceModal);

  // Preset Buttons
  document.querySelectorAll('.preset-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const val = btn.getAttribute('data-val');
      if (batchMode) batchMode.value = 'multiplier';
      if (batchValueLabel) batchValueLabel.textContent = '가중치 배율 (예: 1.10 = +10%, 1.20 = +20%)';
      if (batchValue) {
        batchValue.value = val;
        updateBatchPreview();
      }
    });
  });

  if (batchMode) {
    batchMode.addEventListener('change', () => {
      if (batchMode.value === 'multiplier') {
        batchValueLabel.textContent = '가중치 배율 (예: 1.10 = +10%, 1.20 = +20%, 0.90 = -10%)';
        batchValue.value = '1.10';
        batchValue.step = '0.01';
      } else {
        batchValueLabel.textContent = '고정 가감액 (KRW, 예: 500000, -200000)';
        batchValue.value = '500000';
        batchValue.step = '10000';
      }
      updateBatchPreview();
    });
  }

  if (batchScope) batchScope.addEventListener('change', updateBatchPreview);
  if (batchValue) batchValue.addEventListener('input', updateBatchPreview);

  // Calculate new price with 10,000 KRW unit policy
  function calcNewPrice(currentPrice, mode, val) {
    let raw = currentPrice;
    if (mode === 'multiplier') {
      raw = currentPrice * parseFloat(val || 1);
    } else {
      raw = currentPrice + (parseInt(val, 10) || 0);
    }
    if (raw < 0) raw = 0;
    // 최소 10,000원 단위 반올림 정렬 (Round to 10,000 KRW)
    return Math.round(raw / 10000) * 10000;
  }

  function getTargetWorksForBatch() {
    const scope = batchScope ? batchScope.value : 'all';
    return currentArtworks.filter(art => {
      if (scope === 'all') return true;
      const cat = art.category || (art.series && art.series.includes('Quad') ? 'modular' : art.series && art.series.includes('Duo') ? 'duo' : 'master');
      return cat === scope;
    });
  }

  function updateBatchPreview() {
    if (!batchPreviewBody) return;
    const targets = getTargetWorksForBatch();
    const mode = batchMode ? batchMode.value : 'multiplier';
    const val = batchValue ? batchValue.value : '1.10';

    if (batchAffectedCount) {
      batchAffectedCount.textContent = `적용 대상: 총 ${targets.length}건`;
    }

    batchPreviewBody.innerHTML = '';
    const sample = targets.slice(0, 5); // Show first 5 previews

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

  // Batch Apply Execution
  if (btnApplyBatchPrice) {
    btnApplyBatchPrice.addEventListener('click', async () => {
      const targets = getTargetWorksForBatch();
      const mode = batchMode ? batchMode.value : 'multiplier';
      const val = batchValue ? batchValue.value : '1.10';

      if (targets.length === 0) {
        alert('조정할 대상 작품이 없습니다.');
        return;
      }

      const confirmMsg = `총 ${targets.length}개 작품의 소장 가격을 ${mode === 'multiplier' ? `${val}배` : `${parseInt(val, 10).toLocaleString()}원`} 가중치(10,000원 단위 정렬)로 일괄 변경하시겠습니까?`;
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

  // 7. Inquiry Ledger (Tab 2)
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
          <select class="form-control inq-status-select" data-id="${inq.id}" style="padding:4px 8px; font-size:0.8rem; width:100px;">
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
        showToast('문의 처리 상태가 변경되었습니다.');
      });
    });
  }

  // 8. Exhibitions & Statements (Tab 3)
  async function renderExhibitionsAndStatement() {
    const artist = await window.ArtDatabase.getArtistProfile();
    const titleKr = document.getElementById('statTitleKr');
    const titleEn = document.getElementById('statTitleEn');
    const bodyKr = document.getElementById('statBodyKr');
    const bodyEn = document.getElementById('statBodyEn');

    if (titleKr) titleKr.value = artist.statementTitleKr || '';
    if (titleEn) titleEn.value = artist.statementTitleEn || '';
    if (bodyKr) bodyKr.value = Array.isArray(artist.statementKr) ? artist.statementKr.join('\n\n') : (artist.statementKr || '');
    if (bodyEn) bodyEn.value = Array.isArray(artist.statementEn) ? artist.statementEn.join('\n\n') : (artist.statementEn || '');
  }

  const btnSaveStatement = document.getElementById('btnSaveStatement');
  if (btnSaveStatement) {
    btnSaveStatement.addEventListener('click', async () => {
      const statementTitleKr = document.getElementById('statTitleKr').value.trim();
      const statementTitleEn = document.getElementById('statTitleEn').value.trim();
      const statementKr = document.getElementById('statBodyKr').value.split('\n\n').filter(Boolean);
      const statementEn = document.getElementById('statBodyEn').value.split('\n\n').filter(Boolean);

      await window.ArtDatabase.saveArtistProfile({
        statementTitleKr,
        statementTitleEn,
        statementKr,
        statementEn
      });
      showToast('작가노트가 저장되었습니다.');
    });
  }

  // 9. System & Cloud Sync (Tab 4)
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

      // Test connection
      try {
        const works = await window.ArtDatabase.getArtworks();
        showToast('Supabase Cloud 연결에 성공했습니다!');
      } catch (e) {
        alert('연결 테스트 중 오류가 발생했습니다: ' + e.message);
      }
    });
  }

  const btnExportJson = document.getElementById('btnExportJson');
  if (btnExportJson) {
    btnExportJson.addEventListener('click', async () => {
      const artworks = await window.ArtDatabase.getArtworks();
      const inquiries = await window.ArtDatabase.getInquiries();
      const profile = await window.ArtDatabase.getArtistProfile();
      const settings = await window.ArtDatabase.getSettings();

      const dump = {
        exportedAt: new Date().toISOString(),
        brand: settings,
        artist: { ...profile, artworks },
        inquiries
      };

      const blob = new Blob([JSON.stringify(dump, null, 2)], { type: 'application/json' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = `majiyoung_edition_backup_${new Date().toISOString().slice(0, 10)}.json`;
      a.click();
      showToast('데이터베이스 전체 백업 JSON이 다운로드되었습니다.');
    });
  }

  const btnResetDefault = document.getElementById('btnResetDefault');
  if (btnResetDefault) {
    btnResetDefault.addEventListener('click', async () => {
      if (confirm('모든 데이터를 초기 공장출하 상태(기본 시드 데이터 42점)로 복원하시겠습니까?')) {
        window.ArtDatabase.resetToDefaultSeed();
        showToast('초기 기본 데이터로 복원되었습니다.');
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
