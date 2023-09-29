#!/usr/bin/env python3
import setuptools
from setuptools import setup

# -----------------------------------------------------------------------------

setup(
    name="wyoming",
    version="1.2.0",
    description="Protocol for Rhasspy Voice Assistant",
    url="http://github.com/rhasspy/rhasspy3",
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
    ],
    keywords="voice assistant rhasspy",
)
