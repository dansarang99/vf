# DATA&EDA.md 추출 및 작성 표준 규격
## (Quantitative Metrics, Statistical Modeling & EDA Visualization Framework)

> **목적**: 슬라이드 및 비즈니스 백서에 포함되는 모든 정량적 통계, 시계열 전망, 시뮬레이션 지표, 기술통계, 상관분석 결과물을 20년차 데이터 사이언티스트 수준의 통계적 엄밀성으로 규격화하기 위함.

---

## 1. 4대 정량 분석 계층 (4-Tier Analytical Framework)

1. **거시 시장 시계열 분석 (Macro Time-Series Forecast)**:
   - 지표: 글로벌 시장 규모($B), 연평균 성장률(CAGR), 누적 보급 대수(대), 점유율(%)
   - 모형: 지수 성장 곡선 모형(Exponential Growth Model) 및 시장 침투율 S-Curve
2. **엔지니어링 벤치마크 (Hardware & Engineering Metrics)**:
   - 지표: 가반하중(Payload, kg), 자유도(DoF), 파지력(Grip Force, kg), 배터리 연속 가동(h), 가동률(%)
   - 모형: ISO 18646-1 로봇 하드웨어 성능 평가 국제 규격
3. **공정 및 운영 경제성 (Operational Efficiency & OPEX)**:
   - 지표: 종합설비효율(OEE, %), 예지보전 다운타임(MTTR/MTBF), 불량률(PPM), 데이터센터 PUE
   - 모형: 험프리-라이트 82% 학습 곡선(Wright's Law) 및 연간 전력비용 절감 모델
4. **거시경제 파급효과 및 정책 세제 (Macroeconomic & Tax Modeling)**:
   - 지표: 생산유발액(조 원), 부가가치유발액(조 원), 취업유발인원(명), 지역 GRDP 순증률(%), 세제감면액(억 원)
   - 모형: 한국은행 산업연관표 투입산출모형(I-O Model), 프로젝트 내부수익률(IRR), 투자회수기간(Payback Period)

---

## 2. 300 DPI 고해상도 시각화 차트 렌더링 규격

- **해상도**: 가로 3000px × 세로 1500px (10인치 × 5인치, 300 DPI)
- **차트 스타일**:
  - 배경: 퓨어 화이트 (`#FFFFFF`)
  - 그리드: 라이트 슬레이트 (`#E2E8F0`, 투명도 0.6, 점선)
  - 주 데이터 계열: 세룰리안 블루 (`#0785C0`), 에메랄드 제이드 (`#0D7C5B`), 앰버 골드 (`#D97706`)
  - 한글 폰트: `koreanize-matplotlib`를 통한 맑은 고딕(Malgun Gothic) 렌더링
- **차트 내 필수 메타데이터 박스**:
  - 차트 최하단에 회색 배경 박스(`facecolor='#F8FAFC'`)로 감싼 2줄 캡션 필수 수록:
    - 1행: `[공식 1차 출처] {기관명 / 공식 통계 보고서 / 발표 연도}`
    - 2행: `[분석 모형 및 법적 근거] {적용 수학 모형 / 관련 법률 조항 및 국제 표준}`
