run:
	python3 example.py

test:
	python3 -m unittest discover -vvv ./tests -p '*.py' -b

lint:
	black .
	flake8 .
	mypy --strict .
	pytype .

coverage:
	coverage run -m unittest discover -vvv ./tests -p '*.py' -b
	coverage report -m

html: coverage
	coverage html
	open htmlcov/index.html

clean:
	python setup.py clean
	rm -rf build dist cdbpie.egg-info

build: clean
	python setup.py sdist bdist_wheel
