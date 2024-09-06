.PHONY: venv

PY = python3
PIP = pip3

# MAIN_SCRIPT = main.py
MAIN_SCRIPT = bot.py
REQUIREMENTS = requirements.txt

DB = ./skurun.sql

run:
#	rm -rf $(DB)
	$(PY) $(MAIN_SCRIPT)

venv:
	$(PY) -m venv venv

freeze_deps: $(REQUIREMENTS)
	$(PIP) freeze > $^

install_deps: $(REQUIREMENTS)
	$(PIP) install -r $^

clean:
	rm -rf __pycache__
	rm -rf ../__pycache__
	rm -rf ../research/__pycache__
