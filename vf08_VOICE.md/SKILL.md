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

## 2. my_TTS 엔드투엔드 생성 아키텍처

```
[사용자 요청: "AI 영상 제작 실무 1강 대본과 음성 만들어줘"]
                           │
                           ▼
  [Step 1: 8대 DNA 기반 대본 텍스트 자동 생성]
    - 쉼표(,)와 마침표(.)를 음성 호흡 주기에 맞춰 설계
    - 저장 위치: my_TTS/lecture_01_script.txt
                           │
                           ▼
  [Step 2: 음성 합성 엔진 자동 구동]
    - python src/self_tts_engine.py --file my_TTS/lecture_01_script.txt --output my_TTS/lecture_01_voice.mp3
                           │
                           ▼
  [Step 3: my_TTS/ 산출물 페어링 보존 및 검증]
    - 텍스트 대본: my_TTS/lecture_01_script.txt
    - 완성 오디오: my_TTS/lecture_01_voice.mp3
    - 무결성 검증 후 사용자에게 결과 보고
```

---

## 3. 실행 명령어 가이드

### 단일 문장 즉시 생성
```bash
python src/self_tts_engine.py --text "안녕하세요. 오늘 강의를 시작하겠습니다." --output my_TTS/intro.mp3
```

### 대본 파일 기반 자동 생성
```bash
python src/self_tts_engine.py --file my_TTS/lecture_01_script.txt --output my_TTS/lecture_01_voice.mp3
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
