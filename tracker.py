import os
import sys
import time
import requests
import phonenumbers
from phonenumbers import geocoder, carrier, timezone, number_type

# Colorama for styling
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    os.system("pip install colorama")
    from colorama import Fore, Style, init
    init(autoreset=True)

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    print(Fore.RED + """
██████╗ ███████╗████████╗██████╗  ██████╗ 
██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔═══██╗
██████╔╝█████╗     ██║   ██████╔╝██║   ██║
██╔═══╝ ██╔══╝     ██║   ██╔══██╗██║   ██║
██║     ███████╗   ██║   ██║  ██║╚██████╔╝
╚═╝     ╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ 
    """ + Fore.CYAN + "=======================================\n"
        + "           ALL-IN-ONE OSINT TOOL\n"
        + "               DEVELOPED BY: PETRO\n"
        + "=======================================")

def track_ip(ip_address=""):
    print(Fore.BLUE + f"\n[+] Fetching data for: {ip_address if ip_address else 'Your Network'}")
    url = f'http://ip-api.com/json/{ip_address}' if ip_address else 'http://ip-api.com/json/'
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'fail':
                print(Fore.RED + f"[-] Error: {data.get('message')}")
                return
            print(Fore.GREEN + "\n--- IP ADDRESS DETAILS ---")
            for key, value in data.items():
                print(f"{Fore.YELLOW}{key:<15}: {Fore.WHITE}{value}")
            print(Fore.GREEN + "--------------------------")
    except Exception as e:
        print(Fore.RED + f"[-] Network Error: {e}")

def track_phone():
    print(Fore.GREEN + "\n--- Phone Info ---")
    phone = input(Fore.YELLOW + "[?] Enter number (with +): " + Fore.WHITE).strip()
    if not phone: return

    try:
        parsed = phonenumbers.parse(phone if phone.startswith('+') else '+' + phone, None)
        if phonenumbers.is_valid_number(parsed):
            print(Fore.BLUE + "[+] Analyzing...")
            time.sleep(0.5)
            
            # Local Database
            clean_digits = "".join(filter(str.isdigit, phone))[-10:]
            local_db = {"7907685171": "Shibu Pallipuram", "8330097122": "Adarsh Petro"}
            
            # Deep Data
            n_type = number_type(parsed)
            types = {0: "FIXED_LINE", 1: "MOBILE", 2: "FIXED_LINE_OR_MOBILE", 3: "TOLL_FREE"}
            
            print(Fore.GREEN + "\n[ TELECOMMUNICATION DATA ]")
            print(f"{Fore.YELLOW}Number            : {Fore.WHITE}{phone}")
            print(f"{Fore.YELLOW}Identity          : {Fore.CYAN}{local_db.get(clean_digits, 'Verified User')}")
            print(f"{Fore.YELLOW}Country           : {Fore.WHITE}{geocoder.description_for_number(parsed, 'en')}")
            print(f"{Fore.YELLOW}Carrier           : {Fore.WHITE}{carrier.name_for_number(parsed, 'en')}")
            print(f"{Fore.YELLOW}Line Type         : {Fore.WHITE}{types.get(n_type, 'UNKNOWN')}")
            print(f"{Fore.YELLOW}Timezone          : {Fore.WHITE}{', '.join(timezone.time_zones_for_number(parsed))}")
            print(Fore.GREEN + "--------------------------")
        else:
            print(Fore.RED + "[-] Invalid phone number format.")
    except Exception as e:
        print(Fore.RED + f"[-] Error: {e}")

def track_username():
    print(Fore.GREEN + "\n--- USERNAME TRACKER ---")
    username = input(Fore.YELLOW + "[?] Enter Username: " + Fore.WHITE).strip()
    if username:
        print(Fore.BLUE + f"\n[+] Searching footprints for: {username}")
        platforms = {
            "GitHub": f"https://github.com/{username}",
            "Instagram": f"https://instagram.com/{username}",
            "Twitter": f"https://twitter.com/{username}"
        }
        for name, link in platforms.items():
            print(f"{Fore.WHITE}[+] {name:<10} : {Fore.CYAN}{link}")

def main():
    while True:
        clear_terminal() # Screen clearing loop fix
        display_banner()
        print(f"{Fore.WHITE}[1] IP Tracker\n[2] My IP Details\n[3] Phone numer Basic Info\n[4] Username Tracker\n[0] Exit")
        
        choice = input(Fore.RED + "\nchoose from menu>" + Fore.WHITE).strip()
        
        if choice == '1':
            ip = input("Enter IP: ")
            track_ip(ip)
            input("\nPress Enter to return...")
        elif choice == '2':
            track_ip()
            input("\nPress Enter to return...")
        elif choice == '3':
            track_phone()
            input("\nPress Enter to return...")
        elif choice == '4':
            track_username()
            input("\nPress Enter to return...")
        elif choice == '0':
            print(Fore.RED + "\n[-] Exiting...")
            sys.exit()

if __name__ == "__main__":
    main()
