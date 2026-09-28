@echo off
chcp 65001 > nul
title [vf10] K-Space Zero-Token Pipeline
echo ==========================================================================
echo   [vf10] AI 토큰 소비 완전 제로(Zero-Token) 원클릭 배치 실행기
echo   * 100% 로컬 연산 기반 AI 토큰 소모량: 0
echo ==========================================================================
cd /d "%~dp0"
python src\run_zero_token_master.py
pause
