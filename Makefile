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

# This recipe intentionally blank.
all:

.PHONY: \
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

check: \
  .git_submodule_init.done.log
	$(MAKE) \
	  PYTHON3=$(PYTHON3) \
	  --directory tests \
	  check

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
