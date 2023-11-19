# Validates the audio file format. supported formats are: wav and aiff

# imports here
# necessary for the rule to be loaded
RULE_NAME = "Check Format"


def process(input):
    """
    This function is called for each file that is checked. The input is the file path.
    The function should return an empty json if the file is valid and a json object with the status and required information.
    status can be one of the following: "error", "warning", "info"
    """
    result_json = {"status": "error"}  # default status is error
    details_json = {}
    # Implement your rule here
    valid_formats = ["wav", "aiff"]
    file_extension = input.split('.')[-1]
    if file_extension not in valid_formats:
        details_json[input] = "File format is not supported. Supported formats are: " + \
            ", ".join(valid_formats)
    if details_json != {}:
        result_json["details"] = details_json
        return result_json
    else:
        return {}
