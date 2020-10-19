# Cookiecutter template for 3 Musketeers Python API

This is a [Cookiecutter](https://cookiecutter.readthedocs.io/) template that bootstraps
a "3 Pythoneers" project using either [FastAPI](https://fastapi.tiangolo.com/) or
[Falcon 3](https://falconframework.org/) (WSGI only, for now).

**Please note:** Falcon 3 is currently an alpha release! I am including it because the
WSGI functionality is quite stable (mostly unchanged from Falcon 2). For ASGI under
Falcon 3, you will need to adjust the template to use SQLAlchemy 1.4 pre-release and
`asyncpg` instead of `psycopg2`(the current Python dependencies all assume you're using
synchronous SQLAlchemy). I would have supported this out of the box, but I haven't had
a chance to test this setup myself, yet.

### Why 3 Musketeers?

Python APIs are really annoying to develop locally, because you have to install a database,
make sure you've got the right version of Python (which could be different across different
projects), and a number of other headaches.

A [3 Musketeers](https://3musketeers.io/) project requires you to populate a `.env` file,
and run **a single command**. And it works exactly the same on macOS, Windows, and Linux.

You'll never look back.

## Usage

**I do not recommend using this template with a globally-installed version of Cookiecutter**
because the post-run script: 1) requires `sh` in a Unix environment; and 2) will install Poetry
in your global default Python namespace, which you probably don't want.

Instead, you should get a head-start on your 3 Musketeers local environment by installing the
following:

* [Docker](https://docs.docker.com/engine/installation/)
* [Docker Compose](https://docs.docker.com/compose/install/) (included in Docker Desktop on
  Windows and macOS)
* Make

After installing the dependencies above, simply run `make` from the root directory! Once the
Docker container is built, you will be able to go through the standard Cookiecutter command
line interface to create your project. You can then move your newly created project folder
out of this project's root directory, and you'll be good to go!

Refer to the README in your new project for how to get a local server up and running (you're
halfway there already!).

### Running on Windows

**Please note:** in order to run Docker Desktop on Windows you will either need a recent copy of
Windows 10 Home with [WSL 2 enabled](https://docs.microsoft.com/en-us/windows/wsl/install-win10),
or Windows 10 Pro.

One easy way to install `make` on Windows:

1. Install the [Chocolatey](https://chocolatey.org/install) package manager
2. Run `choco install make` in an elevated command prompt
