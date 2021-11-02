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
from routingpy.client_base import DEFAULT
from routingpy.client_default import Client
from routingpy.optimization import Optimization, Vehicle, Summary, Route, Unassigned


class Vroom:
    def __init__(
        self,
        base_url,
        user_agent=None,
        timeout=DEFAULT,
        retry_timeout=None,
        retry_over_query_limit=False,
        skip_api_error=None,
        client=Client,
        **client_kwargs
    ):
        """
        Initializes a Vroom client.

        :param base_url: The base URL for the request.
        :type base_url: str

        :param user_agent: User Agent to be used when requesting.
            Default :attr:`routingpy.routers.options.default_user_agent`.
        :type user_agent: str

        :param timeout: Combined connect and read timeout for HTTP requests, in
            seconds. Specify ``None`` for no timeout. Default :attr:`routingpy.routers.options.default_timeout`.
        :type timeout: int or None

        :param retry_timeout: Timeout across multiple retriable requests, in
            seconds.  Default :attr:`routingpy.routers.options.default_retry_timeout`.
        :type retry_timeout: int

        :param retry_over_query_limit: If True, client will not raise an exception
            on HTTP 429, but instead jitter a sleeping timer to pause between
            requests until HTTP 200 or retry_timeout is reached.
            Default :attr:`routingpy.routers.options.default_retry_over_query_limit`.
        :type retry_over_query_limit: bool

        :param skip_api_error: Continue with batch processing if a :class:`routingpy.exceptions.RouterApiError` is
            encountered (e.g. no route found). If False, processing will discontinue and raise an error.
            Default :attr:`routingpy.routers.options.default_skip_api_error`.
        :type skip_api_error: bool

        :param client: A client class for request handling. Needs to be derived from :class:`routingpy.base.BaseClient`
        :type client: abc.ABCMeta

        :param **client_kwargs: Additional arguments passed to the client, such as headers or proxies.
        :type **client_kwargs: dict
        """

        self.client = client(
            base_url,
            user_agent,
            timeout,
            retry_timeout,
            retry_over_query_limit,
            skip_api_error,
            **client_kwargs
        )

    def optimization(
        self, vehicles, jobs=None, shipments=None, matrices=None, geometry=False, dry_run=None
    ):
        """
        Optimize a fleet of vehicles on a number of jobs.
        For more information, visit https://github.com/VROOM-Project/vroom/blob/master/docs/API.md.
        Example:
            >>> from routingpy.routers import Vroom
            >>> from routingpy.optimization import Job, Vehicle
            >>> vehicles = [Vehicle(0, start=[7.414210118164926, 43.72810792282373], end=[7.414210118164926, 43.72810792282373])]
            >>> jobs = [Job(0, location=[7.423805608013283, 43.739198887075084]), Job(1, location=[7.414257185161816, 43.73378896481369])]
            >>> v = Vroom("http://localhost:3000")
            >>> o = v.optimization(jobs, vehicles, geometry=True)
        :param vehicles: array of vehicle objects describing the available vehicles.
        :type vehicles: list of Vehicle
        :param jobs: array of job objects describing the places to visit.
        :type jobs: list of Job
        :param shipments: array of shipment objects describing pickup and delivery tasks.
        :type shipments: list of Shipment
        :param matrices: optional description of per-profile custom matrices
        :type matrices: object
        :param geometry: Whether the geometry of the resulting routes should be calculated. Defaults to False.
        :type geometry: bool
        :param dry_run: Print URL and parameters without sending the request.
        :param dry_run: boolean
        :returns: Optimization result object.
        :rtype: Optimization
        """
        params = {"vehicles": []}

        if not all([isinstance(vehicle, Vehicle) for vehicle in vehicles]):
            raise TypeError("All vehicles must be of type Vehicle.")

        for vehicle in vehicles:
            vehicle_dict = {"id": vehicle.id}
            for attr in (
                "profile",
                "description",
                "start",
                "start_index",
                "end",
                "end_index",
                "capacity",
                "skills",
                "speed_factor",
                "max_tasks",
            ):
                if hasattr(vehicle, attr):
                    vehicle_dict[attr] = getattr(vehicle, attr)

            if hasattr(vehicle, "breaks"):
                vehicle_dict["breaks"] = [break_.__dict__ for break_ in vehicle.breaks]

            params["vehicles"].append(vehicle_dict)

        if jobs:
            params["jobs"] = [job.__dict__ for job in jobs]

        if shipments:
            params["shipments"] = []
            for shipment in shipments:
                shipment_dict = {}
                for method in ("pickup", "delivery"):
                    if hasattr(shipment, method):
                        shipment_dict[method] = getattr(shipment, method).__dict__
                for attr in ("amount", "skills", "priority"):
                    if hasattr(shipment, attr):
                        shipment_dict[attr] = getattr(shipment, attr)

                params["shipments"].append(shipment_dict)

        if geometry:
            params.update({"options": {"g": geometry}})

        if matrices:
            params["matrices"] = matrices

        return self._parse_optimization_json(
            self.client._request("", post_params=params, dry_run=dry_run)
        )

    @staticmethod
    def _parse_optimization_json(response):
        if response is None:
            return Optimization()

        code = response["code"]
        error = response.get("error")
        summary = Summary(**response["summary"])
        routes = [Route(**r) for r in response["routes"]]
        unassigned = (
            [Unassigned(**u) for u in response["unassigned"]] if response.get("unassigned") else []
        )
        return Optimization(code, error, summary, unassigned, routes)
