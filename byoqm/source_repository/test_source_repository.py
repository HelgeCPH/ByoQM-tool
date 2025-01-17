import unittest

import tree_sitter

from byoqm.source_repository.source_repository import SourceRepository
from pathlib import Path


class TestSourceRepository(unittest.TestCase):
    def setUp(self) -> None:
        self.source_repository = SourceRepository(
            Path("byoqm/source_repository/test/data"), "python"
        )

    def test_get_ast_given_a_child_file_returns_a_tree_sitter_ast(self):
        target = Path("./byoqm/source_repository/test/data/a_file.py")
        actual = self.source_repository.getAst(target)

        self.assertIsInstance(actual, tree_sitter.Tree)

    def test_get_ast_given_a_sibling_file_fails(self):
        target = Path("./byoqm/source_repository/source_repository.py")
        self.assertRaises(ValueError, self.source_repository.getAst, target)

    def test_get_ast_returns_tree_with_2_elements(self):
        target = Path("./byoqm/source_repository/test/data/a_file.py")
        tree = self.source_repository.getAst(target)
        actual = len(tree.root_node.children)
        self.assertEqual(actual, 2)

    def test_new_source_repository_findes_c_sharp_files(self):
        new_coordinator = SourceRepository(
            Path("byoqm/source_repository/test/data"), "c_sharp"
        )
        actual = new_coordinator.src_paths

        self.assertEqual(
            actual, [Path("byoqm/source_repository/test/data/a_nother_file.cs")]
        )
