from byoqm.metric.metric import Metric
from byoqm.metric.result import Result
from byoqm.metric.violation import Violation
from byoqm.source_repository.source_repository import SourceRepository
from metrics.util.query_translations import translate_to


class ComplexLogic(Metric):
    def __init__(self):
        self._source_repository: SourceRepository = None

    def run(self):
        result = Result("complex logic", [])
        for file in self._source_repository.src_paths:
            result.violations.extend(
                self._parse(self._source_repository.getAst(file), file)
            )
        return result

    def _parse(self, ast, file):
        """
        Finds the conditionals of a file and returns the number of conditionals that have more than 4 conditions
        """
        violations = []
        query = self._source_repository.tree_sitter_language.query(
            f"""
            (_ [{translate_to[self._source_repository.language]["bool_operator"]}] @bool_operator)
            """
        )
        captures = query.captures(ast.root_node)
        for capture in captures:
            # initial count is always at least 2 (right and left)
            boolean_count = 2
            node = capture[0]
            bool_operator = translate_to[self._source_repository.language][
                "bool_operator_child"
            ]
            children = [
                node.child_by_field_name("left"),
                node.child_by_field_name("right"),
            ]
            while len(children) > 0:
                if boolean_count > 4:
                    break
                child = children.pop()
                if child.type == bool_operator:
                    boolean_count += 1
                    children.extend(
                        [
                            child.child_by_field_name("left"),
                            child.child_by_field_name("right"),
                        ]
                    )
            if boolean_count > 4:
                violations.append(
                    Violation(
                        "complex logic",
                        (
                            str(file),
                            node.start_point[0] + 1,
                            node.end_point[0] + 1,
                        ),
                    )
                )
        return violations


metric = ComplexLogic()
