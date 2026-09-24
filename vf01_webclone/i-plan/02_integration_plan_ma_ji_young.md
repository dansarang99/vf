# 02. 마지영 작가 개인전 《Moments》 웹사이트 자연 통합 설계서

**연계 파일:** `C:\Users\note\Downloads\Web_마지영전시회.pptx`  
**전시 정보:**  
* **작가:** 마지영 (MA JI YOUNG)  
* **전시명:** 《Moments: 흔들리던 순간조차 찬란했던, 기억의 유닛(Unit)》 (MA JI YOUNG SOLO EXHIBITION: Moments)  
* **일시:** 2026. 10. 13. ~ 10. 18.  
* **장소:** 청목 미술관 (Cheongmok Museum of Art)  
* **소재/기법:** mixed media on wooden Blocks  

---

## 1. PPTX 슬라이드별 웹 매핑 설계 매트릭스

| 슬라이드 번호 | 원본 슬라이드 내용 | 추출 에셋 | 웹사이트 배치 컴포넌트 |
|---|---|---|---|
| **Slide 1** | 메인 전시 포스터 (청목미술관 개인전) | `image1.png` | 연계 전시(`Exhibition`) 배너 & 전시 상세 모달 |
| **Slide 2** | 작가 프로필, 국문 서문, 작가 인물/스튜디오 | `image2.png`, `image3.png` | `.artist-detail` 좌측 프로필 사진, 우측 국문 서문 |
| **Slide 3** | 영문 서문 (Units of Memory) | `image2.png`, `image3.png` | `.artist-detail` 영문 큐레이토리얼 텍스트 |
| **Slide 4** | Moments 26-001 ("바람이 머무는 곳", 67.5x40.0cm) | `image5.png` | Artworks 대표작 #1 + 시적 큐레이션 노트 |
| **Slide 5** | Moments 26-002 ("바로 지금, 여기", 17.5x27.5cm) | `image6.png` | Artworks 대표작 #2 |
| **Slide 6** | Moments 26-003 ("중심을 지키는 것", 57.5x37.5cm) | `image7.png` | Artworks 대표작 #3 |
| **Slide 7** | Moments 26-004 ("중심을 지키는 것", 30.0x16.0cm) | `image8.png` | Artworks 대표작 #4 |
| **Slide 8** | Moments 26-005 ("흐름에 맡기는 힘", 20.0x35.0cm) | `image9.png` | Artworks 대표작 #5 |
| **Slide 9** | Moments 26-006 ("무제", 27.5x27.5cm) | `image10.png` | Artworks #6 |
| **Slide 10** | Moments 26-007 ("무제", 27.5x27.5cm) | `image11.png` | Artworks #7 |
| **Slide 11** | Moments 26-008 ("무제", 27.5x27.5cm) | `image12.png` | Artworks #8 |
| **Slide 12** | Moments 26-009 ("무제", 25.0x25.0cm) | `image13.png` | Artworks #9 |
| **Slide 13** | Moments 26-010 ("무제", 25.0x25.0cm) | `image14.png` | Artworks #10 |
| **Slide 14** | Moments 26-011 ~ 014 (15.0x12.5cm each) | `image15.png`, `image16.png` | Artworks 4연작 세트 A |
| **Slide 15** | Moments 26-015 ~ 018 (15.0x12.5cm each) | `image17.png`, `image18.png` | Artworks 4연작 세트 B |
| **Slide 16** | Moments 26-019 ~ 022 (15.0x12.5cm each) | `image19.png`, `image20.png` | Artworks 4연작 세트 C |
| **Slide 17** | Moments 26-023 ~ 026 (15.0x12.5cm each) | `image21.png`, `image22.png` | Artworks 4연작 세트 D |
| **Slide 18** | Moments 26-027 ~ 030 (15.0x12.5cm each) | `image23.png`, `image24.png` | Artworks 4연작 세트 E |
| **Slide 19** | Moments 26-031 ~ 034 (15.0x12.5cm each) | `image25.png`, `image26.png` | Artworks 4연작 세트 F |
| **Slide 20** | Moments 26-035~036 (15.0x25.0cm each) | `image27.png`, `image28.png` | Artworks 2연작 듀오 A |
| **Slide 21** | Moments 26-037~038 (15.0x25.0cm each) | `image29.png`, `image30.png` | Artworks 2연작 듀오 B |
| **Slide 22** | Moments 26-039~040 (15.0x25.0cm each) | `image31.png`, `image32.png` | Artworks 2연작 듀오 C |
| **Slide 23** | Moments 26-041~042 (14.0x14.0cm each) | `image33.png`, `image34.png` | Artworks 2연작 듀오 D |
| **Slide 24** | 종합 도록 카탈로그 뷰 (Artworks Summary) | `image35.png` ~ `image40.png` | 카탈로그 뷰 모드 및 썸네일 그리드 |

---

## 2. 웹 통합의 핵심 자연스러움(Natural Integration) 4대 전략

1. **상호 교차 탐색 (Cross-Browsing System):**
   * 박서보 작가 페이지(`park-seo-bo`)와 마지영 작가 페이지(`ma-ji-young`)를 자유롭게 오갈 수 있는 상단 아티스트 셀렉터 및 GNB 메뉴 연동.
   * 실시간 검색 모달(`search-layer`)의 'Featured Artists'에 박서보와 마지영을 나란히 배치.
2. **아트앤에디션 정통 스타일시트 완벽 상속:**
   * `.sub-wrap-in`, `.artist-detail`, `.artist-info`, `.photo`, `.statement`, `.artworks-detail-bx`, `.sub-artwork-list`, `.event-bx` 등 실제 아트앤에디션 CSS 클래스명과 계층 구조를 100% 동일하게 구현.
   * `Read More` 아코디언 토글 애니메이션, 위시리스트 하트 클릭 인터랙션, 장바구니 카운트 동적 반영.
3. **고해상도 라이트박스 & 시적 큐레이션 모달 (Artwork Detail Lightbox):**
   * 슬라이드에 수록된 각 작품별 깊이 있는 시적 텍스트("삶을 통째로 뒤흔들던 거친 폭풍이 지나가고...", "어제와 내일의 소음을 걷어내고...")를 클릭 시 나타나는 작품 상세 팝업에 수록하여 단순 이커머스를 넘어선 갤러리 도록 수준의 몰입감 제공.
4. **전시회 특별관 (Cheongmok Museum Exhibition Special):**
   * 하단 `Exhibition` 섹션에 청목미술관 개인전 포스터(`image1.png`)와 함께 2026.10.13 - 10.18 일정을 배치하고, 클릭 시 전시 상세 팝업이 부드럽게 열리도록 구성.
