import codecs
import os
import re
from setuptools import setup


setup(
    name='usps-api',
    version='0.1,
    author='Tobin Brown',
    author_email='tobin@brobin.me',
    packages=['usps'],
    include_package_data=True,
    url='http://github.com/brobin/usps-api',
    license='MIT',
    description='Python wrapper for the USPS API',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
    ],
    keywords='usps shipping',
    long_description=open('README.rst', 'r').read(),
    install_requires=['requests', 'lxml', 'xmltodict'],
    zip_safe=False,
)