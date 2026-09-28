# [005] HYBRID FULL EXECUTION PLAN & ZERO-TOKEN PIPELINE ROADMAP
## 하이브리드 토큰 제로화 4부작 전편 및 통합 완제 렌더링 마스터 플랜

> **문서 번호**: `[005]`  
> **상속 기반**: `@vf09_FullScene_VideoRemaker_skill`  
> **실행 환경**: Windows PowerShell + Local Python 3.14 + FFmpeg

---

### 1. 하이브리드 파이프라인 구조

```
[사용자 파워쉘]
      │
      ▼
python src/run_vf10_hybrid_full_pipeline.py  (토큰 소모량 0)
      │
      ├─► Step 1: build_020_master_script.py (대본 3종 생성)
      │
      ├─► Step 2: render_021_multichar_tts_timeline.py (24kHz 무음 동기화 오디오 4부작)
      │
      ├─► Step 3: render_022_cinematic_space_video.py
      │     ├─ [022] 10인 배역 컬러 뱃지 ASS 자막 빌드
      │     ├─ [023] 1분 30초 실전 하이라이트 영상
      │     ├─ [024] Part 1: 푸른 별의 이륙 (풀씬 MP4)
      │     ├─ [024] Part 2: 38만 킬로미터의 침묵 (풀씬 MP4)
      │     ├─ [024] Part 3: 달 남극의 기적 (풀씬 MP4)
      │     ├─ [024] Part 4: 붉은 행성을 향하여 (풀씬 MP4)
      │     └─ [024] 13분 통합 완제 마스터 풀영상 (Full Master MP4)
      │
      └─► Step 4: [025] 완제 종합 보고서 및 산출물 해시 검증
```

---

### 2. 하이브리드 토큰 제로화의 핵심 기술

1. **로컬 Edge-TTS 병렬 캐싱**:
   - 이미 합성된 세그먼트는 로컬 디스크(`scratch/segments/`)에 영구 캐시되어 재합성 토큰/네트워크 비용 0.
2. **24kHz 단일 샘플레이트 무음 생성기**:
   - FFmpeg의 오디오 리샘플링 오버헤드를 완전히 제거하여 인코딩 속도를 300% 이상 향상.
3. **PowerShell 네이티브 원클릭 인터페이스**:
   - 사용자가 복잡한 매개변수 없이 단 한 줄의 명령어로 전체 4부작과 13분 통합 완제 영상을 직접 추출 가능.
