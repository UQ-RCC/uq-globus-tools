#!/usr/bin/env python3

import setuptools

setuptools.setup(
    name='uq-globus-tools',
    version='1.0.0',
    author='Zane van Iperen',
    author_email='z.vaniperen@uq.edu.au',
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    package_data={'rccutil.globus.idmap': ['*.json']},
    entry_points={
        'console_scripts': [
            'uq-globus-idmap=rccutil.globus.idmap:climain',
            'uq-globus-idmap-dbg=rccutil.globus.idmap:main'
        ],
    },
)
