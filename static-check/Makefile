flake8files := $(wildcard *.flake8)
reportnames := $(foreach name, $(flake8files), $(basename $(name)).html)

all: clean $(reportnames) index

clean:
	$(RM) *.html

%.html: %.flake8
	pepper8 -o $@ $<

index:
	./reportbuilder.py > index.html
