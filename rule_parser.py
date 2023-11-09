import importlib
import json
import os
import sys
from types import ModuleType
from typing import List, Optional
from rule_base import InputType, RuleList
from utils.logger import logger

rules_base_path: str = "rules"
precheck_subdir: str = "precheck"
check_subdir: str = "check"
postcheck_subdir: str = "postcheck"

supported_3d_extensions: List[str] = [
    'fbx', 'obj', 'gltf', 'glb', 'x3d', 'abc', 'dae', 'ply', 'stl', 'usd', 'blend']
supported_2d_extensions: List[str] = [
    'jpg', 'jpeg', 'png', 'tga', 'tif', 'tiff', 'bmp', 'exr', 'psd']
custom_extensions: List[str] = []

all_rules: List[RuleList] = []


def get_rules_path() -> str:
    application_path: str = os.path.dirname(sys.executable) if getattr(
        sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
    return os.path.join(application_path, rules_base_path)


def create_rules() -> None:
    rules_path: str = get_rules_path()

    list2D: RuleList = find_rules(os.path.join(
        rules_path, InputType.FILE_2D.value.lower()), InputType.FILE_2D)
    list3D: RuleList = find_rules(os.path.join(
        rules_path, InputType.FILE_3D.value.lower()), InputType.FILE_3D)
    listAudio: RuleList = find_rules(os.path.join(
        rules_path, InputType.FILE_AUDIO.value.lower()), InputType.FILE_AUDIO)
    listDir: RuleList = find_rules(os.path.join(
        rules_path, InputType.DIRECTORY.value.lower()), InputType.DIRECTORY)
    listCustom: RuleList = find_rules(os.path.join(
        rules_path, InputType.CUSTOM.value.lower()), InputType.CUSTOM)

    all_rules.append(list2D)
    all_rules.append(list3D)
    all_rules.append(listAudio)
    all_rules.append(listDir)
    all_rules.append(listCustom)

    custom_extensions = load_custom_extensions()


def load_custom_extensions() -> list[str]:
    _extensions: list[str] = []
    rules_path: str = get_rules_path()
    custom_extensions_file_path: str = os.path.join(
        rules_path, InputType.CUSTOM.value.lower(), "formats.json")
    if os.path.isfile(custom_extensions_file_path):
        with open(custom_extensions_file_path, 'r') as file:
            # read contents of the file as json
            extention_json = json.load(file)
            # {'EXTENSIONS': ['txt', 'csv']}
            _extensions = extention_json['EXTENSIONS']

    logger.info(f"Loaded custom extensions: {_extensions}")
    return _extensions


def find_rules(path: str, input_type: InputType) -> None:
    precheck_subdir_path: str = os.path.join(path, precheck_subdir)
    check_subdir_path: str = os.path.join(path, check_subdir)
    postcheck_subdir_path: str = os.path.join(path, postcheck_subdir)

    precheck_rule_files: List[str] = get_rule_files(precheck_subdir_path)
    check_rule_files: List[str] = get_rule_files(check_subdir_path)
    postcheck_rule_files: List[str] = get_rule_files(postcheck_subdir_path)

    rule_list: RuleList = RuleList(input_type)

    for rule_file_name in precheck_rule_files:
        module: Optional[ModuleType] = create_rule_from_file(
            precheck_subdir_path, rule_file_name)
        if module is not None:
            rule_list.add_precheck_rule(module)
    for rule_file_name in check_rule_files:
        module: Optional[ModuleType] = create_rule_from_file(
            check_subdir_path, rule_file_name)
        if module is not None:
            rule_list.add_check_rule(module)
    for rule_file_name in postcheck_rule_files:
        module: Optional[ModuleType] = create_rule_from_file(
            postcheck_subdir_path, rule_file_name)
        if module is not None:
            rule_list.add_postcheck_rule(module)
    return rule_list


def get_rule_files(rules_path: str) -> List[str]:
    rules: List[str] = [file for file in os.listdir(
        rules_path) if file.endswith(".py")]
    rules.sort()
    return rules


def create_rule_from_file(subdir: str, rule_file_name: str) -> Optional[ModuleType]:
    rule_name: str = os.path.splitext(rule_file_name)[0]
    spec = importlib.util.spec_from_file_location(
        rule_name, os.path.join(subdir, rule_file_name))
    module: ModuleType = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    module_name: Optional[str] = getattr(module, "RULE_NAME", None)
    if module_name is not None:
        logger.info("Loaded module: " + module_name)
    else:
        logger.error(
            f"Module \"{rule_name}\" in \"{rule_file_name}\" does not have a RULE_NAME attribute. skipping this rule...")
        return None
    return module


def get_input_type(input):
    file_extension = input.split('.')[-1]
    if os.path.isfile(input):
        if file_extension in supported_3d_extensions:
            return InputType.FILE_3D
        elif file_extension in supported_2d_extensions:
            return InputType.FILE_2D
        elif file_extension in custom_extensions:
            return InputType.CUSTOM
        else:
            return InputType.UNSUPPORTED
    elif os.path.isdir(input):
        return InputType.DIRECTORY


def get_rules_names():
    # The command name is a variable called RULE_NAME in each module
    commands = []
    for ruleList in all_rules:
        for module in ruleList.check_rules:
            commands.append(module.RULE_NAME)
        for module in ruleList.precheck_rules:
            commands.append(module.RULE_NAME)
        for module in ruleList.postcheck_rules:
            commands.append(module.RULE_NAME)
    return commands
