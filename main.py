from turtle import color
import requests
import os
import time
import random
import threading
import string
import colorama
import console
from console.utils import set_title

proxies = set()
with open("proxies.txt", "r") as f1:
    fl1 = f1.readlines()
    for line in fl1:
        proxies.add(line.strip())

webhook = input("Webhook: ")
proxyConfirm = input("Use Proxy? [YES/NO]: ")
if proxyConfirm.casefold() != "yes".casefold() and proxyConfirm.casefold() != "no".casefold():
    print("Invaild Choose!")
    exit()
vaild = 0
invaild = 0
used = 0

def checker():
    global vaild
    global invaild
    global used
    while True:
        set_title(f"NitroGenX - Vaild: {vaild} | Invaild: {invaild} | Used: {used}")
        proxy = random.choice(list(proxies))
        proxy_form = {'http': f"socks4://{proxy}", 'https': f"socks4://{proxy}"}
        nitro = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(16))
        try:
            if proxyConfirm.casefold() == "yes".casefold():
                check = requests.get(f"https://discord.com/api/v9/entitlements/gift-codes/{nitro}?with_application=false&with_subscription_plan=true", proxies=proxy_form, timeout=6000)
            elif proxyConfirm.casefold() == "no".casefold():
                check = requests.get(f"https://discord.com/api/v9/entitlements/gift-codes/{nitro}?with_application=false&with_subscription_plan=true")
            if check.status_code == 200:
                if check.json().get("uses") != 0:
                    print(colorama.Fore.YELLOW + f"[-] Used | {nitro}")
                    used += 1
                else:
                    print(colorama.Fore.GREEN + f"[+] Vaild | {nitro}")
                    requests.post(webhook, headers={"Content-Type": "application/json"}, json={"username": "Nitro Gen", "content": f"https://discord.gift/{nitro}"})
                    vaild += 1
            else:
                print(colorama.Fore.RED + f"[-] Invaild Code | {nitro} | {check.status_code}")
                invaild += 1
        except:
            pass

threadCount = int(input("Thread: "))
for i in range(threadCount):
    threading.Thread(target=checker).start()