export PATH := venv/bin:$(PATH)

venv: venv/bin/activate

venv/bin/activate: requirements.txt requirements/all.txt requirements/development.txt requirements/production.txt
	test -d venv || python3 -m venv venv
	venv/bin/pip install -Ur requirements.txt
	touch venv/bin/activate

clean:
	find . -name "__pycache__" -exec rm -r {} +
	find . -name "*.pyc" -exec rm {} +

mrproper: clean
	rm -rf venv/

pytest: venv
	pytest

coverage: venv
	pytest --cov=c3bottles

htmlcov: coverage
	coverage html -i -d .htmlcov/
	(cd .htmlcov/ ; ../venv/bin/python -m http.server 3333)

flake8: venv
	flake8 c3bottles config.default.py manage.py wsgi.py

pycodestyle: venv
	pycodestyle c3bottles

pylint: venv
	pylint c3bottles

black: venv
	black --line-length=100 c3bottles config.default.py manage.py wsgi.py tests

isort: venv
	isort c3bottles manage.py wsgi.py tests

format: black isort

pre-commit: flake8 pytest
	black --check --line-length=100 c3bottles config.default.py manage.py wsgi.py tests
	isort --check-only c3bottles manage.py wsgi.py tests
	pnpm run eslint
