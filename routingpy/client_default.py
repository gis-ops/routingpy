# -*- coding: utf-8 -*-
# Copyright (C) 2021 GIS OPS UG
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

from .client_base import BaseClient, DEFAULT, _RETRIABLE_STATUSES, options
from . import exceptions
from .utils import get_ordinal

from datetime import datetime
import json
import random
import requests
import time
import warnings


class Client(BaseClient):
    """Default client class for requests handling, which is passed to each router. Uses the requests package."""

    def __init__(
        self,
        base_url,
        user_agent=None,
        timeout=DEFAULT,
        retry_timeout=None,
        retry_over_query_limit=None,
        skip_api_error=None,
        **kwargs
    ):
        """
        :param base_url: The base URL for the request. All routers must provide a default.
            Should not have a trailing slash.
        :type base_url: string

        :param user_agent: User-Agent to send with the requests to routing API.
            Overrides ``options.default_user_agent``.
        :type user_agent: string

        :param timeout: Combined connect and read timeout for HTTP requests, in
            seconds. Specify "None" for no timeout.
        :type timeout: int

        :param retry_timeout: Timeout across multiple retriable requests, in
            seconds.
        :type retry_timeout: int

        :param retry_over_query_limit: If True, client will not raise an exception
            on HTTP 429, but instead jitter a sleeping timer to pause between
            requests until HTTP 200 or retry_timeout is reached.
        :type retry_over_query_limit: bool

        :param skip_api_error: Continue with batch processing if a :class:`routingpy.exceptions.RouterApiError` is
            encountered (e.g. no route found). If False, processing will discontinue and raise an error. Default False.
        :type skip_api_error: bool

        :param **kwargs: Additional arguments, such as headers or proxies.
        :type **kwargs: dict
        """

        self._session = requests.Session()
        super(Client, self).__init__(
            base_url,
            user_agent=user_agent,
            timeout=timeout,
            retry_timeout=retry_timeout,
            retry_over_query_limit=retry_over_query_limit,
            skip_api_error=skip_api_error,
            **kwargs
        )

        self.kwargs = kwargs or {}
        try:
            self.headers.update(self.kwargs["headers"])
        except KeyError:
            pass

        self.kwargs["headers"] = self.headers
        self.kwargs["timeout"] = self.timeout

        self.proxies = self.kwargs.get("proxies") or options.default_proxies
        if self.proxies:
            self.kwargs["proxies"] = self.proxies

    def _request(
        self,
        url,
        get_params={},
        post_params=None,
        first_request_time=None,
        retry_counter=0,
        dry_run=None,
    ):
        """Performs HTTP GET/POST with credentials, returning the body as
        JSON.

        :param url: URL path for the request. Should begin with a slash.
        :type url: string

        :param get_params: HTTP GET parameters.
        :type get_params: dict or list of tuples

        :param post_params: HTTP POST parameters. Only specified by calling method.
        :type post_params: dict

        :param first_request_time: The time of the first request (None if no
            retries have occurred).
        :type first_request_time: :class:`datetime.datetime`

        :param retry_counter: The number of this retry, or zero for first attempt.
        :type retry_counter: int

        :param dry_run: If true, only prints URL and parameters. true or false.
        :type dry_run: bool

        :raises routingpy.exceptions.RouterApiError: when the API returns an error due to faulty configuration.
        :raises routingpy.exceptions.RouterServerError: when the API returns a server error.
        :raises routingpy.exceptions.RouterError: when anything else happened while requesting.
        :raises routingpy.exceptions.JSONParseError: when the JSON response can't be parsed.
        :raises routingpy.exceptions.Timeout: when the request timed out.
        :raises routingpy.exceptions.TransportError: when something went wrong while trying to
            execute a request.

        :returns: raw JSON response.
        :rtype: dict
        """

        if not first_request_time:
            first_request_time = datetime.now()

        elapsed = datetime.now() - first_request_time
        if elapsed > self.retry_timeout:
            raise exceptions.Timeout()

        if retry_counter > 0:
            # 0.5 * (1.5 ^ i) is an increased sleep time of 1.5x per iteration,
            # starting at 0.5s when retry_counter=1. The first retry will occur
            # at 1, so subtract that first.
            delay_seconds = 1.5 ** (retry_counter - 1)

            # Jitter this value by 50% and pause.
            time.sleep(delay_seconds * (random.random() + 0.5))

        authed_url = self._generate_auth_url(url, get_params)

        final_requests_kwargs = self.kwargs

        # Determine GET/POST.
        requests_method = self._session.get
        if post_params is not None:
            requests_method = self._session.post
            if final_requests_kwargs["headers"]["Content-Type"] == "application/json":
                final_requests_kwargs["json"] = post_params
            else:
                # Send as x-www-form-urlencoded key-value pair string (e.g. Mapbox API)
                final_requests_kwargs["data"] = post_params

        # Only print URL and parameters for dry_run
        if dry_run:
            print(
                "url:\n{}\nParameters:\n{}".format(
                    self.base_url + authed_url, json.dumps(final_requests_kwargs, indent=2)
                )
            )
            return

        try:
            response = requests_method(self.base_url + authed_url, **final_requests_kwargs)
            self._req = response.request

        except requests.exceptions.Timeout:
            raise exceptions.Timeout()

        tried = retry_counter + 1

        if response.status_code in _RETRIABLE_STATUSES:
            # Retry request.
            warnings.warn(
                "Server down.\nRetrying for the {}{} time.".format(tried, get_ordinal(tried)),
                UserWarning,
            )

            return self._request(url, get_params, post_params, first_request_time, retry_counter + 1)

        try:
            result = self._get_body(response)

            return result

        except exceptions.RouterApiError:
            if self.skip_api_error:
                warnings.warn(
                    "Router {} returned an API error with "
                    "the following message:\n{}".format(self.__class__.__name__, response.text)
                )
                return

            raise

        except exceptions.RetriableRequest as e:
            if isinstance(e, exceptions.OverQueryLimit) and not self.retry_over_query_limit:
                raise

            warnings.warn(
                "Rate limit exceeded.\nRetrying for the {}{} time.".format(tried, get_ordinal(tried)),
                UserWarning,
            )
            # Retry request.
            return self._request(url, get_params, post_params, first_request_time, retry_counter + 1)

    @property
    def req(self):
        """Holds the :class:`requests.PreparedRequest` property for the last request."""
        return self._req

    @staticmethod
    def _get_body(response):
        status_code = response.status_code

        try:
            body = response.json()
        except json.decoder.JSONDecodeError:
            raise exceptions.JSONParseError("Can't decode JSON response:{}".format(response.text))

        if status_code == 429:
            raise exceptions.OverQueryLimit(status_code, body)

        if 400 <= status_code < 500:
            raise exceptions.RouterApiError(status_code, body)

        if 500 <= status_code:
            raise exceptions.RouterServerError(status_code, body)

        if status_code != 200:
            raise exceptions.RouterError(status_code, body)

        return body
