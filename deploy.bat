@echo off
chcp 65001 >nul
title XIM超级图书馆 - 一键部署工具

echo ╔══════════════════════════════════════════════════════════════════╗
echo ║          🚀 XIM超级图书馆 - 一键部署工具                         ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

echo 📦 正在检查Python环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未找到Python，请先安装Python 3.8+
    echo    下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python环境已就绪

echo.
echo 📦 正在安装依赖...
pip install py7zr -q

if %errorlevel% neq 0 (
    echo ❌ 依赖安装失败，请检查网络连接
    pause
    exit /b 1
)

echo ✅ 依赖安装完成

echo.
echo 🚀 启动部署工具...
echo.

python deploy.py

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                      部署工具已退出                              ║
echo ╚══════════════════════════════════════════════════════════════════╝
pause
