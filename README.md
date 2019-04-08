# routing-py

[![Latest
Version](https://img.shields.io/pypi/v/routing-py.svg?style=flat-square)](https://pypi.python.org/pypi/routing-py/)

[![Build
Status](https://img.shields.io/travis/routing-py/routing-py.svg?style=flat-square)](https://travis-ci.org/gis-ops/routing-py)

[![License](https://img.shields.io/github/license/routing-py/routing-py.svg?style=flat-square)](https://pypi.python.org/pypi/routing-py/)

*One to unite them all* - routing-py is a Python 3 client for several popular routing webservices.

This library makes it extremely easy for Python developers to request directions, isochrones or time-distance matrices using third-party spatial webservices.

routing-py currently includes support for the following services:

- [Mapbox, either Valhalla or OSRM](https://docs.mapbox.com/api/navigation)
- [Openrouteservice](https://openrouteservice.org/dev/#/api-docs)
- [Here Maps](https://developer.here.com/documentation)
- [Google Maps](https://developers.google.com/maps/documentation)
- [Graphhopper](https://graphhopper.com/api/1/docs)
- [Local Valhalla](https://github.com/valhalla/valhalla-docs)
- [Local Mapbox](https://github.com/Project-OSRM/osrm-backend/wiki)

The up-to-date list is available on the [routing-py doc section](https://routing-py.readthedocs.io/en/latest/#routers). 
Router classes are located in [routing-py.routers](https://github.com/gis-ops/routing-py/tree/master/routing-py/routers).

routing-py is tested against versions 3.6, 3.7. 

© routing-py contributors 2018 under the [Apache 2.0 License](https://github.com/gis-ops/routing-py/blob/master/LICENSE).

## Installation

Install using [pip](http://www.pip-installer.org/en/latest/) with:

    pip install routing-py

Or, [download a wheel or source archive from PyPI](https://pypi.python.org/pypi/routing-py).

## Generic Response Objects

...

## Directions using openrouteservice vs. Google Maps

To geolocate a query to an address and coordinates:

``` python
>>> from geopy.geocoders import Nominatim
>>> geolocator = Nominatim(user_agent="specify_your_app_name_here")
>>> location = geolocator.geocode("175 5th Avenue NYC")
>>> print(location.address)
Flatiron Building, 175, 5th Avenue, Flatiron, New York, NYC, New York, ...
>>> print((location.latitude, location.longitude))
(40.7410861, -73.9896297241625)
>>> print(location.raw)
{'place_id': '9167009604', 'type': 'attraction', ...}
```

## Isochrones using Mapbox-Valhalla vs. HERE Maps

To geolocate a query to an address and coordinates:

``` python
>>> from geopy.geocoders import Nominatim
>>> geolocator = Nominatim(user_agent="specify_your_app_name_here")
>>> location = geolocator.reverse("52.509669, 13.376294")
>>> print(location.address)
Potsdamer Platz, Mitte, Berlin, 10117, Deutschland, European Union
>>> print((location.latitude, location.longitude))
(52.5094982, 13.3765983)
>>> print(location.raw)
{'place_id': '654513', 'osm_type': 'node', ...}
```

## Matrix using Mapbox-OSRM vs Google Maps

To find the address corresponding to a set of coordinates:

``` python
>>> from geopy.geocoders import Nominatim
>>> geolocator = Nominatim(user_agent="specify_your_app_name_here")
>>> location = geolocator.reverse("52.509669, 13.376294")
>>> print(location.address)
Potsdamer Platz, Mitte, Berlin, 10117, Deutschland, European Union
>>> print((location.latitude, location.longitude))
(52.5094982, 13.3765983)
>>> print(location.raw)
{'place_id': '654513', 'osm_type': 'node', ...}
```

## Contributions

...
