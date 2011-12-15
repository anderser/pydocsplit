#!/usr/bin/env python

from setuptools import setup

setup(
    name='pydocsplit',
    version='0.2.0',
    description="A toolkit for splitting PDFs and documents to images and text. Based on ProPublicas's Docsplit (Ruby)",
    long_description=open('README.md').read(),
    author='Anders Eriksen',
    author_email='anders@anderser.no',
    url='http://github.com/anderser/pydocsplit',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Topic :: Multimedia :: Graphics :: Graphics Conversion',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ],
    packages=[
        'pydocsplit'
    ],
)