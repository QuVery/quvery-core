
from enum import Enum
import json
from types import ModuleType
from utils.logger import logger


class InputType(Enum):
    FILE_3D = "3D"
    FILE_2D = "2D"
    FILE_AUDIO = "AUDIO"
    DIRECTORY = "DIR"
    CUSTOM = "CUSTOM"
    UNSUPPORTED = "UNSUPPORTED"

# an abstract class for rules to inherit from


class RuleList:
    def __init__(self, type):
        self.type = type
        self._precheck_rules: list[ModuleType] = []
        self._check_rules: list[ModuleType] = []
        self._postcheck_rules: list[ModuleType] = []

    def add_precheck_rule(self, rule: ModuleType):
        self._precheck_rules.append(rule)

    def add_check_rule(self, rule: ModuleType):
        self._check_rules.append(rule)

    def add_postcheck_rule(self, rule: ModuleType):
        self._postcheck_rules.append(rule)

    def get_rules(self):
        rules = []
        for module in self._precheck_rules:
            rules.append(module.RULE_NAME)
        for module in self._check_rules:
            rules.append(module.RULE_NAME)
        for module in self._postcheck_rules:
            rules.append(module.RULE_NAME)
        return rules

    def execute_rules(self, input):
        result = []
        for module in self._precheck_rules:
            logger.info(f"Processing rule {module.RULE_NAME}")
            process_result = module.process(input)
            if process_result != True:
                return f"Precheck failed at rule \"{module.RULE_NAME}\"."
        for module in self._check_rules:
            logger.info(f"Processing rule {module.RULE_NAME}")
            process_result = module.process(input)
            if process_result != True:
                json_result = {}
                json_result[module.RULE_NAME] = process_result
                result.append(json_result)
        for module in self._postcheck_rules:
            logger.info(f"Processing rule {module.RULE_NAME}")
            process_result = module.process(input)
            if process_result != True:
                return f"Postcheck failed at rule \"{module.RULE_NAME}\"."
        return json.dumps(result)
