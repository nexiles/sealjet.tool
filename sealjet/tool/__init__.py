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
import json
import urllib
import logging
import argparse
import urlparse
import httplib2

logger = logging.getLogger("sealjet.tool")

def setup_logging(log_path="sealjet_tool.log", level=logging.DEBUG):
    logging.basicConfig(
            filename=log_path,
            level=level,
            format="%(asctime)s: %(name)s: %(levelname)s: %(message)s"
            )

def q(v, *a, **kw):
    if type(v) == unicode:
        v = v.encode("utf-8")
    return urllib.quote_plus(v, *a, **kw)

def safe_unicode(v):
    if type(v) == str:
        return v
    elif type(v) == unicode:
        return v
    else:
        return str(v)

def is_url(string):
    scheme, netloc, path, query, fragment = urlparse.urlsplit(string)
    if not scheme:
        raise argparse.ArgumentTypeError("'%s' does not look like an URL." % string)
    if query or fragment:
        raise argparse.ArgumentTypeError("'%s' contains query args or a fragment part -- please remove these." % string)
    return string

class API(object):

    def __init__(self, url, username, password):
        self.username = username
        self.password = password
        self.url = url

        self.http = httplib2.Http()

        self.plone_login()

        # default headers
        self.headers = {
                "Cookie": self.auth_cookie
        }

    def plone_login(self):
        url = self.url + "/login_form"
        headers =  {"User-agent" : "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)",
                    "Content-type": "application/x-www-form-urlencoded",
                    "Accept": "text/plain"}
        params = {'came_from': url,
                  'form.submitted': '1',
                  'js_enabled': '0',
                  'cookies_enabled': '',
                  'login_name': '',
                  'pwd_empty': '0',
                  '__ac_name': self.username,
                  '__ac_password': self.password,
                  'submit': 'Log in'}
        resp, content = self.http.request(url, "POST", body=urllib.urlencode(params), headers=headers)
        self.auth_cookie = resp['set-cookie']

    def request(self, api_method, body=None, **kwargs):
        logger.debug("REQUEST: %s %s" % (api_method, kwargs))
        headers = dict()
        headers.update(self.headers)

        if body:
            headers["Content-Length"] = str(len(body))
        else:
            headers["Content-Length"] = "0"

        params = ["m=%s" % api_method, ]
        for key in sorted(kwargs.keys()):
            value = kwargs[key]
            value = safe_unicode(value)
            params.append("%s=%s" % (key, q(value)))

        path = "@@API?%s" % "&".join(params)
        url = os.path.join(self.url, path)

        logger.debug("path=%s" % path)
        logger.debug("url=%s" % url)

        response, content = self.http.request(
                url,
                "GET",
                body,
                headers)

        logger.debug("RESPONSE: %s content: %d bytes." % (response.status, len(content)))
        return response, content

    def query_import(self, username, partnumber):
        response, content = self.request("query_import", username=username, partnumber=partnumber)
        assert response.status == 200
        return json.loads(content)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", dest="loglevel", action="store_const", const=logging.DEBUG, default=logging.INFO)
    parser.add_argument("-l", "--logfile", default="sealjetpdm.log")
    parser.add_argument("-u", "--username", required=True, help="the user name to use")
    parser.add_argument("-p", "--password", required=True, help="the password")
    parser.add_argument("-U", "--url", required=True, type=is_url, help="the base URL to the sealjet PDM system's root cabinet")

    args = parser.parse_args()
    setup_logging(log_path=args.logfile, level=args.loglevel)

    logger.debug("-"*70)
    logger.debug("Start")

    api = API(args.url, args.username, args.password)

    print api.query_import("fred@example.com", "washer")

    logger.debug("Stop")
    logger.debug("-"*70)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

# vim: set ft=python ts=4 sw=4 expandtab :
