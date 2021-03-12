VENV_NAME = venv
VENV_ACTIVATE_PATH = $(VENV_NAME)/bin/activate
output_path = output.csv

.PHONY: venv

venv:
	@echo "==================== Create virtual environment ========================"
	python3 -m virtualenv ./$(VENV_NAME)
	. ./$(VENV_ACTIVATE_PATH) && \
	python3 -m pip install -r requirements.txt

venv-dev: venv
	@echo "==================== Create virtual environment for developers ========="
	. ./$(VENV_ACTIVATE_PATH) && \
	python3 -m pip install -r requirements-dev.txt

test:
	@echo "==================== Run unittests ====================================="
	. ./$(VENV_ACTIVATE_PATH) && \
	python3 -m pytest

run:
	@echo "==================== Run clicstream parser ============================="
	. ./$(VENV_ACTIVATE_PATH) && \
	python3 parse_clickstream_logs.py --input_path=$(input_path) --output_path=$(output_path)
