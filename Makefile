DOCKER_RUN=docker run --rm -v ${PWD}:'/code' -w '/code' -it cookiecutter:3pythoneers

# Default command: create a new Cookiecutter project from this project
new: build
	@$(DOCKER_RUN) cookiecutter /code

build:
	@docker build -t cookiecutter:3pythoneers .

shell:
	@$(DOCKER_RUN) bash


