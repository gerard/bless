APPS=$(wildcard apps/*.py)

$(APPS): %.py: 
	PYTHONPATH=src/ ./$@

clean:
	find . -name '*.pyc' | xargs -r rm
	rm -rf logs
	rm -rf build

.PHONY: $(APPS)
