"""Test report_temperatures.py."""
import os
import pathlib
from py._path.local import LocalPath
from tv_temp_report import report_temperatures as sut


def test_gen_key_when_key_does_not_exist(tmpdir: LocalPath):
    """Test the gen_key function."""
    key_name = tmpdir.join("the_key.txt")
    assert not os.path.exists(key_name)
    sut.gen_key(key_name)
    assert os.path.exists(key_name)
    assert len(pathlib.Path(key_name).read_text()) > 0
