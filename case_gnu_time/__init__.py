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

"""
This library parses the output of GNU Time into a UCO Process graph node.
"""

__version__ = "0.5.0"

import argparse
import datetime
import logging
import os

import dateutil
import dateutil.parser
import rdflib

import case_utils

_logger = logging.getLogger(os.path.basename(__file__))

NS_RDF = rdflib.RDF
NS_UCO_CORE = rdflib.Namespace("https://unifiedcyberontology.org/ontology/uco/core#")
NS_UCO_OBSERVABLE = rdflib.Namespace("https://unifiedcyberontology.org/ontology/uco/observable#")
NS_XSD = rdflib.namespace.XSD

class ProcessUCOObject(object):
    def __init__(self, graph, ns_base, **kwargs):
        """
        Initializing a ProcessUCOObject will create one triple in the graph.  To add data to the new node, call populate_from_gnu_time_log().
        """

        assert isinstance(graph, rdflib.Graph)

        self.graph = graph

        prefix_slug = kwargs.get("prefix_slug", "process-")

        # Guarantee at least one triple enters the graph.
        self._node = rdflib.URIRef(ns_base[prefix_slug + case_utils.local_uuid.local_uuid()])
        self.graph.add((self.node, NS_RDF.type, NS_UCO_OBSERVABLE.ObservableObject))

        self._bnode_process = None
        self._created_time = None
        self._exit_status = None
        self._exit_time = None

    def populate_from_gnu_time_log(self, gnu_time_log):
        """
        This method populates Process data from a GNU Time log file.  If self.exit_time is not set before this method is called, it will be set by reading the modification time of gnu_time_log.
        """
        # First, guarantee exit time.
        if self.exit_time is None:
            st_time_log = os.stat(gnu_time_log)
            # Reminders on fromtimestamp vs. utcfromtimestamp:
            #   https://docs.python.org/3/library/datetime.html#datetime.datetime.utcfromtimestamp
            #   "To get an aware datetime object, call fromtimestamp()"
            exit_time_datetime = datetime.datetime.fromtimestamp(st_time_log.st_mtime, tz=datetime.timezone.utc)
            exit_time_str = exit_time_datetime.isoformat()
            self.exit_time = exit_time_str
        else:
            exit_time_datetime = dateutil.parser.isoparse(self.exit_time)

        kvdict = dict()
        with open(gnu_time_log, "r") as fh:
            for line in fh:
                cleaned_line = line.strip()
                line_parts = cleaned_line.split(": ")
                key = line_parts[0]
                value = ": ".join(line_parts[1:])
                kvdict[key] = value

        self.exit_status = int(kvdict["Exit status"])

        elapsed_str = kvdict["Elapsed (wall clock) time (h:mm:ss or m:ss)"]
        elapsed_str_parts = elapsed_str.split(":")
        elapsed_seconds_str = elapsed_str_parts[-1]
        elapsed_seconds = int(elapsed_str_parts[-1].split(".")[0])
        elapsed_microseconds = int(elapsed_str_parts[-1].split(".")[1]) * 10000
        elapsed_minutes = int(elapsed_str_parts[-2])
        if len(elapsed_str_parts) == 3:
            elapsed_minutes += (60 * int(elapsed_str_parts[-3]))

        delta = dateutil.relativedelta.relativedelta(
          minutes=elapsed_minutes,
          seconds=elapsed_seconds,
          microseconds=elapsed_microseconds
        )

        #logging.debug("delta = %r." % delta)
        created_time_datetime = exit_time_datetime - delta
        #logging.debug("created_time_datetime = %r." % created_time_datetime)
        #logging.debug("exit_time_datetime = %r." % exit_time_datetime)

        self.created_time = created_time_datetime.isoformat()

    @property
    def bnode_process(self):
        """
        Created on first access.
        """
        if self._bnode_process is None:
            self._bnode_process = rdflib.BNode()
            self.graph.add((self._bnode_process, NS_RDF.type, NS_UCO_OBSERVABLE.ProcessFacet))
            self.graph.add((self.node, NS_UCO_CORE.hasFacet, self._bnode_process))
        return self._bnode_process

    @property
    def created_time(self):
        return self._created_time

    @created_time.setter
    def created_time(self, value):
        """
        Only set once.
        """
        assert not value is None
        assert self._created_time is None
        str_value = str(value) # For e.g. datetime objects.
        # Confirm text is ISO-8601.
        check_value = dateutil.parser.isoparse(str_value)
        self.graph.add((self.bnode_process, NS_UCO_OBSERVABLE.observableCreatedTime, rdflib.Literal(str_value, datatype=NS_XSD.dateTime)))
        self._created_time = value
        return self._created_time

    @property
    def exit_status(self):
        return self._exit_status

    @exit_status.setter
    def exit_status(self, value):
        assert isinstance(value, int)
        self.graph.add((self.bnode_process, NS_UCO_OBSERVABLE.exitStatus, rdflib.Literal(value, datatype=NS_XSD.long)))
        return self._exit_status

    @property
    def exit_time(self):
        return self._exit_time

    @exit_time.setter
    def exit_time(self, value):
        """
        Only set once.
        """
        assert not value is None
        assert self._exit_time is None
        str_value = str(value) # For e.g. datetime objects.
        # Confirm text is ISO-8601.
        check_value = dateutil.parser.isoparse(str_value)
        literal_time = rdflib.Literal(str_value, datatype=NS_XSD.dateTime)
        self.graph.add((self.bnode_process, NS_UCO_OBSERVABLE.exitTime, literal_time))
        self._exit_time = value
        return self._exit_time

    @property
    def node(self):
        """
        Read-only property.
        """
        return self._node

def build_process_object(graph, ns_base, gnu_time_log, mtime=None, prefix_slug=None):
    """
    This function builds a Process UCO Object from a file that contains the output of GNU Time's --verbose flag.

    GNU Time does not record the time at which a process finished, but the duration of the process is recorded in several forms.  This function builds a start time estimate by subtracting the wall clock time from the "end time".

    "end time" is defined in one two ways:
    * The mtime argument, which should be an ISO-8601 string.
    * The modification time of the file (via st_time of os.stat).

    The optional argument prefix_slug is a short prefix to add to the node's in-namespace identifier, ending with "-".  If absent, the ProcessUCOObject will supply a default of "process-".
    """
    case_utils.local_uuid.configure()

    process_object_kwargs = dict()
    if not prefix_slug is None:
        process_object_kwargs["prefix_slug"] = prefix_slug
    process_object = ProcessUCOObject(graph, ns_base, **process_object_kwargs)

    if not mtime is None:
        process_object.exit_time = mtime

    process_object.populate_from_gnu_time_log(gnu_time_log)

    return process_object

argument_parser = argparse.ArgumentParser(epilog=__doc__)
argument_parser.add_argument("--base-prefix", default="http://example.org/kb/")
argument_parser.add_argument("--debug", action="store_true")
argument_parser.add_argument("--done-log", help="A file recording the completion time of the process that GNU Time was timing, as an ISO-8601 string.  If this argument is not provided, the Stat mtime of gnu_time_log is used.")
argument_parser.add_argument("--output-format", help="Override extension-based format guesser.")
argument_parser.add_argument("gnu_time_log", help="A file recording the output of the process wrapper GNU time, with the --verbose flag (recorded with the --output flag).  Used to retrieve exit status, conclusion time (if --done-log not provided), and run length.")
argument_parser.add_argument("out_graph", help="A self-contained RDF graph file, in the format either requested by --output-format or guessed based on extension.")

def main():
    args = argument_parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    NS_BASE = rdflib.Namespace(args.base_prefix)
    graph = rdflib.Graph()
    graph.namespace_manager.bind("kb", NS_BASE)
    graph.namespace_manager.bind("uco-core", NS_UCO_CORE)
    graph.namespace_manager.bind("uco-observable", NS_UCO_OBSERVABLE)

    mtime_str = None
    if args.done_log:
        with open(args.done_log, "r") as mtime_fh:
            mtime_str = mtime_fh.read(64).strip()
    process_object = build_process_object(graph, NS_BASE, args.gnu_time_log, mtime_str)

    #_logger.debug("args.output_format = %r." % args.output_format)
    output_format = args.output_format or case_utils.guess_format(args.out_graph)

    graph.serialize(destination=args.out_graph, format=output_format)

if __name__ == "__main__":
    main()
