# tv_temp_check

Automate launching the Skyward to do temperature checks at Tri-Valley schools.

[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![Issues](https://img.shields.io/github/issues-raw/ambauma/tv_temp_check.svg?maxAge=25000)](https://github.com/ambauma/tv_temp_check/issues)
![CI Build](https://github.com/ambauma/tv_temp_check/workflows/Test/badge.svg)
![Coverage](coverage.svg)

## Development Notes

### Setup

python3 -m venv venv
source venv/bin/activate
python setup.py develop

### Run tests

pytest tests/

### Run the application

python tv_temp_report/report_temperatures

### Release

```bash
pip install pyinstaller
pyinstaller --console --onefile tv_temp_report/report_temperatures.py
```
