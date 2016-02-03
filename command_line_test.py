import unittest
from command_line import *

class CommandLineTest(unittest.TestCase):

    def test_command_start(self):
        cl = CommandLine(["name"])
        self.assertEqual(cl.get_command(), "start")
        self.assertEqual(cl.get_name(),    "name")

        cl = CommandLine(["--", "stop"])
        self.assertEqual(cl.get_command(), "start")
        self.assertEqual(cl.get_name(),    "stop")

    def test_command_stop(self):
        cl = CommandLine(["stop"])
        self.assertEqual(cl.get_command(), "stop")

    def test_command_status(self):
        cl = CommandLine([])
        self.assertEqual(cl.get_command(), "status")

        cl = CommandLine(["status"])
        self.assertEqual(cl.get_command(), "status")

    def test_command_continue(self):
        cl = CommandLine(["continue"])
        self.assertEqual(cl.get_command(), "continue")

    def test_command_name(self):
        cl = CommandLine(["name"])
        self.assertEqual(cl.get_name(), "name")

        cl = CommandLine(["   a   bit    longer  name  "])
        self.assertEqual(cl.get_name(), "a bit longer name")

        cl = CommandLine(["a", "bit", "longer", "name"])
        self.assertEqual(cl.get_name(), "a bit longer name")

    def test_command_category(self):
        cl = CommandLine(["start", "category:name"])
        self.assertEqual(cl.get_category(), "category")
        self.assertEqual(cl.get_name(), "name")

        cl = CommandLine(["start", "    your favorite   category:   a   bit    longer  name  "])
        self.assertEqual(cl.get_category(), "your favorite category")
        self.assertEqual(cl.get_name(), "a bit longer name")

        cl = CommandLine(["start", "your", "favorite", "category", ":", "a", "bit", "longer", "name"])
        self.assertEqual(cl.get_category(), "your favorite category")
        self.assertEqual(cl.get_name(), "a bit longer name")

        cl = CommandLine(["start", "your", "favorite", "category", ":", "a", "bit", "longer", "name"])
        self.assertEqual(cl.get_category(), "your favorite category")
        self.assertEqual(cl.get_name(), "a bit longer name")


if __name__ == '__main__':
    unittest.main()
