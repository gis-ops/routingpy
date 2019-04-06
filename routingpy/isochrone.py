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
:class:`Isochrone` returns directions results.
"""


class Isochrones(object):
    """
    Contains a list of :class:`Isochrone`, which can be iterated over or accessed by index. The property
     ``raw`` contains the complete raw response of the isochrone request.
    """

    def __init__(self, isochrones=None, raw=None):
        self._isochrones = isochrones
        self._raw = raw

    @property
    def isochrones(self):
        """
        Holds the individual isochrone objects

        :rtype: list or None
        """
        return self._isochrones

    @property
    def raw(self):
        """
        Returns the route's raw, unparsed response. For details, consult the routing engine's API documentation.
        :rtype: dict or None
        """
        return self._raw

    def __repr__(self):
        return f'Isochrones({self.isochrones}, {self.raw})'

    def __str__(self):
        return str(self.raw)

    def __getitem__(self, item):
        return self._isochrones[item]

    def __iter__(self):
        return iter(self._isochrones)

    def __len__(self):
        return len(self._isochrones)


class Isochrone(object):
    """
    Contains a parsed single isochrone response. Access via properties ``geometry``, ``center`` and``range``.
    """

    def __init__(self, geometry=None, range=None, center=None):
        self._geometry = geometry
        self._range = range
        self._center = center

    @property
    def range(self):
        """
        The range of the isochrone. The unit is in meters or seconds.

        :rtype: int
        """
        return self._range

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
        Not available for all routing engines (e.g. GraphHopper).

        :rtype: list of float
        """
        return self._center

    def __repr__(self):
        return f'Isochrone({self.geometry}, {self.range})'

    def __str__(self):
        return str(self.raw)
