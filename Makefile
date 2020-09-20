MODULE=src

lint:
	python -m pylint $(MODULE)
	python -m flake8 $(MODULE)
	python -m mypy $(MODULE)