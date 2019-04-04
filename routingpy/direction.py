"""
:class:`.Direction` returns directions results.
"""


class Directions(object):
    """
    Contains a list of directions and the complete raw response. Access via properties ``directions`` and ``raw``.
    """

    def __init__(self, directions=None, raw=None):
        """
        Initialize a :class:`Directions` instance to hold multiple :class:`Direction` instances in a list-like fashion.

        :param directions: List of :class:`Direction` objects
        :type directions: list/tuple of :class:`Direction`

        :param raw: The whole raw directions response of the routing engine.
        :type raw: dict
        """
        self._directions = directions
        self._raw = raw

    @property
    def directions(self):
        """
        Holds the individual direction objects.

        :rtype: list of :class:`Direction` or None
        """
        return self._directions

    @property
    def raw(self):
        """
        Returns the directions raw, unparsed response. For details, consult the routing engine's API documentation.
        :rtype: dict or None
        """
        return self._raw

    def __repr__(self):
        return f'Isochrones({self._directions}, {self.raw})'

    def __str__(self):
        return str(self.raw)

    def __getitem__(self, item):
        return self._directions[item]

    def __iter__(self):
        return iter(self._directions)

    def __len__(self):
        return len(self._directions)


class Direction(object):
    """
    Contains a parsed directions response. Access via properties ``geometry`` and ``raw``.
    """

    def __init__(self, geometry=None, duration=None, distance=None, raw=None):
        """
        Initialize a :class:`Direction` object to hold the properties of a directions request.

        :param geometry: The geometry list in [[lon1, lat1], [lon2, lat2]] order.
        :type geometry: list of lists of float

        :param duration: The duration of the direction in seconds.
        :type duration: int or float

        :param distance: The distance of the direction in meters.
        :type distance: int

        :param raw: The raw response of an individual direction (for multiple alternative routes) or the whole direction
            response.
        :type raw: dict
        """
        self._geometry = geometry
        self._duration = int(duration)
        self._distance = int(distance)
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
