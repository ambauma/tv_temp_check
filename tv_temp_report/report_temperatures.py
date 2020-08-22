#!/usr/bin/env python3
import base64
import os
from urllib.request import urlopen
import gzip
from pathlib import Path
import sys
import tarfile
import time
from typing import Tuple
import socket
from getpass import getpass
from cryptography.fernet import Fernet
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait


def gen_key(location: str) -> bytes:
    if os.path.exists(location):
        key = open(location, "rb").read()
        return key
    else:
        key = Fernet.generate_key()
        with open(location, "wb") as key_file:
            key_file.write(key)
            print(f"Wrote encryption key to {location}")
        return key 
 

def credentials() -> Tuple[str, str]:
    """Prompt the user for credentials."""
    home = str(Path.home())
    CTRL_A = chr(1)
    creds_file = f"{home}/.tv_temp_check.creds"
    if os.path.exists(creds_file):
        f = Fernet(gen_key(f"{home}/.tv_temp_check.key"))
        with open(creds_file, "rb") as encrypted:
            encrypted_data = encrypted.read()
        decrypted_data = f.decrypt(encrypted_data)
        return tuple(decrypted_data.decode().split(CTRL_A))
    else:
        username = input("Enter your username for skyward: ")
        password = getpass("Enter your password for skyward: ")
        message = f"{username}{CTRL_A}{password}"
        f = Fernet(gen_key(f"{home}/.tv_temp_check.key"))
        encrypted = f.encrypt(message.encode())
        with open(f"{home}/.tv_temp_check.creds", "wb") as creds_file:
            creds_file.write(encrypted)
        print(f"Your credentials have been encrypted and saved at '{home}/.tv_temp_check.creds'.")
        return username, password


def pull_from_internet(url: str, file_name: str) -> None:
    """Pull a file from the internet."""
    handle = urlopen(url)
    with open(file_name, "wb") as archive:
        while True:
            data = handle.read(1024)
            if len(data) == 0:
                break
            archive.write(data)


def gunzip(gz_compressed_file: str, tar_file) -> None:
    """Remove gzip compression from a tar.gz file, leaving a tar file."""
    with gzip.open(gz_compressed_file, "rb") as compressed, open(tar_file, "wb") as extracted:
        while True:
            block = compressed.read(1024)
            if not block:
                break
            else:
                extracted.write(block)


def untar(input_file: str, extracted_folder: str):
    """Un-tar file(s) into a folder."""
    with tarfile.open(input_file) as data:
        data.extractall(extracted_folder)


def install_driver():
    """Installing the Firefox Driver."""
    url = "https://github.com/mozilla/geckodriver/releases/download/v0.27.0/geckodriver-v0.27.0-linux64.tar.gz"
    tar_gz_file = "geckodriver.tar.gz"
    pull_from_internet(url, tar_gz_file)
    #extracted_file = "geckodriver.tar"
    #gunzip(tar_gz_file, extracted_file)
    untar(tar_gz_file, "./venv/bin/")
    os.unlink(tar_gz_file)
    if os.path.exists("geckodriver.log"):
        os.unlink("geckodriver.log")
    sys.path.insert(0, f"{os.getcwd()}/")
    print(f"Path is now {sys.path}")

def run_browser(login_value: str, password_value: str):
    browser = webdriver.Firefox()
    browser.get("https://skyward.iscorp.com/scripts/wsisa.dll/WService=wsedutrivalleyil/seplog01.w")
    browser.implicitly_wait(10) # seconds
    login_id = browser.find_element_by_id("login")
    password = browser.find_element_by_id("password")
    login_id.send_keys(login_value)
    password.send_keys(password_value)
    browser.find_element_by_id("bLogin").click()


def main():
    if not os.path.exists(f"{os.getcwd()}/venv/bin/geckodriver"):
        install_driver()
    username, password = credentials()
    run_browser(username, password)

if __name__ == "__main__":
    main()
