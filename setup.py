from setuptools import find_namespace_packages
from setuptools import setup

setup(
    name="tuffer",
    packages=find_namespace_packages(),
    version="0.0.1",
    description="Tuffer",
    author="Harley Pellowe",
    author_email="hpellowe@gmail.com",
    install_requires=[
        "pyyaml",
        "questionary",
        "requests",
        "requests-oauthlib",
        "click",
    ],
    entry_points={
        "console_scripts": ["tuffer = tuffer.commands.tuffer:tuffer"]
    },
)
