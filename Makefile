.PHONY: venv 

PY = python3
PIP = pip3

MAIN_SCRIPT = bot_main.py
REQUIREMENTS = requirements.txt

DB = ./skurun.sql

launch_bot:
#	rm -rf $(DB)
	$(PY) $(MAIN_SCRIPT)

venv:
	$(PY) -m venv venv

install_deps: $(REQUIREMENTS)
	$(PIP) install -r $^

research: research.py
	$(PY) $^
