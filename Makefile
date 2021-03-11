VENV_NAME = venv
VENV_ACTIVATE_PATH = $(VENV_NAME)/bin/activate
output_path = output.csv

.PHONY: venv

venv:
	@echo "==================== Create virtual environment ========================"
	python3 -m virtualenv ./$(VENV_NAME)
	. ./$(VENV_ACTIVATE_PATH) && \
	python3 -m pip install -r requirements.txt

test:
	@echo "==================== Run unittests ====================================="
	. ./$(VENV_ACTIVATE_PATH) && \
	python3 -m unittest

run:
	@echo "==================== Run clicstream parser ============================="
	. ./$(VENV_ACTIVATE_PATH) && \
	python3 parse_clickstream_logs.py --input_path=$(input_path) --output_path=$(output_path)
