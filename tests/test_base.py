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
"""Tests for client module."""

import time

import requests
import responses

import routingpy
import tests as _test
from routingpy import client_default
from routingpy.routers import options


class ClientMock(client_default.Client):
    def __init__(self, *args, **kwargs):
        super(ClientMock, self).__init__(*args, **kwargs)

    def directions(self, *args, **kwargs):
        return self._request(*args, **kwargs)

    def isochrones(self):
        pass

    def matrix(self):
        pass


class BaseTest(_test.TestCase):
    def setUp(self):
        self.client = ClientMock("https://httpbin.org/")
        self.params = {"c": "d", "a": "b", "1": "2"}

    def test_router_by_name(self):
        for s in routingpy.routers._SERVICE_TO_ROUTER.keys():
            routingpy.routers.get_router_by_name(s)

        with self.assertRaises(routingpy.exceptions.RouterNotFound):
            routingpy.routers.get_router_by_name("orsm")

    def test_options(self):
        options.default_user_agent = "my_agent"
        options.default_timeout = 10
        options.default_retry_timeout = 10
        options.default_retry_over_query_limit = False
        options.default_proxies = {"https": "192.103.10.102"}
        new_client = ClientMock("https://foo.bar")
        req_kwargs = {
            "timeout": options.default_timeout,
            "headers": {"User-Agent": options.default_user_agent, "Content-Type": "application/json"},
            "proxies": options.default_proxies,
        }
        self.assertEqual(req_kwargs, new_client.kwargs)
        self.assertEqual(new_client.retry_over_query_limit, options.default_retry_over_query_limit)

    def test_urlencode(self):
        encoded_params = self.client._generate_auth_url("directions", self.params)
        self.assertEqual("directions?1=2&a=b&c=d", encoded_params)

    @responses.activate
    def test_skip_api_error(self):
        query = self.params
        responses.add(
            responses.POST,
            "https://httpbin.org/post",
            json=query,
            status=400,
            content_type="application/json",
        )

        client = ClientMock(base_url="https://httpbin.org", skip_api_error=False)
        print(client.skip_api_error)
        with self.assertRaises(routingpy.exceptions.RouterApiError):
            client.directions(url="/post", post_params=self.params)

        client = ClientMock(base_url="https://httpbin.org", skip_api_error=True)
        client.directions(url="/post", post_params=self.params)
        self.assertEqual(responses.calls[1].response.json(), query)

    @responses.activate
    def test_retry_timeout(self):
        query = self.params
        responses.add(
            responses.POST,
            "https://httpbin.org/post",
            json=query,
            status=429,
            content_type="application/json",
        )

        client = ClientMock(base_url="https://httpbin.org", retry_over_query_limit=True, retry_timeout=3)
        with self.assertRaises(routingpy.exceptions.OverQueryLimit):
            client.directions(url="/post", post_params=query)

    @responses.activate
    def test_raise_over_query_limit(self):
        query = self.params
        responses.add(
            responses.POST,
            "https://httpbin.org/post",
            json=query,
            status=429,
            content_type="application/json",
        )

        with self.assertRaises(routingpy.exceptions.OverQueryLimit):
            client = ClientMock(base_url="https://httpbin.org", retry_over_query_limit=False)
            client.directions(url="/post", post_params=query)

    @responses.activate
    def test_raise_timeout_retriable_requests(self):
        # Mock query gives 503 as HTTP status, code should try a few times to
        # request the same and then fail on Timeout() error.
        retry_timeout = 3
        query = self.params
        responses.add(
            responses.POST,
            "https://httpbin.org/post",
            json=query,
            status=503,
            content_type="application/json",
        )

        client = ClientMock(base_url="https://httpbin.org", retry_timeout=retry_timeout)

        start = time.time()
        with self.assertRaises(routingpy.exceptions.Timeout):
            client.directions(url="/post", post_params=self.params)
        end = time.time()
        self.assertTrue(retry_timeout < end - start < 2 * retry_timeout)

    @responses.activate
    def test_dry_run(self):
        # Test that nothing is requested when dry_run is 'true'

        responses.add(
            responses.POST,
            "https://api.openrouteservice.org/directions",
            json=None,
            status=200,
            content_type="application/json",
        )

        self.client.directions(get_params={"format_out": "geojson"}, url="directions/", dry_run="true")

        self.assertEqual(0, len(responses.calls))

    def test_headers(self):
        # Test that existing request_kwargs keys are not scrubbed

        timeout = {"holaDieWaldFee": 600}
        headers = {"headers": {"X-Rate-Limit": "50"}}

        client = ClientMock("https://httpbin.org", **dict(timeout, **headers))

        self.assertDictContainsSubset(timeout, client.kwargs)
        self.assertDictContainsSubset(headers["headers"], client.kwargs["headers"])

    @responses.activate
    def test_req_property(self):
        # Test if the req property is a PreparedRequest

        responses.add(
            responses.GET,
            "https://httpbin.org/routes?a=b",
            json={},
            status=200,
            content_type="application/json",
        )

        self.client.directions(url="routes", get_params={"a": "b"})

        assert isinstance(self.client.req, requests.PreparedRequest)
        self.assertEqual("https://httpbin.org/routes?a=b", self.client.req.url)
