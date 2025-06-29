#!/usr/bin/env python3
import os
import sys
from dotenv import load_dotenv
from outline_vpn.outline_vpn import OutlineVPN, OutlineServerErrorException
from colorama import Fore, Style, init
import dict_file

# Инициализация colorama
init(autoreset=True)

# Загрузка переменных окружения
config_path = "/usr/local/bin/config.env"
load_dotenv(config_path)

# Константы API
CENTOS_API_URL = os.getenv("CENTOS_API_URL")
CENTOS_CERT_SHA256 = os.getenv("CENTOS_CERT_SHA256")
UBUNTU_API_URL = os.getenv("Ubuntu_API_URL")
UBUNTU_CERT_SHA256 = os.getenv("Ubuntu_CERT_SHA256")

# Справка по командам
help_descriptions = dict_file.help_descriptions

# Инициализация OutlineVPN менеджера
def init_outline_manager(server_name):
    if server_name == 'u':
        return OutlineVPN(api_url=UBUNTU_API_URL, cert_sha256=UBUNTU_CERT_SHA256)
    elif server_name == 'c':
        return OutlineVPN(api_url=CENTOS_API_URL, cert_sha256=CENTOS_CERT_SHA256)
    else:
        print(f"{Fore.RED}❌ Неизвестный сервер: {Fore.LIGHTWHITE_EX}{server_name}")
        sys.exit(1)

# Утилиты
def bytes_to_gb(bytes_val):
    return bytes_val / (1024 ** 3) if isinstance(bytes_val, int) else 0

def server_name_style(server_name):
    if server_name == 'c':
        host = 'vdsina.com'
        server_os = 'CentOS 7'
    elif server_name == 'u':
        host = 'timeweb.cloud'
        server_os = 'Ubuntu 24'
    else:
        host = 'Неизвестно'
        server_os = 'N/A'
    print(f"{Style.BRIGHT}{Fore.LIGHTWHITE_EX}{host} — {Fore.CYAN}{server_os}")

def all_keys():
    return outline_manager.get_keys()

def client_info(key):
    print(f"{Style.BRIGHT}{Fore.CYAN}ID ключа:        {Fore.LIGHTWHITE_EX}{key.key_id}")
    print(f"{Style.BRIGHT}{Fore.CYAN}Имя ключа:       {Fore.LIGHTWHITE_EX}{key.name}")
    print(f"{Style.BRIGHT}{Fore.CYAN}Использовано:    {Fore.BLUE}{bytes_to_gb(key.used_bytes):.2f} GB")
    print(f"{Style.BRIGHT}{Fore.CYAN}Ключ доступа:    {Fore.GREEN}{key.access_url}")

# Основные команды
def list_keys(server_name):
    server_name_style(server_name)
    print(f"{Style.BRIGHT}{Fore.BLUE}-- Список ключей --")
    for key in all_keys():
        client_info(key)
        print(f"{Fore.LIGHTBLACK_EX}{'-'*80}")

def inspect_key(server_name):
    server_name_style(server_name)
    try:
        key_id = input(f"{Style.BRIGHT}{Fore.CYAN}ID Ключа: {Fore.YELLOW}")
        key = outline_manager.get_key(key_id)
        client_info(key)
    except OutlineServerErrorException:
        print(f"{Fore.RED}❌ Ошибка: {Fore.LIGHTWHITE_EX}Ключа с таким ID не существует.")

def create_new_key(server_name):
    server_name_style(server_name)
    print(f"{Style.BRIGHT}{Fore.BLUE}-- Создание нового ключа --")
    name = input(f"{Fore.CYAN}Введите название ключа: {Fore.YELLOW}")
    key_id = input(f"{Fore.CYAN}Введите ID ключа: {Fore.YELLOW}")
    key = outline_manager.create_key(key_id=key_id, name=name)
    print(f"{Fore.GREEN}✅ Ключ создан! Ссылка доступа: {Style
