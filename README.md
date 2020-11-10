# AudNauseum

AudNausem is...


## Running AudNauseum from source code

...

### Install Python 3

Python3 must be installed to use AudNauseum. MacOS and Linux systems should already have Python3 installed.

### Clone Source Code

```
git clone https://github.com/AudNauseum/AudNauseum.git
cd AudNauseum
```

### Create Virtual Environment

```
python3 -m venv .venv
source .venv/bin/activate
```

### Install Qt C++/Python bindings

The GUI of AudNauseum uses the Qt library with PyQt5 bindings.

On Ubuntu/Debian/Linux Mint the following command must be run to install the underlying C/C++ libraries.

```
sudo apt install python3-pyqt5
```

### Install Python Libraries

```
pip install -r requirements.txt
```
