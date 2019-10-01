from setuptools import setup, find_packages

from pyhidentity import __version__, __author__, __email__, __license__

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open("README.md", encoding='utf-8') as f:
    readme = f.read()

with open("CHANGELOG.rst") as f:
    changelog = f.read()

setup(
    name="pyhidentity",
    version=__version__,
    description="hiding your real identity with python",
    long_description=readme + "\n\n" + changelog,
    license=__license__,
    author=__author__,
    author_email=__email__,
    url="https://github.com/bierschi/pyhidentity",
    packages=find_packages(),
    #data_files=[],
    install_requires=required,
    keywords=["proxy", "grabber", "pyhidentity", "public-ip", "tor", "renew-ip"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet :: Name Service (DNS)",
    ],
    entry_points={
        "console_scripts": [
            "pyhidentity = pyhidentity.pyhidentity:main",
        ],
    },
    zip_safe=False,
)
