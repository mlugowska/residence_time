containers-tool := docker-compose
prod-dockerfile = -f docker-compose.yml -f docker-compose.prod.yml

.PHONY: makemigrations
makemigrations:
	$(containers-tool) run --rm backend bash -c 'python manage.py makemigrations && python manage.py migrate'

.PHONY: makemigrations-prod
makemigrations-prod:
	$(containers-tool) $(prod-dockerfile) run --rm backend bash -c 'python manage.py makemigrations && python manage.py migrate'

.PHONY: make-sdf
make-sdf:
	$(containers-tool) run --rm backend bash -c 'python2.7 utils/convert_pdb_to_sdf.py'

.PHONY: django-shell
django-shell:
	$(containers-tool) exec backend bash -c "./manage.py shell"

.PHONY: build-prod
build-prod:
	$(containers-tool) $(prod-dockerfile) build

.PHONY: start-prod
start-prod:
	$(containers-tool) $(prod-dockerfile) up -d
