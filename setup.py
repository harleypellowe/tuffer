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
        "appdirs",
        "certifi",
        "chardet",
        "click",
        "idna",
        "mypy-extensions",
        "oauthlib",
        "pathspec",
        "prompt-toolkit",
        "PyYAML",
        "questionary",
        "regex",
        "requests",
        "requests-oauthlib",
        "toml",
        "typed-ast",
        "typing-extensions",
        "urllib3",
        "wcwidth",
    ],
    entry_points={"console_scripts": ["tuffer = tuffer.commands.tuffer:tuffer"]},
)
