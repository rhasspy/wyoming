#!/usr/bin/env python3
from pathlib import Path
from setuptools import setup

_DIR = Path(__file__).parent
_MODULE_DIR = _DIR / "wyoming"
_VERSION = (_MODULE_DIR / "VERSION").read_text(encoding="utf-8").strip()

# -----------------------------------------------------------------------------

setup(
    name="wyoming",
    version=_VERSION,
    description="Protocol for Rhasspy Voice Assistant",
    url="http://github.com/rhasspy/wyoming",
    author="Michael Hansen",
    author_email="mike@rhasspy.org",
    license="MIT",
    packages=["wyoming", "wyoming.util"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Text Processing :: Linguistic",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="voice assistant rhasspy",
    extras_require={"zeroconf": ["zeroconf==0.88.0"]},
)
