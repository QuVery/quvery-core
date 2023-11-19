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

#### API

The API is a FastAPI server that will run on the local machine. You can check the endpoints at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) after running the core executable.
