#### Rule Structure

There are 3 stages for each rule type:

##### PreCheck

These rules will be run before the Check rules and will be used for things like loading the file. They will return a boolean value if the rule is passed or not.

##### Check

These rules will be run after all precheck rules and will be used for checking the file. They will return an empty array {} if no error has been occured, otherwise they will return a json containing the error message. Check the exsisting rules for more info.s

##### PostCheck

Same as PreCheck but will be run after the Check rules.

### Creating new rules:

Before creating a new rule, you need to know the structure of the rules.
There are 5 predefined rule categories: `2d`, `3d`, `audio`, `custom` and `dir`.
There is also a directory called ‌`generic` which contains the generic rules that are used for all categories.

To create a new rule, you need to create a new python file in the rules folder under the one if these subfolders: `2d`, `3d`, `audio`, `custom`, `dir` depending on the type of the rule you are creating. Then you can fill the file with the following template:

A rule can also return a link to a page containing more information about the rule. To do so, you need to add a `link` key to the returned json object. The value of the key should be the link to the page. this is useful if the client wants to know more about what caused the error and how to fix it.

```python
# imports here

# necessary for the rule to be loaded
RULE_NAME = "{{rule_name}}"

def process(input):
    """
    This function is called for each file that is checked. The input is the file path.
    the function should return an empty json if the file is valid and a json object with the status and required information.
    status can be one of the following: "error", "warning", "info"
    example:
    for a single error with link:
    {"status": "error" , "details": {"object_name": "error message"}, "link": "https://example.com"}
    for multiple errors:
    {"status": "error" , "details": {"object_name": "error message", "object_name2": "error message2"}}
    for a single warning:
    {"status": "warning" , "details": {"object_name": "warning message"}}
    for info:
    {"status": "info" , "details": {"object_name": "info message"}}
    """

    result_json = {"status": "info"} # default status is info
    details_json = {}

    # Implement your rule here and fill the details_json with the appropriate information or errors or leave it empty if there are no errors or warnings

    if details_json != {}:
        result_json["details"] = details_json
        return result_json
    else:
        return {}
```

You can check the existing rules for more info.
