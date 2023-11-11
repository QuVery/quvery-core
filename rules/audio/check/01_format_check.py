# Validates the audio file format. supported formats are: wav and aiff

# imports here

# necessary for the rule to be loaded
RULE_NAME = "Check Format"


def process(input):
    """
    This function is called for each file that is checked. The input is the file path.
    """

    report_json = {}

    # Implement your rule here
    valid_formats = ["wav", "aiff"]
    file_extension = input.split('.')[-1]
    if file_extension not in valid_formats:
        report_json[input] = "File format is not supported. Supported formats are: " + \
            ", ".join(valid_formats)

    if report_json == {}:  # if no error
        return True
    else:
        return report_json
