#!/usr/bin/env python3

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

import os

import rdflib.plugins.sparql

srcdir = os.path.dirname(__file__)

def _parse_graph(filename):
    graph_filename = os.path.join(srcdir, filename)
    graph = rdflib.Graph()
    graph.parse(graph_filename)
    return graph

def test_gtime_and_done_log_validation():
    graph = _parse_graph("validation.ttl")
    result = None
    for triple in graph.triples((None, rdflib.SH.conforms, None)):
        result = triple[2].toPython()
    assert result
