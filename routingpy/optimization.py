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
from typing import List, Optional

from routingpy.utils import _ReprMixin, _short_list_repr, decode_polyline5


class Job(_ReprMixin):
    def __init__(
        self,
        id: int,
        description: Optional[str] = None,
        location: Optional[List[float]] = None,
        location_index: Optional[int] = None,
        setup: Optional[int] = None,
        service: Optional[int] = None,
        delivery: Optional[List[int]] = None,
        pickup: Optional[List[int]] = None,
        skills: Optional[List[int]] = None,
        priority: int = None,
        time_windows: Optional[List[int]] = None,
    ):
        """
        :param id: The job id
        :param description: The job's description.
        :param location: A coordinates array in the format of [lon, lat]
        :param location_index: index of relevant row and column in custom matrices
        :param setup: job setup duration (in seconds; 0 if not specified)
        :param service: job service duration (in seconds; 0 if not specified)
        :param delivery: an array of integers describing multidimensional quantities for delivery
        :param pickup: an array of integers describing multidimensional quantities for pickup
        :param skills: an array of integers defining mandatory skills
        :param priority: an integer in the [0, 100] range describing priority level (0 if not specified)
        :param time_windows: an array of time_window objects in the format [start, end] describing valid slots for job service start
        """
        self.id = id

        if description is not None:
            self.description = description

        if location is not None:
            self.location = location

        if location_index is not None:
            self.location_index = location_index

        if setup is not None:
            self.setup = setup

        if service is not None:
            self.service = service

        if pickup is not None:
            self.pickup = pickup

        if delivery is not None:
            self.delivery = delivery

        if skills is not None:
            self.skills = skills

        if priority is not None:
            self.priority = priority

        if time_windows is not None:
            self.time_windows = time_windows


class ShipmentStep(_ReprMixin):
    def __init__(
        self,
        id,
        description=None,
        location=None,
        location_index=None,
        setup=None,
        service=None,
        time_windows=None,
    ):
        """
        :param id: The shipment step id
        :type id: int
        :param description: A string describing this step
        :type description: str
        :param location: A coordinates array in the format of [lon, lat]
        :type location: list of float
        :param location_index: Index of relevant row and column in custom matrices
        :type location_index: int
        :param setup: job setup duration (in seconds; 0 if not specified)
        :type setup: int
        :param service: task service duration (in seconds; 0 if not specified)
        :type service: int
        :param time_windows: an array of time_window objects in the format [start, end] describing valid slots for task service start
        :type time_windows: list of int
        """
        self.id = id

        if description is not None:
            self.description = description

        if location is not None:
            self.location = location

        if location_index is not None:
            self.location_index = location_index

        if setup is not None:
            self.setup = setup

        if service is not None:
            self.service = service

        if time_windows is not None:
            self.time_windows = time_windows


class Shipment(_ReprMixin):
    def __init__(
        self,
        pickup: Optional[ShipmentStep] = None,
        delivery: Optional[ShipmentStep] = None,
        amount: Optional[List[int]] = None,
        skills: Optional[List[int]] = None,
        priority: Optional[int] = None,
    ):
        """
        :param pickup: A :class:`ShipmentStep` object describing pickup
        :param delivery: A :class:`ShipmentStep` object describing delivery
        :param amount: An array of integers describing multidimensional quantities
        :param skills: An array of integers defining mandatory skills
        :param priority: An integer in the [0, 100] range describing priority level (0 if not specified)
        """

        if pickup is not None:
            self.pickup = pickup

        if delivery is not None:
            self.delivery = delivery

        if amount is not None:
            self.amount = amount

        if skills is not None:
            self.skills = skills

        if priority is not None:
            self.priority = priority


class Break(_ReprMixin):
    def __init__(self, id, time_windows, service=None, description=None):
        """
        :param id: The break id.
        :type id: int
        :param time_windows: An array of time_window objects in the format [start, end] describing valid slots for break start
        :type time_windows: list of int
        :param service: The break duration (in seconds; 0 if not specified)
        :type service: int
        :param description: The break's description
        :type description: str
        """
        self.id = id
        self.time_windows = time_windows

        if service is not None:
            self.service = service

        if description is not None:
            self.description = description


class Vehicle(_ReprMixin):
    def __init__(
        self,
        id: int,
        profile: Optional[str] = None,
        description: Optional[str] = None,
        start: Optional[List[float]] = None,
        start_index: Optional[int] = None,
        end: Optional[List[float]] = None,
        end_index: Optional[int] = None,
        capacity: Optional[List[int]] = None,
        skills: Optional[List[int]] = None,
        time_window: Optional[List[int]] = None,
        breaks: Optional[List[Break]] = None,
        speed_factor: Optional[float] = None,
        max_tasks: Optional[float] = None,
    ):
        """
        :param id: The vehicle id
        :param profile: Routing profile (defaults to car)
        :param description: A string describing this vehicle
        :param start: Coordinates array in the form [lon, lat]
        :param start_index: Index of relevant row and column in custom matrices
        :param end: Coordinates array in the form [lon, lat]
        :param end_index: Index of relevant row and column in custom matrices
        :param capacity: An array of integers describing multidimensional quantities
        :param skills: An array of integers defining skills
        :param time_window: An array of time_window objects in the format [start, end] describing working hours
        :param breaks: An array of :class:`routingpy.optimization.Break` objects
        :param speed_factor: A double value in the range (0, 5] used to scale all vehicle travel times (defaults to 1.), the respected precision is limited to two digits after the decimal point
        :param max_tasks: An integer defining the maximum number of tasks in a route for this vehicle
        """
        self.id = id

        if profile is not None:
            self.profile = profile

        if description is not None:
            self.description = description

        if start is not None:
            self.start = start

        if start_index is not None:
            self.start_index = start_index

        if end is not None:
            self.end = end

        if end_index is not None:
            self.end_index = end_index

        if capacity is not None:
            self.capacity = capacity

        if skills is not None:
            self.skills = skills

        if time_window is not None:
            self.time_window = time_window

        if breaks is not None:
            self.breaks = breaks

        if speed_factor is not None:
            self.speed_factor = speed_factor

        if max_tasks is not None:
            self.max_tasks = max_tasks


class Summary(_ReprMixin):
    def __init__(
        self,
        cost,
        unassigned,
        service,
        duration,
        waiting_time,
        priority,
        violations,
        computing_times,
        routes=None,
        setup=None,
        delivery=None,
        pickup=None,
        distance=None,
    ):
        """
        :param cost: Total cost for all routes
        :type cost: int
        :param unassigned: Number of tasks that could not be served
        :type unassigned: int
        :param service: Total service time for all routes (in seconds)
        :type service: int
        :param duration: Total travel time for all routes (in seconds)
        :type duration: int
        :param waiting_time: Total waiting time for all routes (in seconds)
        :type waiting_time: int
        :param priority: Total priority sum for all assigned tasks
        :type priority: int
        :param violations: Array of violation objects for all routes
        :type violations: list of dict
        :param computing_times: Dictionary of times necessary to compute optimization
        :type computing_times: dict
        :param routes: Number of routes in the solution
        :type routes: int
        :param setup: Total setup time for all routes (in seconds)
        :type setup: int
        :param delivery: Total delivery for all routes
        :type delivery: int
        :param pickup: Total pickup for all routes
        :type pickup: int
        :param distance: Total distance for all routes (in meters; returned if geometry was set to True)
        :type distance: float
        """
        self.cost = cost
        self.routes = routes
        self.unassigned = unassigned
        self.setup = setup
        self.service = service
        self.duration = duration
        self.waiting_time = waiting_time
        self.priority = priority
        self.violations = violations
        self.computing_times = computing_times

        if delivery is not None:
            self.delivery = delivery

        if pickup is not None:
            self.pickup = pickup

        if distance is not None:
            self.distance = distance


class Unassigned(_ReprMixin):
    def __init__(self, id, type, location=None):
        """
        :param id: id of the unassigned task
        :type id: int
        :param type: Type of the unassigned task
        :type type: str
        :param location: Array of coordinates (if provided)
        :type location: list of float
        """
        self.id = id
        self.type = type

        if location is not None:
            self.location = location


class Route:
    def __init__(
        self,
        vehicle,
        steps,
        cost,
        service,
        duration,
        waiting_time,
        priority,
        violations,
        setup=None,
        delivery=None,
        pickup=None,
        description=None,
        geometry=None,
        distance=None,
    ):
        """
        :param vehicle: id of the vehicle assigned to this route
        :type vehicle: int
        :param steps: array of :class:`routingpy.optimization.Step` objects
        :type steps: Step
        :param cost: Cost for this route
        :type cost: int
        :param service: Total service time for this route (in seconds)
        :type service: int
        :param duration: Total travel time for this route (in seconds)
        :type duration: int
        :param waiting_time: Total waiting time for this route (in seconds)
        :type waiting_time: int
        :param priority: Total priority sum for tasks in this route
        :type priority: int
        :param violations: Array of violation objects for this route
        :type violations: dict
        :param setup: Total setup time for this route (in seconds)
        :type setup: int
        :param delivery: Total delivery for tasks in this route (in seconds)
        :type delivery: int
        :param pickup: Total pickup for tasks in this route (in seconds)
        :type pickup: int
        :param description: Vehicle description, if provided in input
        :type description: str
        :param geometry: Decoded route geometry (only if geometry flag was set to True)
        :type geometry: list of tuple of float
        :param distance: Total route distance in meters (only if geometry flag was set to True)
        :type distance: float
        """
        self.vehicle = vehicle
        self.steps = [Step(**s) for s in steps]
        self.cost = cost
        self.service = service
        self.duration = duration
        self.waiting_time = waiting_time
        self.priority = priority
        self.violations = violations

        if setup is not None:
            self.setup = setup

        if delivery is not None:
            self.delivery = delivery

        if pickup is not None:
            self.pickup = pickup

        if description is not None:
            self.description = description

        if geometry is not None:
            self.geometry = decode_polyline5(geometry)

        if distance is not None:
            self.distance = distance

    def __repr__(self):
        return "{}({})".format(
            type(self).__name__,
            ", ".join(
                [
                    f"{k}: {v}"
                    if not k == "geometry" and v is not None
                    else f"{k}: {_short_list_repr(v)}"
                    for k, v in self.__dict__.items()
                ]
            ),
        )


class Optimization:
    def __init__(
        self,
        code: Optional[int] = None,
        error: Optional[str] = None,
        summary: Optional[Summary] = None,
        unassigned: Optional[List[Unassigned]] = None,
        routes: Optional[List[Route]] = None,
    ):
        """
        :param code: The response code. Possible values for the status code are: 0 – no error raised; 1 – internal error; 2 – input error; 3 - routing error
        :param error: Error message (present if code is different from 0)
        :param summary: Object summarizing solution indicators
        :param unassigned: Array of objects describing unassigned tasks with their id, type and location (if provided)
        :param routes: array of route objects
        """
        self.code = code
        self.error = error
        self.summary = summary
        self.unassigned = unassigned
        self.routes = routes

    def __repr__(self):
        return f"Optimization(code: {self.code}, error: {self.error}, cost: {self.summary.cost if self.summary else None})"


class Step(_ReprMixin):
    def __init__(
        self,
        type: str,
        arrival: int,
        duration: int,
        service: int,
        waiting_time: int,
        violations: List[dict],
        setup: Optional[int] = None,
        description: Optional[str] = None,
        location: Optional[List[float]] = None,
        id: Optional[int] = None,
        load: Optional[int] = None,
        distance: Optional[int] = None,
        job: Optional[int] = None,
    ):
        """
        :param type: A string (either start, job, pickup, delivery, break or end)
        :param arrival: Estimated time of arrival at this step
        :param duration: Cumulated travel time upon arrival at this step (in seconds)
        :param service: Service time at this step
        :param waiting_time: Waiting time upon arrival at this step
        :param violations: Array of violation objects for this step
        :param setup: Setup time at this step (in seconds)
        :param description: Step description, if provided in input
        :param location: Coordinates array for this step (if provided in input)
        :param id: id of the task performed at this step, only provided if type value is job, pickup, delivery or break
        :param load: Vehicle load after step completion (with capacity constraints)
        :param distance: Traveled distance upon arrival at this step (in meters)
        :param job: id of the job performed at this step, only provided if type value is job
        """
        self.type = type
        self.arrival = arrival
        self.duration = duration
        self.service = service
        self.waiting_time = waiting_time
        self.violations = violations

        if setup is not None:
            self.setup = setup

        if description is not None:
            self.description = description

        if location is not None:
            self.location = location

        if id is not None:
            self.id = id

        if load is not None:
            self.load = load

        if distance is not None:
            self.distance = distance

        if job is not None:
            self.job = job
