import sys
from setuptools import setup, find_packages

# we only support Python 3 version >= 3.2
if len(sys.argv) >= 2 and sys.argv[1] == "install" and sys.version_info < (3, 2):
    raise SystemExit("Python 3.2 or higher is required")


setup(
    name="igmp",
    description="IGMPv2 router-side protocol implementation for Python",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    keywords="IGMP IGMPv2 Router IPv4 Multicast Interest",
    version="1.0.4",
    url="http://github.com/pedrofran12/igmp",
    author="Pedro Oliveira",
    author_email="pedro.francisco.oliveira@tecnico.ulisboa.pt",
    license="MIT",
    install_requires=[
        'netifaces',
        'ipaddress',
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms="any",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Information Technology",
        "Topic :: System :: Networking",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.2",
)
