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

import os
import logging
import argparse

logger = logging.getLogger("sealjet.tool")

def setup_logging(log_path="sealjet_tool.log", level=logging.DEBUG):
    logging.basicConfig(
            filename=log_path,
            level=level,
            format="%(asctime)s: %(name)s: %(levelname)s: %(message)s"
            )



def main():
    setup_logging()

    logger.info("-"*70)
    logger.info("Start")

    logger.info("Stop")
    logger.info("-"*70)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

# vim: set ft=python ts=4 sw=4 expandtab :
