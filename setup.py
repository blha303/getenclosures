from setuptools import setup

with open("README.rst", "rb") as f:
    long_descr = f.read().decode('utf-8')

setup(
    name = "getenclosures",
    packages = ["getenclosures"],
    install_requires = ['requests', 'beautifulsoup4', 'appdirs', 'lxml'],
    entry_points = {
        "console_scripts": ['getenclosures = getenclosures.getenclosures:main']
        },
    version = "1.0.2",
    description = "Gets all enclosure urls from an RSS feed and pipes them to stdout",
    long_description = long_descr,
    author = "Steven Smith",
    author_email = "stevensmith.ome@gmail.com",
    license = "MIT",
    url = "https://github.com/blha303/getenclosures/",
    classifiers = [
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators"
        ]
    )
