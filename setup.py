"""Setup script for Raven"""

import os.path
import setuptools
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

setup(
    name="jupyter_widgets",
    version="0.1",
    description="Widgets for Jupyter Notebooks",
    url="https://github.com/hyperparameters/jupyter-widgets",
    author="Tushar Kolhe",
    author_email="tushark.engg@outlook.com",
    license="MIT",
    packages=setuptools.find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        "ipywidgets"])

