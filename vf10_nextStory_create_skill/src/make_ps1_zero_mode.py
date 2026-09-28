# -*- coding: utf-8 -*-
"""run_vf10_pipeline.ps1에 -Mode zero를 기본값으로 탑재하고 UTF-8 BOM으로 저장"""

ps_content = """# PowerShell Native Pipeline Runner
param(
    [ValidateSet("zero", "full", "quick", "highlight", "real", "audio_only", "status")]
    [string]$Mode = "zero"
)

# 콘솔 UTF-8 설정
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host "  [vf10] AI 토큰 소비 완전 제로(Zero-Token) PowerShell 파이프라인" -ForegroundColor Yellow
Write-Host "  * 외부 유료 LLM 호출 0회 / AI 토큰 소모량 완전 0(Zero)" -ForegroundColor Green
Write-Host "  * 100% 로컬 연산 및 NASA 공인 실제 우주 촬영 실사 에셋 결합" -ForegroundColor Green
Write-Host "  * 덮어쓰기 0% 무손실 불변 번호 체계([001]~[999]) 자동 연동" -ForegroundColor Green
Write-Host "==========================================================================" -ForegroundColor Cyan

$CurrentDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $CurrentDir

if ($Mode -eq "status") {
    Write-Host "`n[*] 현재 result 폴더 무손실 영구 보존 산출물 현황:" -ForegroundColor Yellow
    Get-ChildItem -Path "result" | Sort-Object Name | Format-Table Name, @{Label="Size (KB)"; Expression={[math]::round($_.Length/1KB, 2)}}, LastWriteTime
    exit 0
}

Write-Host "`n[1/2] 파이썬 가상환경 및 필수 도구 점검..." -ForegroundColor Cyan
$pythonExe = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonExe) {
    Write-Host "[ERROR] 시스템에 Python이 설치되어 있지 않거나 PATH에 등록되지 않았습니다." -ForegroundColor Red
    exit 1
}

Write-Host "[2/2] 토큰 제로화 파이프라인 구동 (모드: $Mode)..." -ForegroundColor Cyan
if ($Mode -eq "zero") {
    python src/run_zero_token_master.py
} elseif ($Mode -eq "audio_only") {
    python src/render_021_multichar_tts_timeline.py
} elseif ($Mode -eq "highlight") {
    python src/render_022_cinematic_space_video.py --mode highlight
} elseif ($Mode -eq "real") {
    python src/render_real_scene_video.py --mode full
} elseif ($Mode -eq "quick") {
    python src/run_vf10_hybrid_full_pipeline.py --mode quick
} else {
    python src/run_vf10_hybrid_full_pipeline.py --mode full
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n==========================================================================" -ForegroundColor Green
    Write-Host "  [SUCCESS] 파이프라인 완결! AI 토큰 소모량 0 으로 모든 작업이 완료되었습니다." -ForegroundColor Green
    Write-Host "==========================================================================" -ForegroundColor Green
    Write-Host "`n[*] 최신 결과물 목록:" -ForegroundColor Yellow
    Get-ChildItem -Path "result" | Sort-Object LastWriteTime -Descending | Select-Object -First 6 | Format-Table Name, @{Label="Size (MB)"; Expression={[math]::round($_.Length/1MB, 2)}}, LastWriteTime
} else {
    Write-Host "`n[ERROR] 파이프라인 실행 중 오류가 발생했습니다. (종료 코드: $LASTEXITCODE)" -ForegroundColor Red
}
"""

with open("run_vf10_pipeline.ps1", "w", encoding="utf-8-sig") as f:
    f.write(ps_content)

print("[SUCCESS] run_vf10_pipeline.ps1 (Default: -Mode zero) 생성 완료")
