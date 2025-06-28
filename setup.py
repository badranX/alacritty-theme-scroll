import os
from setuptools import setup, find_packages

setup(
    name="alacritty_theme_scroll",
    version="0.0.2",
    author="Yahya Badran",
    author_email="techtweaking@gmail.com",
    description="pick your alacritty theme by scrolling and live updating",
    url="https://github.com/badranx/alacritty-theme-scroll",
    install_requires=["GitPython >=3.1.42", "toml", "tqdm"],
    packages=[
        package
        for package in find_packages()
        if package.startswith("alacritty_theme_scroll")
    ],
    entry_points={
        "console_scripts": [
            "alacritty-scroll = alacritty_theme_scroll.main:run",
        ],
    },
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
