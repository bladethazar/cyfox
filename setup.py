"""Setup script for Cyfox"""
from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

# Read version
version_file = Path(__file__).parent / "cyfox" / "__init__.py"
version = "1.0.0"
if version_file.exists():
    for line in version_file.read_text().splitlines():
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"').strip("'")
            break

setup(
    name="cyfox",
    version=version,
    description="Animated Desktop DevOps Buddy for Raspberry Pi Zero 2W",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/cyfox",
    packages=find_packages(),
    install_requires=[
        "pygame>=2.5.0",
        "PyYAML>=6.0",
        "requests>=2.31.0",
    ],
    extras_require={
        "rpi": [
            "RPi.GPIO>=0.7.1",
        ],
        "scanner": [
            "python-nmap>=0.7.1",
        ],
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "flake8>=6.1.0",
        ],
    },
    python_requires=">=3.11",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Topic :: System :: Hardware",
        "Topic :: System :: Monitoring",
    ],
    entry_points={
        "console_scripts": [
            "cyfox=cyfox.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "cyfox": ["../config/*.yaml", "../frontend/assets/*.png"],
    },
)

