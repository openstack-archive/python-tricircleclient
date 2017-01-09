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

from tricircleclient import utils


class ListPods(command.Lister):
    """Lists pods"""

    COLS = ('pod_id', 'region_name')

    log = logging.getLogger(__name__ + ".ListPods")

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)
        client = self.app.client_manager.multiregion_networking
        data = client.pod.list()
        remap = {'pod_id': 'Id',
                 'region_name': 'Region Name',
                 'az_name': 'Availability Zone',
                 'dc_name': 'Data Center'}
        column_headers = utils.prepare_column_headers(self.COLS,
                                                      remap)

        return utils.list2cols(
            self.COLS, data['pods'], column_headers)


class CreatePod(command.ShowOne):
    """Creates pod"""

    log = logging.getLogger(__name__ + ".CreatePod")

    @staticmethod
    def _pod_from_args(parsed_args):
        return {'pod': {'region_name': parsed_args.region_name,
                        'az_name': parsed_args.availability_zone,
                        'pod_az_name': parsed_args.pod_availability_zone,
                        'dc_name': parsed_args.data_center,
                        }}

    def get_parser(self, prog_name):
        parser = super(CreatePod, self).get_parser(prog_name)

        parser.add_argument(
            '--region-name',
            metavar="<region_name>",
            required=True,
            help="Region name registered in Keystone",
        )
        parser.add_argument(
            '--availability-zone',
            metavar="<az_name>",
            help="Name of the Availability Zone",
        )
        parser.add_argument(
            '--pod-availability-zone',
            metavar="<pod_az_name>",
            help="Name of the Availability Zone forwarded to local Neutron",
        )
        parser.add_argument(
            '--data-center',
            metavar="<dc_name>",
            help="Name of the Data Center",
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)
        client = self.app.client_manager.multiregion_networking
        data = client.pod.create(self._pod_from_args(parsed_args))

        return self.dict2columns(data['pod'])


class ShowPod(command.ShowOne):
    """Display pod details."""

    log = logging.getLogger(__name__ + ".ShowPod")

    def get_parser(self, prog_name):
        parser = super(ShowPod, self).get_parser(prog_name)
        parser.add_argument(
            "pod",
            metavar="<pod>",
            help="Id of the pod to display",
        )

        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)
        client = self.app.client_manager.multiregion_networking
        data = client.pod.get(parsed_args.pod)

        if 'pod' in data.keys():
            return self.dict2columns(data['pod'])


class DeletePod(command.Command):
    """Deletes Pod."""

    log = logging.getLogger(__name__ + ".DeletePod")

    def get_parser(self, prog_name):
        parser = super(DeletePod, self).get_parser(prog_name)
        parser.add_argument(
            "pod",
            metavar="<pod>",
            nargs="+",
            help="ID(s) of the pod(s) to delete",
        )

        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)
        client = self.app.client_manager.multiregion_networking
        for pod_id in parsed_args.pod:
            client.pod.delete(pod_id)
