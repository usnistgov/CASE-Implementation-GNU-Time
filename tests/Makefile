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

PYTHON3 ?= python3

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
  check-as_import \
  check-from_pip \
  check-gtime_log \
  check-gtime_and_done_log \
  check-mypy \
  download

.venv.done.log: \
  $(top_srcdir)/.git_submodule_init.done.log \
  $(top_srcdir)/dependencies/CASE-Utilities-Python/tests/requirements.txt \
  $(top_srcdir)/setup.cfg \
  $(top_srcdir)/setup.py \
  requirements.txt
	rm -rf venv
	$(PYTHON3) -m venv \
	  venv
	source venv/bin/activate \
	  && pip install \
	    --upgrade \
	    pip \
	    setuptools \
	    wheel
	source venv/bin/activate \
	  && pip install \
	    --requirement $(top_srcdir)/dependencies/CASE-Utilities-Python/tests/requirements.txt
	source venv/bin/activate \
	  && pip install \
	    --editable \
	    $(top_srcdir)
	source venv/bin/activate \
	  && pip install \
	    --requirement requirements.txt
	touch $@

.venv_minimal.done.log: \
  $(top_srcdir)/.git_submodule_init.done.log \
  $(top_srcdir)/dependencies/CASE-Utilities-Python/tests/requirements.txt \
  $(top_srcdir)/setup.cfg \
  $(top_srcdir)/setup.py \
  requirements.txt
	rm -rf venv_minimal
	$(PYTHON3) -m venv \
	  venv_minimal
	source venv_minimal/bin/activate \
	  && pip install \
	    --upgrade \
	    pip \
	    setuptools \
	    wheel
	source venv_minimal/bin/activate \
	  && pip install \
	    --requirement $(top_srcdir)/dependencies/CASE-Utilities-Python/tests/requirements.txt
	source venv_minimal/bin/activate \
	  && pip install \
	    --requirement requirements.txt
	touch $@

all-as_import: \
  .venv.done.log
	$(MAKE) \
	  --directory as_import

all-from_pip: \
  .venv.done.log
	$(MAKE) \
	  --directory from_pip

all-gtime_log: \
  .venv_minimal.done.log
	$(MAKE) \
	  --directory gtime_log

all-gtime_and_done_log: \
  .venv_minimal.done.log
	$(MAKE) \
	  --directory gtime_and_done_log

# Dependencies are listed here in desired execution-progression order.
check: \
  check-gtime_log \
  check-gtime_and_done_log \
  check-from_pip \
  check-as_import \
  check-mypy

check-as_import: \
  all-as_import
	$(MAKE) \
	  --directory as_import \
	  check

check-from_pip: \
  all-from_pip
	$(MAKE) \
	  --directory from_pip \
	  check

check-gtime_log: \
  all-gtime_log
	$(MAKE) \
	  --directory gtime_log \
	  check

check-gtime_and_done_log: \
  all-gtime_and_done_log
	$(MAKE) \
	  --directory gtime_and_done_log \
	  check

check-mypy: \
  .venv.done.log
	source venv/bin/activate \
	  && mypy \
	    --strict \
	    $(top_srcdir)/case_gnu_time \
	    as_import

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
	@rm -f \
	  .venv.done.log \
	  .venv_minimal.done.log
	@rm -rf \
	  venv \
	  venv_minimal

download: \
  .venv.done.log \
  .venv_minimal.done.log
