setup:
	uv sync

install:
	uv sync

dev:
	uv run python manage.py runserver

collectstatic:
	uv run python manage.py collectstatic --noinput

migrate:
	uv run python manage.py migrate

build:
	bash ./build.sh

render-start:
	gunicorn task_manager.wsgi

test:
	uv run python manage.py test
