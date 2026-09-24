// ========================================================
// MA JI YOUNG EDITION Application Controller (main.js)
// Dedicated Artist & Exhibition Experience
// ========================================================

document.addEventListener("DOMContentLoaded", () => {
  let currentFilter = "all";
  let wishlist = new Set();
  let cartCount = 0;

  const artist = GALLERY_DATA.artist;

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

    let items = artist.artworks;
    if (currentFilter !== "all") {
      items = items.filter(a => a.category === currentFilter);
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
      cartCount++;
      cartCountEl.textContent = cartCount;
      showToast(`'${artwork.title}'이(가) 소장 장바구니에 담겼습니다.`);
      closeModal();
    };

    modalBtnBuy.onclick = () => {
      showToast(`'${artwork.title}' 마지영 아틀리에 소장 문의 접수 페이지로 연결됩니다.`);
      closeModal();
    };

    modalOverlay.classList.add("active");
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

  // Initialize
  renderArtistProfile();
});
