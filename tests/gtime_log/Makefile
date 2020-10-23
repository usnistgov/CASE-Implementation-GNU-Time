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

top_srcdir := ../..

tests_srcdir := $(top_srcdir)/tests

# Use GNU time.
GTIME ?= $(shell which gtime || which time)

RDF_TOOLKIT_JAR := $(top_srcdir)/dependencies/CASE-Examples-QC/lib/rdf-toolkit.jar

all: \
  process.json

check: \
  process.json
	@echo "INFO:tests/gtime_log/Makefile:Note that process.json in this directory is expected to change from its Git-tracked state when the test is run in a new repository-clone instance.  This test intentionally does not include a timestamp preservation mechanism." >&2

clean:
	@rm -f \
	  *.json \
	  *.ttl

# This recipe exists to preserve re-creation instructions.
echo.txt:
	$(GTIME) \
	  --output=$@.time.log \
	  --verbose \
	  echo \
	    xyz \
	    > _$@
	mv _$@ $@

# This recipe guarantees timestamp order for Make's idempotent execution.
echo.txt.time.log: \
  echo.txt
	test -r $@
	touch $@

process.json: \
  process.ttl \
  $(RDF_TOOLKIT_JAR) \
  $(tests_srcdir)/src/compact.py
	java -jar $(RDF_TOOLKIT_JAR) \
	  --infer-base-iri \
	  --inline-blank-nodes \
	  --source $< \
	  --source-format turtle \
	  --target __$@ \
	  --target-format json-ld
	source $(tests_srcdir)/venv_minimal/bin/activate ; \
	  python $(tests_srcdir)/src/compact.py \
	    __$@ \
	    _$@
	rm __$@
	mv _$@ $@

process.ttl: \
  $(top_srcdir)/case_gnu_time/__init__.py \
  $(top_srcdir)/case_gnu_time/local_uuid.py \
  echo.txt.time.log
	rm -f _$@ __$@
	source $(tests_srcdir)/venv_minimal/bin/activate ; \
	  DEMO_UUID_REQUESTING_NONRANDOM=NONRANDOM_REQUESTED \
	    python $(top_srcdir)/case_gnu_time/__init__.py \
	      echo.txt.time.log \
	      __$@
	java -jar $(RDF_TOOLKIT_JAR) \
	  --infer-base-iri \
	  --inline-blank-nodes \
	  --source __$@ \
	  --source-format turtle \
	  --target _$@ \
	  --target-format turtle
	rm __$@
	mv _$@ $@
