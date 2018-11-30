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
	venv/bin/pytest

coverage: venv
	venv/bin/pytest --cov=c3bottles

flake8: venv
	venv/bin/flake8 c3bottles

pycodestyle: venv
	venv/bin/pycodestyle c3bottles

pyline: venv
	venv/bin/pylint c3bottles
