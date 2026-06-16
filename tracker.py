#!/usr/bin/env python3
# PETRO - ALL-IN-ONE OSINT TOOL
# Created by: PETRO

import os
import sys
import json
import time
import requests
import phonenumbers
from phonenumbers import geocoder, carrier, timezone as ptimezone, number_type as pnumber_type

# Colors for terminal output
try:
    from colorama import Fore, Back, Style, init
    init(autoreset=True)
except ImportError:
    os.system("pip install colorama")
    from colorama import Fore, Back, Style, init
    init(autoreset=True)


def clear_terminal():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def display_banner():
    """Show the tool banner"""
    clear_terminal()
    print(Fore.RED + r"""
██████╗ ███████╗████████╗██████╗  ██████╗ 
██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔═══██╗
██████╔╝█████╗     ██║   ██████╔╝██║   ██║
██╔═══╝ ██╔══╝     ██║   ██╔══██╗██║   ██║
██║     ███████╗   ██║   ██║  ██║╚██████╔╝
╚═╝     ╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ 
    """ + Fore.CYAN + """=======================================
           ALL-IN-ONE OSINT TOOL
               DEVELOPED BY: PETRO
=======================================""")


def show_my_ip():
    """Show your own public IP address and details"""
    display_banner()
    print(Fore.BLUE + "\n[+] GETTING YOUR PUBLIC IP INFORMATION...\n")
    
    try:
        # Get your public IP
        response = requests.get('https://api.ipify.org/', timeout=10)
        my_ip = response.text.strip()
        print(f"{Fore.YELLOW}Your Public IP    : {Fore.GREEN}{my_ip}")
        
        # Get IP details from ip-api.com
        response = requests.get(f"http://ip-api.com/json/{my_ip}", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') != 'fail':
                print(f"\n{Fore.CYAN}--- LOCATION DETAILS ---")
                print(f"{Fore.YELLOW}Country         : {Fore.WHITE}{data.get('country', 'N/A')}")
                print(f"{Fore.YELLOW}Region          : {Fore.WHITE}{data.get('regionName', 'N/A')}")
                print(f"{Fore.YELLOW}City            : {Fore.WHITE}{data.get('city', 'N/A')}")
                print(f"{Fore.YELLOW}Postal Code     : {Fore.WHITE}{data.get('zip', 'N/A')}")
                print(f"{Fore.YELLOW}Latitude        : {Fore.WHITE}{data.get('lat', 'N/A')}")
                print(f"{Fore.YELLOW}Longitude       : {Fore.WHITE}{data.get('lon', 'N/A')}")
                print(f"{Fore.YELLOW}Timezone        : {Fore.WHITE}{data.get('timezone', 'N/A')}")
                print(f"{Fore.YELLOW}ISP             : {Fore.WHITE}{data.get('isp', 'N/A')}")
                print(f"{Fore.YELLOW}Organization    : {Fore.WHITE}{data.get('org', 'N/A')}")
                
                # Google Maps link
                lat = data.get('lat', 0)
                lon = data.get('lon', 0)
                print(f"{Fore.YELLOW}Map Link        : {Fore.CYAN}https://www.google.com/maps/@{lat},{lon},12z")
        
        # Get extra info from ipwho.is
        try:
            response2 = requests.get(f"http://ipwho.is/{my_ip}", timeout=10)
            if response2.status_code == 200:
                data2 = response2.json()
                print(f"\n{Fore.CYAN}--- EXTRA INFO ---")
                print(f"{Fore.YELLOW}Continent       : {Fore.WHITE}{data2.get('continent', 'N/A')}")
                print(f"{Fore.YELLOW}Capital City    : {Fore.WHITE}{data2.get('capital', 'N/A')}")
                print(f"{Fore.YELLOW}Currency        : {Fore.WHITE}{data2.get('currency', {}).get('code', 'N/A')}")
                print(f"{Fore.YELLOW}Calling Code    : {Fore.WHITE}{data2.get('calling_code', 'N/A')}")
                print(f"{Fore.YELLOW}Flag            : {Fore.WHITE}{data2.get('flag', {}).get('emoji', 'N/A')}")
                print(f"{Fore.YELLOW}Connection Type : {Fore.WHITE}{data2.get('connection', {}).get('type', 'N/A')}")
        except:
            pass
            
    except Exception as e:
        print(f"{Fore.RED}[-] Error: {e}")
    
    input(f"\n{Fore.YELLOW}[+] Press Enter to continue...")


def track_target_ip():
    """Track a target IP address and show all details from all sources"""
    display_banner()
    target_ip = input(f"{Fore.YELLOW}\n[?] Enter Target IP : {Fore.WHITE}").strip()
    if not target_ip:
        return
    
    print(f"{Fore.BLUE}[+] GETTING FULL INFO FOR: {target_ip}\n")
    
    try:
        # Get data from ip-api.com
        response = requests.get(
            f"http://ip-api.com/json/{target_ip}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query",
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'fail':
                print(f"{Fore.RED}[-] Error: {data.get('message', 'Invalid IP')}")
            else:
                print(f"{Fore.GREEN}========== IP-API.COM DATA ==========")
                print(f"{Fore.YELLOW}IP Address      : {Fore.WHITE}{data.get('query', target_ip)}")
                print(f"{Fore.YELLOW}Country         : {Fore.WHITE}{data.get('country', 'N/A')}")
                print(f"{Fore.YELLOW}Country Code    : {Fore.WHITE}{data.get('countryCode', 'N/A')}")
                print(f"{Fore.YELLOW}Region          : {Fore.WHITE}{data.get('regionName', 'N/A')}")
                print(f"{Fore.YELLOW}Region Code     : {Fore.WHITE}{data.get('region', 'N/A')}")
                print(f"{Fore.YELLOW}City            : {Fore.WHITE}{data.get('city', 'N/A')}")
                print(f"{Fore.YELLOW}Postal Code     : {Fore.WHITE}{data.get('zip', 'N/A')}")
                print(f"{Fore.YELLOW}Latitude        : {Fore.WHITE}{data.get('lat', 'N/A')}")
                print(f"{Fore.YELLOW}Longitude       : {Fore.WHITE}{data.get('lon', 'N/A')}")
                print(f"{Fore.YELLOW}Timezone        : {Fore.WHITE}{data.get('timezone', 'N/A')}")
                print(f"{Fore.YELLOW}ISP             : {Fore.WHITE}{data.get('isp', 'N/A')}")
                print(f"{Fore.YELLOW}Organization    : {Fore.WHITE}{data.get('org', 'N/A')}")
                print(f"{Fore.YELLOW}AS Number       : {Fore.WHITE}{data.get('as', 'N/A')}")
                
                lat = data.get('lat', 0)
                lon = data.get('lon', 0)
                print(f"{Fore.YELLOW}Google Maps     : {Fore.CYAN}https://www.google.com/maps/@{lat},{lon},12z")
                print(f"{Fore.GREEN}====================================")
        
        # Get extra info from ipwho.is
        try:
            response2 = requests.get(f"http://ipwho.is/{target_ip}", timeout=10)
            if response2.status_code == 200:
                data2 = response2.json()
                print(f"\n{Fore.MAGENTA}========== IPWHOIS EXTRA DATA ==========")
                print(f"{Fore.YELLOW}Type            : {Fore.WHITE}{data2.get('type', 'N/A')}")
                print(f"{Fore.YELLOW}Continent       : {Fore.WHITE}{data2.get('continent', 'N/A')}")
                print(f"{Fore.YELLOW}Continent Code  : {Fore.WHITE}{data2.get('continent_code', 'N/A')}")
                print(f"{Fore.YELLOW}Capital         : {Fore.WHITE}{data2.get('capital', 'N/A')}")
                print(f"{Fore.YELLOW}Borders         : {Fore.WHITE}{data2.get('borders', 'N/A')}")
                print(f"{Fore.YELLOW}EU Member       : {Fore.WHITE}{data2.get('is_eu', 'N/A')}")
                print(f"{Fore.YELLOW}Calling Code    : {Fore.WHITE}{data2.get('calling_code', 'N/A')}")
                print(f"{Fore.YELLOW}Postal          : {Fore.WHITE}{data2.get('postal', 'N/A')}")
                print(f"{Fore.YELLOW}Currency Code   : {Fore.WHITE}{data2.get('currency', {}).get('code', 'N/A')}")
                print(f"{Fore.YELLOW}Currency Symbol : {Fore.WHITE}{data2.get('currency', {}).get('symbol', 'N/A')}")
                print(f"{Fore.YELLOW}Currency Name   : {Fore.WHITE}{data2.get('currency', {}).get('name', 'N/A')}")
                print(f"{Fore.YELLOW}Flag            : {Fore.WHITE}{data2.get('flag', {}).get('emoji', 'N/A')}")
                print(f"{Fore.YELLOW}ASN             : {Fore.WHITE}{data2.get('connection', {}).get('asn', 'N/A')}")
                print(f"{Fore.YELLOW}Organization    : {Fore.WHITE}{data2.get('connection', {}).get('org', 'N/A')}")
                print(f"{Fore.YELLOW}ISP             : {Fore.WHITE}{data2.get('connection', {}).get('isp', 'N/A')}")
                print(f"{Fore.YELLOW}Domain          : {Fore.WHITE}{data2.get('connection', {}).get('domain', 'N/A')}")
                print(f"{Fore.YELLOW}Connection Type : {Fore.WHITE}{data2.get('connection', {}).get('type', 'N/A')}")
                print(f"{Fore.YELLOW}Timezone ID     : {Fore.WHITE}{data2.get('timezone', {}).get('id', 'N/A')}")
                print(f"{Fore.YELLOW}UTC Offset      : {Fore.WHITE}{data2.get('timezone', {}).get('offset', 'N/A')}")
                print(f"{Fore.YELLOW}UTC             : {Fore.WHITE}{data2.get('timezone', {}).get('utc', 'N/A')}")
                print(f"{Fore.YELLOW}Current Time    : {Fore.WHITE}{data2.get('timezone', {}).get('current_time', 'N/A')}")
                print(f"{Fore.YELLOW}DST             : {Fore.WHITE}{data2.get('timezone', {}).get('is_dst', 'N/A')}")
                print(f"{Fore.MAGENTA}========================================")
        except:
            pass
            
        # Get data from ipinfo.io
        try:
            response3 = requests.get(f"https://ipinfo.io/{target_ip}/json", timeout=10)
            if response3.status_code == 200:
                data3 = response3.json()
                print(f"\n{Fore.CYAN}========== IPINFO.IO DATA ==========")
                print(f"{Fore.YELLOW}Hostname        : {Fore.WHITE}{data3.get('hostname', 'N/A')}")
                print(f"{Fore.YELLOW}Anycast         : {Fore.WHITE}{data3.get('anycast', 'N/A')}")
                print(f"{Fore.YELLOW}City            : {Fore.WHITE}{data3.get('city', 'N/A')}")
                print(f"{Fore.YELLOW}Region          : {Fore.WHITE}{data3.get('region', 'N/A')}")
                print(f"{Fore.YELLOW}Country         : {Fore.WHITE}{data3.get('country', 'N/A')}")
                print(f"{Fore.YELLOW}Location        : {Fore.WHITE}{data3.get('loc', 'N/A')}")
                print(f"{Fore.YELLOW}Organization    : {Fore.WHITE}{data3.get('org', 'N/A')}")
                print(f"{Fore.YELLOW}Postal          : {Fore.WHITE}{data3.get('postal', 'N/A')}")
                print(f"{Fore.YELLOW}Timezone        : {Fore.WHITE}{data3.get('timezone', 'N/A')}")
                print(f"{Fore.CYAN}====================================")
        except:
            pass
            
    except Exception as e:
        print(f"{Fore.RED}[-] Network Error: {e}")
    
    input(f"\n{Fore.YELLOW}[+] Press Enter to continue...")


def track_phone_number():
    """Track a phone number and show all details"""
    display_banner()
    phone = input(f"{Fore.YELLOW}\n[?] Enter Phone Number (Example: +6281xxxxx) : {Fore.WHITE}").strip()
    if not phone:
        return
    
    print(f"{Fore.BLUE}[+] ANALYZING PHONE NUMBER: {phone}\n")
    time.sleep(0.5)
    
    try:
        # Add + sign if missing
        if not phone.startswith('+'):
            phone = '+' + phone
        
        # Parse the number
        parsed = phonenumbers.parse(phone, None)
        
        # Check if number is valid
        if not phonenumbers.is_valid_number(parsed):
            print(f"{Fore.RED}[-] INVALID PHONE NUMBER!")
            print(f"{Fore.YELLOW}Possible? : {Fore.WHITE}{phonenumbers.is_possible_number(parsed)}")
            input(f"\n{Fore.YELLOW}[+] Press Enter to continue...")
            return
        
        print(f"{Fore.GREEN}========== PHONE NUMBER INFO ==========")
        
        # Basic information
        national_num = str(parsed.national_number)
        country_code = parsed.country_code
        region_code = phonenumbers.region_code_for_number(parsed)
        
        print(f"{Fore.YELLOW}Number          : {Fore.WHITE}{phone}")
        print(f"{Fore.YELLOW}National Number : {Fore.WHITE}{national_num}")
        print(f"{Fore.YELLOW}Country Code    : {Fore.WHITE}+{country_code}")
        print(f"{Fore.YELLOW}Region Code     : {Fore.WHITE}{region_code}")
        print(f"{Fore.YELLOW}International   : {Fore.WHITE}{phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}")
        print(f"{Fore.YELLOW}E.164 Format    : {Fore.WHITE}{phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)}")
        
        # Location information
        location_en = geocoder.description_for_number(parsed, "en")
        print(f"{Fore.YELLOW}Location        : {Fore.WHITE}{location_en if location_en else 'N/A'}")
        
        # Carrier information
        carrier_name = carrier.name_for_number(parsed, "en")
        print(f"{Fore.YELLOW}Carrier/Operator: {Fore.WHITE}{carrier_name if carrier_name else 'N/A'}")
        
        # Timezone information
        timezone_list = ptimezone.time_zones_for_number(parsed)
        timezone_str = ', '.join(timezone_list) if timezone_list else 'N/A'
        print(f"{Fore.YELLOW}Timezone        : {Fore.WHITE}{timezone_str}")
        
        # Number type
        num_type = pnumber_type(parsed)
        type_names = {
            0: "FIXED LINE",
            1: "MOBILE",
            2: "FIXED LINE OR MOBILE",
            3: "TOLL FREE",
            4: "PREMIUM RATE",
            5: "SHARED COST",
            6: "VOIP",
            7: "PERSONAL NUMBER",
            8: "PAGER",
            9: "UAN",
            10: "VOICEMAIL",
            27: "UNKNOWN"
        }
        print(f"{Fore.YELLOW}Number Type     : {Fore.WHITE}{type_names.get(num_type, 'UNKNOWN')}")
        
        # Validity checks
        print(f"{Fore.YELLOW}Is Valid?       : {Fore.WHITE}{phonenumbers.is_valid_number(parsed)}")
        print(f"{Fore.YELLOW}Is Possible?    : {Fore.WHITE}{phonenumbers.is_possible_number(parsed)}")
        print(f"{Fore.YELLOW}Leading Zeros   : {Fore.WHITE}{parsed.number_of_leading_zeros}")
        
        # Country profile
        country_profiles = {
            "ID": {"name": "Indonesia", "capital": "Jakarta", "language": "Bahasa Indonesia"},
            "US": {"name": "United States", "capital": "Washington D.C.", "language": "English"},
            "IN": {"name": "India", "capital": "New Delhi", "language": "Hindi/English"},
            "GB": {"name": "United Kingdom", "capital": "London", "language": "English"},
            "MY": {"name": "Malaysia", "capital": "Kuala Lumpur", "language": "Malay"},
            "SG": {"name": "Singapore", "capital": "Singapore", "language": "English/Malay/Chinese/Tamil"},
            "PH": {"name": "Philippines", "capital": "Manila", "language": "Filipino/English"},
            "TH": {"name": "Thailand", "capital": "Bangkok", "language": "Thai"},
            "VN": {"name": "Vietnam", "capital": "Hanoi", "language": "Vietnamese"},
            "AE": {"name": "UAE", "capital": "Abu Dhabi", "language": "Arabic"},
            "SA": {"name": "Saudi Arabia", "capital": "Riyadh", "language": "Arabic"},
            "PK": {"name": "Pakistan", "capital": "Islamabad", "language": "Urdu/English"},
            "BD": {"name": "Bangladesh", "capital": "Dhaka", "language": "Bengali"},
            "LK": {"name": "Sri Lanka", "capital": "Colombo", "language": "Sinhala/Tamil"},
            "NP": {"name": "Nepal", "capital": "Kathmandu", "language": "Nepali"},
        }
        
        profile = country_profiles.get(region_code, {})
        if profile:
            print(f"\n{Fore.CYAN}--- COUNTRY PROFILE ({region_code}) ---")
            print(f"{Fore.YELLOW}Country Name    : {Fore.WHITE}{profile.get('name', 'N/A')}")
            print(f"{Fore.YELLOW}Capital         : {Fore.WHITE}{profile.get('capital', 'N/A')}")
            print(f"{Fore.YELLOW}Language        : {Fore.WHITE}{profile.get('language', 'N/A')}")
        
        print(f"{Fore.GREEN}=======================================")
        
    except Exception as e:
        print(f"{Fore.RED}[-] Error: {e}")
    
    input(f"\n{Fore.YELLOW}[+] Press Enter to continue...")


def track_username():
    """Search for a username across many websites"""
    display_banner()
    username = input(f"{Fore.YELLOW}\n[?] Enter Username to Search : {Fore.WHITE}").strip()
    if not username:
        return
    
    print(f"{Fore.BLUE}[+] SEARCHING FOR USERNAME: {username}\n")
    time.sleep(1)
    
    # List of websites to check
    websites = [
        ("Facebook", "https://www.facebook.com/{}"),
        ("Twitter/X", "https://twitter.com/{}"),
        ("Instagram", "https://www.instagram.com/{}"),
        ("LinkedIn", "https://www.linkedin.com/in/{}"),
        ("GitHub", "https://www.github.com/{}"),
        ("Pinterest", "https://www.pinterest.com/{}"),
        ("YouTube", "https://www.youtube.com/@{}"),
        ("TikTok", "https://www.tiktok.com/@{}"),
        ("Snapchat", "https://www.snapchat.com/add/{}"),
        ("Reddit", "https://www.reddit.com/user/{}"),
        ("Telegram", "https://t.me/{}"),
        ("Twitch", "https://www.twitch.tv/{}"),
        ("SoundCloud", "https://soundcloud.com/{}"),
        ("Medium", "https://medium.com/@{}"),
        ("Quora", "https://www.quora.com/profile/{}"),
        ("Flickr", "https://www.flickr.com/people/{}"),
        ("Behance", "https://www.behance.net/{}"),
        ("Dribbble", "https://dribbble.com/{}"),
        ("CodePen", "https://codepen.io/{}"),
        ("GitLab", "https://gitlab.com/{}"),
        ("BitBucket", "https://bitbucket.org/{}"),
        ("HackerRank", "https://www.hackerrank.com/{}"),
        ("Dev.to", "https://dev.to/{}"),
        ("Keybase", "https://keybase.io/{}"),
        ("Mastodon", "https://mastodon.social/@{}"),
        ("VK", "https://vk.com/{}"),
        ("Steam", "https://steamcommunity.com/id/{}"),
        ("Chess.com", "https://www.chess.com/member/{}"),
        ("Spotify", "https://open.spotify.com/user/{}"),
        ("About.me", "https://about.me/{}"),
        ("Imgur", "https://imgur.com/user/{}"),
        ("Patreon", "https://www.patreon.com/{}"),
        ("ProductHunt", "https://www.producthunt.com/@{}"),
        ("SlideShare", "https://www.slideshare.net/{}"),
        ("Tumblr", "https://{}.tumblr.com"),
        ("Hashnode", "https://hashnode.com/@{}"),
        ("Replit", "https://replit.com/@{}"),
    ]
    
    found = 0
    not_found = 0
    errors = 0
    
    print(f"{Fore.CYAN}========== SEARCH RESULTS ==========")
    
    for site_name, url_template in websites:
        url = url_template.format(username)
        try:
            response = requests.get(url, timeout=8, allow_redirects=True)
            if response.status_code == 200:
                print(f"{Fore.GREEN}[FOUND] {site_name:<15} : {Fore.WHITE}{url}")
                found += 1
            elif response.status_code == 403:
                print(f"{Fore.YELLOW}[BLOCK] {site_name:<15} : {Fore.WHITE}Access blocked (403)")
                not_found += 1
            elif response.status_code == 429:
                print(f"{Fore.YELLOW}[RATE]  {site_name:<15} : {Fore.WHITE}Rate limited (429)")
                not_found += 1
            else:
                print(f"{Fore.RED}[NO]    {site_name:<15} : {Fore.WHITE}Not found ({response.status_code})")
                not_found += 1
        except requests.exceptions.ConnectionError:
            print(f"{Fore.RED}[ERROR] {site_name:<15} : {Fore.WHITE}Connection failed")
            errors += 1
        except requests.exceptions.Timeout:
            print(f"{Fore.RED}[ERROR] {site_name:<15} : {Fore.WHITE}Timeout")
            errors += 1
        except Exception as e:
            print(f"{Fore.RED}[ERROR] {site_name:<15} : {Fore.WHITE}{str(e)[:30]}")
            errors += 1
    
    print(f"{Fore.CYAN}=====================================")
    print(f"\n{Fore.GREEN}[FOUND] {found}")
    print(f"{Fore.RED}[NOT FOUND] {not_found}")
    print(f"{Fore.YELLOW}[ERRORS] {errors}")
    print(f"{Fore.CYAN}Total Sites Checked: {len(websites)}")
    
    input(f"\n{Fore.YELLOW}[+] Press Enter to continue...")


def main():
    """Main menu of the tool"""
    while True:
        display_banner()
        
        print(f"""
{Fore.CYAN}[1] IP Tracker
{Fore.CYAN}[2] My IP Details
{Fore.CYAN}[3] Phone Number Basic Info
{Fore.CYAN}[4] Username Tracker
{Fore.CYAN}[0] Exit
        """)
        
        try:
            choice = input(f"{Fore.YELLOW}choose from menu> {Fore.WHITE}").strip()
            
            if choice == '1':
                track_target_ip()
            elif choice == '2':
                show_my_ip()
            elif choice == '3':
                track_phone_number()
            elif choice == '4':
                track_username()
            elif choice == '0':
                print(f"{Fore.RED}\n[-] Exiting... Goodbye!")
                time.sleep(1)
                sys.exit(0)
            else:
                print(f"{Fore.RED}[-] Invalid option! Choose 0-4.")
                time.sleep(1.5)
        except KeyboardInterrupt:
            print(f"\n{Fore.RED}[-] Interrupted. Exiting...")
            sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[-] Exiting...")
        sys.exit(0)
