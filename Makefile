# UTILS
PY = python3
PIP = pip3

# FILENAMES
VENV = .venv2
APP = app
MAIN_SCRIPT = $(APP)/run.py
REQUIREMENTS = requirements.txt
APP_PACK = app.tar
WEEKDAY = Sat


# MAIN TARGET
run:
	$(PY) $(MAIN_SCRIPT)

pythonanywhere_run:
	@echo $(shell date)
	@if [ $(shell date +%a) = $(WEEKDAY) ]; \
	then \
		echo "SkuRunCoffeeBreakBot launching..."; \
		$(PY) $(MAIN_SCRIPT); \
	else \
		echo "SkuRunCoffeeBreakBot not launched"; \
	fi;

# DEPLOYMENT
pack: clean
	rm -rf $(APP_PACK)
	tar -cf $(APP_PACK) $(APP) $(REQUIREMENTS)

unpack: $(APP_PACK)
	tar -xvf $(APP_PACK)

# SERVICE
venv:
	$(PY) -m venv $(VENV)

freeze_deps:
	$(PIP) freeze > $(REQUIREMENTS)

install_deps: $(REQUIREMENTS)
	$(PIP) install -r $^

clean:
	rm -rf __pycache__
	rm -rf $(APP)/__pycache__
	rm -rf research/__pycache__
	rm -rf reserves/__pycache__
	rm -rf $(APP)/admin/__pycache__
	rm -rf $(APP)/database/__pycache__
	rm -rf $(APP)/filters/__pycache__
	rm -rf $(APP)/handlers/__pycache__
	rm -rf $(APP)/keyboards/__pycache__
	rm -rf $(APP)/utils/__pycache__
