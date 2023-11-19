# QuVery Core

QuVery Core is the core library of QuVery. It provides the basic functions of QuVery to be used in other projects like QuVery-CLI or QuVery-GUI.

## Introduction

### For Artists

If you are an artist, you know that how hard and time consuming it is to get a message from the client that your file has some technical issues. QuVery is here to help you with that. It will check your file for any technical issues and will let you know if there is any. It will also provide you with a list of the issues and how to fix them. Of course it will not check everything but it will check the most common issues that can be found in a file.

### For Teams

If you are part of a team, QuVery can help streamline your workflow. By automating the process of checking files for technical issues, it can save your team valuable time and effort. It can also help ensure consistency across different team members' work, as it applies the same set of rules to every file it checks. This can be particularly useful for large teams or for teams working remotely, where it can be harder to maintain consistency.

### For Companies

QuVery can be a valuable addition to your company's CI/CD pipeline. By integrating QuVery into your CI/CD tool, you can automate the process of checking files for technical issues. This can help you catch and fix issues early in the development process, before they become more costly and time-consuming to resolve. It can also help ensure that all files meet your company's technical standards before they are deployed, which can improve the quality of your products and services.

Some of the advantages of integrating QuVery into your CI/CD pipeline include:

- **Early detection of issues:** QuVery can help you catch technical issues early in the development process, when they are typically easier and less costly to fix.

- **Improved quality control:** By automatically checking all files for technical issues, QuVery can help ensure that all files meet your company's technical standards before they are deployed.

- **Increased efficiency:** Automating the process of checking files for technical issues can save your team valuable time and effort, allowing them to focus on other important tasks.

- **Consistency:** QuVery applies the same set of rules to every file it checks, helping to ensure consistency across different team members' work.

Remember, QuVery is not just a tool, it's a solution to streamline your workflow and maintain the quality of your projects.

### Quvery Core

This is the heart of Quvery. It runs a local server providing FastAPI endpoints for clients to send requests to. The server will then run the rules and return the result to the client.
Here are some of the available endpoints:

| Endpoint                      | Method | Description                                        |
| ----------------------------- | ------ | -------------------------------------------------- |
| `/live`                       | GET    | Check the server live status                       |
| `/get_category/{file_path}`   | GET    | Get the category of a given file (2d,3d,audio,..). |
| `/rules`                      | GET    | Get all available rules.                           |
| `/check/file/{file_path}`     | GET    | Run all the rules on the given file path.          |
| `/check/dir/{directory_path}` | GET    | Run all the rules on the given directory path.     |

Embeded tools:
| Library | Alias | URL | Description |
|---------|-------|-----|-------------|
| Blender API | bpy | [https://docs.blender.org/api/3.6/](https://docs.blender.org/api/3.6/) | For checking 3d models |
| FastAPI | fastapi | [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/) | For running the server and providing the endpoints |
| PIL | PIL | [https://pillow.readthedocs.io/en/stable/](https://pillow.readthedocs.io/en/stable/) | For checking images |
| pydub | pydub | [http://pydub.com/](http://pydub.com/) | For checking audio files |

#### Rule Structure

There are 3 stages for each rule type:

##### PreCheck

These rules will be run before the Check rules and will be used for things like loading the file. They will return a boolean value if the rule is passed or not.

##### Check

These rules will be run after all precheck rules and will be used for checking the file. They will return True if no error has been occured, otherwise they will return a json containing the error message. Check the exsisting rules for more info.s

##### PostCheck

Same as PreCheck but will be run after the Check rules.

#### API

The API is a FastAPI server that will run on the local machine. You can check the endpoints at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) after running the core executable.

### Creating new rules:

Before creating a new rule, you need to know the structure of the rules.
There are 5 predefined rule types: `2d`, `3d`, `audio`, `custom` and `dir`.

To create a new rule, you need to create a new python file in the rules folder under the one if these subfolders: `2d`, `3d`, `audio`, `custom`, `dir` depending on the type of the rule you are creating. Then you need to fill the file with the following template:

```
# imports here

# necessary for the rule to be loaded
RULE_NAME = "{{rule_name}}"

def process(input):
    \"\"\"
    This function is called for each file that is checked. The input is the file path.
    the function should return True if the file is valid and a json object with the errors if the file is not valid.
    example:
    for a single error: {"file_path": "error message"}
    for multiple errors: {"object_name1": "error message1", "object_name2": "error message2"}
    \"\"\"

    errors_json = {}

    # Implement your rule here

    if errors_json != {}:
        return errors_json
    else:
        return True
```

You can check the existing rules for more info.

### Client

The client can be anything that can send a request to the server. It can be a CLI or a GUI or even a web app. You can check the [QuVery-CLI](https://github.com/QuVery/quvery-cli) and a GUI version will be available soon.
You also can use the API Doc directly by sending requests to the server from [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) after running the core executable.

## Build

run the following command to build the project:

```bash
pyinstaller  main.py --collect-all bpy -n QuVery-Core
```
