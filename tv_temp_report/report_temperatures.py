#!/usr/bin/env python3
"""Open a Skyward window to report temperatures."""
import platform
import tempfile
import os
from os import unlink, path, getcwd
from urllib.request import urlopen
from pathlib import Path
import tarfile
from typing import Tuple
from getpass import getpass
from cryptography.fernet import Fernet
from zipfile import ZipFile
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


def gen_key(location: str) -> bytes:
    """Generate a key for the symmetric encryption."""
    if path.exists(location):
        key = open(location, "rb").read()
        return key
    key = Fernet.generate_key()
    with open(location, "wb") as key_file:
        key_file.write(key)
        print(f"Wrote encryption key to {location}")
    return key


def credentials() -> Tuple[str, str]:
    """Prompt the user for credentials."""
    home = str(Path.home())
    ctrl_a = chr(1)
    creds_file = f"{home}/.tv_temp_check.creds"
    if path.exists(creds_file):
        fernet = Fernet(gen_key(f"{home}/.tv_temp_check.key"))
        with open(creds_file, "rb") as encrypted:
            encrypted_data = encrypted.read()
        decrypted_data = fernet.decrypt(encrypted_data)
        return tuple(decrypted_data.decode().split(ctrl_a))

    username = input("Enter your username for skyward: ")
    password = getpass("Enter your password for skyward: ")
    message = f"{username}{ctrl_a}{password}"
    fernet = Fernet(gen_key(f"{home}/.tv_temp_check.key"))
    encrypted = fernet.encrypt(message.encode())
    with open(f"{home}/.tv_temp_check.creds", "wb") as creds_file:
        creds_file.write(encrypted)
    print(
        f"Your credentials have been encrypted and saved at '{home}/.tv_temp_check.creds'."
    )
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


def unzip(input_file: str, extracted_folder: str):
    """Un-zip file(s) into a folder."""
    with ZipFile(input_file, "r") as data:
        data.extractall(extracted_folder)


def untar(input_file: str, extracted_folder: str):
    """Un-tar file(s) into a folder."""
    with tarfile.open(input_file) as data:
        def is_within_directory(directory, target):
        	
        	abs_directory = os.path.abspath(directory)
        	abs_target = os.path.abspath(target)
        
        	prefix = os.path.commonprefix([abs_directory, abs_target])
        	
        	return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
        	for member in tar.getmembers():
        		member_path = os.path.join(path, member.name)
        		if not is_within_directory(path, member_path):
        			raise Exception("Attempted Path Traversal in Tar File")
        
        	tar.extractall(path, members, numeric_owner=numeric_owner) 
        	
        
        safe_extract(data, extracted_folder)


def install_driver():
    """Installing the Firefox Driver."""
    version = "v0.27.0"
    os_platform = "win64.zip" if platform.system() == "Windows" else "linux64.tar.gz"
    url = (
        "https://github.com/mozilla/geckodriver/releases/download/"
        f"{version}/geckodriver-{version}-{os_platform}"
    )
    compressed_file = f"geckodriver-{version}-{os_platform}"
    pull_from_internet(url, compressed_file)
    if platform.system() == "Windows":
        unzip(compressed_file, tempfile.gettempdir())
    else:
        untar(compressed_file, tempfile.gettempdir())
    unlink(compressed_file)


def run_browser(login_value: str, password_value: str):
    """Interact with the web browser."""
    file_extension = ".exe" if platform.system() == "Windows" else ""
    print(
        f"Geckodriver location {tempfile.gettempdir() + os.path.sep + 'geckodriver' + file_extension}"
    )
    browser = webdriver.firefox.webdriver.WebDriver(
        executable_path=tempfile.gettempdir()
        + os.path.sep
        + "geckodriver"
        + file_extension
    )
    browser.get(
        "https://skyward.iscorp.com/scripts/wsisa.dll/WService=wsedutrivalleyil/seplog01.w"
    )
    browser.implicitly_wait(10)  # seconds
    browser.find_element_by_id("login").send_keys(login_value)
    browser.find_element_by_id("password").send_keys(password_value)
    browser.find_element_by_id("bLogin").click()


def main():
    """Run the application."""
    file_extension = ".exe" if platform.system() == "Windows" else ""
    if not path.exists(f"{tempfile.gettempdir()}/geckodriver{file_extension}"):
        install_driver()
    username, password = credentials()
    run_browser(username, password)


if __name__ == "__main__":
    main()
