# About
Pre-assignment for Reaktor's 2020 junior dev positions. A hosted version should be available [here](https://kimsappi-dpkg-status.herokuapp.com/).

The goal of the exercise was to parse the contents of `/var/lib/dpkg/status` (containing package information for Debian-based distributions) and display them in an HTML interface, listing the following information about each package:
* name
* description
* dependencies
* reverse dependencies (packages that depend on current package)
* (reverse) dependencies should link to the package in question

Contrary to the original spec I also check the Pre-Depends field for dependencies.

There's also a JSON API available through [/api/](https://kimsappi-dpkg-status.herokuapp.com/api/) and it's documentation can be found at [/apiDocs](https://kimsappi-dpkg-status.herokuapp.com/apiDocs).

# Requirements
One of the goals of the exercise was to avoid extraneous dependencies. Therefore this implementation is quite standard, requiring only:
* Python 3 (>= 3.6 or so, for f-string support)
* Flask (Python web framework)
* sqlite3 and similar modules that should be included with Python

# Instructions
```shell
git clone https://github.com/kimsappi/dpkg-status.git
cd dpkg-status
pip3 install -r requirements.txt OR pip3 install flask
python3 app.py
```
The database is only generated once. If you wish to regenerate the database, you have to remove the the `database` file in the root directory.
