sync:
	@echo "Starting sync process..."
	uv sync
	@echo "Sync process completed."

migrate:
	uv run python manage.py makemigrations books accounts && uv run python manage.py migrate
	

superuser:
	uv run python manage.py createsuperuser

dev:
	uv run python manage.py runserver