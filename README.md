# Cookiecutter template for 3 Pythoneers setup

This is a [Cookiecutter](https://cookiecutter.readthedocs.io/) template that bootstraps
a "3 Pythoneers" project using either FastAPI or Falcon 3 (WSGI only, for now).

## Dependencies

**I do not recommend copying this template with a globally-installed version** because the
post-run script 1) requires `sh` in a Unix environment and 2) will install Poetry in your
global default Python namespace.

Instead, you should get a head-start on your [3 Musketeers](https://3musketeers.io/) local
environment by installing the following:

* [Docker](https://docs.docker.com/engine/installation/)
* [Docker Compose](https://docs.docker.com/compose/install/) (included in Docker
  Desktop on Windows and Mac)
* Make

### Running on Windows

**Please note:** in order to run Docker Desktop on Windows you will either need a recent copy of
Windows 10 Home with [WSL 2 enabled](https://docs.microsoft.com/en-us/windows/wsl/install-win10),
or Windows 10 Pro.

One easy way to install `make` on Windows:

1. Install the [Chocolatey](https://chocolatey.org/install) package manager
2. Run `choco install make` in an elevated command prompt

## Initialize your project

After installing the dependencies above, simply run `make` from the root directory! Once the
Docker container is built, you will be able to go through the standard Cookiecutter command
line interface to create your project. You can then move your newly created project folder
out of this project's root directory, and you'll be good to go!
