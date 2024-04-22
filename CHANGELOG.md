# Changelog

All notable changes will be added in this file starting **_v1.0.10_**. All updates before that are squashed.

## Table of Contents

- [**_v1.1.1_**](#v111)
- [**_v1.1.0_**](#v110--version-bump)
- [**_v1.0.10_**](#v1010)
- [Before **_v1.0.10_**](#before-v1010)

## CHANGELOG

### _v1.1.1_

- replaced dependecy termcolor -> colorama

- fixed windows GUI window homescreen

### _v1.1.0_ ~ Version Bump

- fixed an issue with import-export -> program was quitting unexpectedly.

- added `pasta_man/utilities/Exceptions/TerminalExceptions.py`

- added `pasta_man/architectures/terminal.py` => All terminal related stuffs were moved here from `pasta_man/pasta_man.py`

- updated `README.md`.

### _v1.0.10_

- added Import and Export Feature in CLI

- added export and imported functions in `pasta_man/architectures/targets`

- created `pasta_man/utilities/retransform.py`

- moved `pasta_man/encryption.py` => `pasta_man/utilities/encryption.py`

- moved `pasta_man/exceptions.py` => `pasta_man/utilities/Exceptions/exceptions.py`

- updated `README.md` for instructions related to importing and exporting.

### Before _v1.0.10_

- added docstrings to half of the files.

- added docstring viewer feature => `-dwl` and `--doc-w-list`

- added path viewer feature => `-p` and `--path`

- fixed and issue with the app, where the window was too short in Windows operating system.

- yanked _v1.0.5_ for major thread bugs.

- added a feature where calling `pasta-man` from the terminal, doesn't associate `pasta-man` with the terminal, but launches as a separate process => the terminal will be available for use.
  - fixed an issue in windows with new process creation by generating three windows specific files => `pasta_man.exe`, `pasta_man.vbs`, and `win-setup.bat`. All these will be done only during the first time pasta_man is opened.

  - added two entry points in pyproject.toml => `pasta-man` and `pasta-man-launcher`. `pasta-man` will launch as a separate process while `pasta-man-launcher` will execute in the terminal.

- added a clean slate feature where user/developed can remove all configurations of `pasta-man` => `-rmc` and `--remove-configurations`. **NOTE:** This is irreversible and only the configurations will be deleted such as master password and any saved settings or passwords. `pasta-man` will not be uninstalled by this.

- added a home screen in the gui.

- added themes.

- divided all codes into separate modules.
