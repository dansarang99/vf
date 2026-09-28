# -*- coding: utf-8 -*-
"""PowerShell 스크립트를 UTF-8 with BOM (utf-8-sig)으로 안전하게 생성"""

ps_content = """# PowerShell Native Pipeline Runner
param(
    [ValidateSet("full", "quick", "highlight", "audio_only", "status")]
    [string]$Mode = "full"
)

# 콘솔 UTF-8 설정
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host "  [vf10] K-Space Hybrid Zero-Token PowerShell Pipeline" -ForegroundColor Yellow
Write-Host "  * 로컬 오프로딩 기반 AI 토큰 소모량 0(Zero) 실현" -ForegroundColor Green
Write-Host "  * 덮어쓰기 0% 무손실 불변 번호 체계([001]~[999]) 자동 연동" -ForegroundColor Green
Write-Host "==========================================================================" -ForegroundColor Cyan

$CurrentDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $CurrentDir

if ($Mode -eq "status") {
    Write-Host "`n[*] 현재 result 폴더 무손실 영구 보존 산출물 현황:" -ForegroundColor Yellow
    Get-ChildItem -Path "result" | Sort-Object Name | Format-Table Name, @{Label="Size (KB)"; Expression={[math]::round($_.Length/1KB, 2)}}, LastWriteTime
    exit 0
}

Write-Host "`n[1/3] 파이썬 가상환경 및 필수 도구 점검..." -ForegroundColor Cyan
$pythonExe = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonExe) {
    Write-Host "[ERROR] 시스템에 Python이 설치되어 있지 않거나 PATH에 등록되지 않았습니다." -ForegroundColor Red
    exit 1
}

Write-Host "[2/3] 하이브리드 파이프라인 구동 (모드: $Mode)..." -ForegroundColor Cyan
if ($Mode -eq "audio_only") {
    python src/render_021_multichar_tts_timeline.py
} elseif ($Mode -eq "highlight") {
    python src/render_022_cinematic_space_video.py --mode highlight
} elseif ($Mode -eq "quick") {
    python src/run_vf10_hybrid_full_pipeline.py --mode quick
} else {
    python src/run_vf10_hybrid_full_pipeline.py --mode full
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n==========================================================================" -ForegroundColor Green
    Write-Host "  [SUCCESS] 파이프라인 완결! AI 토큰 소모량 0 으로 모든 영상이 완성되었습니다." -ForegroundColor Green
    Write-Host "==========================================================================" -ForegroundColor Green
    Write-Host "`n[*] 최신 결과물 목록:" -ForegroundColor Yellow
    Get-ChildItem -Path "result" | Sort-Object LastWriteTime -Descending | Select-Object -First 6 | Format-Table Name, @{Label="Size (MB)"; Expression={[math]::round($_.Length/1MB, 2)}}, LastWriteTime
} else {
    Write-Host "`n[ERROR] 파이프라인 실행 중 오류가 발생했습니다. (종료 코드: $LASTEXITCODE)" -ForegroundColor Red
}
"""

with open("run_vf10_pipeline.ps1", "w", encoding="utf-8-sig") as f:
    f.write(ps_content)

print("[SUCCESS] run_vf10_pipeline.ps1 (UTF-8 BOM) 생성 완료")
