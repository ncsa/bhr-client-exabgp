from setuptools import setup, find_packages
from glob import glob

version = '0.1'

setup(name='bhr-client-exabgp',
    version=version,
    description="BHR Client",
    long_description="",
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='passive dns',
    author='Justin Azoff',
    author_email='JAzoff@illinois.edu',
    url='',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "requests>=2.0",
        "bhr_client>=0.1"
    ],
    entry_points = {
        'console_scripts': [
            'bhr-client-exabgp-process = bhr_client_exabgp.process:main',
            'bhr-client-exabgp-write-template = bhr_client_exabgp.write_template:main',
        ]
    },
    scripts=glob('scripts/*'),
)
