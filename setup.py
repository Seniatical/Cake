from setuptools import setup, find_packages
import re
import sys

versionInfo = sys.version_info

if (versionInfo.major < 3) and (versionInfo.minor < 8):
    sys.exit('Cannot install Cake on python version below 3.8, Please upgrade!')

version = ""

with open("cake/__init__.py") as f:
    contents = f.read()

    _match = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', contents, re.MULTILINE
    )

    version = _match.group(1)

if not version:
    raise RuntimeError("Cannot resolve version")


classifiers = [
    "Development Status :: 1 - Planning",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: MIT License",
    
    "Programming Language :: Python :: Implementation :: CPython"
    "Programming Language :: Python :: 3",

    'Topic :: Scientific/Engineering :: Mathematics',
    'Topic :: Scientific/Engineering',
]

packages = [
    'cake',
    'cake.constants',
    'cake.core',
    'cake.core.expressions',
    'cake.functions',
    'cake.expressions',
    'cake.geometry',
]

setup(
    name="Cake",
    version=version,
    description="An object orientated math library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Seniatical/Cake",
    project_urls={
        "Documentation": "https://github.com/Seniatical/Cake",
        "Issue tracker": "https://github.com/Seniatical/Cake/issues",
    },
    author="Seniatical",
    license="MIT License",
    classifiers=classifiers,
    keywords="Math,Python3,OOP",
    packages=packages,
)
