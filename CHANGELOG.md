# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

**Unreleased** is available in Github's `master` branch, but not on PyPI.

## **Unreleased**

## [v1.3.0](https://pypi.org/project/routingpy/1.3.0/)

### Added
- Valhalla `/expansion` examples in the Jupyter Notebook
- OpenTripPlanner v2 support for routing & isochrones

### Fixed
- Google router's `duration` and `distance` attributes not being calculated correctly in single route response ([#107](https://github.com/gis-ops/routingpy/issues/107))
- pointer issue when requesting multiple times with the same connection

### Removed
- `MapboxValhalla` provider, since Mapbox doesn't expose a public Valhalla endpoint anymore

## [v1.2.1](https://pypi.org/project/routingpy/1.2.1/)
### Fixed
- Graphhopper 7.0 deprecated the "vehicle" parameter for the new "profile" parammeter


## [v1.2.0](https://pypi.org/project/routingpy/1.2.0/)
### Fixed
- Unit conversion did not work properly in ors' directions method
- Docstring for `intersections` parameter in ors' isochrones method was missing
- `profile` parameter was unnecessarily passed to POST params in ors' isochrones and matrix methods
- switched Graphhopper to POST endpoints & fixed any outdated parameters

## [v1.1.0](https://pypi.org/project/routingpy/1.1.0/)

### Added
- Added Valhalla's trace_attributes endpoint

## [v1.0.4](https://pypi.org/project/routingpy/1.0.4/)

### Fixed
- Passing a Valhalla.Waypoint to isochrones resulted in an unhandled exception

## [v1.0.3](https://pypi.org/project/routingpy/1.0.3/)

### Fixed
- OSRM does have a weird URL concept for profiles, so revert [#64](https://github.com/gis-ops/routing-py/issues/64))

### Added
- `interval_type` to `Isochrone` and `Expansions` objects

## [v1.0.2](https://pypi.org/project/routingpy/1.0.2/)

### Fixed
- Valhalla's 'matrix' endpoint couldn't deal with NULL entries

## [v1.0.0](https://pypi.org/project/routingpy/1.0.0/)

### Changed
- made all `parse_*` functions public so they can be used by super projects

### Fixed
- OSRM wasn't requesting the right endpoints: profile is meaningless
- GraphHopper parsing fails with not encoded points ([#54](https://github.com/gis-ops/routing-py/issues/54))
- Allow "narrative" argument for Valhalla's directions endpoint

## [0.4.0](https://pypi.org/project/routingpy/0.4.0/)

### Added
- support for Valhalla's `/expansion` endpoint
- support for HereMaps kwargs arguments

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


## [0.3.3](https://github.com/gis-ops/routing-py/releases/tag/0.3.3)
### Added
- 2020/2021 Valhalla HTTP API improvements
### Fixed
- README local OSRM description

## [0.3.2](https://github.com/gis-ops/routing-py/releases/tag/0.3.2)
### Fixed
- HERE isochrones had lat, lon instead of lon, lat ([#14](https://github.com/gis-ops/routing-py/issues/14))

## [0.3.1](https://github.com/gis-ops/routing-py/releases/tag/0.3.2)
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
