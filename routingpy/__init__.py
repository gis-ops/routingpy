# -*- coding: utf-8 -*-
# Copyright (C) 2021 GIS OPS UG
#
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#
"""
**routingpy** is a Python 3 client for a lot of popular web routing services.

Using **routingpy** you can easily request **directions**, **isochrones** and
**matrices** from many reliable online providers in a consistent fashion. Base parameters
are the same for all services, while still preserving each service's special parameters (for
more info, please look at our `README`_.
Take a look at our `Examples`_ to see how simple you can compare routes from different providers.

**routingpy** is tested against 3.6, 3.7, 3.8, 3.9 and PyPy3.

.. _`README`: https://github.com/gis-ops/routing-py#api
.. _`Examples`: https://github.com/gis-ops/routing-py#examples
"""

from .routers import *  # noqa: F401

# Delete so options is only available over routingpy.routers.options
del options  # noqa: F821
