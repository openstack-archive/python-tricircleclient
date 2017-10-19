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
from tricircleclient.v1 import routings_cli


class _TestRoutingCommand(utils.TestCommand):

    def setUp(self):
        super(_TestRoutingCommand, self).setUp()
        self.routing_manager = \
            self.app.client_manager.multiregion_networking.routing


class TestCreateRouting(_TestRoutingCommand, utils.TestCommandWithoutOptions):

    def setUp(self):
        super(TestCreateRouting, self).setUp()
        self.cmd = routings_cli.CreateRouting(self.app, None)

    def test_create_all_options(self):
        _routing = utils.FakeRouting.create_single_routing()
        arglist = [
            '--top-id', _routing['routing']['top_id'],
            '--bottom-id', _routing['routing']['bottom_id'],
            '--pod-id', _routing['routing']['pod_id'],
            '--project-id', _routing['routing']['project_id'],
            '--resource-type', _routing['routing']['resource_type'],
        ]
        verifylist = [
            ('top_id', _routing['routing']['top_id']),
            ('bottom_id', _routing['routing']['bottom_id']),
            ('pod_id', _routing['routing']['pod_id']),
            ('project_id', _routing['routing']['project_id']),
            ('resource_type', _routing['routing']['resource_type']),
        ]
        self.routing_manager.create = mock.Mock(return_value=_routing)
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = (self.cmd.take_action(parsed_args))

        self.assertEqual(sorted(_routing['routing'].keys()), sorted(columns))
        self.assertEqual(sorted(_routing['routing'].values()), sorted(data))


class TestShowRouting(_TestRoutingCommand, utils.TestCommandWithoutOptions):

    def setUp(self):
        super(TestShowRouting, self).setUp()
        self.cmd = routings_cli.ShowRouting(self.app, None)

    def test_show_valid_routing(self):
        _routing = utils.FakeRouting.create_single_routing()
        arglist = [
            _routing['routing']['id'],
            ]
        verifylist = [
            ('routing', _routing['routing']['id']),
            ]
        self.routing_manager.get = mock.Mock(return_value=_routing)
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = (self.cmd.take_action(parsed_args))

        self.assertEqual(sorted(_routing['routing'].keys()), sorted(columns))
        self.assertEqual(sorted(_routing['routing'].values()), sorted(data))


class TestListRouting(_TestRoutingCommand):

    columns = [
        'ID',
        'Pod ID',
        'Resource Type',
        'Top ID'
    ]

    def setUp(self):
        super(TestListRouting, self).setUp()
        self.cmd = routings_cli.ListRoutings(self.app, None)

    def test_list(self):
        _routings = utils.FakeRouting.create_multiple_routings()

        for routing in _routings:
            for key in ('bottom_id', 'project_id'):
                routing.pop(key)

        self.routing_manager.list = mock.Mock(
            return_value={'routings': _routings})
        parsed_args = self.check_parser(self.cmd)
        columns, data = (self.cmd.take_action(parsed_args))
        self.assertEqual(sorted(self.columns), sorted(columns))
        self.assertEqual(len(_routings), len(data))

    def test_list_with_filters(self):
        _routing = utils.FakeRouting.create_single_routing()
        _routing = _routing['routing']

        # we filter the routings by the following fields
        # given values of _routing, then only single item _routing
        # is retrieved.
        arglist = [
            '--top-id', _routing['top_id'],
            '--bottom-id', _routing['bottom_id'],
            '--pod-id', _routing['pod_id'],
            '--project-id', _routing['project_id'],
            '--resource-type', _routing['resource_type'],
            '--created-at', _routing['created_at'],
            '--updated-at', _routing['updated_at'],
        ]
        verifylist = [
            ('top_id', _routing['top_id']),
            ('bottom_id', _routing['bottom_id']),
            ('pod_id', _routing['pod_id']),
            ('project_id', _routing['project_id']),
            ('resource_type', _routing['resource_type']),
            ('created_at', _routing['created_at']),
            ('updated_at', _routing['updated_at']),
        ]
        for key in ('bottom_id', 'project_id'):
            _routing.pop(key)

        self.routing_manager.list = mock.Mock(
            return_value={'routings': [_routing]})
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = (self.cmd.take_action(parsed_args))

        self.assertEqual(self.columns, sorted(columns))
        self.assertEqual(1, len(data))

    def test_throw_exception(self):
        arglist = [
            '--resource-type', 'fake_resource_type',
        ]
        verifylist = []
        self.assertRaises(utils.ParserException, self.check_parser,
                          self.cmd, arglist, verifylist)

    def test_list_with_pagination(self):
        _routings = utils.FakeRouting.create_multiple_routings(count=3)
        arglist = [
            '--limit', '2',
            '--marker', _routings[0]['id'],
        ]
        verifylist = [
            ('limit', 2),
            ('marker', _routings[0]['id']),
        ]
        for routing in _routings:
            for key in ('bottom_id', 'project_id'):
                routing.pop(key)

        self.routing_manager.list = mock.Mock(
            return_value={'routings': _routings[1:]})
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = (self.cmd.take_action(parsed_args))

        self.assertEqual(sorted(self.columns), sorted(columns))
        self.assertEqual(2, len(data))


class TestDeleteRouting(_TestRoutingCommand, utils.TestCommandWithoutOptions):

    def setUp(self):
        super(TestDeleteRouting, self).setUp()
        self.cmd = routings_cli.DeleteRouting(self.app, None)

    def test_delete_routing(self):
        _routings = utils.FakeRouting.create_multiple_routings(count=2)

        arglist = [
            _routings[0]['id'],
            _routings[1]['id'],
            ]
        verifylist = [
            ('routing', [_routings[0]['id'], _routings[1]['id']]),
            ]
        self.routing_manager.delete = mock.Mock(return_value=None)
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        result = self.cmd.take_action(parsed_args)

        self.assertIsNone(result)

    def test_delete_multiple_routing(self):
        arglist = [routing['id'] for routing in
                   utils.FakeRouting.create_multiple_routings()]
        verifylist = [
            ('routing', arglist),
            ]
        self.routing_manager.delete = mock.Mock(return_value=None)
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        result = self.cmd.take_action(parsed_args)

        self.assertIsNone(result)


class TestUpdateRouting(_TestRoutingCommand, utils.TestCommandWithoutOptions):

    def setUp(self):
        super(TestUpdateRouting, self).setUp()
        self.cmd = routings_cli.UpdateRouting(self.app, None)

    def test_update_all_options(self):
        _routing = utils.FakeRouting.create_single_routing()
        arglist = [
            '--top-id', _routing['routing']['top_id'],
            '--bottom-id', _routing['routing']['bottom_id'],
            '--project-id', _routing['routing']['project_id'],
            '--resource-type', _routing['routing']['resource_type'],
            _routing['routing']['pod_id'],
        ]
        verifylist = [
            ('top_id', _routing['routing']['top_id']),
            ('bottom_id', _routing['routing']['bottom_id']),
            ('project_id', _routing['routing']['project_id']),
            ('resource_type', _routing['routing']['resource_type']),
            ('routing', _routing['routing']['pod_id']),
        ]
        self.routing_manager.update = mock.Mock(return_value=_routing)
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
