@echo off
REM ============================================================
REM  AI Video Prompt Builder — Windows .exe Build Script
REM  ساخت فایل اجرایی ویندوز از سورس پایتون
REM ============================================================
REM  Run this file on a Windows PC that has Python 3.8+ installed.
REM  این فایل را روی یک سیستم ویندوزی که پایتون نصب دارد اجرا کنید.
REM ============================================================

echo.
echo [1/3] Installing PyInstaller...
pip install pyinstaller

echo.
echo [2/3] Building the .exe (this may take 1-2 minutes)...
pyinstaller --noconfirm --onefile --windowed --name "AI_Prompt_Builder" prompt_builder.py

echo.
echo [3/3] Done! Your .exe file is inside the "dist" folder.
echo فایل اجرایی شما داخل پوشه dist ساخته شد.
echo.
pause
