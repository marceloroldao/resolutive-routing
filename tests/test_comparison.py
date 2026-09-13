import unittest

from resolutive_routing.comparison import compare_strategies
from resolutive_routing.corpus import scenario_corpus


class ComparisonTests(unittest.TestCase):
    def test_resolutive_hits_expected_targets(self):
        results = {item.strategy: item for item in compare_strategies(scenario_corpus())}
        resolutive = results["resolutive"]
        self.assertEqual(resolutive.target_hits, resolutive.scenarios)
        self.assertEqual(resolutive.unnecessary_dispatches, 0)
        self.assertLessEqual(resolutive.mean_fanout, 1.0)

    def test_broadcast_has_higher_fanout_than_resolutive(self):
        results = {item.strategy: item for item in compare_strategies(scenario_corpus())}
        self.assertGreater(results["broadcast"].mean_fanout, results["resolutive"].mean_fanout)
        self.assertGreater(results["broadcast"].unnecessary_dispatches, 0)

    def test_static_assignment_misses_some_cases(self):
        results = {item.strategy: item for item in compare_strategies(scenario_corpus())}
        self.assertLess(results["static"].target_hit_rate, results["resolutive"].target_hit_rate)


if __name__ == "__main__":
    unittest.main()
