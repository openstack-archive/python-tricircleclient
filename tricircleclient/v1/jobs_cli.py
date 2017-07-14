# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from osc_lib.command import command
from oslo_log import log as logging

from tricircleclient import constants
from tricircleclient import utils


def _job_from_args(parsed_args):
    # necessary parameters
    data = {'type': parsed_args.type,
            'project_id': parsed_args.project_id,
            }

    # optional parameters vary with job type
    resources = {}
    for id in constants.job_resource_map[data['type']]:
        resources[id] = getattr(parsed_args, id, None)
    data['resource'] = resources

    return {'job': data}


def expand_job_resource(job):
    # because job['resource'] is a dict value, so we should
    # expand its values and let them show as other fields in the
    # same level.
    for id in constants.job_resource_map[job['type']]:
        job[id] = job['resource'][id]
    job.pop('resource')
    return job


class ListJobs(command.Lister):
    """List Jobs"""
    log = logging.getLogger(__name__ + ".ListJobs")

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)
        client = self.app.client_manager.multiregion_networking
        data = client.job.list()
        column_headers = utils.prepare_column_headers(constants.COLUMNS,
                                                      constants.COLUMNS_REMAP)
        return utils.list2cols(constants.COLUMNS, data['jobs'], column_headers)


class CreateJob(command.ShowOne):
    """Create a Job"""

    log = logging.getLogger(__name__ + ".CreateJob")

    def get_parser(self, prog_name):
        parser = super(CreateJob, self).get_parser(prog_name)

        # as resource is a compound attribute, so we expand its fields
        # and list them as optional parameters. If new resources are
        # provisioned, they should be added here.
        parser.add_argument(
            '--type',
            metavar="<type>",
            required=True,
            help="Job type",
        )
        parser.add_argument(
            '--project_id',
            metavar="<project_id>",
            required=True,
            help="Uuid of a project object in Keystone",
        )
        parser.add_argument(
            '--router_id',
            metavar="<router_id>",
            help="Uuid of a router",
        )
        parser.add_argument(
            '--network_id',
            metavar="<network_id>",
            help="Uuid of a network",
        )
        parser.add_argument(
            '--pod_id',
            metavar="<pod_id>",
            help="Uuid of a pod",
        )
        parser.add_argument(
            '--port_id',
            metavar="<port_id>",
            help="Uuid of a port",
        )
        parser.add_argument(
            '--trunk_id',
            metavar="<trunk_id>",
            help="Uuid of a trunk",
        )
        parser.add_argument(
            '--subnet_id',
            metavar="<subnet_id>",
            help="Uuid of a subnet",
        )
        parser.add_argument(
            '--portchain_id',
            metavar="<portchain_id>",
            help="Uuid of a port chain",
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)
        client = self.app.client_manager.multiregion_networking
        data = client.job.create(_job_from_args(parsed_args))

        if 'job' in data.keys():
            return self.dict2columns(expand_job_resource(data['job']))


class ShowJob(command.ShowOne):
    """Display Job details."""
    log = logging.getLogger(__name__ + ".ShowJob")

    def get_parser(self, prog_name):
        parser = super(ShowJob, self).get_parser(prog_name)
        parser.add_argument(
            "id",
            metavar="<id>",
            help="Uuid of the job to display",
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)
        client = self.app.client_manager.multiregion_networking
        data = client.job.get(parsed_args.id)

        if 'job' in data.keys():
            return self.dict2columns(expand_job_resource(data['job']))


class DeleteJob(command.Command):
    """Delete a Job."""

    log = logging.getLogger(__name__ + ".DeleteJob")

    def get_parser(self, prog_name):
        parser = super(DeleteJob, self).get_parser(prog_name)
        parser.add_argument(
            "id",
            metavar="<id>",
            help="Uuid of the job to delete",
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)
        client = self.app.client_manager.multiregion_networking
        client.job.delete(parsed_args.id)


class RedoJob(command.Command):
    """Redo a Job."""

    log = logging.getLogger(__name__ + ".RedoJob")

    def get_parser(self, prog_name):
        parser = super(RedoJob, self).get_parser(prog_name)

        parser.add_argument(
            'id',
            metavar="<id>",
            help="Uuid of the job to redo",
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)
        client = self.app.client_manager.multiregion_networking
        client.job.update(parsed_args.id)
