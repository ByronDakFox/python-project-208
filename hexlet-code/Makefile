install:
	uv sync

dev:
	uv run python manage.py runserver

collectstatic:
	uv run python manage.py collectstatic --no--input

migrate:
	uv run python manage.py migrate

build:
	bash ./build.sh

render-start:
	gunicorn task_manager.wsgi

test:
	uv run python manage.py test
