import os
from setuptools import setup

HERE = os.path.abspath(os.path.dirname(__file__))

setup(
    name="example",
    version="0.0.1",
    # Author details
    author="<Add your name>",
    author_email="<Add your email address>",
    # Choose your license
    license="All Rights Reserved",
    package_dir={"": "main"},
    entry_points={"console_scripts": ["db_import=assignment.main:main"]},
    install_requires=[
        "psycopg2==1.2.13",
    ],
    tests_require=[
        "pytest",
    ],
)
