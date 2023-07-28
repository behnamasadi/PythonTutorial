# conda
### Difference between Conda and anaconda

`Conda` and `Anaconda` are closely related but serve different roles within the data science ecosystem. Here's a breakdown of their differences:

1. **Conda**:
   - **Type**: Conda is a cross-platform, language-agnostic **package manager** and **environment management system**.
   - **Purpose**: It allows you to install software packages and manage different environments, which can be especially useful when different projects have different requirements.
   - **Languages**: While Conda was created for Python, it's not restricted to it. Conda can also manage packages from other languages like R.
   - **Scope**: Conda is concerned with ensuring that different software packages work well together and can be installed without conflict. With Conda, you can maintain isolated environments to ensure that software dependencies don't interfere with each other.
   - **Origin**: Conda is developed by Anaconda, Inc.

2. **Anaconda**:
   - **Type**: Anaconda is a **distribution** of many scientific packages and data science tools for Python and R.
   - **Purpose**: It provides a bundled collection of software out-of-the-box for people who want to do scientific computing and data analysis. Anaconda aims to simplify the setup process for new users by providing a curated set of libraries and tools.
   - **Included**: Anaconda comes with over 1500 packages, including popular libraries like NumPy, Pandas, SciPy, Scikit-learn, and more. It also includes the Conda package and environment manager.
   - **Scope**: Anaconda is a larger umbrella that provides a lot of tools, libraries, and the Conda system. Think of Anaconda as a "starter kit" for scientific computing.
   - **Origin**: Like Conda, Anaconda is also developed by Anaconda, Inc.

In essence:
- **Conda** is the system that handles package management and environment management.
- **Anaconda** is a distribution – a pre-packaged collection of tools and libraries. One of the tools included in this distribution is Conda.

There's also **Miniconda**, which provides a minimal Conda installation (just Conda and its dependencies) without the additional libraries and tools that come bundled with Anaconda. Some users prefer Miniconda to keep their setup lightweight and then install only the packages they need.

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

All of these commands are related to updating packages within the Conda ecosystem. Here's a breakdown of what each one does:

1. **`conda update conda`**:
   
   This command updates the Conda package manager itself to the latest version available in the currently active environment and channel. It ensures that you have the latest features, bug fixes, and performance improvements for Conda.

2. **`conda update anaconda`**:
   
   The Anaconda distribution is a bundled collection of various scientific libraries and tools. When you run this command, you're updating the entire Anaconda distribution within the currently active environment. Note that this might not always give you the latest versions of individual packages. Instead, it'll update to versions that are tested and confirmed to work well together by the Anaconda team.

3. **`conda update -n base -c defaults conda`**:
   
   This is similar to the first command but with more specificity:
   - `-n base`: This specifies that you want to update Conda in the base (or root) environment, which is the primary Conda environment that gets created upon installation.
   - `-c defaults`: This specifies the default channel from which to fetch the Conda update. Channels are like repositories that host different versions (or builds) of packages.

4. **`conda update --all`**:
   
   This command updates all packages in the currently active Conda environment to their latest versions, respecting the environment's constraints (i.e., ensuring compatibility between packages). It's a way to ensure that all of the libraries and tools in your current environment are up-to-date.

5. **`conda update -n myenv --all`**:
   
   Similar to the previous command, but instead of updating the currently active environment, it updates a specific environment named `myenv`. All packages within the `myenv` environment will be updated to their latest compatible versions.

To summarize:

- The first two commands focus on updating either the Conda tool itself or the bundled Anaconda distribution.
- The third command specifically updates the Conda tool in the base environment from the default channel.
- The last two commands update all packages either in the current environment or a specified one.





### rename a conda environment

`conda create --name new_name --clone old_name`

`conda remove --name old_name --all #` 

or its alias: 

`conda env remove --name old_name`



### list all conda environments

`conda info --envs` 

or 

`conda info -e`

create requirements.txt:

`conda list -e > requirements.txt`

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

`pip freeze > requirements.txt`

To install the packages in your requirements.txt file

`pip install -r requirements.txt`

If you are using conda environment:

`conda list -e > requirements.txt`

To install the packages in your requirements.txt file

`conda install --file requirements.txt`
 
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

1. **Multiple Python Versions**: 
   
   On systems where multiple versions of Python are installed (e.g., Python 2.x and Python 3.x), just using the `pip` command directly might not correspond to the Python version you think it does. Running `python -m pip` ensures you're using the `pip` associated with that specific Python version.

2. **Virtual Environments**:

   When working inside a virtual environment, you'd want to ensure that you're installing packages to that environment and not the global Python installation. Using `python -m pip` within an activated virtual environment ensures that the correct version of `pip` associated with the virtual environment is used.

3. **Avoiding PATH Issues**:

   Sometimes, especially on Windows, the `pip` command might not be in the system's PATH. Running `pip` directly might throw an error. However, if you can run the `python` command, then `python -m pip` will also work, bypassing any PATH issues.

4. **Ensuring Consistency**:

   If you're writing instructions or scripts and you want them to work regardless of the user's environment or setup, using `python -m pip` can be more consistent and reliable.

5. **Avoiding Shadowing**:

   On some systems, there might be another command or script named `pip` which could "shadow" the Python pip tool, meaning it would be called instead of the desired pip tool when the user simply types `pip`. Using `python -m pip` ensures you're calling Python's pip tool and not some other unrelated command.

6. **Explicitness**:

   Being explicit in what version of Python and pip you're using can prevent unexpected behaviors, especially in shared or diverse development environments.

For all these reasons, `python -m pip` can be a safer and more explicit way to ensure you're using the `pip` associated with your intended Python interpreter.

