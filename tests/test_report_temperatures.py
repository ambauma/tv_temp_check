"""Test report_temperatures.py."""
import builtins
import io
import os
import pathlib
from pathlib import Path
from cryptography.fernet import Fernet
from py._path.local import LocalPath
from mockito import expect, mock, contains
from tv_temp_report import report_temperatures as sut


def test_gen_key_when_key_does_not_exist(tmpdir: LocalPath):
    """Test the gen_key function when a key does not exist."""
    key_name = tmpdir.join("the_key.txt")
    assert not os.path.exists(key_name)
    sut.gen_key(key_name)
    assert os.path.exists(key_name)
    assert len(pathlib.Path(key_name).read_text()) > 0


def test_gen_key_when_key_does_exist(tmpdir: LocalPath):
    """Test the gen_key function when a key exists."""
    key_name = tmpdir.join("the_key.txt")
    with open(key_name, "wb") as bfile:
        bfile.write("I'm the key".encode())
    returned_key = sut.gen_key(key_name)
    assert returned_key.decode() == "I'm the key"


def test_credentials_when_not_cached(tmpdir: LocalPath):
    """Test credentials when credentials are not already cached."""
    expect(Path, times=1).home().thenReturn(tmpdir)
    expect(builtins, times=1).input("Enter your username for skyward: ").thenReturn("user")
    expect(sut, times=1).getpass("Enter your password for skyward: ").thenReturn("password")
    creds = sut.credentials()
    assert os.path.exists(tmpdir.join(".tv_temp_check.key"))
    assert creds[0] == "user"
    assert creds[1] == "password"


def test_credentials_when_cached(tmpdir: LocalPath):
    """Test credentials when credentials are not already cached."""
    expect(Path, times=1).home().thenReturn(tmpdir)
    key = Fernet.generate_key()
    with open(tmpdir.join(".tv_temp_check.key"), "wb") as creds_key:
        creds_key.write(key)
    fernet = Fernet(key)
    encrypted = fernet.encrypt("user\001password".encode())
    with open(tmpdir.join(".tv_temp_check.creds"), "wb") as creds_file:
        creds_file.write(encrypted)
    creds = sut.credentials()
    assert os.path.exists(tmpdir.join(".tv_temp_check.key"))
    assert creds[0] == "user"
    assert creds[1] == "password"


def test_pull_from_internet(tmp_path: Path):
    """Test the pull_from_internet function."""
    fake_handle = io.BytesIO()
    fake_handle.write('First line.\nSecond Line.'.encode())
    fake_handle.seek(0)
    expect(sut, times=1).urlopen("http://www.theurl.com").thenReturn(fake_handle)
    sut.pull_from_internet("http://www.theurl.com", tmp_path / "the_archive")
    with open(tmp_path / "the_archive", "r") as fake_archive:
        assert fake_archive.readlines() == ["First line.\n", "Second Line."]


def test_untar():
    """Test the untar function."""
    fake_tar = mock()
    expect(sut.tarfile).open("the_tar_file").thenReturn(fake_tar)
    expect(fake_tar).__enter__(...).thenReturn(fake_tar)
    expect(fake_tar).extractall("the_folder")
    expect(fake_tar).__exit__(...).thenReturn(fake_tar)
    sut.untar("the_tar_file", "the_folder")


def test_install_driver():
    """Test the install_driver function."""
    url = (
        "https://github.com/mozilla/geckodriver/releases/download/"
        "v0.27.0/geckodriver-v0.27.0-linux64.tar.gz"
    )
    expect(sut).pull_from_internet(url, "geckodriver.tar.gz")
    expect(sut).untar("geckodriver.tar.gz", "./venv/bin/")
    expect(sut).unlink("geckodriver.tar.gz")
    sut.install_driver()


def test_run_browser():
    """Test the run_browser function."""
    the_url = "https://skyward.iscorp.com/scripts/wsisa.dll/WService=wsedutrivalleyil/seplog01.w"
    mock_firefox = mock()
    mock_login_box = mock()
    mock_password_box = mock()
    mock_submit_button = mock()
    expect(sut.webdriver.firefox.webdriver, times=1).WebDriver().thenReturn(mock_firefox)
    expect(mock_firefox, times=1).get(the_url)
    expect(mock_firefox, times=1).implicitly_wait(10)
    expect(mock_firefox).find_element_by_id("login").thenReturn(mock_login_box)
    expect(mock_login_box).send_keys("user")
    expect(mock_firefox).find_element_by_id("password").thenReturn(mock_password_box)
    expect(mock_password_box).send_keys("password")
    expect(mock_firefox).find_element_by_id("bLogin").thenReturn(mock_submit_button)
    expect(mock_submit_button).click()
    sut.run_browser("user", "password")


def test_main_with_driver_already_there():
    """Test the main function with driver existing."""
    expect(sut.path, times=1).exists(contains("venv/bin/geckodriver")).thenReturn(True)
    expect(sut, times=1).credentials().thenReturn(tuple(["user", "password"]))
    expect(sut, times=1).run_browser("user", "password")
    sut.main()


def test_main_downloading_driver():
    """Test the main function with driver missing."""
    expect(sut.path, times=1).exists(contains("venv/bin/geckodriver")).thenReturn(False)
    expect(sut, times=1).install_driver()
    expect(sut, times=1).credentials().thenReturn(tuple(["user", "password"]))
    expect(sut, times=1).run_browser("user", "password")
    sut.main()
