# vf08_VOICE.md : VOICE_CLONER_SKILL & my_TTS 음성 파이프라인

본 디렉터리는 사용자가 직접 녹음한 음성 파일(`FISH_01` ~ `FISH_05.mp3`)로부터 **8대 음성 DNA(VOICE.md)**를 정밀 역공학 추출하고, 새로운 대본 텍스트를 기획·생성하여 `my_TTS` 폴더에 텍스트와 고품질 음성 오디오를 영구 보존하는 마스터 파이프라인입니다.

---

## 1. 주요 구성 파일

- `SKILL.md` : Antigravity 정식 스킬 규격서
- `VOICE_BASIC_01.md` ~ `05.md` : 5개 원천 음성 클립별 8대 DNA 분석서
- `VOICE_MASTER.md` : 5개 음성 통합 표준 음성 프로필
- `my_TTS/` : 사용자가 생성한 텍스트 대본 및 완성된 음성(mp3) 저장소
  - `lecture_01_script.txt` : AI 영상 제작 1강 대본
  - `lecture_01_voice.mp3` : 로컬 무제한 엔진으로 합성된 1강 오디오
- `src/self_tts_engine.py` : 무제한 로컬 신경망 + ElevenLabs 1:1 보이스 클론 듀얼 엔진
- `src/create_clone_voice.py` : ElevenLabs 1:1 보이스 클론 모델 등록기
- `generate_voice.bat` : 원클릭 음성 생성 배치 파일

---

## 2. 사용법

```bash
# 대본 파일을 my_TTS 오디오로 변환
python src/self_tts_engine.py --file my_TTS/lecture_01_script.txt --output my_TTS/lecture_01_voice.mp3
```
