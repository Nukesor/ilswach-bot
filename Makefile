default: install

install:
	poetry install

run:
	poetry run ./initdb.py
	poetry run ./main.py
