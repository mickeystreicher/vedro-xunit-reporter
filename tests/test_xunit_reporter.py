import unittest

from vedro.plugins.director import Reporter

from vedro_xunit_reporter import XUnitReporter, XUnitReporterPlugin


class TestXUnitReporter(unittest.TestCase):
    def test_plugin(self):
        self.assertIsInstance(XUnitReporterPlugin(XUnitReporter), Reporter)


if __name__ == "__main__":
    unittest.main()
