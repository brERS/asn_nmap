from setuptools import find_packages, setup

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="asn-nmap",
    version="0.1.1",
    author="Edgar Reis",
    description="Get status service from a ASN.",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brERS/asn_nmap",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)
