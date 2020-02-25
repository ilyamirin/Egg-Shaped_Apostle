-include local.mk

.PHONY: build run stop rm rmi

ENV ?= dev
CONTAINER_NAME = place-search

ifeq ($(ENV),prod)
DC_FILE = docker-compose.prod.yaml
else
DC_FILE = docker-compose.yaml
endif

local.mk:
	@cp local.mk.dist local.mk

build:
	@docker build -t $(IMAGE_NAME) -f ./docker/server.Docker .

push:
	@docker push $(IMAGE_NAME)

run: build
	@docker run -d --name $(CONTAINER_NAME) -p 80:80 $(IMAGE_NAME)

stop:
	@docker stop $(CONTAINER_NAME)

rm:
	@docker rm $(CONTAINER_NAME)

rmi:
	@docker rmi $(IMAGE_NAME)

pull:
	@docker-compose -f $(DC_FILE) pull

server:
	@docker-compose -f $(DC_FILE) up -d

server-stop:
	@docker-compose -f $(DC_FILE) stop
