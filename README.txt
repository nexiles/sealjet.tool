========================
Projekt: sealjet.content
========================

:Author:   Stefan Eletzhofer
:Date:     2011-05-23
:Version:  0.2dev

Abstract
========

This package contains an command line tool to the sealjet PDM
system.

Installation
============

Install the package as usual.  Preferred installation method is
to add the package to the sealjet PDM main buildout.  Once installed,
teh setup will create a `sealjetpdm` executable/script.

Usage
=====

The `sealjetpdm` tool's usage is as follows::

    usage: sealjetpdm [-h] [-d] [-l LOGFILE] -u USERNAME -p PASSWORD -U URL
                      {import,query-import,lock-design,export,unlock-design} ...

    positional arguments:
      {import,query-import,lock-design,export,unlock-design}

    optional arguments:
      -h, --help            show this help message and exit
      -d, --debug
      -l LOGFILE, --logfile LOGFILE
      -u USERNAME, --username USERNAME
                            the user name to use
      -p PASSWORD, --password PASSWORD
                            the password
      -U URL, --url URL     the base URL to the sealjet PDM system's root cabinet

There are several subcommands:

- **query-import**
- **import**
- **export**
- **lock-design**
- **unlock-design**

Each of the subcommands has it's own help accessible using the `-h` option.

Changes
=======

0.2 - unreleased
----------------

- BUGFIX: fix lock/unlock https://github.com/seletz/sealjet.content/issues/4

0.1 - ????-??-??
----------------

- first revision

..  vim: set ft=rst tw=75 nocin nosi ai sw=4 ts=4 expandtab:
