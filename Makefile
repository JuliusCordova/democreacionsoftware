PYTHON ?= python3

.PHONY: test compile smoke inventory-smoke evidence

test:
	$(PYTHON) -m pytest -q

compile:
	$(PYTHON) -m compileall -q src tests scripts

smoke:
	PYTHONPATH=src $(PYTHON) -m stock_unico.smoke

inventory-smoke:
	PYTHONPATH=src $(PYTHON) -m stock_unico.inventory_smoke

evidence:
	PYTHONPATH=src $(PYTHON) scripts/cloudshell/run_evidence.py
