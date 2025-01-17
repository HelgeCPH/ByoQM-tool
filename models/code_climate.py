from typing import Dict

from byoqm.qualitymodel.qualitymodel import QualityModel


class CodeClimate(QualityModel):
    # Arbitrary choice of 30 minutes implementation time per line
    _LINE_IMPLEMENTATiON_TIME = 30
    # Code Climate reports 45 minutes to fix when 3 over the allowed cognitive complexity
    _COGNITIVE_COMPLEXITY_REMEDIATION_COST = 45
    # Too many return statements is reported as 30 minutes to fix
    _RETURN_STATEMENTS_REMEDIATION_COST = 30
    # Nested control flow is reported as taking 45 minutes to fix
    _NESTED_CONTROL_FLOW_REMEDIATION_COST = 60
    # When argument count is exactly one over the threshhold (5) it takes 35 minutes
    # to fix It seems to scale with 10 minutes per argument hat is over when it is (6)
    # then it takes 45 minutes to fix
    _ARGUMENT_COUNT_REMEDIATION_COST = 35
    # When the method is 9 lines over 25, Code Climate reports that it takes 1 hour to fix
    _METHOD_LINES_REMEDIATION_COST = 60
    # When the file is exactly 1 line over 250, Code Climate reports that it will take 2 hours to fix
    _FILE_LINES_REMEDIATION_COST = 120
    # When there is code duplication in 2 places, Code Climate reports that it will take 1 hour to fix
    # It does, however, appear that they account for the size of the code snippet somehow as they sometimes
    # report 45, 50 mminutes
    _IDENTICAL_CODE_REMEDIATION_COST = 60
    _SIMILAR_CODE_REMEDIATION_COST = 60

    def getDesc(self) -> Dict:
        model = {
            "metrics": {
                "method_lines": "./metrics/method_length.py",
                "file_lines": "./metrics/file_length.py",
                "argument_count": "./metrics/argument_count.py",
                "complex_logic": "./metrics/complex_logic.py",
                "method_count": "./metrics/method_count.py",
                "return_statements": "./metrics/return_statements.py",
                "identical-code": "./metrics/identical_codeblocks.py",
                "similar-code": "./metrics/similar_codeblocks.py",
                "nested_control_flow": "./metrics/nested_controlflows.py",
                "cognitive_complexity": "./metrics/cognitive_complexity.py",
                "code_size": "./metrics/code_size.py",
            },
            "aggregations": {
                "Complexity": self.complexity,
                "Duplication": self.duplication,
                "Maintainability": self.maintainability,
            },
        }
        return model

    def maintainability(self, results: Dict) -> str:
        # https://docs.codeclimate.com/docs/maintainability-calculation
        code_size: int = results["code_size"]
        implementation_time: int = code_size * self._LINE_IMPLEMENTATiON_TIME
        technical_debt = results["Complexity"] + results["Duplication"]
        tech_debt_ratio: float = technical_debt / implementation_time

        return self._map_to_letter(tech_debt_ratio)

    def _map_to_letter(self, tech_debt_ratio: float) -> str:
        # Intervals are taken from Pfeiffers and Lungu's Paper:
        # Technical Debt and Maintainability: How do tools measure it?
        if 0 <= tech_debt_ratio <= 0.05:
            return "A"
        elif 0.05 < tech_debt_ratio <= 0.1:
            return "B"
        elif 0.1 < tech_debt_ratio <= 0.2:
            return "C"
        elif 0.2 < tech_debt_ratio <= 0.5:
            return "D"
        else:
            return "F"

    def complexity(self, results: Dict) -> int | float:
        return (
            results["cognitive_complexity"].get_frequency()
            * self._COGNITIVE_COMPLEXITY_REMEDIATION_COST
            + results["return_statements"].get_frequency()
            * self._RETURN_STATEMENTS_REMEDIATION_COST
            + results["nested_control_flow"].get_frequency()
            * self._NESTED_CONTROL_FLOW_REMEDIATION_COST
            + results["argument_count"].get_frequency()
            * self._ARGUMENT_COUNT_REMEDIATION_COST
            + results["method_lines"].get_frequency()
            * self._METHOD_LINES_REMEDIATION_COST
            + results["file_lines"].get_frequency() * self._FILE_LINES_REMEDIATION_COST
        )

    def duplication(self, results: Dict) -> int | float:
        return (
            results["identical-code"].get_frequency()
            * self._IDENTICAL_CODE_REMEDIATION_COST
            + results["similar-code"].get_frequency()
            * self._SIMILAR_CODE_REMEDIATION_COST
        )


model = CodeClimate()
