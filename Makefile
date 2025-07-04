VENV=.venv

.PHONY: test

test: $(VENV)/bin/activate
	$(VENV)/bin/pip install -r dev-requirements.txt
	PYTHONPATH=. $(VENV)/bin/pytest

$(VENV)/bin/activate:
	python -m venv $(VENV)
