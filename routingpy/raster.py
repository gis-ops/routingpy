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
:class:`Raster` returns rasters results.
"""
from typing import Optional


class Raster(object):
    """
    Contains a parsed single raster response. Access via properties ``image``, ``interval``
    """

    def __init__(self, image=None, interval=None):
        self._image = image
        self._interval = interval

    @property
    def image(self) -> Optional[bytes]:
        """
        The image of the raster.

        :rtype: bytes
        """
        return self._image

    @property
    def interval(self) -> int:
        """
        The interval of the raster in seconds.

        :return: int
        """
        return self._interval

    def __repr__(self):  # pragma: no cover
        return "Raster({})".format(self.interval)
