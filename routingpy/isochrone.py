"""
:class:`.Isochrone` returns directions results.
"""


class Isochrones(object):
    """
    Contains a list of isochrones and the complete raw response. Access via properties ``isochrones`` and ``raw``.
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

    #TODO: add list-like magic methods, so 'for iso in isochrones' is possible (NOT 'for iso in isochrones.isochrones'!)


class Isochrone(object):
    """
    Contains a parsed single isochrone response. Access via properties ``geometry`` and ``range``.
    """

    def __init__(self, geometry=None, range=None):
        self._geometry = geometry
        self._range = range

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

    def __repr__(self):
        return f'Isochrone({self.geometry}, {self.range})'

    def __str__(self):
        return str(self.geometry)
