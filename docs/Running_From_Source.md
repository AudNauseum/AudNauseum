# Run AudNauseum from source code

Please follow the instructions below to ensure your system is ready to run the AudNauseum projects. If you’ve run Python programs in the past, these steps will be familiar to you.

## Shell commands

Any commands preceded by a dollar-sign “$ “ are shell commands which will work with most shells, including bash or zsh. Lines preceded by “#” are comments for additional context.

- **MacOS**: The default shell is zsh (since Catalina) or bash for older versions
- **Linux**: Most distributions use bash as the default shell
- **Windows**: Git Bash can be used as a bash shell

### Check Python3 and Git installation

Check that Python3 (at least v3.8) is installed on your computer.

- **MacOS**: Python3 is already installed, check its version using python3 --version
- **Linux**: Python3 is already installed, modern distributions such as Ubuntu 20.04 will have at least v3.8
- **Windows**: Python3 can be installed from the official [Python site](https://www.python.org/downloads/windows/)

Check that Git is installed on your computer.

- **MacOS/Linux**: Git is already installed
- **Windows**: Git and Git Bash can be installed from the official [Git site](https://git-scm.com/)

### Clone Source Code

Clone the GitHub repository into a free folder using the following commands:

```sh
$ git clone https://github.com/AudNauseum/AudNauseum.git
$ cd AudNauseum
```

### Create Virtual Environment

Create a virtual environment so that dependencies are kept in a local folder and not installed globally.

```sh
$ python3 -m venv .venv
# MacOS / Linux
$ source .venv/bin/activate
# Windows
$ source .venv/Scripts/activate
```

### Install OS Dependencies (if necessary)

The GUI of AudNauseum uses the Qt framework with PyQt5 bindings.

On Ubuntu/Debian/Linux Mint the following command must be run to install the underlying C/C++ libraries, other Linux distributions may need to use a similar command with their package manager. Windows and MacOS users likely do not need to follow this step.

```sh
$ sudo apt install python3-pyqt5
```

### Install Python Libraries

Install the required Python libraries. While using the virtual environment, the “pip” command corresponds to the pip package manager in the virtual environment.

```sh
$ pip install -r requirements.txt
```

### Launch AudNauseum Application

Launch the application by running main.py, the entry point of the project.

```sh
$ python3 main.py
```
