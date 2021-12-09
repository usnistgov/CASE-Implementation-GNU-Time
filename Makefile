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
	git submodule init
	git submodule update
	touch $@

check: \
  dependencies/CASE-Examples-QC/tests/ontology_vocabulary.txt
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
	@#A full clean here erases test files and causes unnecessary rebuilding for the purposes of testing GNU Time mapping.
	@rm -f \
	  dependencies/CASE-Examples-QC/.lib.done.log
	@test ! -d dependencies/CASE-Examples-QC/tests \
	  || rm -f dependencies/CASE-Examples-QC/tests/ontology_vocabulary.txt

dependencies/CASE-Examples-QC/tests/ontology_vocabulary.txt: \
  .git_submodule_init.done.log
	test ! -z "$(PYTHON3)" \
	  || (echo "ERROR:Makefile:PYTHON3 not defined" >&2 ; exit 1)
	$(MAKE) \
	  PYTHON3=$(PYTHON3) \
	  --directory dependencies/CASE-Examples-QC \
	  .git_submodule_init.done.log \
	  .lib.done.log \
	  .venv.done.log
	$(MAKE) \
	  PYTHON3=$(PYTHON3) \
	  --directory dependencies/CASE-Examples-QC/tests \
	  ontology_vocabulary.txt
	test -r $@

distclean: \
  clean
	@rm -f \
	  .git_submodule_init.done.log \
	  dependencies/CASE-Examples-QC/.lib.done.log \
	  dependencies/CASE-Examples-QC/lib/rdf-toolkit.jar
	@$(MAKE) \
	  --directory tests \
	  distclean

download: \
  dependencies/CASE-Examples-QC/tests/ontology_vocabulary.txt
	test ! -z "$(PYTHON3)" \
	  || (echo "ERROR:Makefile:PYTHON3 not defined" >&2 ; exit 1)
	$(MAKE) \
	  PYTHON3=$(PYTHON3) \
	  --directory tests \
	  download
