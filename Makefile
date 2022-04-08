all: help

##
## Repository Docker Helper Commands
## Available commands:
##

.PHONY: help up debug down stop shell logs

help: Makefile
	@sed -n 's/^##//p' $<

## shell:               Interactive shell to use commands inside docker
shell:
	docker-compose exec scrapper-seo bash

## up:                  Run the necessary services to run repo without xdebug
up:
	docker-compose build
	docker-compose up -d


shell:
	docker-compose exec scrapper-seo bash

down:
	docker-compose scrapper-seo down