SHELL := /bin/bash

create-venv:
	python3 -m venv venv
	source venv/bin/activate && pip install -r requirements.txt && pip install -e .

delete-venv:
	rm -rf venv

show-activate:
	source venv/bin/activate
