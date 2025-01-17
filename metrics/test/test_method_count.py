from pathlib import Path
import unittest
import os
from byoqm.source_repository.source_repository import SourceRepository
from metrics.method_count import MethodCount


class TestMethodCount(unittest.TestCase):
    def setUp(self):
        # chdir because paths are assumed to be relative from the project root but test
        # paths start at the test file
        os.chdir("../../")
        self._source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_method_count"), "python"
        )
        self._methodcount = MethodCount()
        self._methodcount._source_repository = self._source_repository

    def test_method_count_given__python_file_returns_1(self):
        result = self._methodcount.run()
        self.assertEqual(result.get_frequency(), 1)
        locations = result.get_violation_locations()
        self.assertEqual((locations[0][1], locations[0][2]), (1, 81))

    def test_method_count_given_java_file_returns_1(self):
        new_source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_method_count"), "java"
        )
        new_method_counter = MethodCount()
        new_method_counter._source_repository = new_source_repository
        result = new_method_counter.run()
        self.assertEqual(result.get_frequency(), 1)
        locations = result.get_violation_locations()
        self.assertEqual((locations[0][1], locations[0][2]), (2, 65))

    def test_method_count_given_c_sharp_file_returns_1(self):
        new_source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_method_count"), "c_sharp"
        )
        new_method_counter = MethodCount()
        new_method_counter._source_repository = new_source_repository
        result = new_method_counter.run()
        self.assertEqual(result.get_frequency(), 1)
        locations = result.get_violation_locations()
        self.assertEqual((locations[0][1], locations[0][2]), (3, 98))

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())


if __name__ == "__main__":
    unittest.main()
