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

import rdflib

_logger = logging.getLogger(os.path.basename(__file__))

srcdir = os.path.dirname(__file__)

def _parse_graph(filename, format):
    graph_filename = os.path.join(srcdir, filename)
    graph = rdflib.Graph()
    graph.parse(graph_filename, format=format)
    return graph

def _test_as_import_load(graph_filename, format):
    graph = _parse_graph(graph_filename, format)
    assert len(graph) > 0

def _test_as_import_query(graph_filename, format):
    #TODO This try block can be removed, and the import put at the script's top, when rdflib Issue #1190 is resolved.
    # https://github.com/RDFLib/rdflib/issues/1190
    try:
        import rdflib.plugins.sparql
    except:
        import pyparsing
        _logger.debug("pyparsing.__version__ = %r." % pyparsing.__version__)
        raise

    graph = _parse_graph(graph_filename, format)

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
    uco-observable:exitStatus "0"^^xsd:long ;
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
    _test_as_import_load("process.json", "json-ld")

def test_as_import_load_turtle():
    _test_as_import_load("process.ttl", "turtle")

def test_as_import_query_json():
    _test_as_import_query("process.json", "json-ld")

def test_as_import_query_turtle():
    _test_as_import_query("process.ttl", "turtle")
