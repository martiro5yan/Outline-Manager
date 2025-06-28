#!/usr/bin/env python3
import os
import sys
from dotenv import load_dotenv
from outline_vpn.outline_vpn import OutlineVPN, OutlineServerErrorException
from colorama import Fore, Style, init, Back
import dict_file

# Инициализация colorama
init(autoreset=True)

# Загрузка переменных окружения
load_dotenv('config.env')

# Константы API
CENTOS_API_URL = os.getenv("Centos_API_URL")
CENTOS_CERT_SHA256 = os.getenv("Centos_CERT_SHA256")

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
        print(f"{Fore.RED}❌ Неизвестный сервер: {server_name}")
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
    print(f"{Back.BLACK}{Fore.WHITE}{host} -- {server_os}")

def all_keys():
    return outline_manager.get_keys()

def client_info(key):
    """Печатает информацию о конкретном ключе"""
    print(f"{Style.BRIGHT + Fore.CYAN}ID ключа: {Back.BLACK}{Fore.WHITE}{key.key_id}")
    print(f"{Style.BRIGHT + Fore.CYAN}Имя ключа: {Back.BLACK}{Fore.WHITE}{key.name}")
    print(f"{Style.BRIGHT + Fore.CYAN}Использовано: {Fore.BLUE}{bytes_to_gb(key.used_bytes):.2f} GB")
    print(f"{Style.BRIGHT + Fore.CYAN}Ключ: {Fore.GREEN}{key.access_url}")

# Основные команды
def list_keys(server_name):
    """Выводит список всех ключей"""
    server_name_style(server_name)
    print(f"{Style.BRIGHT}{Fore.BLUE}-- Список ключей --")
    for key in all_keys():
        client_info(key)
        print(f"{Back.BLACK}{Fore.WHITE}{'-'*100}")

def inspect_key(server_name):
    """Просмотр информации по ключу по ID"""
    server_name_style(server_name)
    try:
        key_id = input(f"{Style.BRIGHT + Fore.CYAN}ID Ключа: {Fore.WHITE}")
        key = outline_manager.get_key(key_id)
        client_info(key)
    except OutlineServerErrorException:
        print(f"{Fore.BLUE}❌ Ошибка: {Fore.WHITE}Ключа с таким ID не существует.")

def create_new_key(server_name):
    """Создание нового ключа"""
    server_name_style(server_name)
    print(f"{Style.BRIGHT}{Fore.BLUE}-- Создание нового ключа --")
    name = input(f"{Fore.CYAN}Введите название ключа: {Fore.YELLOW}")
    key_id = input(f"{Fore.CYAN}Введите ID ключа: {Fore.YELLOW}")
    key = outline_manager.create_key(key_id=key_id, name=name)
    print(f"{Fore.GREEN}✅ Ключ создан! Ссылка доступа: {Style.BRIGHT}{key.access_url}")

def delete_key(server_name):
    """Удаление ключа по ID"""
    server_name_style(server_name)
    print(f"{Style.BRIGHT}{Fore.RED}-- Удаление ключа --")
    key_id = input(f"{Fore.CYAN}Введите ID ключа для удаления: {Fore.YELLOW}")
    outline_manager.delete_key(key_id)
    print(f"{Fore.GREEN}🗑️ Ключ {key_id} успешно удалён.")

def stop_key(server_name):
    """Отключить ключ без удаления"""
    key_id = input('ID ключа для отключения: ')
    outline_manager.set_key_enabled(key_id, enabled=False)
    print("Ключ отключён.")

def get_service_info(server_name):
    """Получить общую информацию о сервере"""
    server_name_style(server_name)
    info = outline_manager.get_server_information()
    print(info)

def total_consumption_list(server_name):
    """Выводит список всех ключей с трафиком"""
    server_name_style(server_name)
    print("-" * 70)
    print(f"{Style.BRIGHT + Fore.BLUE}{'Имя ключа':<25} {'Использовано (байт)':>20} {'Использовано (GB)':>20}")
    print("-" * 70)
    for key in all_keys():
        used = int(key.used_bytes) if key.used_bytes is not None else 0
        gb = bytes_to_gb(used)
        print(f"{key.name:<25} {used:>20,} {gb:>20.2f}")
    print("-" * 70)

def total_consumption_sum(server_name):
    """Суммарный трафик всех ключей"""
    server_name_style(server_name)
    summ = sum(int(k.used_bytes or 0) for k in all_keys())
    print(f"{Style.BRIGHT + Fore.BLUE}Итоговое потребление: {Fore.WHITE}{bytes_to_gb(summ):.2f} GB")

def total_consumption_all(server_name):
    """Показать и список и итог"""
    total_consumption_list(server_name)
    total_consumption_sum(server_name)

# Словарь команд
dictionary_commands = {
    'lk': list_keys,
    'ci': inspect_key,
    'ck': create_new_key,
    'dk': delete_key,
    'info': get_service_info,
    'tc': total_consumption_all,
    'tc-list': total_consumption_list,
    'tc-sum': total_consumption_sum
}
available_commands = ", ".join(dictionary_commands.keys())

# Основная функция
def main(func_name, server_name):
    if func_name in dictionary_commands:
        dictionary_commands[func_name](server_name)
    else:
        print(f"{Fore.RED}❌ Команда '{func_name}' не существует. Доступные: {available_commands}")

# Точка входа
if __name__ == "__main__":
    if '--help' in sys.argv or '-h' in sys.argv:
        print(f"{Fore.CYAN}Использование: python om.py [c|u] [команда]")
        print(f"{Fore.CYAN}c - CentOS 7 сервер (vdsina.com)")
        print(f"{Fore.CYAN}u - Ubuntu 24 сервер (timeweb.cloud)")
        print(f"\n{Fore.CYAN}Доступные команды:\n")
        for cmd, desc in help_descriptions.items():
            print(f"  {Fore.YELLOW}{cmd:<10} {Fore.RESET}{desc}")
        sys.exit(0)

    if len(sys.argv) < 3:
        print(f"{Fore.RED}❌ Использование: python om.py [c|u] [команда]")
        sys.exit(1)

    server_name = sys.argv[1]
    func_name = sys.argv[2]

    outline_manager = init_outline_manager(server_name)
    main(func_name, server_name)
