# This rule detects if the audio file has silence more than 1 second.
# imports here
from pydub import AudioSegment
from pydub.silence import detect_silence

# necessary for the rule to be loaded
RULE_NAME = "HasSilence"


def process(input):
    return {}
    """
    This function is called for each file that is checked. The input is the file path.
    The function should return an empty json if the file is valid and a json object with the status and required information.
    status can be one of the following: "error", "warning", "info"
    """
    result_json = {"status": "error"}  # default status is error
    details_json = {}
    # Implement your rule here
    # Load audio file
    audio = AudioSegment.from_file(input)
    # Define silence threshold and minimum silence length (in milliseconds)
    silence_thresh = -80  # in dBFS
    min_silence_len = 1000  # in milliseconds, 1 second
    # Detect silent chunks
    silent_chunks = detect_silence(
        audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
    # Check if there is any silence more than 1 second
    if any(end - start >= min_silence_len for start, end in silent_chunks):
        details_json[input] = "File has silence more than 1 second"
    if details_json != {}:
        result_json["details"] = details_json
        return result_json
    else:
        return {}
