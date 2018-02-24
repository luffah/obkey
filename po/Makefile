LANGS := $(patsubst obkey.%.po,%,$(wildcard *.po))
TARGETS := $(patsubst %,../resources/locale/%/LC_MESSAGES/obkey.mo,$(LANGS))

all: $(TARGETS)

../resources/locale/%/LC_MESSAGES/obkey.mo: obkey.%.po
	mkdir -p $(dir $@)
	msgfmt -o $@ $<
