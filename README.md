# QuVery Core

QuVery Core is the core library of QuVery. It provides the basic functions of QuVery to be used in other projects like QuVery-CLI or QuVery-GUI.

## Introduction

### For Artists

If you are an artist, you know that how hard and time consuming it is to get a message from the client that your file has some technical issues. QuVery is here to help you with that. It will check your file for any technical issues and will let you know if there is any. It will also provide you with a list of the issues and how to fix them.

### For Teams

### For Companies

---

There are 2 parts for the whole QuVery project:

### Core

The core part of the package runs a local server providing FastAPI endpoints for the client to send requests to. The server will then run the rules and return the result to the client.
Here are some of the available endpoints:

| Endpoint                      | Method | Description                                                |
| ----------------------------- | ------ | ---------------------------------------------------------- |
| `/rule_types`                 | GET    | Get a list of all available rule types.                    |
| `/rules/{rule_type}`          | GET    | Get a list of all available rules for the given rule type. |
| `/check/file/{file_path}`     | GET    | Run all the rules on the given file path.                  |
| `/check/dir/{directory_path}` | GET    | Run all the rules on the given directory path.             |

Embeded tools:
| Library | Alias | URL | Description |
|---------|-------|-----|-------------|
| Blender API | bpy | [https://docs.blender.org/api/3.6/](https://docs.blender.org/api/3.6/) | For checking 3d models |
| FastAPI | fastapi | [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/) | For running the server and providing the endpoints |
| PIL | PIL | [https://pillow.readthedocs.io/en/stable/](https://pillow.readthedocs.io/en/stable/) | For checking images |

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

### Client

The client can be anything that can send a request to the server. It can be a CLI or a GUI or even a web app. You can check the [QuVery-CLI](https://github.com/QuVery/quvery-cli) and a GUI version will be available soon.
You also can use the API Doc directly by sending requests to the server from [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) after running the core executable.

## Build

run the following command to build the project:

```bash
pyinstaller  main.py --collect-all bpy -n QuVery-Core
```
