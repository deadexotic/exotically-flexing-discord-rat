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
    
    if not exist python-3.12.0-amd64.exe (
        echo [!] Failed to download Python installer. Please install Python 3.12 manually.
        pause >nul
        exit /b 1
    )
    
    echo [*] Installing Python 3.12 (this may take a few minutes)...
    start /wait python-3.12.0-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    
    if %errorlevel% neq 0 (
        echo [!] Python installation failed. Please install Python 3.12 manually.
        del python-3.12.0-amd64.exe
        pause >nul
        exit /b 1
    )
    
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
if %errorlevel% neq 0 (
    echo [!] Failed to upgrade pip. Please check your internet connection.
    pause >nul
    exit /b 1
)

:: Check if requirements.txt exists
if not exist requirements.txt (
    echo [!] requirements.txt not found. Please make sure all files are in the same directory.
    pause >nul
    exit /b 1
)

:: Install all requirements from requirements.txt
echo [*] Installing modules from requirements.txt...
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [!] Failed to install some requirements. Please try again.
    pause >nul
    exit /b 1
)

echo.
echo [+] All requirements installed successfully!
echo.
echo [*] Starting Exotically Flexing RAT Builder...
echo.

:: Check if builder.py exists
if not exist builder.py (
    echo [!] builder.py not found. Please make sure all files are in the same directory.
    pause >nul
    exit /b 1
)

:: Run the main script
python builder.py

echo.
echo [*] Exiting...
pause >nul
exit /b 0
