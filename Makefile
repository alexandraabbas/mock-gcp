init:
	pip install -r requirements.txt
	pip install -e .

test:
	pytest -v -p pytest_cov

lint:
	pylama -l "pyflakes,mccabe"
