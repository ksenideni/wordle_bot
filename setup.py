from setuptools import find_packages, setup

setup(
    include_package_data=False,
    name='wordlebot',
    version='0,0,1',
    description='wordle game bot for telegram',
    packages=find_packages(),
    install_requires=['aiogram']
)