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


class JobManager(base.Manager):

    def list(self, path):
        """Get a list of jobs."""
        return self._get(
            path,
            headers={'Content-Type': "application/json"}).json()

    def create(self, job):
        """Create a job."""
        return self._post(
            '/jobs', headers={'Content-Type': "application/json"},
            data=jsonutils.dumps(job)).json()

    def get(self, id):
        """Get information about a job."""
        return self._get(
            '/jobs/%s' % id,
            headers={'Content-Type': "application/json"}).json()

    def delete(self, id):
        """Delete a job."""
        self._delete('/jobs/%s' % id)

    def update(self, id):
        """Redo a job."""
        self._put('/jobs/%s' % id,
                  headers={'Content-Type': "application/json"},
                  data=None).json()
