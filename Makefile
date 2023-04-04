#!/usr/bin/make -f

# This software was developed at the National Institute of Standards
# and Technology by employees of the Federal Government in the course
# of their official duties. Pursuant to title 17 Section 105 of the
# United States Code this software is not subject to copyright
# protection and is in the public domain. NIST assumes no
# responsibility whatsoever for its use by other parties, and makes
# no guarantees, expressed or implied, about its quality,
# reliability, or any other characteristic.
#
# We would appreciate acknowledgement if the software is used.

SHELL := /bin/bash

PYTHON3 ?= python3

all: \
  .venv-pre-commit/var/.pre-commit-built.log

.PHONY: \
  check-supply-chain \
  check-supply-chain-pre-commit \
  download

.git_submodule_init.done.log: \
  .gitmodules
	# Log current submodule pointers.
	cd dependencies \
	  && git diff . \
	    | cat
	git submodule update --init
	$(MAKE) \
	  --directory dependencies/CASE-Utilities-Python \
	  .git_submodule_init.done.log
	touch $@

# This virtual environment is meant to be built once and then persist, even through 'make clean'.
# If a recipe is written to remove this flag file, it should first run `pre-commit uninstall`.
.venv-pre-commit/var/.pre-commit-built.log:
	rm -rf .venv-pre-commit
	test -r .pre-commit-config.yaml \
	  || (echo "ERROR:Makefile:pre-commit is expected to install for this repository, but .pre-commit-config.yaml does not seem to exist." >&2 ; exit 1)
	$(PYTHON3) -m venv \
	  .venv-pre-commit
	source .venv-pre-commit/bin/activate \
	  && pip install \
	    --upgrade \
	    pip \
	    setuptools \
	    wheel
	source .venv-pre-commit/bin/activate \
	  && pip install \
	    pre-commit
	source .venv-pre-commit/bin/activate \
	  && pre-commit install
	mkdir -p \
	  .venv-pre-commit/var
	touch $@

check: \
  .git_submodule_init.done.log \
  .venv-pre-commit/var/.pre-commit-built.log
	$(MAKE) \
	  PYTHON3=$(PYTHON3) \
	  --directory tests \
	  check

# This target's dependencies potentially modify the working directory's Git state, so it is intentionally not a dependency of check.
check-supply-chain: \
  check-supply-chain-pre-commit

check-supply-chain-pre-commit: \
  .venv-pre-commit/var/.pre-commit-built.log
	source .venv-pre-commit/bin/activate \
	  && pre-commit autoupdate
	git diff \
	  --exit-code \
	  .pre-commit-config.yaml

clean:
	@rm -rf \
	  *.egg-info \
	  build \
	  dist
	@$(MAKE) \
	  --directory tests \
	  clean
	@rm -f \
	  .git_submodule_init.done.log

download: \
  .git_submodule_init.done.log
	test ! -z "$(PYTHON3)" \
	  || (echo "ERROR:Makefile:PYTHON3 not defined" >&2 ; exit 1)
	$(MAKE) \
	  PYTHON3=$(PYTHON3) \
	  --directory tests \
	  download
