"""Setup script for Raven"""

import os.path
import setuptools
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

setup(
    name="imageviewer",
    version="0.1",
    description="Image Viewer Widget for Jupyter Notebooks",
    url="https://github.com/hyperparameters/imageviewer",
    author="Tushar Kolhe",
    author_email="tushark.engg@outlook.com",
    license="MIT",
    packages=setuptools.find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        "ipywidgets"])

