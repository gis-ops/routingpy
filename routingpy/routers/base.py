# -*- coding: utf-8 -*-
# Copyright 2014 Google Inc. All rights reserved.
#
# Modifications Copyright (C) 2019 GIS OPS UG
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
Core client functionality, common across all API requests.
"""

from routingpy import exceptions
from ..__version__ import __version__

from abc import ABCMeta, abstractmethod
from datetime import datetime
from datetime import timedelta
import warnings
import requests
from urllib.parse import urlencode
import json
import random
import time

_DEFAULT_USER_AGENT = "routingpy.v{}".format(__version__)
_RETRIABLE_STATUSES = set([503])


class options(object):
    """Set options for all routers."""

    default_timeout = 60
    default_retry_timeout = 60
    default_user_agent = _DEFAULT_USER_AGENT


class Router(metaclass=ABCMeta):
    """Performs requests to the API service of choice."""

    def __init__(self, base_url, user_agent=None, timeout=None, retry_timeout=None, requests_kwargs=None,
                 retry_over_query_limit=True):
        """

        :param base_url: The base URL for the request. Defaults to the ORS API
            server. Should not have a trailing slash.
        :type base_url: string

        :param key: They key for authorization used as GET param or POST auth header.
        :type base_url: string

        :param timeout: Combined connect and read timeout for HTTP requests, in
            seconds. Specify "None" for no timeout.
        :type timeout: int

        :param retry_timeout: Timeout across multiple retriable requests, in
            seconds.
        :type retry_timeout: int

        :param requests_kwargs: Extra keyword arguments for the requests
            library, which among other things allow for proxy auth to be
            implemented. See the official requests docs for more info:
            http://docs.python-requests.org/en/latest/api/#main-interface
        :type requests_kwargs: dict

        :param retry_over_query_limit: If True, client will not raise an exception
            on HTTP 429, but instead jitter a sleeping timer to pause between
            requests until HTTP 200 or retry_timeout is reached.
        """

        self._session = requests.Session()
        self._base_url = base_url

        self._retry_over_query_limit = retry_over_query_limit
        self._retry_timeout = timedelta(seconds=retry_timeout or options.default_retry_timeout)

        self._requests_kwargs = requests_kwargs or {}
        add_headers = {
                "User-Agent": user_agent or options.default_user_agent,
                'Content-Type': 'application/json'
            }
        try:
            self._requests_kwargs['headers'].update(add_headers)
        except KeyError:
            self._requests_kwargs.update({'headers': add_headers})
        add_timeout = self._requests_kwargs.get('timeout') or timeout or options.default_timeout
        self._requests_kwargs['timeout'] = add_timeout

        self._req = None

    def _request(self,
                 url,
                 get_params={},
                 post_params=None,
                 first_request_time=None,
                 retry_counter=0,
                 requests_kwargs=None,
                 dry_run=None):
        """Performs HTTP GET/POST with credentials, returning the body as
        JSON.

        :param url: URL path for the request. Should begin with a slash.
        :type url: string

        :param get_params: HTTP GET parameters.
        :type get_params: dict or list of key/value tuples

        :param first_request_time: The time of the first request (None if no
            retries have occurred).
        :type first_request_time: datetime.datetime

        :param retry_counter: The number of this retry, or zero for first attempt.
        :type retry_counter: int

        :param requests_kwargs: Same extra keywords arg for requests as per
            __init__, but provided here to allow overriding internally on a
            per-request basis.
        :type requests_kwargs: dict

        :param post_params: HTTP POST parameters. Only specified by calling method.
        :type post_params: dict

        :param dry_run: If 'true', only prints URL and parameters. 'true' or 'false'.
        :type dry_run: string

        :raises ApiError: when the API returns an error.
        :raises Timeout: if the request timed out.
        :raises TransportError: when something went wrong while trying to
            execute a request.

        :rtype: dict from JSON response.
        """

        if not first_request_time:
            first_request_time = datetime.now()

        elapsed = datetime.now() - first_request_time
        if elapsed > self._retry_timeout:
            raise exceptions.Timeout()

        if retry_counter > 0:
            # 0.5 * (1.5 ^ i) is an increased sleep time of 1.5x per iteration,
            # starting at 0.5s when retry_counter=1. The first retry will occur
            # at 1, so subtract that first.
            delay_seconds = 1.5 ** (retry_counter - 1)

            # Jitter this value by 50% and pause.
            time.sleep(delay_seconds * (random.random() + 0.5))

        authed_url = self._generate_auth_url(url,
                                             get_params
                                             )

        # Default to the client-level self.requests_kwargs, with method-level
        # requests_kwargs arg overriding.
        requests_kwargs = requests_kwargs or {}
        final_requests_kwargs = dict(self._requests_kwargs, **requests_kwargs)
        # Determine GET/POST.
        requests_method = self._session.get
        if post_params is not None:
            requests_method = self._session.post
            final_requests_kwargs["json"] = post_params

        # Only print URL and parameters for dry_run
        if dry_run:
            print("url:\n{}\nParameters:\n{}".format(self._base_url + authed_url,
                                                     json.dumps(final_requests_kwargs, indent=2)))
            return

        try:
            response = requests_method(self._base_url + authed_url,
                                       **final_requests_kwargs)
            self._req = response.request

        except requests.exceptions.Timeout:
            raise exceptions.Timeout()

        if response.status_code in _RETRIABLE_STATUSES:
            # Retry request.
            warnings.warn('Server down.\nRetrying for the {}th time.'.format(retry_counter + 1),
                          UserWarning)

            return self._request(url, get_params, post_params, first_request_time,
                                 retry_counter + 1, requests_kwargs)

        try:
            result = self._get_body(response)

            return result
        except exceptions._RetriableRequest as e:
            if isinstance(e, exceptions._OverQueryLimit) and not self._retry_over_query_limit:
                raise

            warnings.warn('Rate limit exceeded.\nRetrying for the {}th time.'.format(retry_counter + 1),
                          UserWarning)
            # Retry request.
            return self._request(url, get_params, post_params, first_request_time,
                                 retry_counter + 1, requests_kwargs,
                                )

    @property
    def req(self):
        return self._req

    @staticmethod
    def _get_body(response):
        status_code = response.status_code

        try:
            body = response.json()
        except json.decoder.JSONDecodeError:
            raise exceptions._JSONParseError("Can't decode JSON response")

        if status_code == 429:
            raise exceptions._OverQueryLimit(
                status_code, body
            )

        if 400 <= status_code < 500:
            raise exceptions.RouterApiError(
                status_code, body
            )

        if 500 <= status_code:
            raise exceptions.RouterServerError(
                status_code, body
            )

        if status_code != 200:
            raise exceptions.RouterError(
                status_code,
                body
            )

        return body


    @staticmethod
    def _generate_auth_url(path, params):
        """Returns the path and query string portion of the request URL, first
        adding any necessary parameters.

        :param path: The path portion of the URL.
        :type path: string

        :param params: URL parameters.
        :type params: dict or list of key/value tuples

        :rtype: string

        """
        
        if isinstance(params, dict):
            params = sorted(dict(**params).items())
        elif isinstance(params, (list, tuple)):
            params = sorted(params)

        return path + "?" + requests.utils.unquote_unreserved(urlencode(params))

    @abstractmethod
    def directions(self):
        pass

    @abstractmethod
    def isochrones(self):
        pass

    @abstractmethod
    def distance_matrix(self):
        pass

    def optimization(self):
        pass

    def map_matching(self):
        pass
