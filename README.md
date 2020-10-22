# CASE Implementation: GNU Time

This implementation maps the logged output of [GNU Time](https://www.gnu.org/software/time/) into the [UCO](https://github.com/ucoProject/UCO/) version used by [CASE](https://caseontology.org/).


## Disclaimer

Participation by NIST in the creation of the documentation of mentioned software is not intended to imply a recommendation or endorsement by the National Institute of Standards and Technology, nor is it intended to imply that any specific software is necessarily the best available for the purpose.


## Usage

To install this software, clone this repository, and run `python3 setup.py install` from within this directory.  (You might want to do this in a virtual environment.)

This provides a standalone command:

```bash
/usr/bin/time -v -o echo.txt.time.log echo test > echo.txt
case_gnu_time echo.txt.time.log process.json
```

The tests build several examples of [`process.json`](tests/from_pip/process.json).  The [tests](tests/) directory demonstrates the expected usage pattern of GNU Time that this project analyzes.

The installation also provides a package to import:

```python
import case_gnu_time
help(case_gnu_time.build_process_object)
```


## Development status

This repository follows [CASE community guidance on describing development status](https://caseontology.org/resources/github_repos.html#development-statuses), by adherence to noted support requirements.

The status of this repository is:

3 - Alpha


## Versioning

This project follows [SEMVER 2.0.0](https://semver.org/) where versions are declared.


## Ontology versions supported

This repository supports the CASE and UCO ontology versions that are linked as submodules in the [CASE Examples QC](https://github.com/ajnelson-nist/CASE-Examples-QC) repository.  Currently, those are:

* CASE 0.2.0
* UCO 0.4.0


## Repository locations

This repository is available at the following locations:
* [https://github.com/casework/CASE-Implementation-GNU-Time](https://github.com/casework/CASE-Implementation-GNU-Time)
* [https://github.com/usnistgov/CASE-Implementation-GNU-Time](https://github.com/usnistgov/CASE-Implementation-GNU-Time) (a mirror)

Releases and issue tracking will be handled at the [casework location](https://github.com/casework/CASE-Implementation-GNU-Time).


## Make targets

Some `make` targets are defined for this repository:
* `all` - No effect.
* `check` - Run unit tests.  *NOTE*: The tests entail downloading some software to assist with formatting and conversion, from PyPI and from a [third party](https://github.com/edmcouncil/rdf-toolkit).  `make download` retrieves these files.
* `clean` - Remove test build files, but not downloaded files or the `tests/venv` virtual environment.
* `distclean` - Run `make clean` and further delete downloaded files and the `tests/venv` virtual environment.  Neither `clean` nor `distclean` will remove downloaded submodules.
* `download` - Download files sufficiently to run the unit tests offline.  This will *not* include the ontology repositories tracked as submodules.  Note if you do need to work offline, be aware touching the `setup.py` file in the root, or `tests/requirements.txt`, will trigger a virtual environment rebuild.


## Disambiguation

Several independent implementations of some `time` command exist.

Note that this project does not map the output of [BSD Time](https://www.freebsd.org/cgi/man.cgi?query=time).  Also note that some environments, such as macOS at and before 10.15.7, package a BSD Time version that predates a flag for an independently specified output file.

Note also that the Bash builtin `time` command is not supported.