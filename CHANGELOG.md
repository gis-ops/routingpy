# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

**Unreleased** is available in Github's `master` branch, but not on PyPI.

## Unreleased
### Added
- GeoJSON support for Graphhopper's isochrones
- [MyBinder](https://mybinder.org/v2/gh/gis-ops/routing-py/master?filepath=examples) notebook collection
### Fixed
- Add departure and arrival parameter for HERE isochrones API
- OSRM Mapbox isochrone ranges were using floats (#2)
- Graphhopper isochrones used wrong vehicle parameter
### Changed
- Profile parameter for HERE behaves now like other routers
- ORS alternative_routes parameter (#4)
- Brought Graphhopper support to its v1.x release
### Deprecated
-

## [0.2] 2019-04-30
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

## [0.1 - First Release] 2019-04-14