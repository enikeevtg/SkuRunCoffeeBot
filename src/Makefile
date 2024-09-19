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
	rm -rf ../reserves/__pycache__
	rm -rf ./admin/__pycache__
	rm -rf ./db_handler/__pycache__
	rm -rf ./handlers/__pycache__
	rm -rf ./keyboards/__pycache__
	rm -rf ./utils/__pycache__
