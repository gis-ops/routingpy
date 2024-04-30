# Contribution Guidelines

Thanks for considering to make a contribution to the vast landscape of routing engine APIs. We'd be really happy to
eventually be able to cover all remote open source routing API's, but have to rely on community contributions as this is a big task.

> Note: when this project first came about, the goal was to support commercial and open source APIs. This has since changed and we only focus on the open source ones these days, eventually phasing out the commercial ones as they grow stale.

## Table of Contents

<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:0 orderedList:0 -->

- [Issues](#issues)
- [Submitting fixes](#submitting-fixes)
  - [Setup](#setup)
  - [Tests](#tests)
  - [Documentation](#documentation)
- [Adding router](#adding-router)

<!-- /TOC -->

## Issues

- Please only submit actual technical issues and use [Stack Overflow](stackoverflow.com/) for questions using the tag `routingpy`.

- Please make sure you don't submit a duplicate by browsing open and closed issues first and consult the [CHANGELOG](https://github.com/gis-ops/routingpy/blob/master/CHANGELOG.md) for already fixed issues

## Pull requests

> **Important note**: please open an issue before starting to work on a fix or feature. This helps you save time and frustration. :-)

We welcome patches and fixes to existing clients and want to make sure everything goes smoothly for you while submitting a PR.

We use the PSF's [`black`](https://github.com/psf/black) to make sure the code style is consistent, and `flake8` as a linter.

When contributing, we expect you to:

- close an existing issue. If there is none yet for your fix, please [create one](https://github.com/gis-ops/routingpy/issues/new).
- write/adapt unit tests and/or mock API tests, depending on the introduced or fixed functionality
- limit the number of commits to a minimum, i.e. responsible use of [`git commit --amend [--no-edit]`](https://www.atlassian.com/git/tutorials/rewriting-history#git-commit--amend)
- use meaningful commit messages, e.g. `commit -m "[bugfix] heremaps used [lat, long] as locations input parameter"`
- you can branch off `master` and put a PR against `master` as well

### Setup

1. Create and activate a new virtual environment (optional, but recommended):

```bash
# From the root of your git project
python -m venv .venv
source .venv/bin/activate
```

2. Install development dependencies:

```bash
# From the root of your git project
pip install -r requirements_dev.txt
# or
poetry install
```

3. Run tests to check if all goes well:

```bash
# From the root of your git project
pytest -v
```

4. Please install the pre-commit hook, so your code gets auto-formatted and linted before committing it:

```bash
# From the root of your git project
pre-commit install
```

### Tests

We only do mocked tests as routing results heavily depend on underlying data, which, at least in the case of the FOSS routing
engines, changes on a very regular basis due to OpenStreetMap updates. All queries and most mocked responses are located in
`test/test_helper.py` in `dict`s. This unfortunately also means, that our tests are less API tests and more unit tests and can't catch
updates on providers' API changes.

```bash
# From the root of your git project
coverage run --source=routingpy --module pytest
```

### Documentation

If you add or remove new functionality which is exposed to the user/developer, please make sure to document these in the
docstrings. To build the documentation:

```bash
# From the root of your git project
cd docs
make hmtl
```

The documentation will have been added to `routingpy/docs/build/html` and you can open `index.html` in your web browser to view
the changes.

We realize that _re-structured text_ is not the most user-friendly format, but it is the currently best available
documentation format for Python projects. You'll find lots of copy/paste material in the existing implementations.

## Adding router

Let's add all the open source routers in the world:)

It's really easy:

1. **New class** Create a new router module in `routingpy/routers` and base the new class on `routingpy/routers/base.py:Router`.
   Also, check if the service hasn't been added before. E.g. if the router
   you want to add is based on `GraphHopper`, you probably want to subclass `routingpy/routers/graphhopper.py:Graphhopper` class.
   Additionally, import the new router class in `routingpy/routers/init.py`.

2. **Implementations** Implement the services the routing engine has to offer. The bare minimum is implementing the `directions` method.
   If the routing engine also offers `isochrones` and `matrix`, we'd require you to add those too. If you want to add an
   endpoint that doesn't exist yet in `routingpy/routers/base.py:Router`, please [consult us first](mailto:enquiry@gis-ops.com?subject=contributing%20to%20routingpy), as we need to make sure
   to be similarly consistent across different routing engines as we are with the existing endpoints.

3. **Tests** Create a new test module testing the functionality, **not** the API.
   Use `@responses.activate` decorators for this.
   To run the new tests and ensure consistency, refer to the [Tests](#tests) section above. **Don't store secrets** in the tests.

4. **Document** Please use docstring documentation for all user-exposed functionality, similar to other router implementations.
   Also, please register the new module in `docs/indes.rst`'s `Routers` section. To build the docs, refer to the
   [documentation section](#documentation) for details. Don't forget to add your name to the list of `AUTHORS.md`.
