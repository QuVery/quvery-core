import importlib
import os
import sys
from types import ModuleType
from typing import List, Optional
import error_codes
import rule_base
from utils.logger import logger

rules_base_path: str = "rules"
precheck_subdir: str = "precheck"
check_subdir: str = "check"
postcheck_subdir: str = "postcheck"

all_rules: List[rule_base.RuleList] = []

def get_rules_path() -> str:
    application_path: str = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
    return os.path.join(application_path, rules_base_path)

def create_rules() -> None:
    rules_path: str = get_rules_path()

    list2D : rule_base.RuleList = find_rules(os.path.join(rules_path, rule_base.InputType.FILE_2D.value.lower()), rule_base.InputType.FILE_2D)
    list3D : rule_base.RuleList = find_rules(os.path.join(rules_path, rule_base.InputType.FILE_3D.value.lower()), rule_base.InputType.FILE_3D)
    listAudio : rule_base.RuleList = find_rules(os.path.join(rules_path, rule_base.InputType.FILE_AUDIO.value.lower()), rule_base.InputType.FILE_AUDIO)
    listDir : rule_base.RuleList = find_rules(os.path.join(rules_path, rule_base.InputType.DIRECTORY.value.lower()), rule_base.InputType.DIRECTORY)
    listCustom: rule_base.RuleList = find_rules(os.path.join(rules_path, rule_base.InputType.CUSTOM.value.lower()), rule_base.InputType.CUSTOM)

    all_rules.append(list2D)
    all_rules.append(list3D)
    all_rules.append(listAudio)
    all_rules.append(listDir)
    all_rules.append(listCustom)

def find_rules(path: str, input_type: rule_base.InputType) -> None:
    precheck_subdir_path: str = os.path.join(path, precheck_subdir)
    check_subdir_path: str = os.path.join(path, check_subdir)
    postcheck_subdir_path: str = os.path.join(path, postcheck_subdir)
    
    precheck_rule_files: List[str] = get_rule_files(precheck_subdir_path)
    check_rule_files: List[str] = get_rule_files(check_subdir_path)
    postcheck_rule_files: List[str] = get_rule_files(postcheck_subdir_path)

    rule_list: rule_base.RuleList = rule_base.RuleList(input_type)

    for rule_file_name in precheck_rule_files:
        module: Optional[ModuleType] = create_rule_from_file(precheck_subdir_path, rule_file_name)
        if module is not None:
            rule_list.add_precheck_rule(module)
    for rule_file_name in check_rule_files:
        module: Optional[ModuleType] = create_rule_from_file(check_subdir_path, rule_file_name)
        if module is not None:
            rule_list.add_check_rule(module)
    for rule_file_name in postcheck_rule_files:
        module: Optional[ModuleType] = create_rule_from_file(postcheck_subdir_path, rule_file_name)
        if module is not None:
            rule_list.add_postcheck_rule(module)
    return rule_list

def get_rule_files(rules_path: str) -> List[str]:
    rules: List[str] = [file for file in os.listdir(rules_path) if file.endswith(".py")]
    rules.sort()
    return rules

def create_rule_from_file(subdir: str, rule_file_name: str) -> Optional[ModuleType]:
    rule_name: str = os.path.splitext(rule_file_name)[0]
    spec = importlib.util.spec_from_file_location(rule_name, os.path.join(subdir, rule_file_name))
    module: ModuleType = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    module_name: Optional[str] = getattr(module, "RULE_NAME", None)
    if module_name is not None:
        logger.info("Loaded module: " + module_name)
    else:
        logger.error(f"Module \"{rule_name}\" in \"{rule_file_name}\" does not have a RULE_NAME attribute. skipping this rule...")
        return None
    return module