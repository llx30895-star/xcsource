@echo off
chcp 65001 >nul
cd /d %~dp0

echo ========================================
echo 003 产品上传执行（GitHub 推送模式）
echo ========================================
echo.
echo 将执行：
echo   1. 读取 Excel 中待上传记录
echo   2. 执行 003 local-copy 上传
echo   3. 回写 Excel / upload_state.json / 003-upload.log
echo   4. 生成 batch manifest.json
echo   5. 通过 git commit ^& git push 推送到 GitHub
echo.
echo 默认参数：
echo   --mode local-copy
echo   --target github_pages
echo   --git-push --git-remote origin --git-branch master
echo.

python run_003_upload.py --mode local-copy --target github_pages --git-push --git-remote origin --git-branch master %*

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo ✓ 003 执行完成，并已完成 Git 推送流程
    echo ========================================
) else (
    echo.
    echo ========================================
    echo ✗ 003 执行失败，或 Git 推送未完成
    echo ========================================
)

echo.
pause
