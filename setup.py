# encoding=utf-8
import os
from setuptools import find_packages, setup

setup(
    name='mohand',
    url='https://github.com/littlemo/mohand',
    author='moear developers',
    author_email='moore@moorehy.com',
    maintainer='littlemo',
    maintainer_email='moore@moorehy.com',
    version=os.getenv('PKG_VERSION', '0.0.0'),
    description='通用自动化处理工具',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords='mohand cli automation',
    packages=find_packages('source'),
    package_dir={'': 'source'},
    include_package_data=True,
    zip_safe=False,
    license='GPLv3',
    python_requires='>=2.7',
    project_urls={
        'Documentation': 'http://mohand.rtfd.io/',
        'Source': 'https://github.com/littlemo/mohand',
        'Tracker': 'https://github.com/littlemo/mohand/issues',
    },
    install_requires=open('requirements/pip.txt').read().splitlines(),
    entry_points={
        'console_scripts': [
            'mohand = mohand.cli:cli',
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: MacOS X',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: Chinese (Simplified)',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Communications :: Email',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Software Development :: Testing :: Unit',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Software Development :: Version Control :: Git',
        'Topic :: Terminals',
        'Topic :: Text Editors :: Emacs',
        'Topic :: Utilities',
    ],
)
