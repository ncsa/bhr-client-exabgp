from setuptools import setup, find_packages
from glob import glob

version = '0.8'

setup(name='bhr-client-exabgp',
    version=version,
    description="BHR block manager that uses exabgp for implementing blocks",
    long_description="",
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='bhr bgp exabgp',
    author='Justin Azoff',
    author_email='JAzoff@illinois.edu',
    url='',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "requests>=2.0",
        "bhr_client>=1.0",
        "Mako==0.9.0",
    ],
    entry_points = {
        'console_scripts': [
            'bhr-client-exabgp-process = bhr_client_exabgp.process:main',
            'bhr-client-exabgp-write-template = bhr_client_exabgp.write_template:main',
        ]
    },
    scripts=glob('scripts/*'),
)
