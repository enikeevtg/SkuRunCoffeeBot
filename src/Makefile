.PHONY: venv

PY = python3
PIP = pip3

# MAIN_SCRIPT = main.py
MAIN_SCRIPT = bot.py
REQUIREMENTS = requirements.txt

ALL_FILES = admin db_handler handlers keyboards utils \
						.env creds.json bot.py skurun.sqlite3 \
						requirements.txt
BOT_PACK = bot.tar

run:
	$(PY) $(MAIN_SCRIPT)

pack:
	tar -cvf $(BOT_PACK) $(ALL_FILES)

unpack: $(BOT_PACK)
	tar -xvf $(BOT_PACK)

install: unpack
	$(PIP) install -r $(REQUIREMENTS)
	rm $(BOT_PACK)

uninstall:
	rm -rf $(ALL_FILES)

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
