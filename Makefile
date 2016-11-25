
start:
	@docker-compose -f dev.yml up -d

stop:
	@docker-compose -f dev.yml stop

test:
	@docker-compose -f dev.yml run --rm django python manage.py test --failfast

status:
	@docker-compose -f dev.yml ps

clean:
	@docker-compose -f dev.yml rm

shell:
	@docker-compose -f dev.yml run --rm django python manage.py shell_plus

build:
	@docker-compose -f dev.yml build

logs:
	@docker-compose -f dev.yml logs -f


.PHONY: start stop test status clean shell logs
