#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import mock

from tricircleclient.tests.unit import utils
from tricircleclient.v1 import pods_cli


class _TestPodCommand(utils.TestCommand):

    def setUp(self):
        super(_TestPodCommand, self).setUp()
        self.pod_manager = self.app.client_manager.multiregion_networking.pod


class TestCreatePod(_TestPodCommand, utils.TestCommandWithoutOptions):

    def setUp(self):
        super(TestCreatePod, self).setUp()
        self.cmd = pods_cli.CreatePod(self.app, None)

    def test_create_all_options(self):
        _pod = utils.FakePod.create_single_pod()
        arglist = [
            '--region-name', _pod['pod']['region_name'],
            '--availability-zone', _pod['pod']['az_name'],
            '--pod-availability-zone', _pod['pod']['pod_az_name'],
            '--data-center', _pod['pod']['dc_name']
        ]
        verifylist = [
            ('region_name', _pod['pod']['region_name']),
            ('availability_zone', _pod['pod']['az_name']),
            ('pod_availability_zone', _pod['pod']['pod_az_name']),
            ('data_center', _pod['pod']['dc_name']),
        ]
        self.pod_manager.create = mock.Mock(return_value=_pod)
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = (self.cmd.take_action(parsed_args))

        self.assertEqual(sorted(_pod['pod'].keys()), sorted(columns))
        self.assertEqual(sorted(_pod['pod'].values()), sorted(data))

    def test_create_local_region_with_availability_zone(self):
        keys = ["dc_name", "pod_az_name"]
        _pod = utils.FakePod.create_single_pod({key: " " for key in keys})
        arglist = [
            '--region-name', _pod['pod']['region_name'],
            '--availability-zone', _pod['pod']['az_name']
        ]
        verifylist = [
            ('region_name', _pod['pod']['region_name']),
            ('availability_zone', _pod['pod']['az_name']),
        ]
        self.pod_manager.create = mock.Mock(return_value=_pod)
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = (self.cmd.take_action(parsed_args))

        self.assertEqual(sorted(_pod['pod'].keys()), sorted(columns))
        self.assertEqual(sorted(_pod['pod'].values()), sorted(data))

    def test_create_central_region(self):
        keys = ["dc_name", "pod_az_name", "az_name"]
        _pod = utils.FakePod.create_single_pod({key: " " for key in keys})
        arglist = [
            '--region-name', _pod['pod']['region_name']
        ]
        verifylist = [
            ('region_name', _pod['pod']['region_name']),
        ]
        self.pod_manager.create = mock.Mock(return_value=_pod)
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = (self.cmd.take_action(parsed_args))

        self.assertEqual(sorted(_pod['pod'].keys()), sorted(columns))
        self.assertEqual(sorted(_pod['pod'].values()), sorted(data))


class TestShowPod(_TestPodCommand, utils.TestCommandWithoutOptions):

    def setUp(self):
        super(TestShowPod, self).setUp()
        self.cmd = pods_cli.ShowPod(self.app, None)

    def test_show_valid_pod(self):
        _pod = utils.FakePod.create_single_pod()
        arglist = [
            _pod['pod']['pod_id'],
            ]
        verifylist = [
            ("pod", _pod['pod']['pod_id']),
            ]
        self.pod_manager.get = mock.Mock(return_value=_pod)
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = (self.cmd.take_action(parsed_args))

        self.assertEqual(sorted(_pod['pod'].keys()), sorted(columns))
        self.assertEqual(sorted(_pod['pod'].values()), sorted(data))

    def test_show_valid_pod_with_empty_fields(self):
        keys = ["dc_name", "pod_az_name", "az_name"]
        _pod = utils.FakePod.create_single_pod({key: " " for key in keys})
        arglist = [
            _pod['pod']['pod_id'],
            ]
        verifylist = [
            ("pod", _pod['pod']['pod_id']),
            ]
        self.pod_manager.get = mock.Mock(return_value=_pod)
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = (self.cmd.take_action(parsed_args))

        self.assertEqual(sorted(_pod['pod'].keys()), sorted(columns))
        self.assertEqual(sorted(_pod['pod'].values()), sorted(data))


class TestListPod(_TestPodCommand):

    columns = [
        'ID',
        'Region Name',
    ]

    def setUp(self):
        super(TestListPod, self).setUp()
        self.cmd = pods_cli.ListPods(self.app, None)

    def test_list(self):
        _pods = utils.FakePod.create_multiple_pods()
        for pod in _pods:
            pod.pop('dc_name')
            pod.pop('pod_az_name')
            pod.pop('az_name')
        self.pod_manager.list = mock.Mock(
            return_value={'pods': _pods})
        parsed_args = self.check_parser(self.cmd)
        columns, data = (self.cmd.take_action(parsed_args))

        self.assertEqual(self.columns, sorted(columns))
        self.assertEqual(len(_pods), len(data))


class TestDeletePod(_TestPodCommand, utils.TestCommandWithoutOptions):

    def setUp(self):
        super(TestDeletePod, self).setUp()
        self.cmd = pods_cli.DeletePod(self.app, None)

    def test_delete_pod(self):
        arglist = [utils.FakePod.create_single_pod()['pod']['pod_id']]
        verifylist = [
            ('pod', arglist),
            ]
        self.pod_manager.delete = mock.Mock(
            return_value=None)
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        result = self.cmd.take_action(parsed_args)
        self.assertIsNone(result)

    def test_delete_multiple_pod(self):
        arglist = [pod['pod_id'] for pod in
                   utils.FakePod.create_multiple_pods()]
        verifylist = [
            ('pod', arglist),
            ]
        self.pod_manager.delete = mock.Mock(return_value=None)
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        result = self.cmd.take_action(parsed_args)
        self.assertIsNone(result)
