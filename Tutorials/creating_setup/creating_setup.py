########################## setup ##########################
# setup.py is a python file, which usually tells you that the module/package you are about to install. If you have your package tree like:

#pip install -U
#or pip install --user package_name

#pip install --install-option="--prefix=$HOME/local" package_name
#python setup.py install --user


# foo
# ├── foo
# │   ├── data_struct.py
# │   ├── __init__.py
# │   └── internals.py
# ├── README
# ├── requirements.txt
# ├── scripts
# │   ├── cool
# │   └── skype
# └── setup.py


# Then, you do the following in your setup.py script so that it can be installed on some machine:

from setuptools import setup

with open("README", 'r') as f:
    long_description = f.read()

setup(
    name='foo',
    version='1.0',
    description='A useful module',
    license="MIT",
    long_description=long_description,
    author='Man Foo',
    author_email='foomail@foo.com',
    url="http://www.foopackage.com/",
    packages=['foo'],  # same as name
    install_requires=['bar', 'greek'],  # external packages as dependencies
    scripts=[
        'scripts/cool',
        'scripts/skype',
    ]
)

# a sample available at https://github.com/pytorch/vision/blob/master/setup.py
