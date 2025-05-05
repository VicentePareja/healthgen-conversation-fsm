.PHONY: up down logs migrate revision

up:
	docker-compose up --build

down:
	docker-compose down

logs:
	docker-compose logs -f

migrate:
	docker-compose run --rm backend alembic upgrade head

revision:
	docker-compose run --rm backend alembic revision --autogenerate -m "update"