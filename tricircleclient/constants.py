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

# asynchronous job types
JT_CONFIGURE_ROUTE = 'configure_route'
JT_ROUTER_SETUP = 'router_setup'
JT_PORT_DELETE = 'port_delete'
JT_SEG_RULE_SETUP = 'seg_rule_setup'
JT_NETWORK_UPDATE = 'update_network'
JT_SUBNET_UPDATE = 'subnet_update'
JT_SHADOW_PORT_SETUP = 'shadow_port_setup'
JT_TRUNK_SYNC = 'trunk_sync'
JT_SFC_SYNC = 'sfc_sync'
JT_RESOURCE_RECYCLE = 'resource_recycle'

# all resources needed to run the job. We specify it by
# {job_type: [resource_id1, resource_id2, ...]}.
job_resource_map = {
    JT_CONFIGURE_ROUTE: ["router_id"],
    JT_ROUTER_SETUP: ["pod_id", "router_id", "network_id"],
    JT_PORT_DELETE: ["pod_id", "port_id"],
    JT_SEG_RULE_SETUP: ["project_id"],
    JT_NETWORK_UPDATE: ["pod_id", "network_id"],
    JT_TRUNK_SYNC: ["pod_id", "trunk_id"],
    JT_SUBNET_UPDATE: ["pod_id", "subnet_id"],
    JT_SHADOW_PORT_SETUP: ["pod_id", "network_id"],
    JT_SFC_SYNC: ["pod_id", "portchain_id", "network_id"],
    JT_RESOURCE_RECYCLE: ["project_id"]
}

# job has many attributes, especially its resource attribute may vary with
# job type, To have unified column headers when show the job information,
# only the fields listed below will turn up in column headers. They are
# listed by alphabet order.
COLUMNS = ('id', 'project_id', 'status', 'timestamp', 'type')

# column headers about job that show in command line.
COLUMNS_REMAP = {'id': 'ID',
                 'project_id': 'Project',
                 'timestamp': 'Timestamp',
                 'status': 'Status',
                 'type': 'Type'}
