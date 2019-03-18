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

from .valhalla import Valhalla


class MapboxValhalla(Valhalla):
    """Performs requests to Mapbox's Valhalla instance."""

    _base_url = 'https://api.mapbox.com/valhalla/v1'

    def __init__(self, api_key, user_agent=None, timeout=None,
                 retry_timeout=None, requests_kwargs=None, retry_over_query_limit=False):
        """
        Initializes a Valhalla client.

        :param api_key: Mapbox API key.
        :type api_key: str

        :param base_url: The base URL for the request. Defaults to the ORS API
            server. Should not have a trailing slash.
        :type base_url: str

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

        :param retry_over_query_limit: If True, the client will retry when query
            limit is reached (HTTP 429). Default False.
        :type retry_over_query_limit: bool
        """

        super(MapboxValhalla, self).__init__(self._base_url, api_key, user_agent, timeout, retry_timeout,
                                             requests_kwargs, retry_over_query_limit)
