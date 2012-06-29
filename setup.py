#!/usr/bin/env python
import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def run_setup():
    setup(
        name='transporter',
        version='0.0.1',
        description='A Mail transport for humans',
        keywords = 'smtp',
        url='https://github.com/philipcristiano/transporter',
        author='Philip Cristiano',
        author_email='transporter@philipcristiano.com',
        license='BSD',
        packages=[''],
        install_requires=[
            "flask",
            "marrow.mailer",
        ],
        test_suite='tests',
        long_description=read('README.md'),
        zip_safe=True,
        classifiers=[
            "Development Status :: 2 - Pre-Alpha",
            "License :: OSI Approved :: BSD License",
        ],
        entry_points="""
        [console_scripts]
        """,
    )

if __name__ == '__main__':
    run_setup()
