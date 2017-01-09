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

import six

from osc_lib.command import command
from oslo_log import log as logging

from tricircleclient import utils


def _routing_from_args(parsed_args):
    data = {'top_id': parsed_args.top_id,
            'bottom_id': parsed_args.bottom_id,
            'pod_id': parsed_args.pod_id,
            'project_id': parsed_args.project_id,
            'resource_type': parsed_args.resource_type,
            'id': getattr(parsed_args, 'routing', None),
            }
    result = {}
    result.update((k, v) for k, v in six.iteritems(data) if v)
    return {'routing': result}


class ListRoutings(command.Lister):
    """Lists Routings"""

    COLS = ('id', 'pod_id', 'resource_type')

    log = logging.getLogger(__name__ + ".ListRoutings")

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)
        client = self.app.client_manager.multiregion_networking
        data = client.routing.list()
        remap = {'id': 'Id',
                 'pod_id': 'Pod Id',
                 'resource_type': 'Resource Type'}
        column_headers = utils.prepare_column_headers(self.COLS,
                                                      remap)

        return utils.list2cols(
            self.COLS, data['routings'], column_headers)


class CreateRouting(command.ShowOne):
    """Creates a Resource Routing"""

    log = logging.getLogger(__name__ + ".CreateRouting")

    def get_parser(self, prog_name):
        parser = super(CreateRouting, self).get_parser(prog_name)

        parser.add_argument(
            '--top-id',
            metavar="<top_id>",
            required=True,
            help="Resource id on Central Neutron",
        )
        parser.add_argument(
            '--bottom-id',
            metavar="<bottom_id>",
            required=True,
            help="Resource id on Local Neutron",
        )
        parser.add_argument(
            '--pod-id',
            metavar="<pod_id>",
            required=True,
            help="Uuid of a pod",
        )
        parser.add_argument(
            '--project-id',
            metavar="<project_id>",
            required=True,
            help="Uuid of a project object in Keystone",
        )
        parser.add_argument(
            '--resource-type',
            metavar="<resource_type>",
            choices=['network', 'subnet', 'port', 'router', 'security_group'],
            required=True,
            help="Available resource types",
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)
        client = self.app.client_manager.multiregion_networking
        data = client.routing.create(_routing_from_args(parsed_args))

        return self.dict2columns(data['routing'])


class ShowRouting(command.ShowOne):
    """Display Routing Resource details."""

    log = logging.getLogger(__name__ + ".ShowRouting")

    def get_parser(self, prog_name):
        parser = super(ShowRouting, self).get_parser(prog_name)
        parser.add_argument(
            "routing",
            metavar="<routing>",
            help="Id of the routing resource to display",
        )

        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)
        client = self.app.client_manager.multiregion_networking
        data = client.routing.get(parsed_args.routing)

        if 'routing' in data.keys():
            return self.dict2columns(data['routing'])


class DeleteRouting(command.Command):
    """Deletes Routing Resource."""

    log = logging.getLogger(__name__ + ".DeleteRouting")

    def get_parser(self, prog_name):
        parser = super(DeleteRouting, self).get_parser(prog_name)
        parser.add_argument(
            "routing",
            metavar="<Routing>",
            nargs="+",
            help="ID(s) of the routing resource(s) to delete",
        )

        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)
        client = self.app.client_manager.multiregion_networking
        for routing_id in parsed_args.routing:
            client.routing.delete(routing_id)


class UpdateRouting(command.Command):
    """Updates a Routing Resource."""

    log = logging.getLogger(__name__ + ".UpdateRouting")

    def get_parser(self, prog_name):
        parser = super(UpdateRouting, self).get_parser(prog_name)

        parser.add_argument(
            '--top-id',
            metavar="<top_id>",
            help="Resource id on Central Neutron",
        )
        parser.add_argument(
            '--bottom-id',
            metavar="<bottom_id>",
            help="Resource id on Local Neutron",
        )
        parser.add_argument(
            '--pod-id',
            metavar="<pod_id>",
            help="Uuid of a pod",
        )
        parser.add_argument(
            '--project-id',
            metavar="<project_id>",
            help="Uuid of a project object in Keystone",
        )
        parser.add_argument(
            '--resource-type',
            metavar="<resource_type>",
            choices=['network', 'subnet', 'port', 'router', 'security_group'],
            help="Available resource types",
        )
        parser.add_argument(
            "routing",
            metavar="<Routing>",
            help="ID of the routing resource to update",
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)
        client = self.app.client_manager.multiregion_networking
        client.routing.update(_routing_from_args(parsed_args))
