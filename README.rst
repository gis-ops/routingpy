routing-py
==========

.. image:: https://travis-ci.com/gis-ops/routing-py.svg?branch=master
    :target: https://travis-ci.com/gis-ops/routing-py
    :alt: Build status

.. image:: https://coveralls.io/repos/github/gis-ops/routing-py/badge.svg?branch=master
    :target: https://coveralls.io/github/gis-ops/routing-py?branch=master
    :alt: Coveralls coverage

.. image:: https://readthedocs.org/projects/routing-py/badge/?version=latest
   :target: http://routing-py.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://badge.fury.io/py/routing-py.svg
    :target: https://badge.fury.io/py/routing-py
    :alt: PyPI version

.. image:: https://anaconda.org/gis-ops/routing-py/badges/installer/conda.svg
    :target: https://conda.anaconda.org/gis-ops/routing-py
    :alt: Conda install

|
*One to unite them all* - routing-py is a Python 3 client for several
popular routing webservices.

Inspired by `geopy <https://github.com/geopy/geopy>`_. this library makes it extremely easy for Python developers to request
directions, isochrones or time-distance matrices using third-party
spatial webservices.

routing-py currently includes support for the following services:

-  `Mapbox, either Valhalla or OSRM`_
-  `Openrouteservice`_
-  `Here Maps`_
-  `Google Maps`_
-  `Graphhopper`_
-  `Local Valhalla`_
-  `Local Mapbox`_

The up-to-date list is available on the `routing-py doc section`_.
Router classes are located in `routing-py.routers`_.

routing-py is tested against versions 3.6, 3.7.

© routing-py contributors 2019 under the `Apache 2.0 License`_.


Why routing-py?
---------------

You want to get from A to B by car, compute a region of reachability or you require a time distance matrix for a n times m table and don't know which provider to use?
Stop here. 
As you probably have already guessed, every provider works on different spatial global datasets and uses a plethora of algorithms on top. 
While Google or HERE build on top of proprietary datasets, providers such as Mapbox or Graphhopper consume OpenStreetMap data for their base network.
Ultimately this means that results may differ - and our experience tells us: they do.
This calls for a careful evaluation which service provider to use for which specific use case.
With routing-py we have made an approach to simplify this process for you.


Installation
------------

Install using `pip`_ with:

::

  pip install routing-py

Or, `download a wheel or source archive from PyPI`_.


Examples
--------

Every API has its own specifications and features, however the basic blueprints are the same across all. 
To this end, we have decided to keep the basics the of usage the same for all.
Follow our examples to understand how simple routing-py is to use.


Directions - Graphhopper vs. Google Maps
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    >>> from routingpy import Graphhopper
    >>> api = Graphhopper(api_key='INSERT_YOUR_KEY_HERE')
    >>> routes = api.directions( 
      coordinates=[[8.688641, 49.420577], [8.680916, 49.415776],[8.780916, 49.445776]],
      elevation=True,
      profile='car',
      dry_run=False)
    >>> print(routes.geometry)
    [[8.68091, 49.41574], [8.68144, 49.41575], ...
    >>> print(routes.duration)
    2349
    >>> print(routes.distance)
    15239

.. code:: python

    >>> from routingpy import Google
    >>> api = Google(api_key='INSERT_YOUR_KEY_HERE')
    >>> routes = api.directions(
      coordinates=[[8.688641, 49.420577], [8.680916, 49.415776],[8.780916, 49.445776]],
      profile='car',
      dry_run=False)
    >>> print(routes)
      Direction([[8.68868, 49.4204], [8.68812, 49.42035], ...], 1865, 12323)
    >>> print(routes.geometry)
    [[8.68868, 49.4204], [8.68812, 49.42035], ...
    >>> print(routes.duration)
    1865
    >>> print(routes.distance)
    12323

Isochrones - HERE Maps vs. openrouteservice
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    >>> from routingpy import HereMaps
    >>> api = HereMaps(app_id='INSERT_APP_ID_HERE', app_code='INSERT_APP_CODE_HERE')
    >>> isochrones = here_api.isochrones(
      coordinates=[8.34234, 48.23424],
      intervals=[3000],
      interval_type='distance',
      profile='car;fastest',
      dry_run=False)
    >>> print(isochrones[0].geometry)
    [[8.3724403, 48.2271481], [8.3729553, 48.2272339], [8.3777618, 48.2272339]...
    >>> print(isochrones[0].center)
    [8.3658099, 48.2353663]
    >>> print(isochrones[0].range)
    3000

.. code:: python

    >>> from routingpy import ORS
    >>> api = ORS(api_key='INSERT_YOUR_KEY_HERE')
    >>> isochrones = here_api.isochrones(
      coordinates=[8.34234, 48.23424],
      intervals=[3000],
      interval_type='distance',
      profile='driving-car',
      dry_run=False)
    >>> print(isochrones[0].geometry)
    [[8.313951, 48.226963], [8.318491, 48.223141], [8.320768, 48.218221]...
    >>> print(isochrones[0].center)
    [8.344267867749956, 48.233825673919]
    >>> print(isochrones[0].range)
    3000



Matrix - Mapbox-OSRM vs Google Maps
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

XY


Documentation links
-------------------

.. _Mapbox, either Valhalla or OSRM: https://docs.mapbox.com/api/navigation
.. _Openrouteservice: https://openrouteservice.org/dev/#/api-docs
.. _Here Maps: https://developer.here.com/documentation
.. _Google Maps: https://developers.google.com/maps/documentation
.. _Graphhopper: https://graphhopper.com/api/1/docs
.. _Local Valhalla: https://github.com/valhalla/valhalla-docs
.. _Local Mapbox: https://github.com/Project-OSRM/osrm-backend/wiki
.. _routing-py doc section: https://routing-py.readthedocs.io/en/latest/#routers
.. _routing-py.routers: https://github.com/gis-ops/routing-py/tree/master/routing-py/routers
.. _Apache 2.0 License: https://github.com/gis-ops/routing-py/blob/master/LICENSE
.. _pip: http://www.pip-installer.org/en/latest/
.. _download a wheel or source archive from PyPI: https://pypi.python.org/pypi/routing-py
