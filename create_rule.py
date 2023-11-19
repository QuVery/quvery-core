import os
import re
import sys


file_template = """
# imports here

# necessary for the rule to be loaded
RULE_NAME = "{{rule_name}}"

def process(input):
    \"\"\"
    This function is called for each file that is checked. The input is the file path.
    the function should return an empty json if the file is valid and a json object with the status and required information.
    status can be one of the following: "error", "warning", "info"
    example: 
    for a single error: {"status": "error" , "details": {"object_name": "error message"}}
    for multiple errors: {"status": "error" , "details": {"object_name": "error message", "object_name2": "error message2"}}
    for a single warning: {"status": "warning" , "details": {"object_name": "warning message"}}
    for info: {"status": "info" , "details": {"object_name": "info message"}}
    \"\"\"

    result_json = {"status": "info"} # default status is info
    details_json = {}

    # Implement your rule here and fill the details_json with the appropriate information or errors or leave it empty if there are no errors or warnings

    if details_json != {}:
        result_json["details"] = details_json
        return result_json
    else:
        return {}
"""


def parse_args():
    args = sys.argv[1:]  # Ignore the script name itself
    parsed_args = {}
    # split the arguments by space. the first argument is the rule type and the second argument is the rule name
    if len(args) != 2:
        raise ValueError(
            "Expected rule type and rule name. Example: python create_rule.py 3d format_check")
    parsed_args['rule_type'] = args[0]
    if parsed_args['rule_type'] not in ["3d",
                                        "2d",
                                        "audio",
                                        "dir",
                                        "custom"]:
        raise ValueError(
            "Rule type must be one of the following: 3d, 2d, audio, dir, custom")
    parsed_args['rule_name'] = args[1]
    return parsed_args


if __name__ == "__main__":
    # parse arguments from command line
    args = parse_args()
    # get the rule name from the arguments
    rule_name = args['rule_name']
    # get the rule type from the arguments
    rule_type = args['rule_type']

    # generate the file name from the rule name by replacing spaces with underscores and adding underscore between camel case words
    file_name = re.sub(r"([a-z])([A-Z])", r"\1_\2",
                       rule_name).replace(" ", "_").lower() + ".py"

    # check the existence of the rule file in the rules/check directory and get the last number in the file name before "_" like 01 in 01_rule_name.py
    # if there are no files in the directory, the number is 01
    last_rule_number = 0
    try:
        last_rule_number = int(sorted([file_name.split(
            "_")[0] for file_name in os.listdir(f"rules/{rule_type}/check/")])[-1])
    except:
        pass
    last_rule_number += 1
    # add leading zero to the number if it is less than 10
    last_rule_number = str(last_rule_number).zfill(2)
    # add the number to the file name
    file_name = f"{last_rule_number}_{file_name}"

    print(
        f"Creating rule {rule_name} of type {rule_type} with file name {file_name}")

    # create the file at current directory + /rules/ + rule_type + / "check/" + file_name
    with open(f"rules/{rule_type}/check/{file_name}", "w") as f:
        # replace the placeholder with the rule name
        file_content = file_template.replace("{{rule_name}}", rule_name)
        # write the file content to the file
        f.write(file_content)
