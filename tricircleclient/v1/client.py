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

from tricircleclient import client
from tricircleclient.v1 import pods
from tricircleclient.v1 import routings


class Client(object):
    """Client for the Tricircle v1 API.

    :param string session: session
    :type session: :py:class:`keystoneauth.adapter.Adapter`
    """

    def __init__(self, session=None, service_type='tricircle', **kwargs):
        """Initialize a new client for the Tricircle v1 API."""
        self.api = client.SessionClient(session, service_type=service_type,
                                        **kwargs)
        self.pod = pods.PodManager(self)
        self.routing = routings.RoutingManager(self)
