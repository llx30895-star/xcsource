#!/usr/bin/env pwsh
# 003 产品上传执行（GitHub 推送模式）

Set-Location $PSScriptRoot

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "003 产品上传执行（GitHub 推送模式）" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "将执行：" -ForegroundColor Yellow
Write-Host "  1. 读取 Excel 中待上传记录" -ForegroundColor Yellow
Write-Host "  2. 执行 003 local-copy 上传" -ForegroundColor Yellow
Write-Host "  3. 回写 Excel / upload_state.json / 003-upload.log" -ForegroundColor Yellow
Write-Host "  4. 生成 batch manifest.json" -ForegroundColor Yellow
Write-Host "  5. 通过 git commit + git push 推送到 GitHub" -ForegroundColor Yellow
Write-Host ""
Write-Host "默认参数：" -ForegroundColor Yellow
Write-Host "  --mode local-copy" -ForegroundColor Yellow
Write-Host "  --target github_pages" -ForegroundColor Yellow
Write-Host "  --git-push --git-remote origin --git-branch master" -ForegroundColor Yellow
Write-Host ""

python run_003_upload.py --mode local-copy --target github_pages --git-push --git-remote origin --git-branch master @args

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "✓ 003 执行完成，并已完成 Git 推送流程" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "✗ 003 执行失败，或 Git 推送未完成" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
}

Write-Host ""
Read-Host "按回车键退出"
