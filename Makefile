lint:
	poetry run flake8 src/

run-main:
	poetry run python src/fig_data_challenge/main.py

setup:
	poetry install
	poetry run pre-commit install

test:
	poetry run pytest
