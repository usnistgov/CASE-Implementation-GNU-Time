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

top_srcdir := $(shell cd ../.. ; pwd)

qc_srcdir := $(top_srcdir)/dependencies/CASE-Examples-QC

case_srcdir := $(qc_srcdir)/dependencies/CASE-Examples/dependencies/CASE

tests_srcdir := $(top_srcdir)/tests

# Use GNU time.
GTIME ?= $(shell which gtime || which time)

COMM ?= $(shell which gcomm 2>/dev/null || which comm)
ifeq ($(COMM),)
$(error comm not found)
endif

SORT ?= $(shell which gsort 2>/dev/null || which sort)
ifeq ($(SORT),)
$(error sort not found)
endif

RDF_TOOLKIT_JAR := $(case_srcdir)/lib/rdf-toolkit.jar

all: \
  undefined_vocabulary.txt

check: \
  undefined_vocabulary.txt
	@test ! -s undefined_vocabulary.txt \
	  || (echo "ERROR:tests/gtime_log/Makefile:The output in process.json has undefined CASE or UCO terms.  The first few are:" >&2 && head undefined_vocabulary.txt >&2 && exit 1)
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
	source $(tests_srcdir)/venv_minimal/bin/activate \
	  && python $(tests_srcdir)/src/compact.py \
	    __$@ \
	    _$@
	rm __$@
	mv _$@ $@

process.ttl: \
  $(top_srcdir)/case_gnu_time/__init__.py \
  $(top_srcdir)/case_gnu_time/local_uuid.py \
  echo.txt.time.log
	rm -f _$@ __$@
	export DEMO_UUID_REQUESTING_NONRANDOM=NONRANDOM_REQUESTED \
	  && source $(tests_srcdir)/venv_minimal/bin/activate \
	    && python $(top_srcdir)/case_gnu_time/__init__.py \
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

undefined_vocabulary.txt: \
  process.json \
  $(qc_srcdir)/src/vocabulary_used.py \
  $(qc_srcdir)/tests/ontology_vocabulary.txt
	source $(qc_srcdir)/venv/bin/activate \
	  && python3 $(qc_srcdir)/src/vocabulary_used.py \
	    $< \
	    > $@___
	grep ':' $@___ \
	  | egrep -v 'w3.org' \
	    | grep -v '/kb/' \
	      > $@__
	rm $@___
	LC_ALL=C \
	  $(COMM) \
	    -13 \
	    $(qc_srcdir)/tests/ontology_vocabulary.txt \
	    <(LC_ALL=C $(SORT) $@__) \
	    > $@_
	rm $@__
	mv $@_ $@
