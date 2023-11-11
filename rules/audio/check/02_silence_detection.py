# This rute detects if the audio file has silence more than 1 second. usin
# imports here
from pydub import AudioSegment
from pydub.silence import detect_silence

# necessary for the rule to be loaded
RULE_NAME = "HasSilence"


def process(input):
    """
    This function is called for each file that is checked. The input is the file path.
    the function should return True if the file is valid and a json object with the errors if the file is not valid.
    example: 
    for a single error: {"file_path": "error message"}
    for multiple errors: {"object_name1": "error message1", "object_name2": "error message2"}
    """

    errors_json = {}

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
        errors_json[input] = "File has silence more than 1 second"

    if errors_json != {}:
        return errors_json
    else:
        return True
