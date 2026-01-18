#!/usr/bin/env python3
"""Setup script for TechLang."""
from setuptools import setup, find_packages

setup(
    name="techlang",
    version="1.0.0",
    description="A hacker-themed, stack-based programming language",
    author="TechLang Team",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "requests",
        "Pillow",
    ],
    extras_require={
        "dev": ["pytest"],
        "gui": ["customtkinter"],
        "web": ["flask"],
    },
    py_modules=["cli", "tlpm"],
    entry_points={
        "console_scripts": [
            "tl=cli:main",
            "tlpm=tlpm:main",
        ],
    },
)
