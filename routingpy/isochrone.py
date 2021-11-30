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
:class:`Isochrone` returns directions results.
"""


class Isochrones(object):
    """
    Contains a list of :class:`Isochrone`, which can be iterated over or accessed by index. The property ¸`raw`` contains
    the complete raw response of the isochrones request. The isochrones are reverse ordered by ``interval``.
    """

    def __init__(self, isochrones=None, geom_type=None, raw=None):
        self._isochrones = sorted(isochrones, key=lambda i: i.interval, reverse=True)
        self._geom_type = geom_type
        self._raw = raw

    @property
    def raw(self):
        """
        Returns the isochrones's raw, unparsed response. For details, consult the routing engine's API documentation.

        :rtype: dict or None
        """
        return self._raw

    @property
    def geom_type(self) -> str:
        """
        Returns the isochrones' geometry type as OGC string.
        """
        return self._geom_type

    def __repr__(self):  # pragma: no cover
        return "Isochrones({}, {}, {})".format(self._isochrones, self._geom_type, self.raw)

    def __getitem__(self, item):
        return self._isochrones[item]

    def __iter__(self):
        return iter(self._isochrones)

    def __len__(self):
        return len(self._isochrones)


class Isochrone(object):
    """
    Contains a parsed single isochrone response. Access via properties ``geometry``, ``interval`` ``center``.
    """

    def __init__(self, geometry=None, interval=None, center=None):
        self._geometry = geometry
        self._interval = int(interval)
        self._center = center

    @property
    def geometry(self):
        """
        The geometry of the isochrone as [[lon1, lat1], [lon2, lat2], ...] list.

        :rtype: list or None
        """
        return self._geometry

    @property
    def center(self):
        """
        The center coordinate in [lon, lat] of the isochrone. Might deviate from the input coordinate.
        Not available for all routing engines (e.g. GraphHopper, Mapbox OSRM or Valhalla).
        In this case, it will use the location from the user input.

        :rtype: list of float
        """
        return self._center

    @property
    def interval(self):
        """
        The interval of the isochrone in seconds or in meters.

        :return: int
        """
        return self._interval

    def __repr__(self):  # pragma: no cover
        return "Isochrone({}, {})".format(self.geometry, self.interval)
