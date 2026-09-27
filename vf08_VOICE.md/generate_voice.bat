@echo off
chcp 65001 > nul
echo =====================================================================
echo  [vf08_VOICE] self_tts_skill 음성 생성 엔진 실행기
echo  화자: 50대 남성 IT 디렉터 페르소나 (VOICE_MASTER 규격)
echo =====================================================================
echo.

if not exist "result" mkdir result

echo [1/2] sample_script.txt 대본을 바탕으로 음성 생성을 시작합니다...
python src\self_tts_engine.py --file sample_script.txt --output result\sample_generated.mp3

echo.
echo =====================================================================
echo [2/2] 음성 생성이 완료되었습니다!
echo 생성 파일: result\sample_generated.mp3
echo =====================================================================
pause
