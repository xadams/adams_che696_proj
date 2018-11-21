# -*- coding: utf-8 -*-
"""
adams_che696_proj
Class project that submits a single line of commands to a cluster
"""
from setuptools import setup

DOCLINES = __doc__.split("\n")

setup(
    # Self-descriptive entries which should always be present
    name='adams_che696_proj',
    author='xadams',
    description=DOCLINES[0],
    long_description="\n".join(DOCLINES[2:]),
    license='MIT',

    # Which Python importable modules should be included when your package is installed
    packages=['adams_che696_proj'],

    # Optional include package data to ship with your package
    # Comment out this line to prevent the files from being packaged with your software
    # Extend/modify the list to include/exclude other items as need be
    package_data={'adams_che696_proj': ["data/template*"]
                  },

    entry_points={'console_scripts': ['quick_submit = adams_che696_proj.quick_submit:main',
                                      ],
                  },     package_dir={'adams_che696_proj': 'adams_che696_proj'},

    test_suite='tests',
    # Additional entries you may want simply uncomment the lines you want and fill in the data
    # author_email='me@place.org',      # Author email
    # url='http://www.my_package.com',  # Website
    # install_requires=[],              # Required packages, pulls from pip if needed; do not use for Conda deployment
    # platforms=['Linux',
    #            'Mac OS-X',
    #            'Unix',
    #            'Windows'],            # Valid platforms your code works on, adjust to your flavor
    # python_requires=">=3.5",          # Python version restrictions

    # Manual control if final package is compressible or not, set False to prevent the .egg from being made
    # zip_safe=False,

)
