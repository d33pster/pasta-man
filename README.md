[![Continuous Deployment](https://github.com/d33pster/pasta-man/actions/workflows/ContinuousDeployment.yml/badge.svg)](https://github.com/d33pster/pasta-man/actions/workflows/ContinuousDeployment.yml)
![PyPI - Version](https://img.shields.io/pypi/v/pasta-man)
![PyPI - Status](https://img.shields.io/pypi/status/pasta-man)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pasta-man)
![Libraries.io dependency status for latest release](https://img.shields.io/librariesio/release/pypi/pasta-man)
![PyPI - License](https://img.shields.io/pypi/l/pasta-man)


# Overview
Pasta-Man is a software application designed to securely store passwords and sensitive information in an encrypted format. It provides users with a convenient way to manage their passwords, ensuring they are protected from unauthorized access. 

## Motivation
 - In the digital login password age we need a one stop vault for storing all our login credentials with concerned of atmost  security.
 - The repeated use of single password in multiple accounts may lead to data breach or loss of data.
 - Weak passwords are easy to interpreat for attackers, use of strong passwords is recommended,but it is difficult to remember complex passwords.
 - Mostly passwords written in somewhere lead to comprosing of data and privacy of user.

## Features
 <!-- - Securely Managing Passwords
 - Copy passwords to the clipboard
 - One master password for all
 - Exporting all passwords in desired file format
 - Encrypting passwords
 - Search Password by target name/username -->

### Secure Management of Passwords
`Pasta-Man` uses tripple layer encryption for saving passwords. Once `Pasta-Man` is provided with a password to manage, it encrypts it with a Master Password and stores it in a file, which then again is encrypted with the master password. The so called Master password is stored as an encrypted string (this encryption is done using password and salt not known to users.).

The user will be prompted to provide a master password if it is the first use. If not, `Pasta-Man` will work as usual.

### Tags
`Pasta-Man` stores passwords with tags such as target (the target application or link or any platform the password is meant for), target-type (target-type can be an app or link or any other category defined by the user. --- `Pasta-Man` supports creation of user defined tags and can easily fetch search results for the same.).

### Search
User can search for passwords using keywords in keyword-types.

`For Example:`<br>
If there is a target (say, abcde) which contains a keyword (say, abc), the user can search `abc` in `keyword-type == target`. Similarly, if there is a target-type (say, link) which contains a keyword (say, github), the user can search for `github` in `keyword-type == target-type`.

### Copy to Clipboard
Upon [Search](#search), `Pasta-Man` allows to copy the password for the found match to user's clipboard (given, the user provides the master password), instead of revealing it because of bad management. `Pasta-Man` also allows to Remove that match search result.

### Faster than basic tkinter apps
`Pasta-Man` actively uses Threads to carry out intensive tasks in order to minimize GUI lag as well as have better performance than any basic app created through python tkinter lib.

### Import-Export Passwords
`Pasta-Man` _v1.0.10_ onwards supports importing and exporting of passwords. **Note:** `Pasta-Man` can only import passwords that were exported by `Pasta-Man`. This Import/Export Feature is a solution to changing your PC or system.

Be relieved that the exported passwords will be in encrypted format.

- **Export Format:** `Pasta-Man` will append all the passwords encrypted by master password and all the data associated with it, to the encrypted master password into the output format chosen by user.

- **Import Mechanism:** `Pasta-Man` will decrypt the master password associated with the passwords file and then decrypt all the data appended to it and then encrypt the data and passwords by using the current system master password, then append it to the currently existing passwords. And finally encrypt everything again.

- **Usage:**
    ```bash
    pasta-man -e <output-file-format> # or pasta-man --export <output-file-format>

    pasta-man -i # or pasta-man --import
    ```

    Both of the commands above will trigger a file/directory selector dialog for selecting the desired directory or files.


### Themes
User can now change Theme for the app from the Menu Bar. Default is `Arc`. Whatever theme the user chooses, It will be set as default and next time `Pasta-Man` is launched, that theme will be loaded.

Themes can be changed using the MenuBar -

<img src="images/MenuBar.png">

###### <p align='center'>MenuBar Screenshot<p>

#### Currently Supported Themes

- Adapta
- Arc
- Aquativo
- Black
- Blue
- Breeze
- Clearlooks
- Elegance
- Equilux
- Keramic
- Kroc
- Plastik
- Radiance (Ubuntu)
- Smog
- Win XP
- Yaru

## Code Description

To know more about the code structure and module information like - 

- Modules that are imported
    
    - Internal (all the modules used that already come with your python interpreter)

    - External (all the modules used that were installed using pip, these are also mentioned in pyproject.toml and requirements.txt)

    - Project specifiv (all the modules used that were specifically created for this project.)

- Hierarchy
    
    The hierarchy of classes and functions.

- Individial Object Descriptions

    Descriptions about individual components of the code such as funtions and parameters.

- Working

    If there is any working rule or basic working of the module.

All these can be seen by running the following commands:

```console
# pasta-man v1.0.9 and above supports docstring fetching, and can be done using:

# in the terminal/CMD, run
$ pasta-man -dwl # for docs with listing of hierarchy.
```

## Dependencies
- Python>=3.9
- pandas
- tk
- ttkthemes
- termcolor
- pyperclip
- optioner>=1.5.2
- cryptography
- pyinstaller

## Installation

Easily install pasta-man using pip.

```bash
pip install pasta-man==1.1.0
```

## README before [#Usage](#usage)

After update _v1.0.4_, `pasta-man` launches as a separate process. There are two commands that gets installed with `pip install pasta-man>=1.0.4` -> `pasta-man` and `pasta-man-launcher`.

- `pasta-man` Command

    - This command will launch `pasta-man` as a separate and independent process.
    
    - The terminal will be usable after `pasta-man` command is run.
    
    - The output logs will be stored in -> `HOME/.pastaman/.log` in Linux and MacOS.

- `pasta-man-launcher` Command
    
    - This will launch `pasta-man` in the terminal.

    - The terminal wont be available until this process is running.

    - All outputs will be logged in `stdin` (in the terminal screen)

## Usage

- To run `Pasta-Man`, run the following in the terminal/CMD.

    ```bash
    pasta-man
    ```

- To show version information, run the following in terminal/CMD
    ```bash
    pasta-man -v # or pasta-man --version
    ```

## Troubleshooting

- Windows
    - Running `pasta-man` for the first time will trigger a setup mechanism. If the setup fails for any reason, run the following commands in the CMD.

        ```batch
        pasta-man -rmc
        ```
        
        or

        
        ```batch
        pasta-man --remove-configurations
        ```
        And then run `pasta-man` again.
    
    - For Complete list of Developer Options of pasta-man, run the following commands.

        ```batch
        pasta-man -h
        ```
        
        or

        ```batch
        pasta-man --help
        ```

## Uninstall

Uninstall using pip

```bash
pip uninstall pasta-man
```

## Yanked Versions
- _v1.0.5_
    
    `Major Bug`: After Threads Update and Threads Patch 1, There was a major bug where the code breaks while initializing the app for the first time.
