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

from oslo_serialization import jsonutils

from tricircleclient.v1 import base


class RoutingManager(base.Manager):

    def list(self, path):
        """Get a list of Resource Routings."""
        return self._get(
            path,
            headers={'Content-Type': "application/json"}).json()

    def create(self, routing):
        """Create a Resource Routing."""
        return self._post(
            '/routings', headers={'Content-Type': "application/json"},
            data=jsonutils.dumps(routing)).json()

    def get(self, routing):
        """Get information about a Resource Routing."""
        return self._get(
            '/routings/%s' % routing,
            headers={'Content-Type': "application/json"}).json()

    def delete(self, routing):
        """Delete a Resource Routing."""
        self._delete('/routings/%s' % routing)

    def update(self, routing):
        """Update a Resource Routing."""
        self._put('/routings/%s' % routing['routing'].pop('id'),
                  headers={'Content-Type': "application/json"},
                  data=jsonutils.dumps(routing)).json()
