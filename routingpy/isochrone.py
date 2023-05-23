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
"""
:class:`Isochrone` returns isochrones results.
"""
from typing import List, Optional, Tuple, Union


class Isochrones(object):
    """
    Contains a list of :class:`Isochrone`, which can be iterated over or accessed by index. The property ¸`raw`` contains
    the complete raw response of the isochrones request.
    """

    def __init__(self, isochrones=None, raw=None):
        self._isochrones = isochrones
        self._raw = raw

    @property
    def raw(self) -> Optional[dict]:
        """
        Returns the isochrones' raw, unparsed response. For details, consult the routing engine's API documentation.

        :rtype: dict or None
        """
        return self._raw

    def __repr__(self):  # pragma: no cover
        return "Isochrones({}, {})".format(self._isochrones, self.raw)

    def __getitem__(self, item):
        return self._isochrones[item]

    def __iter__(self):
        return iter(self._isochrones)

    def __len__(self):
        return len(self._isochrones)


class Isochrone(object):
    """
    Contains a parsed single isochrone response. Access via properties ``geometry``, ``interval``, ``center``, ``interval_type``.
    """

    def __init__(self, geometry=None, interval=None, center=None, interval_type=None):
        self._geometry = geometry
        self._interval = int(interval)
        self._center = center
        self._interval_type = interval_type

    @property
    def geometry(self) -> Optional[List[List[float]]]:
        """
        The geometry of the isochrone as [[lon1, lat1], [lon2, lat2], ...] list.

        :rtype: list or None
        """
        return self._geometry

    @property
    def center(self) -> Optional[Union[List[float], Tuple[float]]]:
        """
        The center coordinate in [lon, lat] of the isochrone. Might deviate from the input coordinate.
        Not available for all routing engines (e.g. GraphHopper, Mapbox OSRM or Valhalla).
        In this case, it will use the location from the user input.

        :rtype: list of float or None
        """
        return self._center

    @property
    def interval(self) -> int:
        """
        The interval of the isochrone in seconds or in meters.

        :return: int
        """
        return self._interval

    @property
    def interval_type(self) -> Optional[str]:
        """
        Was it based on 'distance' or 'time'?

        :return: str or None
        """
        return self._interval_type

    def __repr__(self):  # pragma: no cover
        return "Isochrone({}, {})".format(self.geometry, self.interval)
