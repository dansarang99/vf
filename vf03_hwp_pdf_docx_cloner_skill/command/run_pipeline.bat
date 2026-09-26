@echo off
chcp 65001 > nul
echo ==============================================================================
echo [vf03] HWP / PDF to DOCX 100%% Zero-Loss Conversion Pipeline
echo Copyright (c) (AX)창업기술 이한규 대표. All Rights Reserved.
echo ==============================================================================
echo.

if "%~1"=="" (
    echo [사용법]
    echo   run_pipeline.bat ^<입력문서경로(HWP, PDF, DOCX)^> [대상사명] [신규문서접두어]
    echo.
    echo [예시]
    echo   run_pipeline.bat input.hwp "(AX)창업기술" "AX-"
    echo   run_pipeline.bat input.pdf "(AX)창업기술" "AX-"
    echo.
    pause
    exit /b 1
)

python "%~dp0..\scripts\master_doc_cloner.py" %*

echo.
echo [완료] 작업이 성공적으로 완료되었습니다. result 폴더를 확인하세요.
pause
