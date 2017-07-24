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
from six.moves.urllib import parse

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
    result.update((k, v) for k, v in data.items() if v)
    return {'routing': result}


def _add_pagination_argument(parser):
    parser.add_argument(
        '-P', '--page-size',
        dest='limit', metavar='SIZE', type=int,
        help="Maximum number of routings to return",
        default=None)


def _add_marker_argument(parser):
    parser.add_argument(
        '-M', '--marker',
        dest='marker', metavar='MARKER', type=str,
        help="Starting point for next routing list "
             "that shares same routing id",
        default=None)


def _add_filtering_arguments(parser):
    parser.add_argument(
        '--id',
        dest='id', metavar='id', type=int,
        help="Uuid of a routing",
        default=None)
    parser.add_argument(
        '--top-id',
        dest='top_id', metavar='top_id', type=str,
        help="Resource id on Central Neutron",
        default=None)
    parser.add_argument(
        '--bottom-id',
        dest='bottom_id', metavar='bottom_id', type=str,
        help="Resource id on Local Neutron",
        default=None)
    parser.add_argument(
        '--pod-id',
        dest='pod_id', metavar='pod_id', type=str,
        help="Uuid of a pod",
        default=None)
    parser.add_argument(
        '--project-id',
        dest='project_id', metavar='project_id', type=str,
        help="Uuid of a project object in Keystone",
        default=None)
    parser.add_argument(
        '--resource-type',
        dest='resource_type', metavar='resource_type', type=str,
        choices=['network', 'subnet', 'port', 'router', 'security_group',
                 'trunk', 'port_pair', 'port_pair_group', 'flow_classifier',
                 'port_chain'],
        help="Available resource types",
        default=None)
    parser.add_argument(
        '--created-at',
        dest='created_at', metavar='created_at', type=str,
        help="Create time of the resource routing",
        default=None)
    parser.add_argument(
        '--updated-at',
        dest='updated_at', metavar='updated_at', type=str,
        help="Update time of the resource routing",
        default=None)


def _add_search_options(parsed_args):
    search_opts = {}
    for key in ('limit', 'marker', 'id', 'top_id', 'bottom_id', 'pod_id',
                'project_id', 'resource_type', 'created_at', 'updated_at'):
        value = getattr(parsed_args, key, None)
        if value is not None:
            search_opts[key] = value
    return search_opts


def _prepare_query_string(params):
    """Convert dict params to query string"""
    params = sorted(params.items(), key=lambda x: x[0])
    return '?%s' % parse.urlencode(params) if params else ''


class ListRoutings(command.Lister):
    """Lists Routings"""

    COLS = ('id', 'pod_id', 'resource_type')
    path = '/routings'

    pagination_support = True
    marker_support = True

    log = logging.getLogger(__name__ + ".ListRoutings")

    def get_parser(self, prog_name):
        parser = super(ListRoutings, self).get_parser(prog_name)

        if self.pagination_support:
            _add_pagination_argument(parser)
        if self.marker_support:
            _add_marker_argument(parser)
        _add_filtering_arguments(parser)

        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)
        client = self.app.client_manager.multiregion_networking

        # add pagination/marker/filter to list operation
        search_opts = _add_search_options(parsed_args)
        self.path += _prepare_query_string(search_opts)

        data = client.routing.list(self.path)
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
