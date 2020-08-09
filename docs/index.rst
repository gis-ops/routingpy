Welcome to routingpy's documentation!
=====================================

:Documentation: https://routingpy.readthedocs.io/
:Source Code: https://github.com/gis-ops/routing-py
:Issue Tracker: https://github.com/gis-ops/routing-py/issues
:Stack Overflow: https://stackoverflow.com/questions/tagged/routingpy
:PyPI: https://pypi.org/project/routingpy
:Conda: https://conda.org/gis-ops/routingpy
:MyBinder Interactive Examples: https://mybinder.org/v2/gh/gis-ops/routing-py/master?filepath=examples

.. automodule:: routingpy
   :members: __doc__

.. toctree::
    :maxdepth: 4
    :caption: Contents

    index


Installation
~~~~~~~~~~~~

::

    pip install routingpy
    # or
    conda install routingpy

Routers
~~~~~~~~~

.. automodule:: routingpy.routers
   :members: __doc__

.. autofunction:: routingpy.routers.get_router_by_name

Default Options Object
----------------------

.. autoclass:: routingpy.routers.options
   :members:
   :undoc-members:

Google
------

.. autoclass:: routingpy.routers.Google
   :members:

   .. automethod:: __init__

Graphhopper
-----------

.. autoclass:: routingpy.routers.Graphhopper
   :members:

   .. automethod:: __init__

HereMaps
--------

.. autoclass:: routingpy.routers.HereMaps
   :members:

   .. automethod:: __init__

MapboxOSRM
----------

.. autoclass:: routingpy.routers.MapboxOSRM
   :members:

   .. automethod:: __init__

MapboxValhalla
--------------

.. autoclass:: routingpy.routers.MapboxValhalla
   :members:
   :inherited-members:
   :show-inheritance:

   .. automethod:: __init__

ORS
---

.. autoclass:: routingpy.routers.ORS
   :members:

   .. automethod:: __init__

OSRM
----

.. autoclass:: routingpy.routers.OSRM
   :members:

   .. automethod:: __init__

Valhalla
--------

.. autoclass:: routingpy.routers.Valhalla
   :members:

   .. automethod:: __init__

Data
~~~~

.. autoclass:: routingpy.direction.Directions
    :members: raw

.. autoclass:: routingpy.direction.Direction
    :members: geometry, duration, distance

.. autoclass:: routingpy.isochrone.Isochrones
    :members: raw

.. autoclass:: routingpy.isochrone.Isochrone
    :members: geometry, center, range

.. autoclass:: routingpy.matrix.Matrix
    :members: durations, distances, raw

.. autofunction:: routingpy.utils.decode_polyline5

.. autofunction:: routingpy.utils.decode_polyline6

Exceptions
~~~~~~~~~~

.. autoclass:: routingpy.exceptions.RouterError
    :show-inheritance:

.. autoclass:: routingpy.exceptions.RouterApiError
    :show-inheritance:

.. autoclass:: routingpy.exceptions.RouterServerError
    :show-inheritance:

.. autoclass:: routingpy.exceptions.RouterNotFound
    :show-inheritance:

.. autoclass:: routingpy.exceptions.Timeout
    :show-inheritance:

.. autoclass:: routingpy.exceptions.RetriableRequest
    :show-inheritance:

.. autoclass:: routingpy.exceptions.OverQueryLimit
    :show-inheritance:

Changelog
~~~~~~~~~

See our `Changelog.md`_.

.. _Changelog.md: https://github.com/gis-ops/routingpy/CHANGELOG.md

Indices and search
==================

* :ref:`genindex`
* :ref:`search`

