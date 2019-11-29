# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='mockgcp',
    version='0.1.0',
    description='A library that allows to mock out GCP services in unit tests.',
    long_description=readme,
    author='Alexandra Abbas',
    author_email='alexandra.abbas@datatonic.com',
    url='https://github.com/alexandraabbas/mock-gcp',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')))
