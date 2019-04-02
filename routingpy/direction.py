"""
:class:`.Direction` returns directions results.
"""


class Direction(object):
    """
    Contains a parsed directions response. Access via properties ``geometry`` and ``raw``.
    """

    def __init__(self, geometry=None, duration=None, distance=None, raw=None):
        self._geometry = geometry
        self._duration = duration
        self._distance = distance
        self._raw = raw

    @property
    def geometry(self):
        """
        The geometry of the route as [[lon1, lat1], [lon2, lat2], ...] list.

        :rtype: list or None
        """
        return self._geometry

    @property
    def duration(self):
        """
        The duration of the entire trip in seconds.

        :rtype: int
        """
        return self._duration

    @property
    def distance(self):
        """
        The distance of the entire trip in meters.

        :rtype: int
        """
        return self._distance

    @property
    def raw(self):
        """
        Returns the route's raw, unparsed response. For details, consult the routing engine's API documentation.

        :rtype: dict or None
        """
        return self._raw

    def __repr__(self):
        return f'Direction({self.geometry}, {self.duration}, {self.distance}'

    def __str__(self):
        return str(self.raw)
