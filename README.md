# pm-cookie-cutter

_pm-cookie-cutter_ (Poor man's cookie cutter) is a single-file python script with the sole purpose to help scaffold out a folder structure for creating python packages that can be installed using `pip`. Perhaps humourously this project doesn't comply with the required file structure.

# Installation

git clone this repository.

# Usage

Linux:

`python3 ./pmcc.py`

Windows:

`py.exe .\pmcc.py`

Then follow the prompts. This will then create a project in the target location like so

```
Project name [pm-cookie-cutter]: this-is-a-test
Description []: This is a small test for documentation reasons.
Project location [C:\Users\myuser\code\pm-cookie-cutter\this-is-a-test]: ..\..\this-is-a-test
Requires Python [>=3.10]:
Home page URL []: https://github.com/myuser/this-is-a-test
Issues URL []: https://github.com/myuser/this-is-a-test/issues

author.name: <tries to get this from git config --global list>
author.email: <tries to get this from git config --global list>
name: this-is-a-test
description: This is a small test for documentation reasons.
location: C:\Users\Emil\Documents\code\this-is-a-test
requires_python: >=3.10
homepage: https://github.com/myuser/this-is-a-test
issues: https://github.com/myuser/this-is-a-test/issues

Look Okay? [Y]:y
```

This then creates a directory in `C:\Users\myuser\code\` with the following structure

```
- this-is-a-test
  \- src
    \- this-is-a-test
      \- resources
    - __init__.py
  \- tests
  - LICENSE
  - pyproject.toml
  - README.md
  - setup.py
```

Navigate to your project's directory and run `pip install -e .` to install your module as an editable module. Make and save changes until you're ready to upload to PyPI.
