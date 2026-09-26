// ========================================================
// MA JI YOUNG EDITION Application Controller (main.js)
// Dedicated Artist & Exhibition Experience
// ========================================================

document.addEventListener("DOMContentLoaded", async () => {
  let currentFilter = "all";
  let wishlist = new Set();
  let cartCount = 0;

  // Hybrid Database Integration
  let currentArtworks = [];
  let currentArtist = (typeof GALLERY_DATA !== 'undefined' ? GALLERY_DATA.artist : {});
  
  if (window.ArtDatabase) {
    try {
      currentArtworks = await window.ArtDatabase.getArtworks();
      const profile = await window.ArtDatabase.getArtistProfile();
      if (profile && profile.nameKr) currentArtist = { ...currentArtist, ...profile };
    } catch (e) {
      console.warn("DB load fallback:", e);
      currentArtworks = currentArtist.artworks || [];
    }
  } else if (typeof GALLERY_DATA !== 'undefined') {
    currentArtworks = GALLERY_DATA.artist.artworks || [];
  }

  const artist = currentArtist;

  // DOM Elements
  const artistKrEl = document.getElementById("artist-name-kr");
  const artistEnEl = document.getElementById("artist-name-en");
  const artistPhotoEl = document.getElementById("artist-photo");
  const artistConnectsEl = document.getElementById("artist-connects");
  const statementBadgeEl = document.getElementById("statement-badge");
  const statementTitleEl = document.getElementById("statement-title");
  const statementBodyEl = document.getElementById("statement-body");
  const readMoreBtn = document.getElementById("read-more-btn");
  const artworksListEl = document.getElementById("artworks-grid");
  const filterTabsEl = document.getElementById("category-filters");
  const exhibitionListEl = document.getElementById("exhibition-grid");
  const storiesListEl = document.getElementById("stories-grid");
  const cartCountEl = document.getElementById("cart-count-badge");
  const toastEl = document.getElementById("toast-msg");

  // Search Elements
  const searchInput = document.getElementById("top-search-input");
  const searchLayer = document.getElementById("search-layer");
  const keywordTagsEl = document.getElementById("keyword-tags");
  const searchArtistListEl = document.getElementById("search-artist-list");

  // Artwork Modal Elements
  const modalOverlay = document.getElementById("artwork-modal");
  const modalCloseBtn = document.getElementById("modal-close-btn");
  const modalImg = document.getElementById("modal-img");
  const modalArtist = document.getElementById("modal-artist");
  const modalTitle = document.getElementById("modal-title");
  const modalSubTitle = document.getElementById("modal-subtitle");
  const modalPoemKr = document.getElementById("modal-poem-kr");
  const modalPoemEn = document.getElementById("modal-poem-en");
  const modalPoemBox = document.getElementById("modal-poem-box");
  const modalMedium = document.getElementById("modal-medium");
  const modalSize = document.getElementById("modal-size");
  const modalBadge = document.getElementById("modal-badge");
  const modalPrice = document.getElementById("modal-price");
  const modalBtnCart = document.getElementById("modal-btn-cart");
  const modalBtnBuy = document.getElementById("modal-btn-buy");

  // Exhibition Modal Elements
  const exbModalOverlay = document.getElementById("exb-modal");
  const exbModalCloseBtn = document.getElementById("exb-modal-close-btn");
  const exbModalImg = document.getElementById("exb-modal-img");
  const exbModalTitle = document.getElementById("exb-modal-title");
  const exbModalVenue = document.getElementById("exb-modal-venue");
  const exbModalDate = document.getElementById("exb-modal-date");
  const exbModalDesc = document.getElementById("exb-modal-desc");

  // Show Toast
  function showToast(msg) {
    if (!toastEl) return;
    toastEl.textContent = msg;
    toastEl.classList.add("show");
    setTimeout(() => {
      toastEl.classList.remove("show");
    }, 2400);
  }

  // Render Artist Profile & Statement
  function renderArtistProfile() {
    artistKrEl.textContent = artist.nameKr;
    artistEnEl.textContent = artist.nameEn;
    artistPhotoEl.src = artist.photo;
    artistPhotoEl.alt = `${artist.nameKr} 작가 사진`;

    // Connects
    artistConnectsEl.innerHTML = "";
    artist.connects.forEach(c => {
      const li = document.createElement("li");
      const a = document.createElement("a");
      a.href = c.url;
      a.textContent = c.label;
      if (c.url.startsWith("http")) {
        a.target = "_blank";
        a.rel = "noopener noreferrer";
      } else if (c.url.startsWith("#")) {
        a.addEventListener("click", (e) => {
          e.preventDefault();
          const target = document.querySelector(c.url);
          if (target) target.scrollIntoView({ behavior: "smooth" });
        });
      }
      li.appendChild(a);
      artistConnectsEl.appendChild(li);
    });

    // Statement Header & Badge
    statementBadgeEl.textContent = artist.category;
    statementTitleEl.textContent = artist.statementTitleKr;

    // Statement Body (KR + EN)
    statementBodyEl.innerHTML = "";
    statementBodyEl.classList.remove("expanded");
    readMoreBtn.textContent = "Read More";

    artist.statementKr.forEach(pText => {
      const p = document.createElement("p");
      p.textContent = pText;
      statementBodyEl.appendChild(p);
    });

    if (artist.statementEn && artist.statementEn.length > 0) {
      const divP = document.createElement("p");
      divP.className = "lang-divider";
      divP.textContent = `— English Statement: ${artist.statementTitleEn || ""}`;
      statementBodyEl.appendChild(divP);

      artist.statementEn.forEach(pText => {
        const p = document.createElement("p");
        p.textContent = pText;
        statementBodyEl.appendChild(p);
      });
    }

    renderFilterTabs();
    renderArtworks();
    renderExhibitions();
    renderStories();
  }

  // Render Filter Tabs
  function renderFilterTabs() {
    if (!filterTabsEl) return;
    filterTabsEl.innerHTML = "";
    currentFilter = "all";

    const filters = [
      { id: "all", label: "전체 작품 (All Artworks)" },
      { id: "master", label: "대표작 (Moments 26-001~010)" },
      { id: "modular", label: "4연작 모듈 세트 (011~034)" },
      { id: "duo", label: "2연작 듀오 블록 (035~042)" }
    ];

    filters.forEach(f => {
      const btn = document.createElement("button");
      btn.textContent = f.label;
      btn.className = f.id === "all" ? "active" : "";
      btn.addEventListener("click", () => {
        document.querySelectorAll(".category-filter-tabs button").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        currentFilter = f.id;
        renderArtworks();
      });
      filterTabsEl.appendChild(btn);
    });
  }

  // Render Artworks Grid
  function renderArtworks(searchTerm = "") {
    if (!artworksListEl) return;
    artworksListEl.innerHTML = "";

    let items = currentArtworks.filter(a => (a.status || 'available') !== 'private');
    if (currentFilter !== "all") {
      items = items.filter(a => {
        const cat = a.category || (a.series && a.series.includes('Quad') ? 'modular' : a.series && a.series.includes('Duo') ? 'duo' : 'master');
        return cat === currentFilter;
      });
    }

    if (searchTerm) {
      const q = searchTerm.toLowerCase();
      items = items.filter(a =>
        a.title.toLowerCase().includes(q) ||
        (a.subTitle && a.subTitle.toLowerCase().includes(q)) ||
        (a.subTitleEn && a.subTitleEn.toLowerCase().includes(q)) ||
        (a.poemKr && a.poemKr.toLowerCase().includes(q))
      );
    }

    if (items.length === 0) {
      artworksListEl.innerHTML = `<li style="grid-column: 1 / -1; text-align: center; padding: 60px 0; color: #888;">검색 조건에 일치하는 작품이 없습니다.</li>`;
      return;
    }

    items.forEach(artwork => {
      const li = document.createElement("li");

      // Image Container
      const imgBox = document.createElement("div");
      imgBox.className = "img";
      const img = document.createElement("img");
      img.src = artwork.image;
      img.alt = artwork.title;
      img.loading = "eager";
      imgBox.appendChild(img);

      // Hover preview note
      if (artwork.subTitle || artwork.subTitleEn) {
        const preview = document.createElement("div");
        preview.className = "hover-curator-preview";
        preview.innerHTML = `<strong>${artwork.subTitle || artwork.title}</strong><br><span style="opacity:0.85;">클릭하여 시적 큐레이션 및 상세 감상</span>`;
        imgBox.appendChild(preview);
      }

      imgBox.addEventListener("click", () => openArtworkModal(artwork));

      // Info Container
      const infoBox = document.createElement("div");
      infoBox.className = "info";

      // Artist line with heart
      const nameP = document.createElement("p");
      nameP.className = "name";

      const artistLink = document.createElement("span");
      artistLink.className = "artist-link";
      artistLink.innerHTML = `<img src="${artist.photo}" alt="${artist.nameEn}"> <span>${artist.nameEn}</span>`;

      const heartBtn = document.createElement("button");
      heartBtn.className = `heart-btn ${wishlist.has(artwork.id) ? "on" : ""}`;
      heartBtn.title = "관심 작품 담기";
      heartBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        if (wishlist.has(artwork.id)) {
          wishlist.delete(artwork.id);
          heartBtn.classList.remove("on");
          showToast(`'${artwork.title}' 관심 작품에서 제외되었습니다.`);
        } else {
          wishlist.add(artwork.id);
          heartBtn.classList.add("on");
          showToast(`'${artwork.title}' 관심 작품에 추가되었습니다.`);
        }
      });

      nameP.appendChild(artistLink);
      nameP.appendChild(heartBtn);
      infoBox.appendChild(nameP);

      // Title
      const titP = document.createElement("p");
      titP.className = "tit";
      titP.textContent = artwork.title;
      titP.addEventListener("click", () => openArtworkModal(artwork));
      infoBox.appendChild(titP);

      // Subtitle if available
      if (artwork.subTitle) {
        const subP = document.createElement("p");
        subP.className = "sub-tit";
        subP.textContent = `《${artwork.subTitle}》 ${artwork.subTitleEn ? `(${artwork.subTitleEn})` : ""}`;
        infoBox.appendChild(subP);
      }

      // Size
      const sizeP = document.createElement("p");
      sizeP.className = "size";
      sizeP.textContent = artwork.size;
      infoBox.appendChild(sizeP);

      // Price
      const priceP = document.createElement("p");
      priceP.className = "price";
      priceP.textContent = `₩ ${artwork.price}`;
      infoBox.appendChild(priceP);

      // Badge
      const badgeDiv = document.createElement("div");
      badgeDiv.className = `badge-type ${artwork.badge}`;
      badgeDiv.textContent = artwork.badge;
      infoBox.appendChild(badgeDiv);

      // Direct Action Buttons: [🛒 장바구니 담기] & [소장 구매]
      const actionRow = document.createElement("div");
      actionRow.className = "card-action-row";
      actionRow.style.cssText = "display: flex; gap: 6px; margin-top: 10px;";
      actionRow.innerHTML = `
        <button type="button" class="btn-card-cart" style="flex: 1; padding: 7px 8px; background: #fff; border: 1px solid #222; color: #111; border-radius: 4px; font-size: 0.76rem; font-weight: 700; cursor: pointer; display: inline-flex; align-items: center; justify-content: center; gap: 4px; transition: all 0.2s;" title="장바구니 담기">
          🛒 장바구니
        </button>
        <button type="button" class="btn-card-buy" style="flex: 1; padding: 7px 8px; background: #111; border: 1px solid #111; color: #fff; border-radius: 4px; font-size: 0.76rem; font-weight: 700; cursor: pointer; display: inline-flex; align-items: center; justify-content: center; transition: all 0.2s;" title="즉시 주문 결제">
          소장 구매
        </button>
      `;

      actionRow.querySelector(".btn-card-cart").onclick = (e) => {
        e.stopPropagation();
        if (window.firebaseEngine) {
          window.firebaseEngine.addToCart(artwork, 1);
          updateHeaderCartBadge();
        }
        showToast(`'${artwork.title}'이(가) 소장 장바구니에 담겼습니다.`);
      };

      actionRow.querySelector(".btn-card-buy").onclick = (e) => {
        e.stopPropagation();
        if (window.firebaseEngine) {
          window.firebaseEngine.addToCart(artwork, 1);
          updateHeaderCartBadge();
          openCheckoutModal();
        }
      };

      infoBox.appendChild(actionRow);

      li.appendChild(imgBox);
      li.appendChild(infoBox);
      artworksListEl.appendChild(li);
    });
  }

  // Render Exhibitions
  function renderExhibitions() {
    if (!exhibitionListEl) return;
    exhibitionListEl.innerHTML = "";
    artist.exhibitions.forEach(exb => {
      const li = document.createElement("li");

      const imgBox = document.createElement("div");
      imgBox.className = "exb-img-box";
      const img = document.createElement("img");
      img.src = exb.image;
      img.alt = exb.title;
      imgBox.appendChild(img);

      const titP = document.createElement("p");
      titP.className = "tit";
      titP.textContent = exb.title;

      const dateP = document.createElement("p");
      dateP.className = "date";
      dateP.textContent = exb.date;

      li.appendChild(imgBox);
      li.appendChild(titP);
      li.appendChild(dateP);

      if (exb.description) {
        const descP = document.createElement("p");
        descP.className = "desc";
        descP.textContent = exb.description;
        li.appendChild(descP);
      }

      li.addEventListener("click", () => openExhibitionModal(exb));
      exhibitionListEl.appendChild(li);
    });
  }

  // Render Stories
  function renderStories() {
    if (!storiesListEl) return;
    storiesListEl.innerHTML = "";
    artist.stories.forEach(story => {
      const li = document.createElement("li");

      const imgBox = document.createElement("div");
      imgBox.className = "exb-img-box";
      const img = document.createElement("img");
      img.src = story.image;
      img.alt = story.title;
      imgBox.appendChild(img);

      const titP = document.createElement("p");
      titP.className = "tit";
      titP.textContent = story.title;

      const dateP = document.createElement("p");
      dateP.className = "date";
      dateP.textContent = story.date;

      li.appendChild(imgBox);
      li.appendChild(titP);
      li.appendChild(dateP);

      if (story.summary) {
        const descP = document.createElement("p");
        descP.className = "desc";
        descP.textContent = story.summary;
        li.appendChild(descP);
      }

      storiesListEl.appendChild(li);
    });
  }

  // Artwork Lightbox Modal
  function openArtworkModal(artwork) {
    modalImg.src = artwork.image;
    modalImg.alt = artwork.title;
    modalArtist.textContent = `${artist.nameKr} (${artist.nameEn}) Atelier`;
    modalTitle.textContent = artwork.title;
    modalSubTitle.textContent = artwork.subTitle ? `《${artwork.subTitle}》 ${artwork.subTitleEn || ""}` : "";

    if (artwork.poemKr) {
      modalPoemBox.style.display = "block";
      modalPoemKr.textContent = artwork.poemKr;
      modalPoemEn.textContent = artwork.poemEn || "";
    } else {
      modalPoemBox.style.display = "none";
    }

    modalMedium.textContent = artwork.medium || "mixed media on wooden Blocks";
    modalSize.textContent = artwork.size;
    modalBadge.textContent = artwork.badge;
    modalPrice.textContent = `₩ ${artwork.price}`;

    modalBtnCart.onclick = () => {
      if (window.firebaseEngine) {
        window.firebaseEngine.addToCart(artwork, 1);
        updateHeaderCartBadge();
      } else {
        cartCount++;
        cartCountEl.textContent = cartCount;
      }
      showToast(`'${artwork.title}'이(가) 소장 장바구니에 담겼습니다.`);
      closeModal();
    };

    modalBtnBuy.onclick = () => {
      closeModal();
      if (window.firebaseEngine) {
        window.firebaseEngine.addToCart(artwork, 1);
        updateHeaderCartBadge();
        openCheckoutModal();
      } else {
        openInquiryModal(artwork);
      }
    };

    modalOverlay.classList.add("active");
  }

  // Inquiry Modal Handler
  const inquiryModal = document.getElementById("inquiry-modal");
  const inqCloseBtn = document.getElementById("inquiry-modal-close-btn");
  const inqForm = document.getElementById("inquiry-form");
  const inqWorkTitle = document.getElementById("inquiry-work-title");
  const inqArtId = document.getElementById("inq-art-id");
  const inqArtCode = document.getElementById("inq-art-code");
  const inqArtTitle = document.getElementById("inq-art-title");

  function openInquiryModal(artwork) {
    if (!inquiryModal) return;
    const title = artwork.title_kr || `${artwork.title} - ${artwork.subTitle || ''}`;
    inqWorkTitle.textContent = `${title} (${artwork.size || ''}, ₩${typeof artwork.price === 'number' ? artwork.price.toLocaleString('ko-KR') : artwork.price})`;
    inqArtId.value = artwork.id;
    inqArtCode.value = artwork.code || artwork.title;
    inqArtTitle.value = title;
    inquiryModal.classList.add("active");
  }

  function closeInquiryModal() {
    if (inquiryModal) inquiryModal.classList.remove("active");
  }

  if (inqCloseBtn) inqCloseBtn.onclick = closeInquiryModal;
  if (inquiryModal) {
    inquiryModal.onclick = (e) => {
      if (e.target === inquiryModal) closeInquiryModal();
    };
  }

  if (inqForm) {
    inqForm.onsubmit = async (e) => {
      e.preventDefault();
      const payload = {
        artwork_id: inqArtId.value,
        artwork_code: inqArtCode.value,
        artwork_title: inqArtTitle.value,
        client_name: document.getElementById("inq-name").value.trim(),
        client_phone: document.getElementById("inq-phone").value.trim(),
        client_email: document.getElementById("inq-email").value.trim(),
        message: document.getElementById("inq-message").value.trim()
      };

      if (window.ArtDatabase) {
        await window.ArtDatabase.submitInquiry(payload);
      }
      closeInquiryModal();
      inqForm.reset();
      showToast(`'${payload.artwork_code}' 소장 문의가 정식 접수되었습니다. 담당 큐레이터가 곧 연락드리겠습니다.`);
    };
  }

  function closeModal() {
    modalOverlay.classList.remove("active");
  }

  if (modalCloseBtn) modalCloseBtn.onclick = closeModal;
  if (modalOverlay) {
    modalOverlay.onclick = (e) => {
      if (e.target === modalOverlay) closeModal();
    };
  }

  // Exhibition Modal
  function openExhibitionModal(exb) {
    if (!exbModalOverlay) return;
    exbModalImg.src = exb.image;
    exbModalTitle.textContent = exb.title;
    exbModalDate.textContent = exb.date;

    const museumUrl = exb.venueUrl || "http://jbmuseum.or.kr/bbs/board.php?bo_table=b_01&wr_id=122&sfl=wr_4&stx=%EC%A0%84%EC%A3%BC&sop=and";
    exbModalVenue.innerHTML = `<a href="${museumUrl}" target="_blank" rel="noopener noreferrer" style="color: #FA5A50; text-decoration: underline;">${exb.venue || "청목 미술관 (Cheongmok Museum of Art)"} ↗</a>`;

    exbModalDesc.innerHTML = `
      <p style="margin-bottom: 24px; line-height: 1.8;">${exb.description || "마지영 개인전 《Moments》 공식 전시 정보입니다."}</p>
      <div style="text-align: center; margin-top: 25px; padding-top: 20px; border-top: 1px dashed #e0e0e0;">
        <a href="${museumUrl}" target="_blank" rel="noopener noreferrer" style="display: inline-flex; align-items: center; gap: 8px; background: #111; color: #fff; padding: 12px 28px; border-radius: 4px; font-weight: 500; font-size: 0.938rem; text-decoration: none; transition: background 0.2s;" onmouseover="this.style.background='#333'" onmouseout="this.style.background='#111'">
          청목미술관 공식 전시 안내 웹페이지 방문 ↗
        </a>
      </div>
    `;
    exbModalOverlay.classList.add("active");
  }

  function closeExbModal() {
    if (exbModalOverlay) exbModalOverlay.classList.remove("active");
  }

  if (exbModalCloseBtn) exbModalCloseBtn.onclick = closeExbModal;
  if (exbModalOverlay) {
    exbModalOverlay.onclick = (e) => {
      if (e.target === exbModalOverlay) closeExbModal();
    };
  }

  // Read More / Less Toggle
  if (readMoreBtn) {
    readMoreBtn.addEventListener("click", () => {
      const isExpanded = statementBodyEl.classList.toggle("expanded");
      readMoreBtn.textContent = isExpanded ? "Less" : "Read More";
    });
  }

  // Search Logic
  if (keywordTagsEl) {
    keywordTagsEl.innerHTML = "";
    GALLERY_DATA.trendingKeywords.forEach(kw => {
      const li = document.createElement("li");
      const a = document.createElement("a");
      a.href = "#";
      a.textContent = kw;
      a.addEventListener("click", (e) => {
        e.preventDefault();
        searchInput.value = kw;
        executeSearch(kw);
      });
      li.appendChild(a);
      keywordTagsEl.appendChild(li);
    });
  }

  if (searchArtistListEl) {
    searchArtistListEl.innerHTML = "";
    GALLERY_DATA.featuredCollections.forEach(fc => {
      const li = document.createElement("li");
      li.innerHTML = `
        <img src="${fc.thumb}" alt="${fc.name}">
        <div class="info-txt">
          <span class="artist-nm">${fc.name}</span>
          <span class="artist-sub">${fc.desc}</span>
        </div>
      `;
      li.addEventListener("click", () => {
        currentFilter = fc.id;
        document.querySelectorAll(".category-filter-tabs button").forEach(b => {
          b.classList.toggle("active", b.textContent.includes(fc.name) || (fc.id === "master" && b.textContent.includes("대표작")));
        });
        renderArtworks();
        searchLayer.classList.remove("is-open");
        const artSec = document.getElementById("artworks-section");
        if (artSec) artSec.scrollIntoView({ behavior: "smooth" });
      });
      searchArtistListEl.appendChild(li);
    });
  }

  function executeSearch(query) {
    const q = query.trim().toLowerCase();
    if (!q) return;

    renderArtworks(q);
    showToast(`'${query}' 검색 결과로 작품 목록을 필터링했습니다.`);
    searchLayer.classList.remove("is-open");

    const artSec = document.getElementById("artworks-section");
    if (artSec) artSec.scrollIntoView({ behavior: "smooth" });
  }

  if (searchInput) {
    searchInput.addEventListener("focus", () => {
      searchLayer.classList.add("is-open");
    });
    searchInput.addEventListener("input", (e) => {
      renderArtworks(e.target.value);
    });
    searchInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        executeSearch(searchInput.value);
      }
    });
  }

  document.addEventListener("click", (e) => {
    if (searchLayer && !searchLayer.contains(e.target) && e.target !== searchInput) {
      searchLayer.classList.remove("is-open");
    }
  });

  // Top Banner Close
  const bannerCloseBtn = document.querySelector(".top-banner-close-button");
  const topBanner = document.getElementById("glaobalTopBanner");
  if (bannerCloseBtn && topBanner) {
    bannerCloseBtn.addEventListener("click", () => {
      topBanner.classList.add("is-hidden");
    });
  }

  // Header Scroll Effect
  const header = document.getElementById("header");
  window.addEventListener("scroll", () => {
    if (window.scrollY > 30) {
      header.classList.add("scrolled");
    } else {
      header.classList.remove("scrolled");
    }
  });

  // Keybindings (Escape to close modals)
  window.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      closeModal();
      closeExbModal();
      if (searchLayer) searchLayer.classList.remove("is-open");
    }
  });

  // Series Quick Switcher Buttons
  const seriesSwitchBtns = document.querySelectorAll(".artist-switch-btn");
  seriesSwitchBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      const filterId = btn.getAttribute("data-filter");
      if (!filterId) return;
      currentFilter = filterId;

      // Update active states
      seriesSwitchBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

      // Sync category tabs
      if (filterTabsEl) {
        const tabBtns = filterTabsEl.querySelectorAll("button");
        tabBtns.forEach(tb => {
          if (filterId === "all" && tb.textContent.includes("전체")) {
            tb.classList.add("active");
          } else if (filterId === "master" && tb.textContent.includes("대표작")) {
            tb.classList.add("active");
          } else if (filterId === "modular" && tb.textContent.includes("4연작")) {
            tb.classList.add("active");
          } else if (filterId === "duo" && tb.textContent.includes("2연작")) {
            tb.classList.add("active");
          } else {
            tb.classList.remove("active");
          }
        });
      }

      renderArtworks();
      const artSec = document.getElementById("artworks-section");
      if (artSec) {
        artSec.scrollIntoView({ behavior: "smooth" });
      }
    });
  });

  // ============================================================
  // FIREBASE E-COMMERCE SUITE (Auth, Cart, Checkout, Orders)
  // ============================================================
  
  // 1. Header Auth & Cart State
  const headerAuthSection = document.getElementById("header-auth-section");
  const cartBadge = document.getElementById("cart-count-badge");
  const btnHeaderCart = document.getElementById("btn-header-cart");

  function updateHeaderCartBadge() {
    if (window.firebaseEngine) {
      const count = window.firebaseEngine.getCartCount();
      const badge = document.getElementById("cart-count-badge");
      if (badge) badge.textContent = count;
      const floatBadge = document.getElementById("floating-cart-count");
      if (floatBadge) floatBadge.textContent = count;
      cartCount = count;
    }
  }

  function renderHeaderAuth(user) {
    if (!headerAuthSection) return;
    updateHeaderCartBadge();

    if (user) {
      headerAuthSection.innerHTML = `
        <li style="margin-right: 8px;">
          <span class="collector-user-badge" id="btn-header-profile" title="마이페이지 / 컬렉터 정보">
            👑 ${user.name} 컬렉터님
          </span>
        </li>
        <li style="margin-right: 8px;">
          <a href="#orders" class="auth-nav-link" id="btn-header-my-orders">주문내역</a>
        </li>
        <li style="margin-right: 12px;">
          <a href="#logout" class="auth-nav-link" id="btn-header-logout" style="color:#888;">로그아웃</a>
        </li>
        <li>
          <a href="#cart" class="cart" id="btn-header-cart" title="소장 장바구니" style="display:inline-flex; align-items:center; gap:5px; cursor:pointer;">
            <span class="cart-label" style="font-weight:600; font-size:0.813rem; color:#222;">장바구니</span>
            <span class="cart-count" id="cart-count-badge">${window.firebaseEngine ? window.firebaseEngine.getCartCount() : 0}</span>
          </a>
        </li>
      `;

      const btnProfile = document.getElementById("btn-header-profile");
      const btnOrders = document.getElementById("btn-header-my-orders");
      const btnLogout = document.getElementById("btn-header-logout");
      const btnCart = document.getElementById("btn-header-cart");

      if (btnProfile) btnProfile.onclick = () => openMyOrdersModal();
      if (btnOrders) btnOrders.onclick = (e) => { e.preventDefault(); openMyOrdersModal(); };
      if (btnLogout) btnLogout.onclick = async (e) => {
        e.preventDefault();
        if (confirm("로그아웃 하시겠습니까?")) {
          await window.firebaseEngine.signOut();
          showToast("안전하게 로그아웃되었습니다.");
        }
      };
      if (btnCart) btnCart.onclick = (e) => { e.preventDefault(); openCartModal(); };
    } else {
      headerAuthSection.innerHTML = `
        <li style="margin-right: 8px;"><a href="#login" class="auth-nav-link" id="btn-header-login">로그인</a></li>
        <li style="margin-right: 12px;"><a href="#signup" class="auth-nav-link" id="btn-header-signup">회원가입</a></li>
        <li>
          <a href="#cart" class="cart" id="btn-header-cart" title="소장 장바구니" style="display:inline-flex; align-items:center; gap:5px; cursor:pointer;">
            <span class="cart-label" style="font-weight:600; font-size:0.813rem; color:#222;">장바구니</span>
            <span class="cart-count" id="cart-count-badge">${window.firebaseEngine ? window.firebaseEngine.getCartCount() : 0}</span>
          </a>
        </li>
      `;

      const btnLogin = document.getElementById("btn-header-login");
      const btnSignup = document.getElementById("btn-header-signup");
      const btnCart = document.getElementById("btn-header-cart");

      if (btnLogin) btnLogin.onclick = (e) => { e.preventDefault(); openAuthModal('login'); };
      if (btnSignup) btnSignup.onclick = (e) => { e.preventDefault(); openAuthModal('signup'); };
      if (btnCart) btnCart.onclick = (e) => { e.preventDefault(); openCartModal(); };
    }
  }

  // 2. Auth Modal Controls
  const authModal = document.getElementById("auth-modal");
  const authCloseBtn = document.getElementById("auth-modal-close-btn");
  const tabBtnLogin = document.getElementById("tab-btn-login");
  const tabBtnSignup = document.getElementById("tab-btn-signup");
  const authViewLogin = document.getElementById("auth-view-login");
  const authViewSignup = document.getElementById("auth-view-signup");
  const formLogin = document.getElementById("form-login");
  const formSignup = document.getElementById("form-signup");
  const btnDemoLogin = document.getElementById("btn-demo-collector-login");

  function openAuthModal(mode = 'login') {
    if (!authModal) return;
    if (mode === 'signup') {
      tabBtnSignup.classList.add('active');
      tabBtnLogin.classList.remove('active');
      authViewSignup.style.display = 'block';
      authViewLogin.style.display = 'none';
    } else {
      tabBtnLogin.classList.add('active');
      tabBtnSignup.classList.remove('active');
      authViewLogin.style.display = 'block';
      authViewSignup.style.display = 'none';
    }
    authModal.classList.add("active");
  }

  function closeAuthModal() {
    if (authModal) authModal.classList.remove("active");
  }

  if (authCloseBtn) authCloseBtn.onclick = closeAuthModal;
  if (tabBtnLogin) tabBtnLogin.onclick = () => openAuthModal('login');
  if (tabBtnSignup) tabBtnSignup.onclick = () => openAuthModal('signup');

  if (btnDemoLogin) {
    btnDemoLogin.onclick = async () => {
      document.getElementById("login-email").value = "collector@majiyoung.art";
      document.getElementById("login-password").value = "1234567";
      try {
        const user = await window.firebaseEngine.signIn("collector@majiyoung.art", "1234567");
        closeAuthModal();
        showToast(`환영합니다, ${user.name} VIP 컬렉터님!`);
      } catch (err) {
        alert(err.message);
      }
    };
  }

  if (formLogin) {
    formLogin.onsubmit = async (e) => {
      e.preventDefault();
      const email = document.getElementById("login-email").value.trim();
      const pass = document.getElementById("login-password").value;
      try {
        const user = await window.firebaseEngine.signIn(email, pass);
        closeAuthModal();
        showToast(`환영합니다, ${user.name} 컬렉터님!`);
      } catch (err) {
        alert(err.message);
      }
    };
  }

  if (formSignup) {
    formSignup.onsubmit = async (e) => {
      e.preventDefault();
      const payload = {
        name: document.getElementById("signup-name").value.trim(),
        email: document.getElementById("signup-email").value.trim(),
        password: document.getElementById("signup-password").value,
        phone: document.getElementById("signup-phone").value.trim(),
        address: document.getElementById("signup-address").value.trim(),
        tier: document.getElementById("signup-tier").value
      };
      try {
        const user = await window.firebaseEngine.signUp(payload);
        closeAuthModal();
        showToast(`회원가입이 완료되었습니다! ${user.name} 컬렉터님 환영합니다.`);
      } catch (err) {
        alert(err.message);
      }
    };
  }

  // 3. Cart Modal Controls
  const cartModal = document.getElementById("cart-modal");
  const cartCloseBtn = document.getElementById("cart-modal-close-btn");
  const cartItemsContainer = document.getElementById("cart-items-container");
  const cartEmptyNotice = document.getElementById("cart-empty-notice");
  const cartSummaryBox = document.getElementById("cart-summary-box");
  const cartItemCountEl = document.getElementById("cart-summary-item-count");
  const cartSubtotalEl = document.getElementById("cart-summary-subtotal");
  const cartTotalEl = document.getElementById("cart-summary-total");
  const btnCartContinue = document.getElementById("btn-cart-continue");
  const btnCartCheckout = document.getElementById("btn-cart-proceed-checkout");

  function openCartModal() {
    if (!cartModal) return;
    renderCartModalItems();
    cartModal.classList.add("active");
  }

  function closeCartModal() {
    if (cartModal) cartModal.classList.remove("active");
  }

  function renderCartModalItems() {
    if (!cartItemsContainer) return;
    const items = window.firebaseEngine ? window.firebaseEngine.getCart() : [];
    cartItemsContainer.innerHTML = "";

    if (items.length === 0) {
      if (cartEmptyNotice) cartEmptyNotice.style.display = "block";
      if (cartSummaryBox) cartSummaryBox.style.display = "none";
      if (btnCartCheckout) {
        btnCartCheckout.disabled = true;
        btnCartCheckout.style.opacity = "0.5";
      }
      return;
    }

    if (cartEmptyNotice) cartEmptyNotice.style.display = "none";
    if (cartSummaryBox) cartSummaryBox.style.display = "block";
    if (btnCartCheckout) {
      btnCartCheckout.disabled = false;
      btnCartCheckout.style.opacity = "1";
    }

    let subtotal = 0;
    let totalCount = 0;

    items.forEach(item => {
      const priceNum = Math.round(Number(item.price) / 10000) * 10000;
      const rowTotal = priceNum * (item.quantity || 1);
      subtotal += rowTotal;
      totalCount += (item.quantity || 1);

      const row = document.createElement("div");
      row.className = "cart-item-row";
      row.innerHTML = `
        <img src="${item.image || 'assets/images/artwork_moments_26_001.png'}" alt="${item.title}" class="cart-item-thumb">
        <div class="cart-item-info">
          <div class="cart-item-title">${item.title}</div>
          <div class="cart-item-meta">${item.size || ''} ｜ ${item.medium || ''}</div>
          <div class="cart-item-price">₩ ${priceNum.toLocaleString('ko-KR')}</div>
        </div>
        <div class="cart-qty-ctrl">
          <button type="button" class="cart-qty-btn btn-dec" data-id="${item.artwork_id}">-</button>
          <span class="cart-qty-val">${item.quantity || 1}</span>
          <button type="button" class="cart-qty-btn btn-inc" data-id="${item.artwork_id}">+</button>
        </div>
        <button type="button" class="cart-item-remove btn-del" data-id="${item.artwork_id}" title="작품 삭제">×</button>
      `;

      // Event listeners for quantity and delete
      row.querySelector(".btn-dec").onclick = () => {
        window.firebaseEngine.updateCartQuantity(item.artwork_id, -1);
        renderCartModalItems();
        updateHeaderCartBadge();
      };
      row.querySelector(".btn-inc").onclick = () => {
        window.firebaseEngine.updateCartQuantity(item.artwork_id, 1);
        renderCartModalItems();
        updateHeaderCartBadge();
      };
      row.querySelector(".btn-del").onclick = () => {
        window.firebaseEngine.removeFromCart(item.artwork_id);
        renderCartModalItems();
        updateHeaderCartBadge();
      };

      cartItemsContainer.appendChild(row);
    });

    const finalSubtotal = Math.round(subtotal / 10000) * 10000;
    if (cartItemCountEl) cartItemCountEl.textContent = totalCount;
    if (cartSubtotalEl) cartSubtotalEl.textContent = `₩ ${finalSubtotal.toLocaleString('ko-KR')}`;
    if (cartTotalEl) cartTotalEl.textContent = `₩ ${finalSubtotal.toLocaleString('ko-KR')}`;
  }

  if (cartCloseBtn) cartCloseBtn.onclick = closeCartModal;
  if (btnCartContinue) btnCartContinue.onclick = closeCartModal;
  if (btnCartCheckout) {
    btnCartCheckout.onclick = () => {
      closeCartModal();
      openCheckoutModal();
    };
  }

  // 4. Checkout & Purchase Modal Controls
  const checkoutModal = document.getElementById("checkout-modal");
  const checkoutCloseBtn = document.getElementById("checkout-modal-close-btn");
  const chkItemsBrief = document.getElementById("checkout-items-brief");
  const chkSubtotalVal = document.getElementById("chk-subtotal-val");
  const chkFinalTotalVal = document.getElementById("chk-final-total-val");
  const formCheckout = document.getElementById("form-checkout");
  const paymentCards = document.querySelectorAll(".payment-method-card");
  let selectedPaymentMethod = "credit_card";

  paymentCards.forEach(card => {
    card.addEventListener("click", () => {
      paymentCards.forEach(c => c.classList.remove("selected"));
      card.classList.add("selected");
      selectedPaymentMethod = card.getAttribute("data-method");
    });
  });

  function openCheckoutModal() {
    if (!checkoutModal) return;
    const items = window.firebaseEngine ? window.firebaseEngine.getCart() : [];
    if (items.length === 0) {
      alert("주문하실 작품이 장바구니에 없습니다. 작품을 먼저 담아주세요.");
      return;
    }

    const user = window.firebaseEngine ? window.firebaseEngine.getCurrentUser() : null;
    if (user) {
      document.getElementById("chk-name").value = user.name || "";
      document.getElementById("chk-phone").value = user.phone || "";
      document.getElementById("chk-email").value = user.email || "";
      document.getElementById("chk-address").value = user.address || "";
    }

    let subtotal = 0;
    let totalCount = 0;
    items.forEach(i => {
      const p = Math.round(Number(i.price) / 10000) * 10000;
      subtotal += p * (i.quantity || 1);
      totalCount += (i.quantity || 1);
    });

    const finalTotal = Math.round(subtotal / 10000) * 10000;
    const firstTitle = items[0].title;
    const extra = items.length > 1 ? ` 외 ${items.length - 1}개 시리즈 (총 ${totalCount}점)` : ` (1점)`;

    if (chkItemsBrief) {
      chkItemsBrief.innerHTML = `<strong>주문 작품:</strong> ${firstTitle}${extra}`;
    }
    if (chkSubtotalVal) chkSubtotalVal.textContent = `₩ ${finalTotal.toLocaleString('ko-KR')}`;
    if (chkFinalTotalVal) chkFinalTotalVal.textContent = `₩ ${finalTotal.toLocaleString('ko-KR')}`;

    checkoutModal.classList.add("active");
  }

  function closeCheckoutModal() {
    if (checkoutModal) checkoutModal.classList.remove("active");
  }

  if (checkoutCloseBtn) checkoutCloseBtn.onclick = closeCheckoutModal;

  if (formCheckout) {
    formCheckout.onsubmit = async (e) => {
      e.preventDefault();
      const items = window.firebaseEngine ? window.firebaseEngine.getCart() : [];
      if (items.length === 0) {
        alert("장바구니가 비어 있습니다.");
        return;
      }

      const orderPayload = {
        items: items,
        user_name: document.getElementById("chk-name").value.trim(),
        user_phone: document.getElementById("chk-phone").value.trim(),
        user_email: document.getElementById("chk-email").value.trim(),
        shipping_address: document.getElementById("chk-address").value.trim(),
        delivery_note: document.getElementById("chk-note").value.trim(),
        payment_method: selectedPaymentMethod
      };

      try {
        const order = await window.firebaseEngine.createOrder(orderPayload);
        closeCheckoutModal();
        updateHeaderCartBadge();
        openOrderCompleteModal(order);
      } catch (err) {
        alert(err.message);
      }
    };
  }

  // 5. Order Completed Receipt Modal
  const orderCompleteModal = document.getElementById("order-complete-modal");
  const orderCompleteCloseBtn = document.getElementById("order-complete-close-btn");
  const btnGoMyOrders = document.getElementById("btn-go-my-orders");
  const btnOrderCompleteDone = document.getElementById("btn-order-complete-done");

  function openOrderCompleteModal(order) {
    if (!orderCompleteModal) return;
    document.getElementById("receipt-order-id").textContent = order.order_id;
    document.getElementById("receipt-warranty-no").textContent = order.warranty_number;
    document.getElementById("receipt-total-amount").textContent = `₩ ${order.total_amount.toLocaleString('ko-KR')}`;
    document.getElementById("receipt-address").textContent = order.shipping_address;
    orderCompleteModal.classList.add("active");
  }

  function closeOrderCompleteModal() {
    if (orderCompleteModal) orderCompleteModal.classList.remove("active");
  }

  if (orderCompleteCloseBtn) orderCompleteCloseBtn.onclick = closeOrderCompleteModal;
  if (btnOrderCompleteDone) btnOrderCompleteDone.onclick = closeOrderCompleteModal;
  if (btnGoMyOrders) {
    btnGoMyOrders.onclick = () => {
      closeOrderCompleteModal();
      openMyOrdersModal();
    };
  }

  // 6. My Orders / Collector History Modal
  const myOrdersModal = document.getElementById("my-orders-modal");
  const myOrdersCloseBtn = document.getElementById("my-orders-modal-close-btn");
  const myOrdersListContainer = document.getElementById("my-orders-list-container");
  const myOrdersUserInfo = document.getElementById("my-orders-user-info");
  const btnModalLogout = document.getElementById("btn-modal-logout");

  function openMyOrdersModal() {
    if (!myOrdersModal) return;
    renderMyOrdersList();
    myOrdersModal.classList.add("active");
  }

  function closeMyOrdersModal() {
    if (myOrdersModal) myOrdersModal.classList.remove("active");
  }

  function renderMyOrdersList() {
    if (!myOrdersListContainer) return;
    const user = window.firebaseEngine ? window.firebaseEngine.getCurrentUser() : null;
    const orders = window.firebaseEngine ? window.firebaseEngine.getOrders(user?.uid) : [];

    if (myOrdersUserInfo) {
      if (user) {
        myOrdersUserInfo.textContent = `${user.name} (${user.email}) ｜ 회원 등급: ${user.tier === 'vip' ? 'VIP 파트론' : '프라이빗 컬렉터'}`;
      } else {
        myOrdersUserInfo.textContent = "게스트 최근 소장 주문 내역입니다.";
      }
    }

    myOrdersListContainer.innerHTML = "";
    if (orders.length === 0) {
      myOrdersListContainer.innerHTML = `
        <div style="text-align:center; padding: 40px 10px; color:#888;">
          <p style="font-size:1.05rem; margin-bottom:6px;">아직 접수된 작품 소장 내역이 없습니다.</p>
          <p style="font-size:0.84rem; color:#aaa;">마지영 작가의 오리지널 작품을 장바구니에 담아 소장해보세요.</p>
        </div>
      `;
      return;
    }

    orders.forEach(order => {
      const card = document.createElement("div");
      card.style.cssText = "background:#fcfcfc; border:1px solid #eee; border-radius:8px; padding:18px; margin-bottom:14px;";

      let statusBadgeClass = "status-paid";
      if (order.order_status === "작품검수중") statusBadgeClass = "status-inspecting";
      if (order.order_status === "프라이빗배송준비" || order.order_status === "배송중") statusBadgeClass = "status-delivering";
      if (order.order_status === "소장인도완료") statusBadgeClass = "status-completed";

      const itemsHtml = order.items.map(it => `
        <div style="display:flex; justify-content:space-between; font-size:0.86rem; color:#555; margin-bottom:4px;">
          <span>• ${it.title} (${it.size || ''}) × ${it.quantity || 1}</span>
          <span style="font-weight:600;">₩ ${(Math.round(Number(it.price) / 10000) * 10000).toLocaleString('ko-KR')}</span>
        </div>
      `).join("");

      card.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #f0f0f0; padding-bottom:10px; margin-bottom:10px;">
          <div>
            <strong style="font-size:0.95rem; color:#111; font-family:monospace;">${order.order_id}</strong>
            <span style="font-size:0.78rem; color:#888; margin-left:8px;">${order.created_at ? order.created_at.substring(0, 10) : ''}</span>
          </div>
          <span class="order-status-badge ${statusBadgeClass}">${order.order_status}</span>
        </div>
        <div style="margin-bottom:12px;">${itemsHtml}</div>
        <div style="display:flex; justify-content:space-between; align-items:center; border-top:1px dashed #e5e5e5; padding-top:10px; font-size:0.86rem;">
          <span style="color:#777;">보증서 번호: <strong style="color:#FA5A50; font-family:monospace;">${order.warranty_number || '발급준비'}</strong></span>
          <strong style="font-size:1.05rem; color:#111;">총액 ₩ ${Number(order.total_amount).toLocaleString('ko-KR')}</strong>
        </div>
      `;
      myOrdersListContainer.appendChild(card);
    });
  }

  if (myOrdersCloseBtn) myOrdersCloseBtn.onclick = closeMyOrdersModal;
  if (btnModalLogout) {
    btnModalLogout.onclick = async () => {
      await window.firebaseEngine.signOut();
      closeMyOrdersModal();
      showToast("안전하게 로그아웃되었습니다.");
    };
  }

  // Subscribe to Auth changes
  if (window.firebaseEngine) {
    window.firebaseEngine.onAuthStateChanged((user) => {
      renderHeaderAuth(user);
    });
  }

  // Window cart updated listener
  window.addEventListener("mjy-cart-updated", () => {
    updateHeaderCartBadge();
  });

  // Modal close on overlay background click
  [authModal, cartModal, checkoutModal, orderCompleteModal, myOrdersModal].forEach(m => {
    if (m) {
      m.addEventListener("click", (e) => {
        if (e.target === m) m.classList.remove("active");
      });
    }
  });

  // Expose global window modal controllers
  window.openAuthModal = openAuthModal;
  window.openCartModal = openCartModal;
  window.openCheckoutModal = openCheckoutModal;
  window.openMyOrdersModal = openMyOrdersModal;

  // Initialize
  renderArtistProfile();
});
