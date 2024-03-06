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

#!/usr/bin/env python


setup(name='powerindex',
    version = os.environ.get('CI_COMMIT_TAG', '0.0.0-dev'),
    description='python library to calculate power indices in weighted voting games',
    long_description=long_description,  # Include the long description
    long_description_content_type='text/plain',  # Specify the content type, can be 'text/markdown' for Markdown
    author='Maxim Litvak',
    author_email='maxim@litvak.eu',
    url='http://gitlab.com/maxlit/powerindex',
    test_suite='test',
    packages=['powerindex'],
    keywords=['power index','voting','Banzhaf','Shapley','Shubik', 'weighted voting game','game theory', 'political science', 'contested garment rule'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Education',
        'Topic :: Sociology'
        ],
    entry_points={
        'console_scripts': [
            'px = powerindex.powerindex:main'
        ]
        }
                                         )