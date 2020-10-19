# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Dependencies

You must install the following to run the API locally:

* [Docker](https://docs.docker.com/engine/installation/)
* [Docker Compose](https://docs.docker.com/compose/install/) (included in Docker
  Desktop on Windows and Mac)
* Make

That's it! For local development, all other code is executed in Docker via Make using
the standard [3 Musketeers](https://3musketeers.io/) pattern.

### Running on Windows

**Please note:** in order to run Docker Desktop on Windows you will either need a recent copy of
Windows 10 Home with [WSL 2 enabled](https://docs.microsoft.com/en-us/windows/wsl/install-win10),
or Windows 10 Pro.

One easy way to install `make` on Windows:

1. Install the [Chocolatey](https://chocolatey.org/install) package manager
2. Run `choco install make` in an elevated command prompt

## First run

After installing the dependencies above:

1. Create a copy of `.env.example` named `.env` in your root directory
2. *At minimum* update `POSTGRES_PASSWORD` in `.env` (you can update other
   values if you wish; they aren't required to run locally, though)
3. Run `make` from the root project directory

This will build your main Docker container and display the available commands you can
execute with `make`.

Now that you have a functional API stack, you need to setup your database:

1. Run `make migrate` to initialize your database with the latest migrations

At this point, you can execute `make run` to start a local development server, and view your
site's API documentation at <http:localhost:8000>.

From within the API docs, you can query the API directly and inspect its output.

### VSCode: Developing within the Docker container

You can use [Visual Studio Code](https://code.visualstudio.com/) to develop directly within
the Docker container, allowing you access to the Python environment (which means
linting, access to Python tools, working code analysis for free, and bash shell access
without needing to run a make command). To do so:

1. Install [Visual Studio Code](https://code.visualstudio.com/), if you haven't already
2. Install the [Remote Development extension pack](https://aka.ms/vscode-remote/download/extension)
3. **Outside VSCode** in your favored command line, execute `make run` to launch the API container
4. **Inside VSCode** use the Remote Explorer in the left sidebar of VSC to attach to the running
   API container (named `{{ cookiecutter.directory_name }}:dev`). You can find explicit instructions
   for this in the [Visual Studio Code documentation](https://code.visualstudio.com/docs/remote/containers#_attaching-to-running-containers)
5. If this is your first time attaching, open the Command Palette and type "container" then
   select "Remote-Containers: Open Container Configuration", replace the contents
   of the file with the following, save, and then close the window and re-attach to the container:

```json
{
	"workspaceFolder": "/code",
	"settings": {
		"terminal.integrated.shell.linux": "/bin/bash",
		"python.pythonPath": "/usr/local/bin/python3.8",
		"python.linting.pylintEnabled": true,
		"python.linting.enabled": true,
		"editor.formatOnSave": true,
		"python.formatting.provider": "black",
		"editor.wordWrapColumn": 88
	},
	"remoteUser": "root",
	"extensions": [
		"editorconfig.editorconfig",
		"ms-python.python"
	]
}
```

You will need to start the API prior to launching VSCode to automatically attach to it.
(I am looking into ways to improve this workflow, but short-term this is the easiest
to get working consistently.)

**Please note:** you *must* run your make commands in an external shell! The VSCode Terminal
in your attached container window will provide you access to the equivalent of `make shell`,
but running the standard make commands there will result in Docker-in-Docker, which is not
desirable in this instance.

## Development

The API uses the {% if cookiecutter.framework == "FastAPI" %}[FastAPI](https://fastapi.tiangolo.com/){% else %}[Falcon](https://falconframework.org/){% endif %} framework to handle view
logic, and [SQLAlchemy](https://www.sqlalchemy.org/) for models and database interaction.
[Pydantic](https://pydantic-docs.helpmanual.io/) is used for modeling and validating endpoint
input and output. [Pytest](https://docs.pytest.org/en/latest/) is used for testing.

### Code logic

The primary entrypoint for the application is `api/main.py`. This file defines
the main app and attaches all site routers. Site modules are organized as follows:

* `api/views`: Route view {% if cookiecutter.framework == "FastAPI" %}functions{% else %}classes{% endif %}, typically organized by base URL segment.
* `api/models`: Data models used to persist to and represent info from the database
* `api/tests`: Integration tests (with some unit tests where integration testing is not feasible)

You will likely leverage the following files, as well:

* `api/environment.py`: Exports the `settings` object for access to environment settings

### Installing Python dependencies

The API uses [Poetry](https://python-poetry.org/) for dependency management. To
install a new dependency from outside of the container:

```sh
$ make shell
root@123:/code$ poetry add DEPENDENCY
```

(If you are developing within Visual Studio Code, you can open the built-in terminal and skip
the `make shell` command.)

Then commit changes in your updated `poetry.lock` and `pyproject.toml`. Please see the
[Poetry docs](https://python-poetry.org/docs/) for other available commands.

You may wish to shut down your container, run `make build`, and relaunch it to ensure that
newly added dependencies are available on subsequent launches. If you pull down code and stuff
starts failing in weird ways, you probably need to run `make build` and `make migrate`.

**Please note:** `make shell` will log you into the Docker container as the root user!
This is unfortunately necessary to allow Poetry to function properly (I haven't found a
good way yet to install initial dependencies as a non-root account and have them work,
which means the shell has to be root in order to properly calculate the dependency graph).

### Update core tools

The underlying Dockerfile uses the following tools, pinned to specific release versions:

* [Dockerize](https://github.com/jwilder/dockerize)
* [Tini](https://github.com/krallin/tini)
* [Poetry](https://python-poetry.org/)

In order to update these tools, you must update their pinned version in `Dockerfile`
and (for Poetry) in `pyproject.toml` then rebuild your API container using `make build`.
