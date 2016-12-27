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

"""OpenStackClient plugin for Multiregion Networking service."""

from osc_lib import utils


DEFAULT_MULTIREGION_NETWORKING_API_VERSION = '1'

# Required by the OSC plugin interface
API_NAME = 'multiregion_networking'
API_VERSION_OPTION = 'os_multiregion_networking_api_version'
API_VERSIONS = {
    '1': 'tricircleclient.v1.client.Client',
}


# Required by the OSC plugin interface
def make_client(instance):
    plugin_client = utils.get_client_class(
        API_NAME,
        instance._api_version[API_NAME],
        API_VERSIONS)

    instance.setup_auth()

    return plugin_client(
        session=instance.session,
        region_name=instance.region_name)


# Required by the OSC plugin interface
def build_option_parser(parser):
    """Hook to add global options."""
    parser.add_argument(
        "--os-multiregion-networking-api-version",
        metavar="<multiregion-networking-api-version>",
        default=utils.env(
            'OS_MULTIREGION_NETWORKING_API_VERSION',
            default=DEFAULT_MULTIREGION_NETWORKING_API_VERSION),
        help=("Multiregion Networking API version, default=" +
              DEFAULT_MULTIREGION_NETWORKING_API_VERSION +
              ' (Env: OS_MULTIREGION_NETWORKING_API_VERSION)'))
    parser.add_argument(
        "--os-multiregion-networking-url",
        default=utils.env(
            "OS_MULTIREGION_NETWORKING_URL"),
        help=("Data processing API URL, "
              "(Env: OS_MULTIREGION_NETWORKING_URL)"))
    return parser
