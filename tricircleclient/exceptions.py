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

import re
import six

from oslo_utils import encodeutils


@six.python_2_unicode_compatible
class ClientException(Exception):
    """The base exception class for all exceptions this library raises."""
    message = 'Unknown Error'

    def __init__(self, code=None, message=None, request_id=None,
                 url=None, method=None):
        self.code = code
        self.message = encodeutils.safe_decode(
            message or self.__class__.message)
        self.request_id = request_id
        self.url = url
        self.method = method

    def __str__(self):
        formatted_string = "%s" % self.message
        if self.code:
            formatted_string += " (HTTP %s)" % self.code
        if self.request_id:
            formatted_string += " (Request-ID: %s)" % self.request_id
        return formatted_string


class MutipleMeaningException(object):
    """An mixin for exception that can be enhanced by reading the details"""


class BadRequest(ClientException):
    """HTTP 400 - Bad request: you sent some malformed data."""
    http_status = 400
    message = "Bad request"


class Unauthorized(ClientException):
    """HTTP 401 - Unauthorized: bad credentials."""
    http_status = 401
    message = "Unauthorized"


class NotFound(ClientException):
    """HTTP 404 - Not found"""
    http_status = 404
    message = "Not found"


class PodNotFound(NotFound, MutipleMeaningException):
    message = "Pod not found"
    match = re.compile("Pod .* does not exist")


class Conflict(ClientException):
    """HTTP 409 - Conflict"""
    http_status = 409
    message = "Conflict"


class RecordAlreadyExists(Conflict, MutipleMeaningException):
    message = "Record already exists"
    match = re.compile("Record already exists")


class PodRegionDuplicated(Conflict, MutipleMeaningException):
    message = "Pod region name duplicated with the top region name"
    match = re.compile("Pod region name duplicated with the top region name")


class TopRegionAlreadyExists(Conflict, MutipleMeaningException):
    message = "Top region already exists"
    match = re.compile("Top region already exists")


class UnprocessableEntity(ClientException):
    """HTTP 422 - Unprocessable Entity"""
    http_status = 422
    message = "Unprocessable Entity"


class RegionRequiredForTopRegion(UnprocessableEntity, MutipleMeaningException):
    message = "Valid region_name is required for top region"
    match = re.compile("Valid region_name is required for top region")


class RegionRequiredForPod(UnprocessableEntity, MutipleMeaningException):
    message = "Valid region_name is required for pod"
    match = re.compile("Valid region_name is required for pod")


_error_classes = [BadRequest, Unauthorized, NotFound, Conflict]
_error_classes_enhanced = {
    NotFound: [PodNotFound, ],
    Conflict: [RecordAlreadyExists, PodRegionDuplicated,
               TopRegionAlreadyExists],
    UnprocessableEntity: [RegionRequiredForTopRegion, RegionRequiredForPod]
}
_code_map = dict(
    (c.http_status, (c, _error_classes_enhanced.get(c, [])))
    for c in _error_classes)


def from_response(response, method=None):
    """Return an instance of one of the ClientException on an requests response.

    Usage::

        resp, body = requests.request(...)
        if resp.status_code != 200:
            raise from_response(resp)

    """
    if response.status_code:
        cls, enhanced_classes = _code_map.get(response.status_code,
                                              (ClientException, []))

    req_id = response.headers.get("x-openstack-request-id")

    kwargs = {
        'code': response.status_code,
        'method': method,
        'url': response.url,
        'request_id': req_id,
    }

    if "retry-after" in response.headers:
        kwargs['retry_after'] = response.headers.get('retry-after')

    desc = response.text
    if desc:
        for enhanced_cls in enhanced_classes:
            if enhanced_cls.match.match(response.text):
                cls = enhanced_cls
                break
        kwargs['message'] = desc

    if not kwargs['message']:
        del kwargs['message']
    return cls(**kwargs)
