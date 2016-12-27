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


class PodManager(base.Manager):

    def list(self, search_opts=None):
        """Get a list of Pods."""
        return self._get(
            '/pods',
            headers={'Content-Type': "application/json"}).json()

    def create(self, pod):
        """Create a Pod."""
        return self._post(
            '/pods', headers={'Content-Type': "application/json"},
            data=jsonutils.dumps(pod)).json()

    def get(self, pod):
        """Get information about a Pod."""
        return self._get(
            '/pods/%s' % pod,
            headers={'Content-Type': "application/json"}).json()

    def delete(self, pod):
        """Delete a Pod."""
        self._delete('/pods/%s' % pod)
