prod-dockerfile = -f docker-compose.yml -f docker-compose.prod.yml
containers-tool = docker-compose

build-dev:
	docker-compose build
	$(MAKE) dev

dev:
	docker-compose up

build-prod:
	docker-compose $(prod-dockerfile) build
	$(MAKE) prod

prod:
	docker-compose $(prod-dockerfile) up -d
