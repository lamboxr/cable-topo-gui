@echo off
chcp 65001 >nul
echo ================================================
echo 线缆拓扑图生成器 - 打包脚本
echo ================================================

:: 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo × Python 未安装或未添加到PATH
    pause
    exit /b 1
)

:: 安装PyInstaller（如果未安装）
echo 检查PyInstaller...
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo 正在安装PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo × PyInstaller 安装失败
        pause
        exit /b 1
    )
)

:: 清理之前的构建文件
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo ✓ 清理构建目录

:: 使用spec文件打包
echo 开始打包...
pyinstaller cable_topo.spec

if errorlevel 1 (
    echo × 打包失败
    pause
    exit /b 1
)

:: 检查结果
if exist "dist\线缆拓扑图生成器.exe" (
    echo ================================================
    echo ✓ 打包成功！
    echo ✓ 可执行文件: dist\线缆拓扑图生成器.exe
    
    :: 显示文件大小
    for %%I in ("dist\线缆拓扑图生成器.exe") do (
        set /a size=%%~zI/1024/1024
        echo ✓ 文件大小: !size! MB
    )
    
    echo ================================================
    echo 按任意键打开dist目录...
    pause >nul
    explorer dist
) else (
    echo × 未找到生成的exe文件
    pause
)