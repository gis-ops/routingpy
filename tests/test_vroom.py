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
"""Tests for the Vroom module."""

import unittest

import responses

from routingpy import Vroom
from tests.test_helper import ENDPOINTS_QUERIES, ENDPOINTS_RESPONSES


class VroomTest(unittest.TestCase):

    name = "vroom"

    def setUp(self):
        self.client = Vroom("http://solver.vroom-project.org/")

    @responses.activate
    def test_basic_optimization(self):
        query = ENDPOINTS_QUERIES[self.name]["optimization"]
        responses.add(
            responses.POST,
            "http://solver.vroom-project.org",
            status=200,
            json=ENDPOINTS_RESPONSES[self.name]["optimization"],
            content_type="application/json",
        )
        optimization = self.client.optimization(**query)
        self.assertEqual(optimization.code, 0)
        self.assertEqual(optimization.error, None)
        self.assertEqual(optimization.summary.cost, 4097)
