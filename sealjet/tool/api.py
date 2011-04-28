# -*- coding: utf-8 -*-
#
# File: api.py
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
import httplib2

logger = logging.getLogger("sealjet.tool")

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
        logger.debug("RESPONSE: %r" % response)
        logger.debug("CONTENT : %r" % content)
        return response, content

    def query_import(self, username, partnumber):
        response, content = self.request("query_import", username=username, partnumber=partnumber)
        assert response.status == 200
        return json.loads(content)

    def capsule_import(self, username, partnumber):
        response, content = self.request("import", username=username, partnumber=partnumber)
        assert response.status == 200
        return json.loads(content)

    def capsule_export(self, username, partnumber, version=None):
        if version:
            response, content = self.request("export", username=username, partnumber=partnumber)
        else:
            response, content = self.request("export", username=username, partnumber=partnumber, version=version)
        assert response.status == 200
        return json.loads(content)

    def lock_design(self, username, partnumber):
        response, content = self.request("lock_design", username=username, partnumber=partnumber)
        assert response.status == 200
        return json.loads(content)

    def unlock_design(self, username, partnumber):
        response, content = self.request("unlock_design", username=username, partnumber=partnumber)
        assert response.status == 200
        return json.loads(content)

# vim: set ft=python ts=4 sw=4 expandtab :
