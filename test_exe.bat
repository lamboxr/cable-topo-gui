@echo off
chcp 65001 >nul
echo ================================================
echo 测试生成的exe文件
echo ================================================

if not exist "dist\线缆拓扑图生成器.exe" (
    echo × 未找到exe文件，请先运行打包脚本
    pause
    exit /b 1
)

echo ✓ 找到exe文件: dist\线缆拓扑图生成器.exe

:: 显示文件信息
for %%I in ("dist\线缆拓扑图生成器.exe") do (
    set /a size=%%~zI/1024/1024
    echo ✓ 文件大小: !size! MB
    echo ✓ 修改时间: %%~tI
)

echo.
echo 正在启动程序...
echo （如果程序正常启动并显示界面，说明打包成功）
echo.

:: 启动exe文件
start "" "dist\线缆拓扑图生成器.exe"

echo ✓ 程序已启动
echo.
pause