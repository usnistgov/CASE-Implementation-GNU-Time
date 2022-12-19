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
This script redundanty reproduces much of case_gnu_time's main() function.  The main purpose of this script is customizing process_object.
"""

import logging
import os

import rdflib.util
from case_utils.namespace import NS_UCO_CORE, NS_UCO_OBSERVABLE

import case_gnu_time

_logger = logging.getLogger(os.path.basename(__file__))


def main() -> None:
    args = case_gnu_time.argument_parser.parse_args()
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
    _ = case_gnu_time.build_process_object(
        graph, NS_BASE, args.gnu_time_log, mtime_str, "custom-"
    )

    output_format = args.output_format or rdflib.util.guess_format(args.out_graph)
    assert isinstance(output_format, str)

    graph.serialize(destination=args.out_graph, format=output_format)


if __name__ == "__main__":
    main()
