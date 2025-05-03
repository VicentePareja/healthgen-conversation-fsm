# Makefile

# Variables
IMAGE_NAME     := healthgen-api
CONTAINER_NAME := healthgen-conversation-fsm
COMPOSE_FILE   := compose.yaml
PORT           := 8000

.PHONY: help build docker-build up down logs shell clean

help:                  ## Muestra esta ayuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	  | sed 's/:.*##/—/' \
	  | column -t -s '—'

build:                 ## Construye la imagen Docker (target builder)
	docker build --target builder \
	             -t $(IMAGE_NAME) \
	             .

docker-build:          ## Alias de build
	$(MAKE) build

up:                    ## Arranca el servicio con docker-compose
	docker compose -f $(COMPOSE_FILE) up --build api

down:                  ## Detiene y quita contenedores
	docker compose -f $(COMPOSE_FILE) down

logs:                  ## Muestra los logs en tiempo real
	docker logs -f $(CONTAINER_NAME)

shell:                 ## Entra en shell dentro del contenedor de dev-envs
	docker run -it --rm \
	  --name temp-shell \
	  -v $$(pwd)/app:/app \
	  $(IMAGE_NAME):latest \
	  bash

clean:                 ## Elimina imágenes y contenedores generados
	docker compose -f $(COMPOSE_FILE) down --rmi all
	docker image prune -f