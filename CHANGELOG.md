# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## Unreleased
### Added
-
### Fixed
-
### Changed
-
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