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

from tricircleclient import constants
from tricircleclient.tests.unit import utils
from tricircleclient.v1 import jobs_cli


class _TestJobCommand(utils.TestCommand):

    def setUp(self):
        super(_TestJobCommand, self).setUp()
        self.job_manager = self.app.client_manager.multiregion_networking.job


class TestCreateJob(_TestJobCommand, utils.TestCommandWithoutOptions):

    def setUp(self):
        super(TestCreateJob, self).setUp()
        self.cmd = jobs_cli.CreateJob(self.app, None)

    def test_create_all_options(self):
        _job = utils.FakeJob.create_single_job()
        arglist = [
            '--type', _job['job']['type'],
            '--project_id', _job['job']['project_id'],
            '--pod_id', _job['job']['resource']['pod_id'],
            '--router_id', _job['job']['resource']['router_id'],
            '--network_id', _job['job']['resource']['network_id'],
        ]
        verifylist = [
            ('type', _job['job']['type']),
            ('project_id', _job['job']['project_id']),
            ('pod_id', _job['job']['resource']['pod_id']),
            ('router_id', _job['job']['resource']['router_id']),
            ('network_id', _job['job']['resource']['network_id']),
        ]

        self.job_manager.create = mock.Mock(return_value=_job)
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = (self.cmd.take_action(parsed_args))

        self.assertEqual(sorted(_job['job'].keys()), sorted(columns))
        self.assertEqual(sorted(_job['job'].values()), sorted(data))


class TestShowJob(_TestJobCommand, utils.TestCommandWithoutOptions):

    def setUp(self):
        super(TestShowJob, self).setUp()
        self.cmd = jobs_cli.ShowJob(self.app, None)

    def test_show_a_single_job(self):
        _job = utils.FakeJob.create_single_job()
        arglist = [
            _job['job']['id'],
            ]
        verifylist = [
            ('id', _job['job']['id']),
            ]
        self.job_manager.get = mock.Mock(return_value=_job)
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = (self.cmd.take_action(parsed_args))

        self.assertEqual(sorted(_job['job'].keys()), sorted(columns))
        self.assertEqual(sorted(_job['job'].values()), sorted(data))


class TestListJob(_TestJobCommand):

    def setUp(self):
        super(TestListJob, self).setUp()
        self.cmd = jobs_cli.ListJobs(self.app, None)

    def test_list(self):
        _jobs = utils.FakeJob.create_multiple_jobs()
        self.job_manager.list = mock.Mock(return_value={'jobs': _jobs})
        parsed_args = self.check_parser(self.cmd)
        columns, data = (self.cmd.take_action(parsed_args))

        self.assertEqual(sorted(constants.COLUMNS_REMAP.values()),
                         sorted(columns))
        self.assertEqual(len(_jobs), len(data))
        self.assertEqual(
            sorted([tuple(o[k] for k in constants.COLUMNS) for o in _jobs]),
            sorted(data))


class TestDeleteJob(_TestJobCommand, utils.TestCommandWithoutOptions):

    def setUp(self):
        super(TestDeleteJob, self).setUp()
        self.cmd = jobs_cli.DeleteJob(self.app, None)

    def test_delete_job(self):
        _job = utils.FakeJob.create_single_job()
        arglist = [
            _job['job']['id'],
            ]
        verifylist = [
            ('id', _job['job']['id']),
            ]
        self.job_manager.delete = mock.Mock(return_value=None)
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        result = self.cmd.take_action(parsed_args)

        self.assertIsNone(result)


class TestRedoJob(_TestJobCommand, utils.TestCommandWithoutOptions):

    def setUp(self):
        super(TestRedoJob, self).setUp()
        self.cmd = jobs_cli.RedoJob(self.app, None)

    def test_redo_job(self):
        _job = utils.FakeJob.create_single_job()
        arglist = [
            _job['job']['id'],
        ]
        verifylist = [
            ('id', _job['job']['id']),
        ]
        self.job_manager.update = mock.Mock(return_value=None)
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        result = self.cmd.take_action(parsed_args)

        self.assertIsNone(result)
