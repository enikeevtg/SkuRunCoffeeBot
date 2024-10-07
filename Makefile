# UTILS
PY = python3
PIP = pip3

# FILENAMES
VENV = .venv
APP = app
MAIN_SCRIPT = $(APP)/bot.py
ANYWHERE_MAIN_SCRIPT = $(APP)/bot_pythonanywhere.py
RUNNER = runner.sh
REQUIREMENTS = requirements.txt
APP_PACK = app.tar


# MAIN TARGET
run:
	$(PY) $(MAIN_SCRIPT)

pythonanywhere_run:
	$(PY) $(ANYWHERE_MAIN_SCRIPT)

# DEPLOYMENT
pack:
	rm -rf $(APP_PACK)
	tar -cf $(APP_PACK) $(APP) $(RUNNER) $(REQUIREMENTS)

unpack: $(APP_PACK)
	tar -xvf $(APP_PACK)

install: venv unpack
	$(PIP) install -r $(REQUIREMENTS)
	rm $(APP_PACK)

# SERVICE
venv:
	$(PY) -m venv $(VENV)

freeze_deps:
	$(PIP) freeze > $(REQUIREMENTS)

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
