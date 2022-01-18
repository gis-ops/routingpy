# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

**Unreleased** is available in Github's `master` branch, but not on PyPI.

## **Unreleased**
### Added
- support for Valhalla's `/expansion` endpoint
### Fixed
- enhanced error handling for directions with Google [#15](https://github.com/gis-ops/routing-py/issues/15)
- fixed MapboxOSRM client, removing unused parameters and unifying Isochrones interface [#21](https://github.com/gis-ops/routing-py/issues/21)
- fixed bug that caused HereMaps client to use wrong API endpoints [#28](https://github.com/gis-ops/routing-py/pull/28)
- fixed bug that caused HereMaps Isochrones to return lists of `list_reverseiterator`s instead of coordinates [#29](https://github.com/gis-ops/routing-py/issues/29)
- updated jupyter notebooks examples
- switched coordinate order of OSRM
- if no get_params are defined, omit "?" from the request URL

### Changed

- BREAKING: pulled client stuff into a separate Client class which gets passed to the individual router instances with the default being the same as before [#24](https://github.com/gis-ops/routing-py/pull/24)

### Deprecated
-

## [0.3.3](https://github.com/gis-ops/routing-py/releases/tag/0.3.3)
### Added
- 2020/2021 Valhalla HTTP API improvements
### Fixed
- README local OSRM description
### Changed
- 
### Deprecated
-

## [0.3.2](https://github.com/gis-ops/routing-py/releases/tag/0.3.2)
### Fixed
- HERE isochrones had lat, lon instead of lon, lat ([#14](https://github.com/gis-ops/routing-py/issues/14))

## [0.3.1](https://github.com/gis-ops/routing-py/releases/tag/0.3.2)
### Added
- 
### Fixed
- HERE routers can now also be used with api key
- HERE isochrones had lat, lon instead of lon, lat ([#14](https://github.com/gis-ops/routing-py/issues/14))
- Set Google router's profile queryparam correctly (was set to "profile" now is "mode")

## [0.3.0](https://github.com/gis-ops/routing-py/releases/tag/0.3.0) 2020-08-09
### Added
- GeoJSON support for Graphhopper's isochrones
- [MyBinder](https://mybinder.org/v2/gh/gis-ops/routing-py/master?filepath=examples) notebook collection
### Fixed
- Add departure and arrival parameter for HERE isochrones API
- OSRM Mapbox isochrone ranges were using floats (#2)
- OSRM matrix ouputs distances array now (#6)
- Graphhopper isochrones used wrong vehicle parameter
### Changed
- Profile parameter for HERE behaves now like other routers
- ORS alternative_routes parameter (#4)
- Brought Graphhopper support to its v1.x release
- Minimum Python version > 3.6.1 (for Pandas 1.x)
### Deprecated
-

## [0.2](https://github.com/gis-ops/routing-py/releases/tag/v0.2) 2019-04-30
### Added
- Example notebook to compare providers
### Fixed
- Here matrix did not allow `sources` and `destinations` to be optional
- Base class used sorted(params) which messed up the order of parameters for Graphhopper endpoints
- MapboxOSRM directions was parsing geometry to \[lat, lon\]
- README not valid on PyPI, wasn't rendered
- add to PyPI and Conda
### Changed
-
### Deprecated
-

## [0.1 - First Release](https://github.com/gis-ops/routing-py/releases/tag/v0.1) 2019-04-14