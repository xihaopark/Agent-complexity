.PHONY: up down test api worker

up:
	docker compose up --build

down:
	docker compose down -v

test:
	pytest

api:
	python -m apps.api.main

worker:
	python -m workers.sandbox_runner.main
