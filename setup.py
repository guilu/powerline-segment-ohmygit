from setuptools import setup, find_packages

setup(
    name='plohmygit',
    version='0.1.0',
    author='Diego Barrio H',
    author_email='diegobarrioh@gmail.com',
    packages=find_packages(),
    namespace_packages=['plohmygit']
    scripts=['bin/plohmygit.py'],
    url='http://diegobarrioh.es/plohmygit/',
    license='LICENSE.txt',
    description='Module for powerline based on oh-my-git',
    long_description=open('README.md').read()
)