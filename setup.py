#!/usr/bin/env python3
from pathlib import Path
from setuptools import setup

this_dir = Path(__file__).parent
module_dir = this_dir / "wyoming"
version_path = module_dir / "VERSION"
version = version_path.read_text(encoding="utf-8").strip()


# -----------------------------------------------------------------------------

setup(
    name="wyoming",
    version=version,
    description="Protocol for Rhasspy Voice Assistant",
    url="http://github.com/rhasspy/wyoming",
    author="Michael Hansen",
    author_email="mike@rhasspy.org",
    license="MIT",
    packages=["wyoming", "wyoming.util"],
    package_data={"wyoming": [str(p.relative_to(module_dir)) for p in (version_path,)]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Text Processing :: Linguistic",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="voice assistant rhasspy",
    extras_require={
        "zeroconf": ["zeroconf==0.88.0"],
        "http": ["Flask==3.0.2", "swagger-ui-py==23.9.23"],
    },
)
