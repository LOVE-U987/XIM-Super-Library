@echo off
chcp 65001 >nul
title XIM超级图书馆 - 极速部署工具 v2.0

echo ╔══════════════════════════════════════════════════════════════════╗
echo ║     🚀 XIM超级图书馆 - 极速部署工具 v2.0                        ║
echo ║                                                                ║
echo ║     🎯 自动检测最优下载方式                                    ║
echo ║     🎯 实时显示下载速度和进度                                  ║
echo ║     🎯 下载完成自动解压                                        ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

echo 📦 正在检查Python环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未检测到Python！
    echo    请先安装 Python 3.8+: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do echo ✅ Python %%i

echo.
echo 📦 正在检查依赖...

REM 检查并安装py7zr
python -c "import py7zr" 2>nul
if %errorlevel% neq 0 (
    echo   ⏳ 正在安装 py7zr（解压.7z文件所需）...
    pip install py7zr -q
    if %errorlevel% neq 0 (
        echo ⚠️ py7zr 安装失败，将使用备用解压方式
    ) else (
        echo ✅ py7zr 安装成功
    )
) else (
    echo ✅ py7zr 已安装
)

REM 检查 aria2c
where aria2c >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ aria2c 已安装，将使用16线程极速下载！
) else (
    echo ⚡ aria2c 未安装，将使用Python多线程下载
    echo    提示：安装 aria2c 可以获得更快下载速度
    echo    安装命令: winget install aria2
)

echo.
echo 🚀 启动极速部署工具...
echo.

python deploy_fast.py

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                 极速部署工具已退出                               ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo 💡 温馨提示：
echo   - 如果下载速度仍然不理想，可以尝试安装 aria2c: winget install aria2
echo   - 如遇网络问题，脚本会自动降级为单线程下载
echo.
pause
