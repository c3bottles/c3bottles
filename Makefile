export PATH := venv/bin:$(PATH)

venv: venv/bin/activate

venv/bin/activate: requirements.txt requirements/all.txt requirements/development.txt requirements/production.txt
	test -d venv || virtualenv -p python3 venv
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

flake8: venv
	flake8 c3bottles

pycodestyle: venv
	pycodestyle c3bottles

pylint: venv
	pylint c3bottles

black: venv
	black --line-length=100 c3bottles config.default.py manage.py wsgi.py

isort: venv
	isort --recursive c3bottles manage.py wsgi.py

format: black isort
