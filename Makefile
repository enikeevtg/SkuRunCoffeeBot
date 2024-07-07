.PHONY: venv 

PY = python3
PIP = pip3

REQUIREMENTS = requirements.txt

DB = ./skurun.sql

start_bot:
	rm $(DB)
	$(PY) main.py

venv:
	$(PY) -m venv venv

install_deps: $(REQUIREMENTS)
	$(PIP) install -r $^

research: research.py
	$(PY) $^
