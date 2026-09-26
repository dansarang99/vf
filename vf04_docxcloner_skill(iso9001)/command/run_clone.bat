@echo off
chcp 65001 > nul
echo ========================================================
echo  [DOCX CLONER] 100%% Surgical In-Place Cloner Pipeline
echo  (AX)창업기술 이한규 대표 고유 실무 지식재산권 기반
echo ========================================================
echo.
python src\docx_cloner_engine.py
if %ERRORLEVEL% EQU 0 (
    echo.
    echo [SUCCESS] Cloned docx and verified 100%% identical layout.
) else (
    echo.
    echo [ERROR] Pipeline failed with error code %ERRORLEVEL%
)
pause
