"""
Every routing service below has a separate module in ``routingpy.routers``, which hosts a class abstracting the service's
API. Each router has at least a ``directions`` method, many offer additionally ``matrix`` and/or ``isochrones`` methods.
Other available provider endpoints are allowed and generally encouraged. However, please refer
to our `contribution guidelines`_ for general instructions.

The requests are handled via a client class derived from `:class: routingpy.base.BaseClient`.

**routingpy**'s dogma is, that all routers expose the same mandatory arguments for common methods in an
attempt to be consistent for the same method across different routers. Unlike other collective libraries,
we additionally chose to preserve each router's special arguments, only abstracting the most basic arguments, such as
locations and profile (car, bike, pedestrian etc.), among others (full list here_).

.. _`contribution guidelines`: https://github.com/gis-ops/routing-py/blob/master/CONTRIBUTING.md
.. _here: https://github.com/gis-ops/routing-py#api
"""
from ..client_base import options  # noqa: F401
from ..exceptions import RouterNotFound

from .openrouteservice import ORS
from .osrm import OSRM
from .valhalla import Valhalla
from .graphhopper import Graphhopper
from .mapbox_valhalla import MapboxValhalla
from .mapbox_osrm import MapboxOSRM
from .google import Google
from .heremaps import HereMaps

# Provide synonyms
_SERVICE_TO_ROUTER = {
    "ors": ORS,
    "openrouteservice": ORS,
    "osrm": OSRM,
    "mapbox_osrm": MapboxOSRM,
    "mapbox-osrm": MapboxOSRM,
    "mapboxosrm": MapboxOSRM,
    "mapbox": MapboxOSRM,
    "valhalla": Valhalla,
    "mapbox_valhalla": MapboxValhalla,
    "mapbox-valhalla": MapboxValhalla,
    "mapboxvalhalla": MapboxValhalla,
    "graphhopper": Graphhopper,
    "google": Google,
    "here": HereMaps,
    "heremaps": HereMaps,
}


def get_router_by_name(router_name):
    """
    Given a router's name, try to return the router class.

    >>> from routingpy.routers import get_router_by_name
    >>> router = get_router_by_name("ors")(api_key='')
    >>> print(router)
    routingpy.routers.openrouteservice.ORS
    >>> route = router.directions(**params)

    If the string given is not recognized, a
    :class:`routingpy.exceptions.RouterNotFound` exception is raised and the available list of router names is printed.

    :param router_name: Name of the router as string.
    :type router_name: str

    :rtype: Union[:class:`routingpy.routers.google.Google`, :class:`routingpy.routers.graphhopper.Graphhopper`, :class:`routingpy.routers.heremaps.HereMaps`, :class:`routingpy.routers.mapbox_osrm.MapBoxOSRM`, :class:`routingpy.routers.mapbox_valhalla.MapBoxValhalla`, :class:`routingpy.routers.openrouteservice.ORS`, :class:`routingpy.routers.osrm.OSRM`, :class:`routingpy.routers.valhalla.Valhalla`]

    """
    try:
        return _SERVICE_TO_ROUTER[router_name.lower()]
    except KeyError:
        raise RouterNotFound(
            "Unknown router '{}'; options are: {}".format(router_name, _SERVICE_TO_ROUTER.keys())
        )
