#   Copyright 2017 Intel Corporation.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

import sys

import mock


class FakeStdout(object):

    def __init__(self):
        self.content = []

    def write(self, text):
        self.content.append(text)

    def make_string(self):
        result = ''
        for line in self.content:
            result = result + line
        return result


class FakeLog(object):

    def __init__(self):
        self.messages = {}

    def debug(self, msg):
        self.messages['debug'] = msg

    def info(self, msg):
        self.messages['info'] = msg

    def warning(self, msg):
        self.messages['warning'] = msg

    def error(self, msg):
        self.messages['error'] = msg

    def critical(self, msg):
        self.messages['critical'] = msg


class FakeApp(object):

    def __init__(self, _stdout, _log):
        self.stdout = _stdout
        self.client_manager = None
        self.stdin = sys.stdin
        self.stdout = _stdout or sys.stdout
        self.stderr = sys.stderr
        self.log = _log


class FakeMultiregionNetworkV1Client(object):

    def __init__(self, **kwargs):
        self.pod = mock.Mock()
        self.routing = mock.Mock()
        self.job = mock.Mock()


class FakeClientManager(object):
    _api_version = {
        'tricircle': '1',
    }

    def __init__(self):
        self.multiregion_networking = FakeMultiregionNetworkV1Client()
