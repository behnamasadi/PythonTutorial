# 1. conda
## 1.1. difference between Conda and anaconda

- **Conda** is the system that handles package management and environment management.
- **Anaconda** is a distribution – a pre-packaged collection of tools and libraries. One of the tools included in this distribution is Conda.

## 1.2. adding conda to path

`export PATH=/home/$USER/anaconda3/bin/:$PATH`


## 1.3. conda activating the base environment
Enable/ disable auto activate base: you can check this using the following command: 

`conda config --show | grep auto_activate_base`

To set it false: 

`conda config --set auto_activate_base False`

## 1.4.update
 
### 1.4.1 update conda


`conda update conda`: This command updates the Conda package manager itself to the latest version available in the currently active environment and channel. It ensures that you have the latest features, bug fixes, and performance improvements for Conda.

### 1.4.2. update anaconda
`conda update anaconda`: The Anaconda distribution is a bundled collection of various scientific libraries and tools. When you run this command, you're updating the entire Anaconda distribution within the currently active environment. Note that this might not always give you the latest versions of individual packages. Instead, it'll update to versions that are tested and confirmed to work well together by the Anaconda team.

### 1.4.3. updates packages in the currently active conda environment
`conda update --all`: This command updates all packages in the **currently active** conda environment to their latest versions, respecting the environment's constraints (i.e., ensuring compatibility between packages). It's a way to ensure that all of the libraries and tools in your current environment are up-to-date.

or you can specify the environment:  `conda update -n myenv --all`:
   


## 1.5. list all conda environments

`conda info --envs` 

or 

`conda info -e`

## 1.6.  get list of packages installed in Anaconda:

`conda list`


## 1.7. change environment location:

`conda create --prefix /tmp/test-env python=3.10`


## 1.8. create requirements.txt 

If you are using pip, export your packages to the requirements.txt:

`pip freeze > pip-requirements.txt`

To install the packages in your pip-requirements.txt file

`pip install -r pip-requirements.txt`

If you are using conda environment:

`conda list -e > conda-requirements.txt`

or 

`conda list --export > conda-requirements.txt`


To install the packages in your requirements.txt file

`conda install --file conda-requirements.txt`
 
# 2.pip

## 2.1. using pip to install packages to conda environment

```
conda create -n venv_name
conda activate venv_name
conda install pip
```

check the path for default pip: 

`which -a pip`

Now install new packages by doing:

```bash
/anaconda/envs/<env-name>/bin/pip install package_name
```
 
or you can:


```bash
python -m pip install package_name
```

- **`python -m pip install package_name`**:
This command explicitly specifies which Python interpreter to use for the installation process. By invoking `pip` using `python -m pip`, you are essentially saying, "Use the `pip` associated with this Python interpreter."

It's particularly useful when you have multiple versions of Python installed on your system or when using virtual environments. It ensures that the package is installed for the Python version you're currently using or intend to use.


- **`pip install package_name`**:
This command uses the `pip` executable directly. The system decides which `pip` to use based on your environment's configuration, such as the PATH variable in Unix-like operating systems or the system's environment variables in Windows.
If you have a single Python installation and `pip` is correctly set up in your PATH, this command works just fine and installs the package as expected.


###  2.2. list pip installed packages

`pip freeze`

or 

`pip list`



show information and location of installed packages

`pip show <package-name>`


pip default installation path (user site directory):

```
/home/$USER/.local/lib/pythonX.X/site-packages/ where X.X is the Python version.
```

show the installed path: 


```
pip list --format=freeze | cut -d "=" -f 1 | xargs -n 1 pip show | grep "Name\|Location"
```


###  update pip

`pip install --upgrade pip`
 

## Isolating a Conda environment from the global or user site packages


```
python -m site
```

provides you with a list of directories that Python searches for modules


1. **sys.path**: A list showing the paths to directories Python will search for modules. This list will include directories within the currently activated conda environment, such as its `lib/pythonX.Y/site-packages` directory, where `X.Y` is the Python version (e.g., `3.8`). This is where Python looks for installed packages.

2. **USER_BASE**: The path to the user's base directory for user installations as defined by PEP 370. This is often `~/.local` in Linux, but within a conda environment, this might not be particularly relevant.

3. **USER_SITE**: The path to the user site-packages directory. Like `USER_BASE`, this is more relevant for user installations outside of virtual environments.

4. **ENABLE_USER_SITE**: Whether the user-specific site-packages directory is enabled. This can be `True` or `False`, and within a conda environment, it's typically not as relevant since dependency management is handled by conda.

5. **site-packages directories**: Listing of all `site-packages` directories that Python will search. This will include the path to the site-packages directory within your activated conda environment, ensuring that any packages installed into the environment are available for import in your Python sessions.


to isolate your environment:

```
unset PYTHONPATH
export PYTHONNOUSERSITE=1
```
and then 

```
conda activate <conda-environment>
```

