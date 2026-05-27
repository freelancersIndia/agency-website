.PHONY: bootstrap dev build run stop reset status logs

bootstrap:
	sh ./scripts/bootstrap.sh

dev:
	sh ./scripts/dev.sh

run:
	docker compose up -d

stop:
	docker compose down

reset:
	sh ./scripts/reset.sh

build:
	docker compose build

status:
	docker compose ps

logs:
	docker compose logs -f
