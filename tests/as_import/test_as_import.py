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

import logging
import os

import rdflib.plugins.sparql

_logger = logging.getLogger(os.path.basename(__file__))

srcdir = os.path.dirname(__file__)

def _parse_graph(filename):
    graph_filename = os.path.join(srcdir, filename)
    graph = rdflib.Graph()
    graph.parse(graph_filename)
    return graph

def _test_as_import_load(graph_filename):
    graph = _parse_graph(graph_filename)
    assert len(graph) > 0

def _test_as_import_query(graph_filename):
    graph = _parse_graph(graph_filename)

    nsdict = {k:v for (k,v) in graph.namespace_manager.namespaces()}

    iris = set()
    query = rdflib.plugins.sparql.prepareQuery("""\
SELECT ?nProcessObject
WHERE
{
  ?nProcessObject
    a uco-observable:ObservableObject ;
    uco-core:hasFacet ?nProcessFacet ;
    .

  ?nProcessFacet
    a uco-observable:ProcessFacet ;
    uco-observable:exitStatus 0 ;
    .
}
""", initNs=nsdict)

    results = graph.query(query)
    _logger.debug("len(results) = %d." % len(results))
    for result in results:
        _logger.debug("result = %r." % result)
        (
          n_process_object,
        ) = result
        assert not n_process_object is None
        iris.add(n_process_object.toPython())
    assert len(iris) == 1

def test_as_import_load_json():
    _test_as_import_load("process.json")

def test_as_import_load_turtle():
    _test_as_import_load("process.ttl")

def test_as_import_query_json():
    _test_as_import_query("process.json")

def test_as_import_query_turtle():
    _test_as_import_query("process.ttl")

def test_as_import_validation():
    graph = _parse_graph("validation.ttl")
    result = None
    for triple in graph.triples((None, rdflib.SH.conforms, None)):
        result = triple[2].toPython()
    assert result
