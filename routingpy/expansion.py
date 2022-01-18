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
:class:`Expansion` returns expansion results.
"""


class Edge:
    """
    Contains a parsed single line string and its attributes, if specified in the request.
    Access via properties ``geometry``, ``distances`` ``durations``, ``costs``, ``edge_ids``, ``statuses``.
    """

    def __init__(
        self, geometry=None, distances=None, durations=None, costs=None, edge_ids=None, statuses=None
    ):
        self._geometry = geometry
        self._distance = distances
        self._duration = durations
        self._cost = costs
        self._edge_id = edge_ids
        self._status = statuses

    @property
    def geometry(self):
        """
        The geometry of the edge as [[lon1, lat1], [lon2, lat2]] list.

        :rtype: list or None
        """
        return self._geometry

    @property
    def distance(self):
        """
        The accumulated distance in meters for the edge in order of graph traversal.

        :rtype: int or None
        """
        return self._distance

    @property
    def duration(self):
        """
        The accumulated duration in seconds for the edge in order of graph traversal.

        :rtype: int or None
        """
        return self._duration

    @property
    def cost(self):
        """
        The accumulated cost for the edge in order of graph traversal.

        :rtype: int or None
        """
        return self._cost

    @property
    def edge_id(self):
        """
        The internal edge IDs for each edge in order of graph traversal.

        :rtype: int or None
        """
        return self._edge_id

    @property
    def status(self):
        """
        The edge states for each edge in order of graph traversal.
        Can be one of "r" (reached), "s" (settled), "c" (connected).

        :rtype: str or None
        """
        return self._status

    def __repr__(self):  # pragma: no cover
        return "Edge({})".format(", ".join([f"{k[1:]}: {v}" for k, v in vars(self).items() if v]))


class Expansions:
    """
    Contains a list of :class:`Expansion`, which can be iterated over or accessed by index. The property ¸`raw`` contains
    the complete raw response of the expansion request.
    """

    def __init__(self, expansions=None, center=None, raw=None):
        self._expansions = expansions
        self._center = center
        self._raw = raw

    @property
    def raw(self):
        """
        Returns the expansion's raw, unparsed response. For details, consult the documentation
         at https://valhalla.readthedocs.io/en/latest/api/expansion/api-reference/.

        :rtype: dict or None
        """
        return self._raw

    @property
    def center(self):
        """
        The center coordinate in [lon, lat] of the expansion, which is the location from the user input.

        :rtype: list of float
        """
        return self._center

    def __repr__(self):  # pragma: no cover
        if len(self._expansions) < 10:
            return "Expansions({}, {})".format(self._expansions, self.raw)
        else:
            return "Expansions({}, ..., {})".format(
                ", ".join([str(e) for e in self._expansions[:3]]),
                ", ".join(str(e) for e in self._expansions[-3:]),
            )

    def __getitem__(self, item):
        return self._expansions[item]

    def __iter__(self):
        return iter(self._expansions)

    def __len__(self):
        return len(self._expansions)
