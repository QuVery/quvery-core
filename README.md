# QuVery Core

QuVery Core is the core library of QuVery. It provides the basic functions of QuVery to be used in other projects like QuVery-CLI or QuVery-GUI.

## Introduction

There are 2 parts for the whole QuVery project:

### Core

This is the core part of the package. it runs a local server that listens for instruction.
here are some of the messages that the server will listen to:

- get_rule_types : this will return all the rule types that are available in the core. eg: 3d, 2d, audio, custom, etc.

There are 3 types of rules:

#### PreCheck

These rules will be run before the Check rules and will be used for things like cleaning the current instance of blender if we want to import a model or loading blender with the file passed to it. They will return a boolean value.

#### Check

These rules will be run after all precheck rules and will be used for checking the file. They will return a a touple of (ruleName, result).

#### PostCheck

These rules will be run after all check rules. I have no idea what they will be used for yet but will keep them here for now.

If the rule is passed, the result will be OK, otherwise it will be the error message containing all the errors that occured during the process.

### Client

The client can be anything that can send a request to the server. It can be a CLI or a GUI or even a web app. The client will send a request to the server and will recieve the result of the process. The client will be responsible for displaying the result to the user or passing a CI/CD test.

## Build

run the following command to build the project:

```bash
pyinstaller  main.py --collect-all bpy -n QuVery-Core
```
