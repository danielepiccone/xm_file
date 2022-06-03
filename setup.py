from setuptools import setup, find_packages
from xm_file import __version__

setup(
    name="xm_file",
    version=__version__,
    url="https://github.com/danielepiccone/xm_file.git",
    author="Daniele Piccone",
    author_email="mild.taste@gmail.com",
    description="XM (Fasttracker II) module file reader",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[],
)


