#!/usr/bin/env python

from setuptools import setup, find_packages
import os

setup(
    name='grepbible',
    version = os.environ.get('CI_COMMIT_TAG', '0.0.0-dev'),
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'gbib=grepbible.cli:main',
        ],
    },
    author='Maxim Litvak',
    author_email='maxim@litvak.eu',
    description='A CLI tool to look up Bible verses locally.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'requests',  # List other dependencies as needed
    ],
    keywords=['bible', 'KJV'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Education',
        'Topic :: Religion'
        ],
    url='https://gitlab.com/maxlit/grepbible',
    license='MIT',
)