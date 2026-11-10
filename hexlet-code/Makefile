install:
	uv sync

dev:
	uv run python manage.py runserver

collectstatic:
	uv run python manage.py collectstatic --noinput

migrate:
	uv run python manage.py migrate

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi