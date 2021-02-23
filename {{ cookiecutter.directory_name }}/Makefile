# Defines help target logic
# Add help text after each target name starting with '\#\#'
# Inspired by <https://gist.github.com/prwhite/8168133>
DOCKER_RUN = docker-compose run --rm -e STANDALONE=true --no-deps -u root -w /code api
DOCKER_RUN_DB = docker-compose run --rm -u root -w /code api
DOCKER_COMPOSE_TESTS = docker-compose -p {{ cookiecutter.directory_name }}_tests -f docker-compose.yml -f docker/docker-compose.test.yml

##=== Welcome to {{ cookiecutter.project_name }}! ===

help:     ## Show this help.
	@$(DOCKER_RUN) make _help

_help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -E -e 's/: [a-z][ a-z-]+?[a-z](\s+)##/:\1/' | sed -e 's/##//'

##
##=== Local development ===

run:      ## Run development server
	@docker-compose up

test:     ## Execute test suite; or specify target: `make test ARGS='api/tests/example'`
	@(DOCKER_COMPOSE_TESTS) run --rm -w /code api \
		pytest --cov=api --cov-config=.coveragerc --cov-report=term:skip-covered --cov-report=html $(ARGS)

# This ensures that even if they pass in an empty value, we default to "head"
ifndef REV
override REV = head
endif

migrate: clean-api  ## Run database migrations; or specify a revision: `make migrate REV='head'`
	@$(DOCKER_RUN_DB) alembic upgrade $(REV)

##
##=== Access internals ===

db:       ## Run standalone postgres server; accessible at localhost:5432
	@docker-compose run --service-ports --rm postgres

shell:    ## Open a bash shell to API (warning: root user!)
	@$(DOCKER_RUN) bash

shell-db: ## Open a bash shell to API with the database running
	@$(DOCKER_RUN_DB) bash

##
##=== Docker maintenance ===

build:    ## Rebuild the main app container
	@docker-compose build --no-cache api

clean-api:
	@docker-compose down --remove-orphans

clean-tests:
	@$(DOCKER_COMPOSE_TESTS) down --remove-orphans

clean: clean-api clean-tests    ## Clean up Docker containers, images, etc.
	@echo 'All clean!'
