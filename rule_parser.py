import importlib
import json
import os
import sys
from types import ModuleType
from typing import List, Optional
from error_codes import Error_Codes
from rule_base import InputType, RuleList
from utils.logger import logger
from ignore_parser import IgnoreParser

# region private variables

_rules_base_path: str = "rules"
_precheck_subdir: str = "precheck"
_check_subdir: str = "check"
_postcheck_subdir: str = "postcheck"

_supported_3d_extensions: List[str] = [
    'fbx', 'obj', 'gltf', 'glb', 'x3d', 'abc', 'dae', 'ply', 'stl', 'usd', 'blend']
_supported_2d_extensions: List[str] = [
    'jpg', 'jpeg', 'png', 'tga', 'tif', 'tiff', 'bmp', 'exr', 'psd']
_supported_audio_extensions: List[str] = [
    'wav', 'aiff', 'mp3', 'ogg', 'flac', 'wma', 'aac']
_custom_extensions: List[str] = []

_all_rules: List[RuleList] = []

ignore_parser = IgnoreParser(os.path.join(_rules_base_path, ".ignore"))

# endregion

# region public functions


def create_rules() -> None:
    logger.info("Creating rules...")

    rules_path: str = __get_rules_path()

    list2D: RuleList = __find_rules(os.path.join(
        rules_path, InputType.FILE_2D.value.lower()), InputType.FILE_2D)
    logger.info(f"Loading 2D rules completed...")
    list3D: RuleList = __find_rules(os.path.join(
        rules_path, InputType.FILE_3D.value.lower()), InputType.FILE_3D)
    logger.info(f"Loading 3D rules completed...")
    listAudio: RuleList = __find_rules(os.path.join(
        rules_path, InputType.FILE_AUDIO.value.lower()), InputType.FILE_AUDIO)
    logger.info(f"Loading Audio rules completed...")
    listDir: RuleList = __find_rules(os.path.join(
        rules_path, InputType.DIRECTORY.value.lower()), InputType.DIRECTORY)
    logger.info(f"Loading Directory rules completed...")
    listCustom: RuleList = __find_rules(os.path.join(
        rules_path, InputType.CUSTOM.value.lower()), InputType.CUSTOM)
    logger.info(f"Loading Custom rules completed...")

    _all_rules.append(list2D)
    _all_rules.append(list3D)
    _all_rules.append(listAudio)
    _all_rules.append(listDir)
    _all_rules.append(listCustom)
    logger.info("Finished Creating rules...")
    logger.info("Loading custom extensions...")
    custom_extensions = __load_custom_extensions()
    logger.info("Finished loading custom extensions...")


def get_rules(type: str) -> list[str]:
    # The command name is a variable called RULE_NAME in each module
    rules = []
    for ruleList in _all_rules:
        if ruleList.type.value.lower() == type.lower():
            rules = ruleList.get_rules()
    return rules


def is_ignored(input: str) -> bool:
    is_input_ignored = ignore_parser.is_ignored(input)
    # logger.info(f"Checking if {input} is ignored: {is_input_ignored}")
    return is_input_ignored


def execute_rules_for_file(input: str) -> list[str]:
    if (is_ignored(input)):
        return {"input": input, "error": Error_Codes.FILE_IGNORED.value}
    input_type = __get_input_type(input)
    if input_type == InputType.UNSUPPORTED:
        return {"input": input, "error": Error_Codes.FILE_NOT_VALID.value}
    result_json = {}
    for ruleList in _all_rules:
        if ruleList.type == input_type:
            result = ruleList.execute_rules(input)
            if result != True:
                result_json = result
    return result_json


def execute_rules_in_directory(dir: str, rule_type: Optional[str] = None) -> list[str]:
    # list all files in the directory and run execute_rules on each file
    ignore_parser.set_base_path(dir)

    result_json = {}
    result_json["input"] = dir
    files_array = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            file_path = os.path.join(root, file)
            if (is_ignored(file_path)):
                continue
            file_rule_type = __get_input_type(file_path).value.lower()
            if rule_type is not None and file_rule_type != rule_type:
                continue
            logger.info(f"Checking file {file_path}")
            result = execute_rules_for_file(file_path)
            if result != True:
                files_array.append(result)
                logger.info(
                    f"Checked file {file_path} completed with some errors")
    result_json["files"] = files_array
    return result_json


def get_rule_types() -> list[str]:
    return [input_type.value.lower() for input_type in InputType]

# endregion

# region private functions


def __get_input_type(input):
    if os.path.isfile(input):
        file_extension = input.split('.')[-1]
        if file_extension in _supported_3d_extensions:
            return InputType.FILE_3D
        elif file_extension in _supported_2d_extensions:
            return InputType.FILE_2D
        elif file_extension in _supported_audio_extensions:
            return InputType.FILE_AUDIO
        elif file_extension in _custom_extensions:
            return InputType.CUSTOM
        else:
            return InputType.UNSUPPORTED
    elif os.path.isdir(input):
        return InputType.DIRECTORY


def __load_custom_extensions() -> list[str]:
    _extensions: list[str] = []
    rules_path: str = __get_rules_path()
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


def __find_rules(path: str, input_type: InputType) -> None:
    precheck_subdir_path: str = os.path.join(path, _precheck_subdir)
    check_subdir_path: str = os.path.join(path, _check_subdir)
    postcheck_subdir_path: str = os.path.join(path, _postcheck_subdir)

    precheck_rule_files: List[str] = __get_rule_files(precheck_subdir_path)
    check_rule_files: List[str] = __get_rule_files(check_subdir_path)
    postcheck_rule_files: List[str] = __get_rule_files(postcheck_subdir_path)

    rule_list: RuleList = RuleList(input_type)

    for rule_file_name in precheck_rule_files:
        module: Optional[ModuleType] = __create_rule_from_file(
            precheck_subdir_path, rule_file_name)
        if module is not None:
            rule_list.add_precheck_rule(module)
    for rule_file_name in check_rule_files:
        module: Optional[ModuleType] = __create_rule_from_file(
            check_subdir_path, rule_file_name)
        if module is not None:
            rule_list.add_check_rule(module)
    for rule_file_name in postcheck_rule_files:
        module: Optional[ModuleType] = __create_rule_from_file(
            postcheck_subdir_path, rule_file_name)
        if module is not None:
            rule_list.add_postcheck_rule(module)
    return rule_list


def __get_rule_files(rules_path: str) -> List[str]:
    rules: List[str] = [file for file in os.listdir(
        rules_path) if file.endswith(".py")]
    rules.sort()
    return rules


def __create_rule_from_file(subdir: str, rule_file_name: str) -> Optional[ModuleType]:
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


def __get_rules_path() -> str:
    application_path: str = os.path.dirname(sys.executable) if getattr(
        sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
    return os.path.join(application_path, _rules_base_path)

# endregion
