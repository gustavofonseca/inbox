
start:
	@docker-compose -f docker-compose-dev.yml up -d

stop:
	@docker-compose -f docker-compose-dev.yml stop

test:
	@docker-compose -f docker-compose-dev.yml run --rm django python manage.py test --failfast

status:
	@docker-compose -f docker-compose-dev.yml ps

clean:
	@docker-compose -f docker-compose-dev.yml rm

shell:
	@docker-compose -f docker-compose-dev.yml run --rm django python manage.py shell_plus

build:
	@docker-compose -f docker-compose-dev.yml build

logs:
	@docker-compose -f docker-compose-dev.yml logs -f


.PHONY: start stop test status clean shell logs
