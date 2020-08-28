#!/usr/bin/env python3
"""Open a Skyward window to report temperatures."""
from os import unlink, path, getcwd
from urllib.request import urlopen
from pathlib import Path
import tarfile
from typing import Tuple
from getpass import getpass
from cryptography.fernet import Fernet
from selenium import webdriver


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


def untar(input_file: str, extracted_folder: str):
    """Un-tar file(s) into a folder."""
    with tarfile.open(input_file) as data:
        data.extractall(extracted_folder)


def install_driver():
    """Installing the Firefox Driver."""
    version = "v0.27.0"
    url = (
        "https://github.com/mozilla/geckodriver/releases/download/"
        f"{version}/geckodriver-{version}-linux64.tar.gz"
    )
    tar_gz_file = "geckodriver.tar.gz"
    pull_from_internet(url, tar_gz_file)
    untar(tar_gz_file, "./venv/bin/")
    unlink(tar_gz_file)


def run_browser(login_value: str, password_value: str):
    """Interact with the web browser."""
    browser = webdriver.firefox.webdriver.WebDriver()
    browser.get(
        "https://skyward.iscorp.com/scripts/wsisa.dll/WService=wsedutrivalleyil/seplog01.w"
    )
    browser.implicitly_wait(10)  # seconds
    browser.find_element_by_id("login").send_keys(login_value)
    browser.find_element_by_id("password").send_keys(password_value)
    browser.find_element_by_id("bLogin").click()


def main():
    """Run the application."""
    if not path.exists(f"{getcwd()}/venv/bin/geckodriver"):
        install_driver()
    username, password = credentials()
    run_browser(username, password)


if __name__ == "__main__":
    main()
