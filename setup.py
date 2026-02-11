#!/usr/bin/env python3
"""Setup script for CricSim package"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cricsim",
    version="1.0.0",
    author="Your Name",
    description="A Python cricket league simulator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/cricsim",
    py_modules=[
        "main",
        "match_simulator",
        "league_simulator",
        "teams",
        "database",
        "config_manager",
        "top_players",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Games/Entertainment",
    ],
    python_requires=">=3.7",
    install_requires=[
        # No required dependencies - all stdlib
    ],
    extras_require={
        "rich": ["rich>=10.0.0"],  # For beautiful console tables
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.9",
        ],
    },
    entry_points={
        "console_scripts": [
            "cricsim=main:main",
        ],
    },
)
