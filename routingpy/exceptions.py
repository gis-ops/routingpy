# -*- coding: utf-8 -*-
# Copyright (C) 2019 GIS OPS UG
#
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#
"""
Defines exceptions that are thrown by the ORS client.
"""


class RouterError(Exception):
    """Represents an exception returned by the remote API."""

    def __init__(self, status, message=None):
        self.status = status
        self.message = message

    def __str__(self):
        if self.message is None:
            return self.status
        else:
            return "%s (%s)" % (self.status, self.message)


class RouterApiError(RouterError):
    """Represents an exception returned by a routing engine, i.e. 400 <= HTTP status code <= 500"""


class RouterServerError(RouterError):
    """Represents an exception returned by a server, i.e. 500 <= HTTP"""


class HTTPError(Exception):
    """An unexpected HTTP error occurred."""

    def __init__(self, status_code):
        self.status_code = status_code

    def __str__(self):
        return "HTTP Error: %d" % self.status_code


class Timeout(Exception):
    """The request timed out."""
    pass


class JSONParseError(Exception):
    """The Json response can't be parsed.."""
    pass


class RetriableRequest(Exception):
    """Signifies that the request can be retried."""
    pass


class OverQueryLimit(RouterError, RetriableRequest):
    """Signifies that the request failed because the client exceeded its query rate limit.

    Normally we treat this as a retriable condition, but we allow the calling code to specify that these requests should
    not be retried.
    """
    pass
