from setuptools import setup, find_packages

# Package metadata
NAME = 'space_package'
VERSION = '1.0.0'
DESCRIPTION = 'Description of space package'
AUTHOR = 'Behnam Asadi'
EMAIL = 'behnam.asadi@gmail.com'
URL = 'https://github.com/yourusername/your-package-repo'
LICENSE = 'MIT'  # Replace with the appropriate license if needed

# Define the required packages and package directories
PACKAGES = find_packages()

# Define the dependencies of your package
INSTALL_REQUIRES = [
    # List your dependencies here, e.g.,
    'numpy>=1.18.0',
    # 'requests>=2.25.1',
]

# Additional classifiers that describe your project
CLASSIFIERS = [
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
]

# Setup function call
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    license=LICENSE,
    packages=PACKAGES,
    install_requires=INSTALL_REQUIRES,
    classifiers=CLASSIFIERS,
)
