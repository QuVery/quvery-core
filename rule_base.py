
from enum import Enum
from types import ModuleType


class InputType(Enum):
    DIRECTORY = "DIR"
    FILE_3D = "3D"
    FILE_2D = "2D"
    FILE_AUDIO = "AUDIO"
    CUSTOM = "CUSTOM"
    UNSUPPORTED = "UNSUPPORTED"

# an abstract class for rules to inherit from
class RuleList:
    def __init__(self, type):
        self.type = type
        self.precheck_rules : list[ModuleType] = []
        self.check_rules : list[ModuleType] = []
        self.postcheck_rules : list[ModuleType] = []
    
    def add_precheck_rule(self, rule : ModuleType):
        self.precheck_rules.append(rule)

    def add_check_rule(self, rule : ModuleType):
        self.check_rules.append(rule)

    def add_postcheck_rule(self, rule : ModuleType):
        self.postcheck_rules.append(rule)