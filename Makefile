venv: venv/bin/activate

venv/bin/activate: requirements.txt
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
