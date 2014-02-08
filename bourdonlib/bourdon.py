# -*- coding: utf-8 -*-

# Copyright (c) 2014 Michel Petit <petit.michel@gmail.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



import httplib2 as http
import urllib
import json

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse


class Bourdon(object):
    def __init__(self, user, uri):
        self.user = user
        self.uri = uri
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=UTF-8'
        }

    def param(self, opts):
        return urllib.urlencode(opts)

    def request(self, method='GET', path='', body='', opts={}):
        target = urlparse(self.uri + path)

        h = http.Http()

        # authentication:
        h.add_credentials(self.user, 'xxx')

        # TODO use opts param for GET/PUT/POST
        if method == 'GET':
            response, content = h.request(target.geturl() +'?' + self.param(opts), method, body, self.headers)
        else:
            response, content = h.request(target.geturl(), method, self.param(opts), self.headers)
        return {'response': response, 'content': json.loads(content)}

    def get_account(self):
        """Retrieves details about the Teamwork account."""
        return self.request(path='/account.json')

    def get_info(self):
        return self.request(path='/api')

    def get_projects(self, opts={}):
        return self.request(path='/projects', opts=opts)

    def get_project(self, project_id, opts={}):
        return self.request(path='/projects/%d' % project_id, opts=opts)

    def create_project(self, project_id, opts={}):
        return self.request(method='POST', path='/projects/%d' % project_id, opts=opts)

    def update_project(self, project_id, opts={}):
        return self.request(method='PUT', path='/project/%d' % project_id, opts=opts)

    def delete_project(self, project_id):
        return self.request(method='DELETE', path='/project/%d' % project_id)



