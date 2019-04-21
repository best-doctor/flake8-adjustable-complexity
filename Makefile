check:
	flake8 .
	mypy --allow-redefinition .
	python -m pytest --cov=flake8_adjustable_complexity --cov-report=xml
