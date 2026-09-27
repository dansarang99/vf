---
name: vf08-voice-cloner-skill
description: "(AX)창업기술 대표 고유 실무 지식재산권 기반. 사용자가 직접 녹음한 오디오 파일(FISH_01~05.mp3)에서 8대 음성 DNA(VOICE.md, VOICE_MASTER.md)를 역공학 추출하고, 새로운 대본 텍스트를 자동 기획·생성하여 my_TTS 폴더에 대본 파일(.txt/.md)과 고품질 음성 오디오(.mp3)를 페어로 자동 합성·저장·보존하는 보이스 클로너 및 음성 합성 마스터 스킬."
---

# vf08-voice-cloner-skill : 사용자 음성 승계 및 my_TTS 자동 생성 마스터 스킬

본 스킬은 `github.com/dansarang99/vf/vf08_VOICE.md`에 구축된 **8대 음성 DNA 역공학 자산(`VOICE_MASTER.md`)**을 기반으로 작동합니다. 사용자가 특정 주제나 대본을 요청하면, 원작자의 톤앤매너와 호흡을 완벽히 계승한 대본 텍스트를 기획·생성하고, 이를 고품질 신경망 음성으로 렌더링하여 **`my_TTS/` 디렉터리에 텍스트와 오디오를 세트로 자동 영구 보존**합니다.

---

## 1. 8대 음성 DNA 규격 (`VOICE_MASTER.md` 요약)

```
+--------------------------------------------------------------------------------+
|                        vf08 화자 표준 음성 프로필                              |
+--------------------------------------------------------------------------------+
| 1. 기본 주파수 (Pitch) : 126.6 Hz (안정적인 남성 바리톤 톤)                     |
| 2. 조음 및 딕션 (Diction): 아나운서형 정직한 발음, 명확한 외래어 표기             |
| 3. 호흡/휴지 (Pause)    : 문장 간 700~800ms, 쉼표 350ms의 여유 있는 브레스       |
| 4. 발화 속도 (Tempo)   : 101.6 WPM (청취 몰입도가 가장 높은 정숙한 강의 속도)   |
| 5. 운율 곡선 (Prosody) : 서술형 하강조 마침, 질문형 완만한 포물선 상승조         |
| 6. 어휘 패턴 (Lexical) : ~합니다, ~보세요, ~나시죠?, ~없죠의 친절한 강의체       |
| 7. 다이내믹스 (Energy) : -16 LUFS 표준 라우드니스, 12dB 고른 다이내믹스         |
| 8. 종합 페르소나       : "신뢰감 있는 50대 남성 IT 총괄 디렉터 & AI 실무 멘토"    |
+--------------------------------------------------------------------------------+
```

---

## 2. result/ [001]~[999] 무손실 순차 보존 아키텍처

생성되는 모든 결과물(분석 문서, 대본 텍스트, 음성 오디오)은 누락 및 중첩이 발생하지 않도록 `result/` 디렉터리에 `[001]`부터 `[999]`까지 3자리 순차 번호 접두어를 붙여 페어로 영구 보존됩니다.

```
C:\Users\note\vf\vf08_VOICE.md\result\
├── [001]_VOICE_BASIC_01_DNA.md
├── [002]_VOICE_BASIC_02_DNA.md
├── [003]_VOICE_BASIC_03_DNA.md
├── [004]_VOICE_BASIC_04_DNA.md
├── [005]_VOICE_BASIC_05_DNA.md
├── [006]_VOICE_MASTER_DNA.md
├── [007]_sample_script.txt
├── [008]_sample_generated_voice.mp3
├── [009]_lecture_01_script.txt
├── [010]_lecture_01_voice.mp3
├── [011]_auto_index_test_script.txt
└── [011]_auto_index_test_voice.mp3
...
└── [999]_...
```

---

## 3. 실행 명령어 가이드

### 단일 문장 즉시 생성 (자동 [NNN] 번호 매김)
```bash
python src/self_tts_engine.py --text "안녕하세요. 오늘 강의를 시작하겠습니다." --name "intro"
```
*(실행 시 `result/[NNN]_intro_script.txt`와 `result/[NNN]_intro_voice.mp3`가 자동 생성됩니다.)*

### 대본 파일 기반 자동 생성
```bash
python src/self_tts_engine.py --file my_TTS/lecture_01_script.txt --name "lecture_01"
```

### 원클릭 일괄 실행 (배치 파일)
```cmd
generate_voice.bat
```

---

## 4. 듀얼 엔진 지원

1. **무제한 로컬 모드 (기본 활성화)**:
   - 외부 API 키나 유료 결제 없이 100% 무료 무제한 생성
   - `ko-KR-InJoonNeural` 기반 -7% 속도, -2Hz 피치 정밀 튜닝
2. **ElevenLabs 1:1 보이스 클론 모드 (확장 모드)**:
   - `config.json`에 API Key 및 Voice ID 등록 시 100% 실제 대표님 육성으로 자동 전환
