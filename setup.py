"""Set up this project."""
#!/usr/bin/env python

from distutils.core import setup
import setuptools  # pylint: disable=unused-import

TEST_DEPS = [
    "pytest-cov==2.*",
    "pytest-mockito==0.*",
    "pytest-pylint==0.17.*",
    "flake8==3.*",
    "black==19.10b0",
    "coverage-badge==1.0.1",
]

setup(
    name="TvTempReport",
    version="0.1.0",
    description="Report child temperatures to Tri-Valley.",
    author="ambauma",
    author_email="ambauma@users.noreply.github.com",
    url="https://github.com/ambauma/tv_temp_check",
    packages=["tv_temp_report"],
    test_requires=TEST_DEPS,
    extras_require={"TEST": TEST_DEPS,},
    install_requires=[
        "selenium==3.*",
        "wheel==0.*",
        "setuptools==49.*",
        "cryptography==3.0",
    ],
    entry_points={
        "console_scripts": [
            "tv_temp_check = tv_temp_report.report_temperatures:main"
        ]
    }
)
