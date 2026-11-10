# Local development commands. Run them from the repository root.
# Linux and macOS only; on Windows follow the manual steps in processor/README.md.

PYTHON ?= python3
HOST ?= 127.0.0.1
PORT ?= 8000

VENV := processor/.venv

.PHONY: local-setup local-run

local-setup:
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/python -m pip install -r processor/requirements.txt

local-run:
	cd processor && .venv/bin/python -m uvicorn src.main:app --reload --host $(HOST) --port $(PORT)
