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

top_srcdir := $(shell cd .. ; pwd)

srcdir := $(shell pwd)

PYTHON3 ?= $(shell which python3.8 2>/dev/null || which python3.7 2>/dev/null || which python3.6 2>/dev/null || which python3)

# Dependencies are listed here in desired execution-progression order.
all: \
  all-gtime_log \
  all-gtime_and_done_log \
  all-from_pip \
  all-as_import

.PHONY: \
  all-as_import \
  all-from_pip \
  all-gtime_log \
  all-gtime_and_done_log \
  download

.venv.done.log: \
  $(top_srcdir)/.git_submodule_init.done.log \
  $(top_srcdir)/case_gnu_time/__init__.py \
  $(top_srcdir)/case_gnu_time/local_uuid.py \
  $(top_srcdir)/setup.cfg \
  $(top_srcdir)/setup.py \
  requirements.txt
	rm -rf venv
	$(PYTHON3) -m virtualenv \
	  --python=$(PYTHON3) \
	  venv
	source venv/bin/activate ; \
	  pip install \
	    --upgrade \
	    pip
	source venv/bin/activate ; \
	  cd $(top_srcdir) ; \
	    python3 setup.py install
	source venv/bin/activate ; \
	  pip install \
	    -r requirements.txt
	touch $@

.venv_minimal.done.log: \
  $(top_srcdir)/.git_submodule_init.done.log \
  $(top_srcdir)/setup.cfg \
  $(top_srcdir)/setup.py \
  requirements.txt
	rm -rf venv_minimal
	$(PYTHON3) -m virtualenv \
	  --python=$(PYTHON3) \
	  venv_minimal
	source venv_minimal/bin/activate ; \
	  pip install \
	    --upgrade \
	    pip
	source venv_minimal/bin/activate ; \
	  pip install \
	    -r requirements.txt
	touch $@

all-as_import: \
  $(top_srcdir)/dependencies/CASE-Examples-QC/.lib.done.log \
  .venv.done.log
	$(MAKE) \
	  --directory as_import

all-from_pip: \
  $(top_srcdir)/dependencies/CASE-Examples-QC/.lib.done.log \
  .venv.done.log
	$(MAKE) \
	  --directory from_pip

all-gtime_log: \
  $(top_srcdir)/dependencies/CASE-Examples-QC/.lib.done.log \
  .venv_minimal.done.log
	$(MAKE) \
	  --directory gtime_log

all-gtime_and_done_log: \
  $(top_srcdir)/dependencies/CASE-Examples-QC/.lib.done.log \
  .venv_minimal.done.log
	$(MAKE) \
	  --directory gtime_and_done_log

# Dependencies are listed here in desired execution-progression order.
# Each subdirectory may have a 'make check' to call pytest locally, so 'make check' here does not recursively call 'make check' in the directories below.  This is why there are 'all-' recursion targets.
check: \
  all-gtime_log \
  all-gtime_and_done_log \
  all-from_pip \
  all-as_import
	source $(srcdir)/venv/bin/activate ; \
	  pytest \
	    --log-level=DEBUG

clean:
	@$(MAKE) \
	  --directory gtime_log \
	  clean
	@$(MAKE) \
	  --directory gtime_and_done_log \
	  clean
	@$(MAKE) \
	  --directory from_pip \
	  clean
	@$(MAKE) \
	  --directory as_import \
	  clean
	@rm -rf \
	  .pytest_cache

distclean: \
  clean
	@rm -f \
	  .venv.done.log \
	  .venv_minimal.done.log
	@rm -rf \
	  venv \
	  venv_minimal

download: \
  .venv.done.log \
  .venv_minimal.done.log
