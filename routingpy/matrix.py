"""
:class:`.Matrix` returns directions results.
"""


class Matrix(object):
    """
    Contains a parsed matrix response. Access via properties ``geometry`` and ``raw``.
    """

    def __init__(self, durations=None, distances=None, raw=None):
        self._durations = durations
        self._distances = distances
        self._raw = raw

    @property
    def durations(self):
        """
        The durations matrix as list akin to::

            [
                [
                    duration(origin1-destination1,
                    duration(origin1-destination2,
                    duration[origin1-destination3,
                    ...
                ],
                [
                    duration(origin2-destination1,
                    duration(origin2-destination2,
                    duration[origin3-destination3,
                    ...
                },
                ...
            ]

        :rtype: list or None
        """
        return self._durations

    @property
    def distances(self):
        """
        The distance matrix as list akin to::

            [
                [
                    duration(origin1-destination1,
                    duration(origin1-destination2,
                    duration[origin1-destination3,
                    ...
                ],
                [
                    duration(origin2-destination1,
                    duration(origin2-destination2,
                    duration[origin3-destination3,
                    ...
                },
                ...
            ]

        :rtype: list or None
        """
        return self._distances

    @property
    def raw(self):
        """
        Returns the route's raw, unparsed response. For details, consult the routing engine's API documentation.
        :rtype: dict or None
        """
        return self._raw

    def __repr__(self):
        return f'Matrix({self.durations}, {self.distances})'

    def __str__(self):
        return f'Matrix(Durations: {self.durations}, Distances: {self.distances})'
