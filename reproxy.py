import requests
import time
import sys
import os
from colorama import Fore, Style, init
from threading import Thread, Lock
import os

init(autoreset=True)
print_lock = Lock()
stop_code = False

discord = '@cpfein'

VERSION = '1.0.0'

R = '\033[31m'  # red
G = '\033[32m'  # green
C = '\033[36m'  # cyan
W = '\033[0m'  # white
Y = '\033[33m'  # yellow
M = '\033[35m' # Magenta

banner = r'''                                                    

   ___                           
  | _ \___ _ __ _ _ _____ ___  _ 
  |   / -_) '_ \ '_/ _ \ \ / || |
  |_|_\___| .__/_| \___/_\_\\_, |
          |_|               |__/ 
                                                                         
    Proxy Generator / Checker     
'''

def print_banners():
    """
    prints the program banners
    """
    print(f' {M}{banner}{W}\n')
    print(f' {M}[+] {C}Version      : {W}{VERSION}')
    print(f' {M}[+] {C}Created By   : {W}Reproachfully')
    print(f' {M} ╰> {C}Discord      : {W}{discord}')
   

def fetch_proxies(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        proxy_ips = []
        for line in response.text.split('\n'):
            parts = line.strip().split(':')
            if len(parts) == 2:
                ip, port = parts
                if ip.count('.') == 3 and port.isdigit():
                    proxy_ips.append(f'{ip}:{port}')

        return proxy_ips

    except requests.exceptions.RequestException as e:
        with print_lock:
            print(f' Error fetching proxies from {url}: {Fore.RED}{str(e)}{Style.RESET_ALL}')
        return []

def is_proxy_working(proxy):
    try:
        response = requests.get("https://www.example.com", proxies={"http": proxy, "https": proxy}, timeout=5)
        response.raise_for_status()
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        with print_lock:
            print(f' [{Fore.MAGENTA}reproxy{Fore.WHITE}]{proxy} {Fore.CYAN}: {Fore.RED}[Not Working]{Style.RESET_ALL}')
        return False

def validate_and_print_proxies(proxy_ips, print_limit=None):
    global stop_code
    working_proxies = set()  # Use a set to store unique working proxies
    printed_count = 0
    threads = []

    for proxy in proxy_ips:
        if printed_count >= print_limit:
            break

        thread = Thread(target=validate_and_print_proxy, args=(proxy, working_proxies, print_limit))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return working_proxies

def validate_and_print_proxy(proxy, working_proxies, print_limit):
    global stop_code
    if not stop_code and is_proxy_working(proxy):
        with print_lock:
            if len(working_proxies) < print_limit:
                print(f" [{Fore.MAGENTA}reproxy{Fore.WHITE}] {proxy} {Fore.CYAN}: {Fore.GREEN}[Working]{Style.RESET_ALL}")
                working_proxies.add(proxy)
            if len(working_proxies) >= print_limit:
                stop_code = True
'''
def validate_and_print_proxy(proxy, working_proxies, print_limit):
    global stop_code
    if not stop_code and is_proxy_working(proxy):
        with print_lock:
            print(f"{proxy} : {Fore.GREEN}[Working]{Style.RESET_ALL}")
            working_proxies.add(proxy)
            printed_count = len(working_proxies)
            if printed_count >= print_limit:
                stop_code = True
'''

def save_proxies_to_file(proxies, filename="proxies.txt"):
    with open(filename, "w") as file:
        file.writelines([f"{proxy}\n" for proxy in proxies])

def main():
    print_banners()
    try:
        num_proxies_to_print = int(input(f"\n {Fore.CYAN}Amount of proxies to Gen:~$ {Style.RESET_ALL}"))
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        sys.exit(1)

    start_time = time.time()
    
    # Proxy URL options for HTTP, HTTPS, SOCKS4, SOCKS5 and Mix_Proxies
    proxy_urls_HTTP = [
        "https://api.openproxylist.xyz/http.txt",
        "https://alexa.lr2b.com/proxylist.txt",
        "https://rootjazz.com/proxies/proxies.txt",
        "https://www.proxy-list.download/api/v1/get?type=http",
        "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",

    ]

    proxy_urls_HTTPS = [
        "https://www.sslproxies.org/",
        "https://www.proxy-list.download/api/v1/get?type=https",
        "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/https/https.txt",
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt",
        "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/https/https.txt",

    ]

    proxy_urls_SOCKS4 = [
        "https://api.openproxylist.xyz/socks4.txt",
        "https://www.proxy-list.download/api/v1/get?type=socks4",
        "https://www.socks-proxy.net/",
        "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks4/socks4.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
        "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt",
        "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies_anonymous/socks4.txt",

    ]

    proxy_urls_SOCKS5 = [
        "https://www.proxy-list.download/api/v1/get?type=socks5",
        "https://api.openproxylist.xyz/socks5.txt",
        "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks5/socks5.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
        "https://raw.githubusercontent.com/elliottophellia/yakumo/master/results/socks5/global/socks5_checked.txt",
        "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks5.txt",
        "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
        "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies_anonymous/socks5.txt",
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt",

    ]

    mixed_url_proxies =  [
        'https://www.sslproxies.org/',
        'https://www.google-proxy.net/',
        'https://free-proxy-list.net/anonymous-proxy.html',
        'https://free-proxy-list.net/uk-proxy.html',
        'https://www.us-proxy.org/',
        'https://free-proxy-list.net/'

    ]

    # Combined list of all proxy URLs

    proxy_urls_MIX = mixed_url_proxies

    #proxy_urls_MIX = mixed_url_proxies + proxy_urls_HTTP + proxy_urls_HTTPS + proxy_urls_SOCKS4 + proxy_urls_SOCKS5

    # Ask the user to choose proxy type
    os.system("cls")
    print(f' {M}{banner}{W}\n')
    
    print(f"\n {Fore.CYAN}Choose the type of proxy:")
    print(" 1. HTTP")
    print(" 2. HTTPS")
    print(" 3. SOCKS4")
    print(" 4. SOCKS5")
    print(" 5. Mixed Proxies (recommended)")
    proxy_type = input(f"\n {Fore.CYAN}Enter your choice {Fore.MAGENTA}(1/2/3/4/5):{Fore.WHITE}")

    if proxy_type == "1":
        proxy_urls = proxy_urls_HTTP
    elif proxy_type == "2":
        proxy_urls = proxy_urls_HTTPS
    elif proxy_type == "3":
        proxy_urls = proxy_urls_SOCKS4
    elif proxy_type == "4":
        proxy_urls = proxy_urls_SOCKS5
    elif proxy_type == "5":
        proxy_urls = proxy_urls_MIX
    else:
        print("Invalid choice. Please select a valid option.")
        sys.exit(1)

    proxy_ips = []

    for url in proxy_urls:
        proxy_ips.extend(fetch_proxies(url))

    working_proxies = validate_and_print_proxies(proxy_ips, print_limit=num_proxies_to_print)

    print(f"\n{Fore.CYAN}[+]{Fore.GREEN} List of Working Proxies:{Style.RESET_ALL}\n")
    for proxy in working_proxies:
        print(f"{proxy}")

    save_proxies_to_file(working_proxies)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\n{Fore.CYAN}[+]{Fore.GREEN} Time taken: {Fore.CYAN}{elapsed_time} seconds")

    current_directory = os.getcwd()
    save_path = os.path.join(current_directory, "proxies.txt")
    print(f"\n{Fore.CYAN}[+]{Fore.RED} List of Working Proxies saved at: {Fore.GREEN}{save_path}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
