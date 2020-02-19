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

makemigrations:
	$(containers-tool) run --rm web bash -c 'python manage.py makemigrations && python manage.py migrate'

makemigrations-prod:
	$(containers-tool) $(prod-dockerfile) run --rm web bash -c 'python manage.py makemigrations && python manage.py migrate'

shell:
	$(containers-tool) exec web bash -c "./manage.py shell"

shell-prod:
	$(containers-tool) $(prod-dockerfile) exec web bash -c "./manage.py shell"
