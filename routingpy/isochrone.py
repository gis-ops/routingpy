"""
:class:`.Isochrone` returns directions results.
"""


class Isochrone(object):
    """
    Contains a parsed isochrone response. Access via properties ``geometry`` and ``raw``.
    """

    def __init__(self, geometry=None, range=None, raw=None):
        self._geometry = geometry
        self._range = range
        self._raw = raw

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
    def raw(self):
        """
        Returns the route's raw, unparsed response. For details, consult the routing engine's API documentation.
        :rtype: dict or None
        """
        return self._raw

    def __repr__(self):
        return f'Isochrone({self.geometry}, {self.range})'

    def __str__(self):
        return f'Isochrone(Geometry: {len(self.geometry)} coordinates, Range: {self.range})'
