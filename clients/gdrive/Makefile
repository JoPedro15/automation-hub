# clients/gdrive/Makefile

ROOT_DIR := $(shell git rev-parse --show-toplevel)
VENV     := $(ROOT_DIR)/.venv
PY       := $(VENV)/bin/python
# Export PYTHONPATH so the interpreter finds the root packages
export PYTHONPATH := $(ROOT_DIR):$(PYTHONPATH)

.PHONY: setup test lint fmt clean clean-output

setup:
	@echo ">>> Installing GDrive Client and its dependencies..."
	$(PY) -m pip install -U pip
	$(PY) -m pip install -e .
	$(PY) -m pip install pytest ruff

lint:
	@echo ">>> 🧪 Linting GDrive client with Ruff..."
	# We use -m ruff to ensure we use the venv's version.
	# We select 'I' to force import sorting checks (isort logic).
	$(PY) -m ruff check . --select E,F,I
	$(PY) -m ruff format --check .

fmt:
	@echo ">>> 🎨 Formatting code and sorting imports..."
	# Using ruff for both sorting and formatting replaces isort and black
	$(PY) -m ruff check . --select I --fix
	$(PY) -m ruff format .

test:
	@echo ">>> Running GDrive tests..."
	$(PY) -m pytest tests/gdrive_test.py -vv

clean:
	rm -rf .pytest_cache .ruff_cache .mypy_cache __pycache__ *.egg-info

clean-output:
	@echo ">>> Cleaning Google Drive output folder..."
	@$(PY) $(SCRIPTS_DIR)/clean_gdrive_output.py
	@echo ">>> GDrive cleanup task finished."