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

import copy
import testtools
import uuid

from tricircleclient.tests.unit import fakes


class ParserException(Exception):
    pass


class TestCommand(testtools.TestCase):

    def setUp(self):
        super(TestCommand, self).setUp()
        # Build up a fake app
        self.fake_stdout = fakes.FakeStdout()
        self.fake_log = fakes.FakeLog()
        self.app = fakes.FakeApp(self.fake_stdout, self.fake_log)
        self.app.client_manager = fakes.FakeClientManager()

    def check_parser(self, cmd, args, verify_args):
        cmd_parser = cmd.get_parser('check_parser')
        try:
            parsed_args = cmd_parser.parse_args(args)
        except SystemExit:
            raise ParserException("Argument parse failed")
        for attr, value in verify_args:
            if attr:
                self.assertIn(attr, parsed_args)
                self.assertEqual(value, getattr(parsed_args, attr))
        return parsed_args


class FakePod(object):
    """Fake one or more Pods."""

    @staticmethod
    def createPod(opts=None):
        """Create a fake pod.

        :param opts:Dictionary of options to overwrite
        :return:
        A Dictionary with dc_name, pod_name, pod_id,
        az_name, pod_az_name, region_name
        """
        opts = opts or {}
        # Set default options.
        fake_pod = {
            'pod': {
                'dc_name': 'datacenter',
                'pod_az_name': 'pod',
                'pod_id': uuid.uuid4().hex,
                'az_name': 'availability_zone',
                'region_name': 'central_region',
            }
        }

        # Overwrite default options
        fake_pod['pod'].update(opts)
        return copy.deepcopy(fake_pod)
