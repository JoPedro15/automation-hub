# AUTOMATION-HUB Orchestrator
# Central Management for Cross-Domain Automation Clients

# --- Configuration ---
SHELL := /bin/bash
VENV  := .venv
CI    ?= false

# Clients Directory Mapping
CORE_LIB_DIR   := clients/core_lib
AI_UTILS_DIR   := clients/ai_utils
GDRIVE_DIR     := clients/gdrive
GDRIVE_SCRIPTS := $(GDRIVE_DIR)/scripts
SCRIPTS_DIR    := scripts
REQ_DEV        := requirements.txt

# Binary detection based on environment (Local vs CI)
ifeq ($(CI), true)
    BIN :=
    PY  := python3
    PIP := pip
else
    BIN := $(VENV)/bin/
    PY  := $(BIN)python
    PIP := $(BIN)pip
endif

# Tooling definitions
RUFF    := $(BIN)ruff
PRE     := $(BIN)pre-commit
PYTEST  := $(BIN)pytest
BANDIT  := $(BIN)bandit
AUDIT   := $(BIN)pip-audit

# Export PYTHONPATH to ensure all modules are discoverable during lint/test
export PYTHONPATH := .:$(GDRIVE_DIR):$(CORE_LIB_DIR):$(AI_UTILS_DIR)

.PHONY: help setup quality security health test-all clean lint-and-format verify-env

# --- Help Target ---

help:
	@echo "Automation Hub - Management Targets:"
	@echo "  setup            - Full environment initialization and client installation"
	@echo "  quality          - Comprehensive pipeline: Fix -> Format -> Lint -> Security -> Test"
	@echo "  lint-and-format  - Auto-fix and style all clients (Scripts & Notebooks)"
	@echo "  security         - Static Analysis and Dependency Vulnerability Audit"
	@echo "  health           - Run global system diagnostic scripts"
	@echo "  test-all         - Execute the complete automated test suite"
	@echo "  clean            - Wipe temporary caches and build artifacts"

# --- Main Pipelines ---

# Full Quality Gate: The mandatory check before any release or push
quality: clean
	@echo ">>> 🚀 [PIPELINE] Starting Full Quality Gate..."
	@$(MAKE) lint-and-format
	@echo ">>> 🔍 [VALIDATION] Running Pre-commit Hooks..."
	$(PRE) run --all-files
	@echo ">>> 🛡️ [SECURITY] Running Security Analysis..."
	@$(MAKE) security
	@echo ">>> 🧪 [TESTS] Executing Test Suite..."
	@$(MAKE) test-all
	@echo ">>> 🏆 [SUCCESS] System is healthy and production-ready."

# Developer Workflow: Atomically fix and format the codebase
lint-and-format:
	@echo ">>> 🔧 [FIX] Running Ruff (Scripts & Clients)..."
	# Using --exit-zero to ensure formatting continues even if minor lint issues persist
	$(RUFF) check . --fix --exit-zero
	@echo ">>> 🖋️ [FMT] Applying Global Formatting..."
	$(RUFF) format .
	@echo ">>> ✅ Local fixes applied."

# --- Infrastructure & Environment ---

# Global Orchestrator: Creates VENV, installs core/domain dependencies, and secures the environment
setup:
	@echo ">>> 🛠️  [STEP 1/5] Initializing Virtual Environment..."
	@if [ ! -d "$(VENV)" ]; then \
		echo ">>> Creating .venv with Python 3.12..."; \
		python3 -m venv $(VENV); \
	fi
	@$(PIP) install --upgrade pip
	@echo ">>> 📦 [STEP 2/5] Installing Development Requirements from $(REQ_DEV)..."
	$(PIP) install -U -r $(REQ_DEV)
	@echo ">>> 🏗️  [STEP 3/5] Installing Internal Clients in Editable Mode..."
	@echo ">>> Installing core-lib foundation..."
	$(PIP) install -e $(CORE_LIB_DIR)
	@echo ">>> Installing gdrive domain client..."
	$(PIP) install -e $(GDRIVE_DIR)
	@echo ">>> Installing ai-utils domain client..."
	$(PIP) install -e $(AI_UTILS_DIR)
	@echo ">>> 🔍 [STEP 4/5] Verifying Package Integrity..."
	@$(MAKE) verify-env
	@echo ">>> 🛡️  [STEP 5/5] Finalizing Security and Git Hooks..."
	$(PRE) install
	@$(MAKE) security
	@echo ">>> ✅ [SUCCESS] Environment is ready, orchestrated, and secured!"

# Integrity check for critical dependencies and internal packages
verify-env:
	@echo ">>> 🔍 Verifying Package Integrity..."
	@$(PY) -c "import pandas; import core_lib_client; import gdrive_client; print('>>> ✨ Integrity Check Passed.')" || \
	(echo ">>> ❌ Integrity Check Failed: Missing modules." && exit 1)

# --- Tooling ---

security:
	@echo ">>> 🛡️ Running Bandit Security Scan..."
	$(BANDIT) -r clients/ -ll --exclude .venv,*/.venv/*
	@echo ">>> 🛡️ Running Dependency Audit..."
	$(AUDIT) --skip-editable --ignore-vuln CVE-2025-53000

health:
	@echo ">>> 🩺 Running System Health Checks..."
	$(PY) $(SCRIPTS_DIR)/global_health_check.py

test-all:
	@echo ">>> 🧪 Running Pytest suite..."
	$(PYTEST) $(GDRIVE_DIR)/tests/gdrive_test.py -vv

# --- Maintenance ---

clean:
	@echo ">>> 🧹 Cleaning Workspace..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	@echo ">>> Workspace is clean."

clean-gdrive-output:
	@echo ">>> 🧹 Cleaning GDrive Output..."
	@$(PY) $(GDRIVE_SCRIPTS)/clean_gdrive_output.py
