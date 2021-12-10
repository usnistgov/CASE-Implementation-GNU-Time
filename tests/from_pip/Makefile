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

case_srcdir := $(qc_srcdir)/dependencies/CASE-Examples/dependencies/CASE-Utilities-Python/dependencies/CASE

tests_srcdir := $(top_srcdir)/tests

# Use GNU date.
GDATE ?= $(shell which gdate || which date)

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
	  || (echo "ERROR:tests/from_pip/Makefile:The output in process.json has undefined CASE or UCO terms.  The first few are:" >&2 && head undefined_vocabulary.txt >&2 && exit 1)

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

# This recipe exists to preserve re-creation instructions.
echo.txt.done.log: \
  echo.txt
	test -r $<
	test -r $@ \
	  || $(GDATE) --iso-8601=ns > $@
	test -s $@  # Catch in case the GDATE call had failed previously.
	touch $@

# This recipe guarantees timestamps for Make's idempotent execution.
echo.txt.time.log: \
  echo.txt
	test -r $@
	touch $@

process.json: \
  process.ttl \
  $(RDF_TOOLKIT_JAR) \
  $(top_srcdir)/dependencies/CASE-Utilities-Python/tests/src/compact.py
	java -jar $(RDF_TOOLKIT_JAR) \
	  --infer-base-iri \
	  --inline-blank-nodes \
	  --source $< \
	  --source-format turtle \
	  --target __$@ \
	  --target-format json-ld
	source $(tests_srcdir)/venv/bin/activate \
	  && python3 $(top_srcdir)/dependencies/CASE-Utilities-Python/tests/src/compact.py \
	    _$@ \
	    __$@
	rm __$@
	mv _$@ $@

process.ttl: \
  $(tests_srcdir)/.venv.done.log \
  echo.txt.done.log \
  echo.txt.time.log
	rm -f _$@ __$@
	export DEMO_UUID_REQUESTING_NONRANDOM=NONRANDOM_REQUESTED \
	  && source $(tests_srcdir)/venv/bin/activate \
	    && case_gnu_time \
	      --done-log echo.txt.done.log \
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
