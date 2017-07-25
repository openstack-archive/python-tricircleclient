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
from oslo_utils import timeutils
from oslo_utils import uuidutils
import testtools

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

    def check_parser(self, cmd, args=[], verify_args=[]):
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


class TestCommandWithoutOptions(object):

    def test_without_options(self):
        self.assertRaises(ParserException, self.check_parser, self.cmd)


class FakePod(object):
    """Fake one or more Pods."""

    @staticmethod
    def create_single_pod(opts=None):
        """Create a fake pod.

        :param opts:Dictionary of options to overwrite
        :return: A dictionary with dc_name, pod_name, pod_id,
        az_name, pod_az_name, region_name
        """
        opts = opts or {}
        # Set default options.
        fake_pod = {
            'pod': {
                'dc_name': 'datacenter',
                'pod_az_name': 'pod',
                'pod_id': uuidutils.generate_uuid(),
                'az_name': 'availability_zone',
                'region_name': 'central_region',
            }
        }

        # Overwrite default options
        fake_pod['pod'].update(opts)
        return copy.deepcopy(fake_pod)

    @staticmethod
    def create_multiple_pods(opts=None, count=2):
        """Create a list of fake pods.

        :param opts: A dictionary of options to create pod
        :param count: The number of pods to create
        :return: A list of dictionaries with dc_name, pod_name, pod_id,
        az_name, pod_az_name, region_name
        """
        return [FakePod.create_single_pod(opts)['pod']
                for i in range(0, count)]


class FakeRouting(object):
    """Fake one or more Routings."""

    @staticmethod
    def create_single_routing(opts=None):
        """Create a fake routing.

        :param opts: Dictionary of options to overwrite
        :return: A Dictionary with top_id, bottom_id, pod_id,
        project_id, resource_type, id
        """
        opts = opts or {}
        # Set default options.
        fake_routing = {
            'routing': {
                'top_id': uuidutils.generate_uuid(),
                'bottom_id': uuidutils.generate_uuid(),
                'pod_id': uuidutils.generate_uuid(),
                'project_id': uuidutils.generate_uuid(),
                'resource_type': 'network',
                'id': uuidutils.generate_uuid(),
                'created_at': str(timeutils.utcnow()),
                'updated_at': str(timeutils.utcnow()),
            }
        }

        # Overwrite default options
        fake_routing['routing'].update(opts)
        return copy.deepcopy(fake_routing)

    @staticmethod
    def create_multiple_routings(opts=None, count=2):
        """Create a list of fake routings.

        :param opts: A Dictionary of options to create routing
        :param count: The number of routings to create
        :return: A list of Dictionaries with top_id, bottom_id, pod_id,
        project_id, resource_type, id
        """
        return [FakeRouting.create_single_routing(opts)['routing']
                for i in range(0, count)]


class FakeJob(object):
    """Fake one or more Jobs."""

    @staticmethod
    def create_single_job(opts=None):
        """Create a fake job.

        :param opts: Dictionary of options to overwrite
        :return: A Dictionary with type, project_id. optional parameters are:
        router_id, network_id, pod_id, port_id, trunk_id, subnet_id,
        portchain_id. Different job type needs different resources, they
        are specified as optional parameters.
        """
        opts = opts or {}

        # Set default options.
        fake_job = {
            'job': {
                'id': uuidutils.generate_uuid(),
                'type': 'router_setup',
                'resource': {
                    'pod_id': uuidutils.generate_uuid(),
                    'router_id': uuidutils.generate_uuid(),
                    'network_id': uuidutils.generate_uuid(),
                },
                'project_id': uuidutils.generate_uuid(),
                'status': 'NEW',
                'timestamp': str(timeutils.utcnow()),
            }
        }

        # Overwrite default options
        fake_job['job'].update(opts)
        return fake_job

    @staticmethod
    def create_multiple_jobs(opts=None, count=2):
        """Create a list of fake jobs.

        :param opts: A Dictionary of options to create job
        :param count: The number of routings to create
        :return: A list of Dictionaries with type, project_id and some
        optional parameters. Optional paramaters are:
        router_id, network_id, pod_id, port_id, trunk_id, subnet_id,
        portchain_id. Different job type needs different resources, they
        are specified as optional parameters.
        """
        return [FakeJob.create_single_job(opts)['job']
                for i in range(0, count)]
