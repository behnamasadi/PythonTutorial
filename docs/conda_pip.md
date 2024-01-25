# conda
### Difference between Conda and anaconda

- **Conda** is the system that handles package management and environment management.
- **Anaconda** is a distribution – a pre-packaged collection of tools and libraries. One of the tools included in this distribution is Conda.

### conda command not found 

`export PATH=/home/$USER/anaconda3/bin/:$PATH`

### conda create environment

`conda create -n mypython3 python=3.10`


Install additional Python packages: 
`conda install -n yourenvname [package]=<version>`

### conda activating the base environment
Enable/ disable auto activate base: you can check this using the following command: 

`conda config --show | grep auto_activate_base`

To set it false: 

`conda config --set auto_activate_base False`


### update


`conda update conda`: This command updates the Conda package manager itself to the latest version available in the currently active environment and channel. It ensures that you have the latest features, bug fixes, and performance improvements for Conda.

`conda update anaconda`: The Anaconda distribution is a bundled collection of various scientific libraries and tools. When you run this command, you're updating the entire Anaconda distribution within the currently active environment. Note that this might not always give you the latest versions of individual packages. Instead, it'll update to versions that are tested and confirmed to work well together by the Anaconda team.

`conda update -n base -c defaults conda`: This is similar to the first command but with more specificity:
   - `-n base`: This specifies that you want to update Conda in the base (or root) environment, which is the primary Conda environment that gets created upon installation.
   - `-c defaults`: This specifies the default channel from which to fetch the Conda update. Channels are like repositories that host different versions (or builds) of packages.

`conda update --all`: This command updates all packages in the currently active Conda environment to their latest versions, respecting the environment's constraints (i.e., ensuring compatibility between packages). It's a way to ensure that all of the libraries and tools in your current environment are up-to-date.

`conda update -n myenv --all`:
   

### rename a conda environment

`conda create --name new_name --clone old_name`

`conda remove --name old_name --all #` 

or its alias: 

`conda env remove --name old_name`



### list all conda environments

`conda info --envs` 

or 

`conda info -e`

### Get list of packages installed in Anaconda:

`conda list`


### Change environment location:

`conda create --prefix /tmp/test-env python=3.10`


using Google Colab with Conda:

First solution:
```
!pip install -q condacolab
import condacolab
condacolab.install()
```
Second solution:
```
!wget https://repo.anaconda.com/archive/Anaconda3-5.2.0-Linux-x86_64.sh && bash Anaconda3-5.2.0-Linux-x86_64.sh -bfp /usr/local
import sys
sys.path.insert(0, "/usr/local/lib/python3.6/site-packages/")
```
 
### create requirements.txt 

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
 
# pip

### using pip to install packages to Anaconda Environment

```
conda create -n venv_name
conda activate venv_name
conda install pip
```
or within an activated virtual environment

```
python -m pip
```

check the path for default pip: 

`which -a pip`

Now install new packages by doing: `/anaconda/envs/venv_name/bin/pip install package_name`
 
or you can:

`python -m pip install <package>` 


Refs: [1](https://stackoverflow.com/questions/41060382/using-pip-to-install-packages-to-anaconda-environment)

 
###  update pip

`pip install --upgrade pip`


###  list pip installed packages

`pip freeze`

## show information and location of installed packages

`pip show <package-name>`
 

pip default installation path:

```
/home/behnam/.local/lib/python<version>
```


The command `python -m pip` invokes the `pip` module using the Python interpreter's `-m` switch, which runs library modules as scripts.

Breaking it down:

- `python`: This is the command to start the Python interpreter. Depending on your system and how Python is installed, you might use `python3`, `py`, or some other variant to start the Python interpreter.

- `-m`: This switch tells the Python interpreter to run a module as a script. It expects the name of a module as the next argument.

- `pip`: This is the name of the module you want to run as a script. In this case, it's `pip`, which is the package installer for Python.

When combined as `python -m pip`, this command runs the `pip` module as if it were a standalone script. This can be followed by regular `pip` commands, like `install`, `uninstall`, `list`, and so on.

For instance:
- `python -m pip install requests` would install the `requests` library.
- `python -m pip list` would list all installed Python packages.

Using `python -m pip` ensures that the `pip` command being executed corresponds to the Python interpreter version you're invoking. There are several reasons why you might want to use this approach:


## Isolating a Conda environment from the global or user site packages

```
echo $PYTHONPATH
unset PYTHONPATH
export PYTHONNOUSERSITE=True
conda activate PythonTutorial
```
You can verify that your environment is isolated by checking if user site-packages are included in the Python path

```
python -m site
```


##  Install packages with pip  inside my Anaconda environment

```
which python
which pip
```

Verify Installation: 

```
pip list
```

show the installed path:

```
pip list --format=freeze | cut -d "=" -f 1 | xargs -n 1 pip show | grep "Name\|Location"
```


##  Delete all pip packages from every user

```
~/.local/lib/pythonX.X/site-packages/ where X.X is the Python version.
```


