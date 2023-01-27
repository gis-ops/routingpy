import tests as _test
from routingpy import ORS, OSRM, Graphhopper, Valhalla


class TestRoutingpyIntegration(_test.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.valhalla = Valhalla("http://localhost:8002")
        cls.osrm = OSRM("http://localhost:5000")
        cls.ors = ORS(base_url="http://localhost:8005/ors")
        cls.gh = Graphhopper(base_url="http://localhost:8989")

    def test_valhalla_directions(self):

        directions = self.valhalla.directions(
            [
                [1.51886, 42.5063],
                [1.53789, 42.51007],
            ],
            "auto",
        )

        self.assertIsInstance(directions.geometry, list)
        self.assertIsInstance(directions.duration, int)
        self.assertIsInstance(directions.distance, int)

    def test_valhalla_isochrones(self):

        isochrones = self.valhalla.isochrones(
            [
                [1.51886, 42.5063],
            ],
            "auto",
            [20, 50],
        )

        self.assertIsInstance(isochrones[1].geometry, list)
        self.assertEqual(isochrones[0].interval, 20)
        self.assertEqual(isochrones[1].interval, 50)
        self.assertEqual(isochrones[1].center, [1.51886, 42.5063])

    def test_valhalla_matrix(self):
        matrix = self.valhalla.matrix(
            [
                [1.51886, 42.5063],
                [1.53789, 42.51007],
                [1.53489, 42.52007],
                [1.53189, 42.51607],
            ],
            "auto",
        )

        self.assertEqual(len(matrix.distances), 4)
        self.assertEqual(len(matrix.durations), 4)
        self.assertEqual(len(matrix.durations[0]), 4)
        self.assertEqual(len(matrix.distances[0]), 4)

    def test_osrm_directions(self):
        directions = self.osrm.directions(
            [
                [1.51886, 42.5063],
                [1.53789, 42.51007],
            ]
        )

        self.assertIsInstance(directions.geometry, list)
        self.assertIsInstance(directions.duration, int)
        self.assertIsInstance(directions.distance, int)

    def test_osrm_matrix(self):
        matrix = self.osrm.matrix(
            [
                [1.51886, 42.5063],
                [1.53789, 42.51007],
                [1.53489, 42.52007],
                [1.53189, 42.51607],
            ],
            "auto",
        )

        self.assertEqual(len(matrix.distances), 4)
        self.assertEqual(len(matrix.durations), 4)
        self.assertEqual(len(matrix.durations[0]), 4)
        self.assertEqual(len(matrix.distances[0]), 4)

    # def test_ors_directions(self):
    #     directions = self.ors.directions(
    #         [
    #             [1.51886, 42.5063],
    #             [1.53789, 42.51007],
    #         ],
    #         "driving-car",
    #     )
    #
    #     self.assertIsInstance(directions.geometry, list)
    #     self.assertIsInstance(directions.duration, int)
    #     self.assertIsInstance(directions.distance, int)

    def test_ors_isochrones(self):
        isochrones = self.ors.isochrones([1.51886, 42.5063], "driving-car", [20, 50])

        self.assertIsInstance(isochrones[1].geometry, list)
        self.assertEqual(isochrones[0].interval, 20)
        self.assertEqual(isochrones[1].interval, 50)
        self.assertAlmostEqual(isochrones[1].center[0], 1.51886, 1)
        self.assertAlmostEqual(isochrones[1].center[1], 42.5063, 1)

    def test_ors_matrix(self):
        matrix = self.ors.matrix(
            [
                [1.51886, 42.5063],
                [1.53789, 42.51007],
                [1.53489, 42.52007],
                [1.53189, 42.51607],
            ],
            "driving-car",
            metrics=["distance", "duration"],
        )

        self.assertEqual(len(matrix.distances), 4)
        self.assertEqual(len(matrix.durations), 4)
        self.assertEqual(len(matrix.durations[0]), 4)
        self.assertEqual(len(matrix.distances[0]), 4)

    def test_graphhopper_directions(self):
        directions = self.gh.directions(
            [
                [1.51886, 42.5063],
                [1.53789, 42.51007],
            ],
            "car",
        )

        self.assertIsInstance(directions.geometry, list)
        self.assertIsInstance(directions.duration, int)
        self.assertIsInstance(directions.distance, int)

    def test_graphhopper_isochrones(self):
        isochrones = self.gh.isochrones([1.51886, 42.5063], "car", [50])

        self.assertIsInstance(isochrones[0].geometry, list)
        self.assertEqual(isochrones[0].interval, 50)
        self.assertAlmostEqual(isochrones[0].center[0], 1.51886, 1)
        self.assertAlmostEqual(isochrones[0].center[1], 42.5063, 1)
