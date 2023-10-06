from setuptools import setup, find_packages

with open('requirements.txt') as f:
    REQUIREMENTS = f.readlines()

setup(
    name='wvine',
    version='0.1',
    license='MIT',
    url='https://github.com/famgz/wvine',
    packages=['wvine'],
    package_dir={'wvine': 'src/wvine'},
    include_dirs=True,
    include_package_data=True,
    install_requires=REQUIREMENTS
)
