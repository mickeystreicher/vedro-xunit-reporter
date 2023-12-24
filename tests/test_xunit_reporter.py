import unittest

from vedro.plugins.director import Reporter

from vedro_xunit_reporter import XUnitReporterPlugin


class TestXUnitReporter(unittest.TestCase):
    def test_plugin(self):
        assert self.assertIsInstance(XUnitReporterPlugin, Reporter)


if __name__ == "__main__":
    unittest.main()
