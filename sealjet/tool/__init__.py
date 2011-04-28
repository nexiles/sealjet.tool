# -*- coding: utf-8 -*-
#
# File: __init__.py
#
# Copyright (c) nexiles GmbH
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

__author__    = """Stefan Eletzhofer <se@nexiles.de>"""
__docformat__ = 'plaintext'

import logging
import argparse
import urlparse

from sealjet.tool.api import API

logger = logging.getLogger("sealjet.tool")

def setup_logging(log_path="sealjet_tool.log", level=logging.DEBUG):
    logging.basicConfig(
            filename=log_path,
            level=level,
            format="%(asctime)s: %(name)s: %(levelname)s: %(message)s"
            )

def is_url(string):
    scheme, netloc, path, query, fragment = urlparse.urlsplit(string)
    if not scheme:
        raise argparse.ArgumentTypeError("'%s' does not look like an URL." % string)
    if query or fragment:
        raise argparse.ArgumentTypeError("'%s' contains query args or a fragment part -- please remove these." % string)
    return string


def do_query_import(api, args):
    logger.info("query_import: username=%s partnumber=%s" % (args.username, args.partnumber))
    print api.query_import(args.username, args.partnumber)

def do_import(api, args):
    pass

def do_export(api, args):
    pass

def do_unlock_design(api, args):
    pass

def do_lock_design(api, args):
    pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", dest="loglevel", action="store_const", const=logging.DEBUG, default=logging.INFO)
    parser.add_argument("-l", "--logfile", default="sealjetpdm.log")
    parser.add_argument("-u", "--username", required=True, help="the user name to use")
    parser.add_argument("-p", "--password", required=True, help="the password")
    parser.add_argument("-U", "--url", required=True, type=is_url, help="the base URL to the sealjet PDM system's root cabinet")

    subparsers = parser.add_subparsers()
    
    parser_query_import = subparsers.add_parser("query-import")
    #parser_query_import.add_argument("username")
    parser_query_import.add_argument("partnumber")
    parser_query_import.set_defaults(command=do_query_import)

    parser_import = subparsers.add_parser("import")
    #parser_import.add_argument("username")
    parser_import.add_argument("partnumber")
    parser_import.set_defaults(command=do_import)

    parser_export = subparsers.add_parser("export")
    #parser_export.add_argument("username")
    parser_export.add_argument("partnumber")
    parser_export.add_argument("-V", "--version", dest="version")
    parser_export.set_defaults(command=do_export)

    parser_unlock_design = subparsers.add_parser("unlock-design")
    #parser_unlock_design.add_argument("username")
    parser_unlock_design.add_argument("partnumber")
    parser_unlock_design.set_defaults(command=do_unlock_design)

    parser_lock_design = subparsers.add_parser("lock-design")
    #parser_lock_design.add_argument("username")
    parser_lock_design.add_argument("partnumber")
    parser_lock_design.set_defaults(command=do_unlock_design)

    args = parser.parse_args()
    setup_logging(log_path=args.logfile, level=args.loglevel)

    logger.debug("-"*70)
    logger.debug("Start")

    api = API(args.url, args.username, args.password)
    args.command(api, args)

    logger.debug("Stop")
    logger.debug("-"*70)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

# vim: set ft=python ts=4 sw=4 expandtab :
